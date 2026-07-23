from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import (
    DECISION_THRESHOLD,
    EDUCATIONAL_LIMITATION,
    RAW_TARGET_TO_LABEL,
    malignant_scores,
    predictions_from_malignant_scores,
)
from src.data.load_dataset import load_dataset_frame
from src.features.preprocess import split_dataset


def generate_error_analysis(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> pd.DataFrame:
    metadata = json.loads((models_dir / "model_metadata.json").read_text(encoding="utf-8"))
    model = joblib.load(models_dir / "best_model.joblib")
    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, int(metadata["random_seed"]))
    malignant_score = malignant_scores(model.classes_, model.predict_proba(splits.X_test))
    prediction = predictions_from_malignant_scores(malignant_score)
    threshold_margin = np.abs(malignant_score - DECISION_THRESHOLD)

    analysis = splits.X_test.copy()
    analysis.insert(0, "sample_index", analysis.index)
    analysis["actual_class"] = splits.y_test.map(RAW_TARGET_TO_LABEL)
    analysis["predicted_class"] = pd.Series(
        prediction,
        index=analysis.index,
    ).map(RAW_TARGET_TO_LABEL)
    analysis["malignant_class_score"] = malignant_score
    analysis["threshold_margin"] = threshold_margin
    analysis["error_type"] = np.select(
        [
            (splits.y_test.to_numpy() == 0) & (prediction == 1),
            (splits.y_test.to_numpy() == 1) & (prediction == 0),
            threshold_margin < 0.15,
        ],
        ["false_negative", "false_positive", "near_threshold"],
        default="correct",
    )
    notable = analysis[analysis["error_type"] != "correct"].sort_values("threshold_margin")

    reports_dir.mkdir(parents=True, exist_ok=True)
    notable.to_csv(reports_dir / "error_analysis.csv", index=False)
    counts = analysis["error_type"].value_counts()
    (reports_dir / "error_analysis.md").write_text(
        "# Error Analysis\n\n"
        f"Best baseline model: `{metadata['model_name']}`.\n\n"
        f"- False negatives (malignant predicted benign): {int(counts.get('false_negative', 0))}\n"
        f"- False positives (benign predicted malignant): {int(counts.get('false_positive', 0))}\n"
        f"- Other near-threshold rows: {int(counts.get('near_threshold', 0))}\n\n"
        "Rows are identified by stable dataset indices. This review does not tune the model "
        "or threshold after inspecting the governed test set. A few errors do not support "
        "biological or medical conclusions.\n\n"
        f"{EDUCATIONAL_LIMITATION}\n",
        encoding="utf-8",
    )

    thresholds = np.linspace(0.05, 0.95, 37)
    sensitivity: list[float] = []
    specificity: list[float] = []
    validation_score = malignant_scores(
        model.classes_,
        model.predict_proba(splits.X_validation),
    )
    y_true = splits.y_validation.to_numpy()
    for threshold in thresholds:
        malignant_prediction = validation_score >= threshold
        sensitivity.append(float(malignant_prediction[y_true == 0].mean()))
        specificity.append(float((~malignant_prediction[y_true == 1]).mean()))

    figure, axis = plt.subplots(figsize=(7, 5))
    axis.plot(thresholds, sensitivity, label="Sensitivity", color="#d36d5f")
    axis.plot(thresholds, specificity, label="Specificity", color="#6c9b76")
    axis.axvline(
        DECISION_THRESHOLD,
        linestyle=":",
        color="#713c78",
        label="Fixed default threshold",
    )
    axis.set(
        xlabel="Malignant-class score threshold",
        ylabel="Rate",
        ylim=(0, 1.02),
        title="Validation-only threshold trade-off",
    )
    axis.legend(frameon=False)
    axis.grid(alpha=0.2)
    figure.tight_layout()
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(figures_dir / "threshold_analysis.png", dpi=160)
    plt.close(figure)
    return notable


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate prediction error analysis.")
    parser.parse_args()
    rows = generate_error_analysis()
    print(f"Saved {len(rows)} notable predictions.")


if __name__ == "__main__":
    main()
