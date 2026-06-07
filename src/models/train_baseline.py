from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import MODELS_DIR, RANDOM_SEED, REPORTS_DIR
from src.data.load_dataset import load_dataset_frame
from src.features.preprocess import split_dataset
from src.utils.metrics import classification_metrics
from src.utils.tracking import optional_mlflow_run


@dataclass(frozen=True)
class BaselineTrainingResult:
    best_model_name: str
    metrics: dict[str, dict[str, Any]]


def _models(seed: int) -> dict[str, Any]:
    return {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(max_iter=2000, random_state=seed),
                ),
            ]
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=seed,
            n_jobs=-1,
        ),
        "gradient_boosting": GradientBoostingClassifier(random_state=seed),
    }


def _comparison_markdown(metrics: dict[str, dict[str, Any]], best_model: str) -> str:
    rows = [
        "| Model | Validation ROC-AUC | Accuracy | Precision | Recall | F1 |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, values in metrics.items():
        marker = " (best)" if name == best_model else ""
        rows.append(
            f"| {name}{marker} | {values['validation_roc_auc']:.4f} | "
            f"{values['accuracy']:.4f} | {values['precision']:.4f} | "
            f"{values['recall']:.4f} | {values['f1']:.4f} |"
        )
    return "# Baseline Model Comparison\n\n" + "\n".join(rows) + "\n"


def train_baseline_models(
    seed: int = RANDOM_SEED,
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
    mlflow_enabled: bool = False,
) -> BaselineTrainingResult:
    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed)
    models_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics: dict[str, dict[str, Any]] = {}
    trained_models: dict[str, Any] = {}
    for name, model in _models(seed).items():
        with optional_mlflow_run(
            mlflow_enabled,
            name,
            {"model_name": name, "random_seed": seed, "dataset_version": "sklearn-wdbc"},
        ) as tracker:
            model.fit(splits.X_train, splits.y_train)
            validation_prediction = model.predict(splits.X_validation)
            validation_probability = model.predict_proba(splits.X_validation)[:, 0]
            test_prediction = model.predict(splits.X_test)
            test_probability = model.predict_proba(splits.X_test)[:, 0]
            values = classification_metrics(
                splits.y_test.to_numpy(),
                test_prediction,
                test_probability,
            )
            values["validation_roc_auc"] = classification_metrics(
                splits.y_validation.to_numpy(),
                validation_prediction,
                validation_probability,
            )["roc_auc"]
            metrics[name] = values
            trained_models[name] = model
            joblib.dump(model, models_dir / f"{name}.joblib")
            if tracker is not None:
                tracker.log_metrics(
                    {key: value for key, value in values.items() if isinstance(value, float)}
                )

    best_model_name = max(metrics, key=lambda name: metrics[name]["validation_roc_auc"])
    joblib.dump(trained_models[best_model_name], models_dir / "best_model.joblib")
    dataset_hash = hashlib.sha256(
        bundle.frame.to_csv(index=False).encode("utf-8")
    ).hexdigest()[:16]
    payload = {
        "best_model": best_model_name,
        "selection_metric": "validation_roc_auc",
        "feature_names": bundle.feature_names,
        "target_names": bundle.target_names,
        "random_seed": seed,
        "dataset_version": dataset_hash,
        "training_date": datetime.now(UTC).isoformat(),
        "models": metrics,
    }
    (reports_dir / "baseline_metrics.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    (models_dir / "model_metadata.json").write_text(
        json.dumps(
            {
                "model_name": best_model_name,
                "problem_type": "binary_classification",
                "features": len(bundle.feature_names),
                "feature_names": bundle.feature_names,
                "classes": bundle.target_names,
                "random_seed": seed,
                "dataset_version": dataset_hash,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (reports_dir / "model_comparison.md").write_text(
        _comparison_markdown(metrics, best_model_name),
        encoding="utf-8",
    )
    return BaselineTrainingResult(best_model_name=best_model_name, metrics=metrics)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train baseline scikit-learn models.")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--mlflow", action="store_true")
    args = parser.parse_args()
    result = train_baseline_models(seed=args.seed, mlflow_enabled=args.mlflow)
    print(f"Best baseline model: {result.best_model_name}")


if __name__ == "__main__":
    main()
