from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer

from src.config import (
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    REPORTS_DIR,
    SAMPLE_DATA_PATH,
)


@dataclass(frozen=True)
class DatasetBundle:
    frame: pd.DataFrame
    features: pd.DataFrame
    target: pd.Series
    feature_names: list[str]
    target_names: list[str]
    description: str


def load_dataset_frame() -> DatasetBundle:
    dataset = load_breast_cancer(as_frame=True)
    target_names = [str(name) for name in dataset.target_names]
    if target_names != ["malignant", "benign"]:
        raise ValueError(f"Unexpected target mapping: {target_names}")

    feature_names = [str(name) for name in dataset.feature_names]
    features = dataset.data.copy()
    features.columns = feature_names
    target = dataset.target.astype("int64").rename("target")
    frame = features.assign(target=target, label=target.map(dict(enumerate(target_names))))

    return DatasetBundle(
        frame=frame,
        features=features,
        target=target,
        feature_names=feature_names,
        target_names=target_names,
        description=dataset.DESCR,
    )


def _metadata_markdown(bundle: DatasetBundle) -> str:
    feature_lines = "\n".join(f"- `{name}`" for name in bundle.feature_names)
    return (
        "# Dataset Metadata\n\n"
        "## Source\n\n"
        "`sklearn.datasets.load_breast_cancer(as_frame=True)`\n\n"
        "## Shape\n\n"
        f"- Rows: {len(bundle.frame)}\n"
        f"- Numeric features: {len(bundle.feature_names)}\n"
        f"- Saved columns: {bundle.frame.shape[1]}\n\n"
        "## Target Mapping\n\n"
        f"- `0`: {bundle.target_names[0]}\n"
        f"- `1`: {bundle.target_names[1]}\n\n"
        "## Features\n\n"
        f"{feature_lines}\n"
    )


def save_dataset_assets(
    raw_path: Path = RAW_DATA_PATH,
    metadata_path: Path = REPORTS_DIR / "dataset_metadata.md",
) -> DatasetBundle:
    bundle = load_dataset_frame()
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    bundle.frame.to_csv(raw_path, index=False)
    metadata_path.write_text(_metadata_markdown(bundle), encoding="utf-8")
    return bundle


def save_portfolio_data(
    processed_path: Path = PROCESSED_DATA_PATH,
    sample_path: Path = SAMPLE_DATA_PATH,
    sample_rows: int = 6,
) -> DatasetBundle:
    bundle = load_dataset_frame()
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    bundle.frame.to_csv(processed_path, index=False)
    bundle.features.head(sample_rows).to_csv(sample_path, index=False)
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Load the scikit-learn breast cancer dataset.")
    parser.add_argument("--raw-path", type=Path, default=RAW_DATA_PATH)
    parser.add_argument(
        "--metadata-path",
        type=Path,
        default=REPORTS_DIR / "dataset_metadata.md",
    )
    args = parser.parse_args()
    bundle = save_dataset_assets(args.raw_path, args.metadata_path)
    save_portfolio_data()
    print(f"Saved {len(bundle.frame)} rows to {args.raw_path}")


if __name__ == "__main__":
    main()
