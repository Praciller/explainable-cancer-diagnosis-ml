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
    prediction = model.predict(splits.X_test)
    probabilities = model.predict_proba(splits.X_test)
    confidence = probabilities.max(axis=1)
    malignant_probability = probabilities[:, 0]

    analysis = splits.X_test.copy()
    analysis.insert(0, "sample_index", analysis.index)
    analysis["actual_class"] = splits.y_test.map(dict(enumerate(bundle.target_names)))
    analysis["predicted_class"] = pd.Series(
        prediction,
        index=analysis.index,
    ).map(dict(enumerate(bundle.target_names)))
    analysis["confidence"] = confidence
    analysis["malignant_probability"] = malignant_probability
    analysis["error_type"] = np.select(
        [
            (splits.y_test.to_numpy() == 0) & (prediction == 1),
            (splits.y_test.to_numpy() == 1) & (prediction == 0),
            confidence < 0.65,
        ],
        ["false_negative", "false_positive", "low_confidence"],
        default="correct",
    )
    notable = analysis[analysis["error_type"] != "correct"].sort_values("confidence")

    reports_dir.mkdir(parents=True, exist_ok=True)
    notable.to_csv(reports_dir / "error_analysis.csv", index=False)
    counts = analysis["error_type"].value_counts()
    (reports_dir / "error_analysis.md").write_text(
        "# Error Analysis\n\n"
        f"Best baseline model: `{metadata['model_name']}`.\n\n"
        f"- False negatives (malignant predicted benign): {int(counts.get('false_negative', 0))}\n"
        f"- False positives (benign predicted malignant): {int(counts.get('false_positive', 0))}\n"
        f"- Other low-confidence predictions: {int(counts.get('low_confidence', 0))}\n\n"
        "False negatives are the more concerning error in this educational diagnostic framing. "
        "Threshold changes trade sensitivity against specificity and cannot establish clinical "
        "suitability on this small public dataset.\n",
        encoding="utf-8",
    )

    thresholds = np.linspace(0.05, 0.95, 37)
    sensitivity: list[float] = []
    specificity: list[float] = []
    y_true = splits.y_test.to_numpy()
    for threshold in thresholds:
        malignant_prediction = malignant_probability >= threshold
        sensitivity.append(float(malignant_prediction[y_true == 0].mean()))
        specificity.append(float((~malignant_prediction[y_true == 1]).mean()))

    figure, axis = plt.subplots(figsize=(7, 5))
    axis.plot(thresholds, sensitivity, label="Sensitivity", color="#d36d5f")
    axis.plot(thresholds, specificity, label="Specificity", color="#6c9b76")
    axis.axvline(0.5, linestyle=":", color="#713c78", label="Default threshold")
    axis.set(
        xlabel="Malignant probability threshold",
        ylabel="Rate",
        ylim=(0, 1.02),
        title="Threshold trade-off analysis",
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
