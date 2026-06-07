from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import REPORTS_DIR
from src.data.load_dataset import DatasetBundle, load_dataset_frame


def build_validation_report(bundle: DatasetBundle) -> str:
    features = bundle.features
    target_counts = bundle.frame["label"].value_counts()
    missing = bundle.frame.isna().sum()
    duplicate_count = int(bundle.features.duplicated().sum())
    imbalance_ratio = float(target_counts.max() / target_counts.min())
    imbalance_summary = (
        "Class imbalance is mild and is handled with stratified splits."
        if imbalance_ratio < 2
        else "Class imbalance is material and requires mitigation."
    )
    ranges = pd.DataFrame({"min": features.min(), "max": features.max()})
    outliers = ((features - features.mean()).abs() > 3 * features.std()).sum()

    return (
        "# Data Validation Report\n\n"
        "## Summary\n\n"
        f"- Rows: {len(bundle.frame)}\n"
        f"- Numeric features: {len(bundle.feature_names)}\n"
        f"- Duplicate feature rows: {duplicate_count}\n"
        f"- Missing values: {int(missing.sum())}\n"
        f"- Class ratio: {imbalance_ratio:.2f}\n"
        f"- Assessment: {imbalance_summary}\n\n"
        "## Target Distribution\n\n"
        f"{target_counts.to_frame('count').to_markdown()}\n\n"
        "## Missing Values\n\n"
        f"{missing.to_frame('count').to_markdown()}\n\n"
        "## Feature Data Types\n\n"
        f"{features.dtypes.astype(str).to_frame('dtype').to_markdown()}\n\n"
        "## Numeric Feature Ranges\n\n"
        f"{ranges.to_markdown(floatfmt='.4f')}\n\n"
        "## Outlier Summary\n\n"
        "Counts use a simple three-standard-deviation screen and are descriptive, "
        "not grounds for automatic removal.\n\n"
        f"{outliers.to_frame('count').to_markdown()}\n"
    )


def save_validation_report(
    output_path: Path = REPORTS_DIR / "data_validation_report.md",
) -> str:
    report = build_validation_report(load_dataset_frame())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the breast cancer dataset.")
    parser.add_argument(
        "--output-path",
        type=Path,
        default=REPORTS_DIR / "data_validation_report.md",
    )
    args = parser.parse_args()
    save_validation_report(args.output_path)
    print(f"Saved validation report to {args.output_path}")


if __name__ == "__main__":
    main()
