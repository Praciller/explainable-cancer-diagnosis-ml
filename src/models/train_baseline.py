from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config import MODELS_DIR, RANDOM_SEED, REPORTS_DIR
from src.contracts import (
    CALIBRATION_STATUS,
    DECISION_THRESHOLD,
    malignant_scores,
    predictions_from_malignant_scores,
)
from src.data.load_dataset import dataset_fingerprint, load_dataset_frame
from src.features.preprocess import split_dataset, split_manifest
from src.utils.metrics import classification_metrics
from src.utils.tracking import optional_mlflow_run


@dataclass(frozen=True)
class BaselineTrainingResult:
    best_model_name: str
    metrics: dict[str, dict[str, Any]]


def _models(seed: int) -> dict[str, Any]:
    return {
        "dummy_majority": DummyClassifier(strategy="most_frequent"),
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
        "| Model | Validation ROC-AUC | PR-AUC | Balanced accuracy | Sensitivity | Specificity |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, values in metrics.items():
        marker = " (best)" if name == best_model else ""
        rows.append(
            f"| {name}{marker} | {values['roc_auc']:.4f} | "
            f"{values['pr_auc']:.4f} | {values['balanced_accuracy']:.4f} | "
            f"{values['sensitivity']:.4f} | {values['specificity']:.4f} |"
        )
    return (
        "# Validation Model Comparison\n\n"
        "Candidate selection uses validation evidence only. The governed test set is "
        "not included in this table.\n\n" + "\n".join(rows) + "\n"
    )


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
            validation_score = malignant_scores(
                model.classes_,
                model.predict_proba(splits.X_validation),
            )
            validation_prediction = predictions_from_malignant_scores(validation_score)
            values = classification_metrics(
                splits.y_validation.to_numpy(),
                validation_prediction,
                validation_score,
            )
            metrics[name] = values
            trained_models[name] = model
            joblib.dump(model, models_dir / f"{name}.joblib")
            if tracker is not None:
                tracker.log_metrics(
                    {key: value for key, value in values.items() if isinstance(value, float)}
                )

    selection_priority = (
        "logistic_regression",
        "random_forest",
        "gradient_boosting",
    )
    best_model_name = max(
        selection_priority,
        key=lambda name: (metrics[name]["roc_auc"], -selection_priority.index(name)),
    )
    joblib.dump(trained_models[best_model_name], models_dir / "best_model.joblib")
    dataset_hash = dataset_fingerprint(bundle)
    governed_split = split_manifest(splits, seed)
    payload = {
        "selected_model": best_model_name,
        "selection_metric": "validation_roc_auc",
        "tie_breaking_rule": (
            "Highest validation ROC-AUC; ties prefer logistic_regression, then "
            "random_forest, then gradient_boosting for lower complexity and interpretability."
        ),
        "decision_threshold": DECISION_THRESHOLD,
        "calibration_status": CALIBRATION_STATUS,
        "feature_names": bundle.feature_names,
        "target_names": bundle.target_names,
        "random_seed": seed,
        "dataset_fingerprint": dataset_hash,
        "training_date": datetime.now(UTC).isoformat(),
        "validation_models": metrics,
        "split": governed_split,
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
                "raw_classes": [0, 1],
                "random_seed": seed,
                "dataset_fingerprint": dataset_hash,
                "selection_metric": "validation_roc_auc",
                "selection_value": metrics[best_model_name]["roc_auc"],
                "decision_threshold": DECISION_THRESHOLD,
                "calibration_status": CALIBRATION_STATUS,
                "split_assignment_sha256": governed_split["assignment_sha256"],
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
