from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
)

from src.config import MODELS_DIR, REPORTS_DIR
from src.data.load_dataset import load_dataset_frame
from src.features.preprocess import prepare_scaled_splits, split_dataset
from src.models.train_pytorch_mlp import load_mlp_checkpoint
from src.utils.metrics import classification_metrics


def _load_seed(models_dir: Path) -> int:
    metadata_path = models_dir / "model_metadata.json"
    if not metadata_path.exists():
        return 42
    return int(json.loads(metadata_path.read_text(encoding="utf-8"))["random_seed"])


def _pytorch_predictions(
    checkpoint_path: Path,
    raw_features: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    import torch

    model, checkpoint = load_mlp_checkpoint(checkpoint_path)
    mean = np.asarray(checkpoint["scaler_mean"])
    scale = np.asarray(checkpoint["scaler_scale"])
    scaled = (raw_features - mean) / scale
    with torch.inference_mode():
        benign = torch.sigmoid(
            model(torch.tensor(scaled, dtype=torch.float32))
        ).numpy()
    return (benign >= 0.5).astype(int), 1 - benign


def _comparison_markdown(metrics: dict[str, dict[str, Any]]) -> str:
    lines = [
        "# Model Comparison",
        "",
        "| Model | Accuracy | Precision | Recall | F1 | Macro F1 | ROC-AUC | Sensitivity | Specificity |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, values in metrics.items():
        lines.append(
            f"| {name} | {values['accuracy']:.4f} | {values['precision']:.4f} | "
            f"{values['recall']:.4f} | {values['f1']:.4f} | "
            f"{values['macro_f1']:.4f} | {values['roc_auc']:.4f} | "
            f"{values['sensitivity']:.4f} | {values['specificity']:.4f} |"
        )
    return "\n".join(lines) + "\n"


def evaluate_models(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, dict[str, Any]]:
    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, _load_seed(models_dir))
    model_names = ["logistic_regression", "random_forest", "gradient_boosting"]
    predictions: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for name in model_names:
        path = models_dir / f"{name}.joblib"
        if path.exists():
            model = joblib.load(path)
            predictions[name] = (
                model.predict(splits.X_test),
                model.predict_proba(splits.X_test)[:, 0],
            )
    if (models_dir / "pytorch_mlp.pt").exists():
        predictions["pytorch_mlp"] = _pytorch_predictions(
            models_dir / "pytorch_mlp.pt",
            splits.X_test.to_numpy(),
        )
    if not predictions:
        raise FileNotFoundError("No trained model artifacts were found.")

    metrics = {
        name: classification_metrics(
            splits.y_test.to_numpy(),
            prediction,
            malignant_probability,
        )
        for name, (prediction, malignant_probability) in predictions.items()
    }
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    best_name = max(metrics, key=lambda name: metrics[name]["roc_auc"])
    figure, axis = plt.subplots(figsize=(5.5, 5))
    ConfusionMatrixDisplay(
        confusion_matrix=np.asarray(metrics[best_name]["confusion_matrix"]),
        display_labels=bundle.target_names,
    ).plot(ax=axis, colorbar=False, cmap="Purples")
    axis.set_title(f"Confusion matrix: {best_name}")
    figure.tight_layout()
    figure.savefig(figures_dir / "confusion_matrix.png", dpi=160)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7, 5.5))
    for name, (_, probability) in predictions.items():
        RocCurveDisplay.from_predictions(
            splits.y_test == 0,
            probability,
            name=name,
            ax=axis,
        )
    axis.plot([0, 1], [0, 1], linestyle=":", color="#777777")
    axis.set_title("ROC curves on shared test set")
    figure.tight_layout()
    figure.savefig(figures_dir / "roc_curve.png", dpi=160)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7, 5.5))
    for name, (_, probability) in predictions.items():
        PrecisionRecallDisplay.from_predictions(
            splits.y_test == 0,
            probability,
            name=name,
            ax=axis,
        )
    axis.set_title("Precision-recall curves for malignant class")
    figure.tight_layout()
    figure.savefig(figures_dir / "precision_recall_curve.png", dpi=160)
    plt.close(figure)

    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "evaluation_metrics.json").write_text(
        json.dumps({"best_test_model": best_name, "models": metrics}, indent=2),
        encoding="utf-8",
    )
    (reports_dir / "model_comparison.md").write_text(
        _comparison_markdown(metrics),
        encoding="utf-8",
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate all trained models.")
    parser.parse_args()
    metrics = evaluate_models()
    print(f"Evaluated {len(metrics)} models.")


if __name__ == "__main__":
    main()
