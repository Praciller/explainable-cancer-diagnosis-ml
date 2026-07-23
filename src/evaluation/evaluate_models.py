from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay

from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import (
    CALIBRATION_STATUS,
    DECISION_THRESHOLD,
    EDUCATIONAL_LIMITATION,
    malignant_scores,
    predictions_from_malignant_scores,
)
from src.data.load_dataset import dataset_fingerprint, load_dataset_frame
from src.features.preprocess import split_dataset, split_manifest
from src.utils.metrics import classification_metrics


def _load_training_contract(
    models_dir: Path,
    reports_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    metadata_path = models_dir / "model_metadata.json"
    baseline_path = reports_dir / "baseline_metrics.json"
    if not metadata_path.exists() or not baseline_path.exists():
        raise FileNotFoundError(
            "Training metadata is missing. Run the baseline training command first."
        )
    return (
        json.loads(metadata_path.read_text(encoding="utf-8")),
        json.loads(baseline_path.read_text(encoding="utf-8")),
    )


def _validation_models(
    baseline: dict[str, Any],
    reports_dir: Path,
) -> dict[str, dict[str, Any]]:
    metrics = dict(baseline["validation_models"])
    pytorch_path = reports_dir / "pytorch_mlp_metrics.json"
    if pytorch_path.exists():
        pytorch = json.loads(pytorch_path.read_text(encoding="utf-8"))
        metrics["pytorch_mlp"] = pytorch["validation"]
    return metrics


def _comparison_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Governed Model Evaluation",
        "",
        "## Validation-only candidate comparison",
        "",
        "| Model | ROC-AUC | PR-AUC | Balanced accuracy | Sensitivity | Specificity |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, values in report["validation_models"].items():
        marker = " (selected)" if name == report["selected_model"] else ""
        lines.append(
            f"| {name}{marker} | {values['roc_auc']:.4f} | {values['pr_auc']:.4f} | "
            f"{values['balanced_accuracy']:.4f} | {values['sensitivity']:.4f} | "
            f"{values['specificity']:.4f} |"
        )

    locked = report["locked_test"]["metrics"]
    matrix = locked["confusion_matrix"]
    lines.extend(
        [
            "",
            "## Governed test result",
            "",
            f"- Selected model: `{report['selected_model']}`",
            f"- Selection metric: `{report['selection']['metric']}`",
            f"- Fixed threshold: `{report['threshold']['value']}`",
            f"- Calibration status: `{report['calibration_status']}`",
            f"- Sample count: {locked['sample_count']}",
            f"- Confusion matrix order: malignant, benign; values: `{matrix}`",
            f"- Malignant-to-benign errors: {locked['false_negative_count']}",
            f"- Benign-to-malignant errors: {locked['false_positive_count']}",
            f"- ROC-AUC: {locked['roc_auc']:.4f}",
            f"- PR-AUC: {locked['pr_auc']:.4f}",
            "",
            "This 86-row test artifact has been exposed during prior portfolio development. "
            "It is retained as a governed regression set, not represented as a pristine "
            "scientific benchmark.",
            "",
            EDUCATIONAL_LIMITATION,
            "",
        ]
    )
    return "\n".join(lines)


def evaluate_models(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, Any]:
    metadata, baseline = _load_training_contract(models_dir, reports_dir)
    selected_model = str(metadata["model_name"])
    if selected_model != baseline["selected_model"]:
        raise ValueError("Selected-model metadata disagrees with baseline selection evidence.")

    bundle = load_dataset_frame()
    seed = int(metadata["random_seed"])
    splits = split_dataset(bundle.features, bundle.target, seed)
    governed_split = split_manifest(splits, seed)
    if governed_split["assignment_sha256"] != metadata["split_assignment_sha256"]:
        raise ValueError("Split assignment no longer matches the trained-model metadata.")

    model = joblib.load(models_dir / "best_model.joblib")
    score = malignant_scores(model.classes_, model.predict_proba(splits.X_test))
    prediction = predictions_from_malignant_scores(score, DECISION_THRESHOLD)
    locked_metrics = classification_metrics(
        splits.y_test.to_numpy(),
        prediction,
        score,
        threshold=DECISION_THRESHOLD,
    )

    reports_dir.mkdir(parents=True, exist_ok=True)
    predictions = pd.DataFrame(
        {
            "row_id": splits.X_test.index.astype(int),
            "actual_raw_target": splits.y_test.to_numpy(dtype=int),
            "predicted_raw_target": prediction.astype(int),
            "malignant_class_score": score,
        }
    ).sort_values("row_id")
    predictions.to_csv(reports_dir / "locked_test_predictions.csv", index=False)

    report: dict[str, Any] = {
        "schema_version": 1,
        "dataset_fingerprint": dataset_fingerprint(bundle),
        "selected_model": selected_model,
        "selection": {
            "metric": baseline["selection_metric"],
            "value": metadata["selection_value"],
            "tie_breaking_rule": baseline["tie_breaking_rule"],
        },
        "split": governed_split,
        "threshold": {
            "value": DECISION_THRESHOLD,
            "source": "fixed default before governed test evaluation",
        },
        "calibration_status": CALIBRATION_STATUS,
        "validation_models": _validation_models(baseline, reports_dir),
        "locked_test": {
            "status": "governed_portfolio_regression_set_previously_exposed",
            "evaluated_at": datetime.now(UTC).isoformat(),
            "metrics": locked_metrics,
        },
        "educational_limitation": EDUCATIONAL_LIMITATION,
    }

    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(5.5, 5))
    ConfusionMatrixDisplay(
        confusion_matrix=np.asarray(locked_metrics["confusion_matrix"]),
        display_labels=["malignant", "benign"],
    ).plot(ax=axis, colorbar=False, cmap="Purples")
    axis.set_title(f"Governed test confusion matrix: {selected_model}")
    figure.tight_layout()
    figure.savefig(figures_dir / "confusion_matrix.png", dpi=160)
    plt.close(figure)

    malignant_truth = splits.y_test.to_numpy() == 0
    figure, axis = plt.subplots(figsize=(7, 5.5))
    RocCurveDisplay.from_predictions(
        malignant_truth,
        score,
        name=selected_model,
        ax=axis,
    )
    axis.plot([0, 1], [0, 1], linestyle=":", color="#777777")
    axis.set_title("Selected model ROC curve on governed test set")
    figure.tight_layout()
    figure.savefig(figures_dir / "roc_curve.png", dpi=160)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7, 5.5))
    PrecisionRecallDisplay.from_predictions(
        malignant_truth,
        score,
        name=selected_model,
        ax=axis,
    )
    axis.set_title("Selected model precision-recall curve for malignant class")
    figure.tight_layout()
    figure.savefig(figures_dir / "precision_recall_curve.png", dpi=160)
    plt.close(figure)

    (reports_dir / "evaluation_metrics.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    (reports_dir / "model_comparison.md").write_text(
        _comparison_markdown(report),
        encoding="utf-8",
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the frozen selected model.")
    parser.parse_args()
    report = evaluate_models()
    print(
        "Evaluated selected model "
        f"{report['selected_model']} on {report['locked_test']['metrics']['sample_count']} "
        "governed test rows."
    )


if __name__ == "__main__":
    main()
