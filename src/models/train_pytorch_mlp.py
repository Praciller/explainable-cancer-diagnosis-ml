from __future__ import annotations

import argparse
import copy
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from src.config import MODELS_DIR, RANDOM_SEED, REPORTS_DIR
from src.contracts import (
    CALIBRATION_STATUS,
    DECISION_THRESHOLD,
    label_contract,
    predictions_from_malignant_scores,
)
from src.data.load_dataset import load_dataset_frame
from src.features.preprocess import prepare_scaled_splits, split_dataset
from src.utils.metrics import classification_metrics
from src.utils.tracking import optional_mlflow_run


class TabularDataset(Dataset[tuple[torch.Tensor, torch.Tensor]]):
    def __init__(self, features: np.ndarray, target: np.ndarray) -> None:
        self.features = torch.tensor(features, dtype=torch.float32)
        self.target = torch.tensor(target, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.target)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.features[index], self.target[index]


class TabularMLP(nn.Module):
    def __init__(self, input_features: int = 30) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_features, 64),
            nn.ReLU(),
            nn.Dropout(0.20),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.10),
            nn.Linear(32, 1),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features).squeeze(1)


@dataclass(frozen=True)
class PytorchTrainingResult:
    metrics: dict[str, Any]
    history: dict[str, list[float]]


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def _loss_for_loader(
    model: TabularMLP,
    loader: DataLoader[tuple[torch.Tensor, torch.Tensor]],
    loss_function: nn.Module,
) -> float:
    model.eval()
    total = 0.0
    with torch.inference_mode():
        for features, target in loader:
            total += float(loss_function(model(features), target)) * len(target)
    return total / len(loader.dataset)


def _predict(model: TabularMLP, features: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    model.eval()
    with torch.inference_mode():
        benign_probability = torch.sigmoid(
            model(torch.tensor(features, dtype=torch.float32))
        ).numpy()
    malignant_score = 1 - benign_probability
    prediction = predictions_from_malignant_scores(malignant_score)
    return prediction, malignant_score


def _plot_history(history: dict[str, list[float]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 4.5))
    axis.plot(history["train_loss"], label="Training loss", color="#713c78")
    axis.plot(history["validation_loss"], label="Validation loss", color="#d36d5f")
    axis.set(xlabel="Epoch", ylabel="Binary cross-entropy", title="PyTorch MLP training")
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figure.savefig(output_path, dpi=160)
    plt.close(figure)


def train_pytorch_mlp(
    seed: int = RANDOM_SEED,
    epochs: int = 100,
    learning_rate: float = 0.001,
    batch_size: int = 32,
    patience: int = 12,
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
    mlflow_enabled: bool = False,
) -> PytorchTrainingResult:
    _set_seed(seed)
    bundle = load_dataset_frame()
    scaled = prepare_scaled_splits(split_dataset(bundle.features, bundle.target, seed))
    generator = torch.Generator().manual_seed(seed)
    train_loader = DataLoader(
        TabularDataset(scaled.X_train, scaled.y_train),
        batch_size=batch_size,
        shuffle=True,
        generator=generator,
    )
    validation_loader = DataLoader(
        TabularDataset(scaled.X_validation, scaled.y_validation),
        batch_size=batch_size,
    )
    model = TabularMLP(input_features=len(scaled.feature_names))
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_function = nn.BCEWithLogitsLoss()
    history = {"train_loss": [], "validation_loss": []}
    best_state = copy.deepcopy(model.state_dict())
    best_validation_loss = float("inf")
    epochs_without_improvement = 0

    with optional_mlflow_run(
        mlflow_enabled,
        "pytorch_mlp",
        {
            "model_name": "pytorch_mlp",
            "epochs": epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "random_seed": seed,
            "dataset_version": "sklearn-wdbc",
        },
    ) as tracker:
        for _ in range(epochs):
            model.train()
            total_train_loss = 0.0
            for features, target in train_loader:
                optimizer.zero_grad()
                loss = loss_function(model(features), target)
                loss.backward()
                optimizer.step()
                total_train_loss += float(loss) * len(target)

            train_loss = total_train_loss / len(train_loader.dataset)
            validation_loss = _loss_for_loader(model, validation_loader, loss_function)
            history["train_loss"].append(train_loss)
            history["validation_loss"].append(validation_loss)
            if validation_loss < best_validation_loss - 1e-5:
                best_validation_loss = validation_loss
                best_state = copy.deepcopy(model.state_dict())
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1
                if epochs_without_improvement >= patience:
                    break

        model.load_state_dict(best_state)
        validation_prediction, malignant_score = _predict(model, scaled.X_validation)
        metrics = classification_metrics(
            scaled.y_validation,
            validation_prediction,
            malignant_score,
        )
        metrics["epochs_trained"] = len(history["train_loss"])
        metrics["best_validation_loss"] = best_validation_loss
        if tracker is not None:
            tracker.log_metrics(
                {key: value for key, value in metrics.items() if isinstance(value, float)}
            )

    models_dir.mkdir(parents=True, exist_ok=True)
    figures_dir = reports_dir / "figures"
    checkpoint = {
        "state_dict": model.state_dict(),
        "input_features": len(scaled.feature_names),
        "feature_names": scaled.feature_names,
        "scaler_mean": scaled.scaler.mean_.tolist(),
        "scaler_scale": scaled.scaler.scale_.tolist(),
        "target_names": bundle.target_names,
        "label_contract": label_contract(),
        "decision_threshold": DECISION_THRESHOLD,
        "calibration_status": CALIBRATION_STATUS,
        "random_seed": seed,
    }
    torch.save(checkpoint, models_dir / "pytorch_mlp.pt")
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "pytorch_mlp_metrics.json").write_text(
        json.dumps({"validation": metrics, "history": history}, indent=2),
        encoding="utf-8",
    )
    _plot_history(history, figures_dir / "training_curve.png")
    return PytorchTrainingResult(metrics=metrics, history=history)


def load_mlp_checkpoint(path: Path = MODELS_DIR / "pytorch_mlp.pt") -> tuple[TabularMLP, dict]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    model = TabularMLP(input_features=int(checkpoint["input_features"]))
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, checkpoint


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a PyTorch tabular MLP.")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--patience", type=int, default=12)
    parser.add_argument("--mlflow", action="store_true")
    args = parser.parse_args()
    result = train_pytorch_mlp(
        seed=args.seed,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        batch_size=args.batch_size,
        patience=args.patience,
        mlflow_enabled=args.mlflow,
    )
    print(f"PyTorch MLP validation ROC-AUC: {result.metrics['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
