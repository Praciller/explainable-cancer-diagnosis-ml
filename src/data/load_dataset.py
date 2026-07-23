from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.datasets import load_breast_cancer

from src.config import (
    PROCESSED_DATA_PATH,
    RAW_DATA_PATH,
    REPORTS_DIR,
    SAMPLE_DATA_PATH,
)
from src.contracts import (
    EDUCATIONAL_LIMITATION,
    LABEL_TO_RAW_TARGET,
    RAW_TARGET_TO_LABEL,
    label_contract,
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


def dataset_fingerprint(bundle: DatasetBundle | None = None) -> str:
    resolved = bundle or load_dataset_frame()
    canonical_csv = resolved.frame.to_csv(index=False, lineterminator="\n")
    return hashlib.sha256(canonical_csv.encode("utf-8")).hexdigest()


def _metadata_markdown(bundle: DatasetBundle) -> str:
    feature_lines = "\n".join(f"- `{name}`" for name in bundle.feature_names)
    class_counts = bundle.target.value_counts().sort_index()
    fingerprint = dataset_fingerprint(bundle)
    return (
        "# Dataset Metadata\n\n"
        "## Source\n\n"
        "`sklearn.datasets.load_breast_cancer(as_frame=True)` using the Breast Cancer "
        "Wisconsin (Diagnostic) dataset. The source measurements were computed from "
        "digitized images of fine-needle aspirate samples. The bundled scikit-learn "
        "description attributes the data to Wolberg, Street, and Mangasarian and the "
        "University of Wisconsin.\n\n"
        f"- scikit-learn version: `{sklearn.__version__}`\n"
        f"- Canonical CSV SHA-256: `{fingerprint}`\n"
        "- Physical units: not specified by the bundled dataset documentation\n\n"
        "## Shape\n\n"
        f"- Rows: {len(bundle.frame)}\n"
        f"- Numeric features: {len(bundle.feature_names)}\n"
        f"- Saved columns: {bundle.frame.shape[1]}\n\n"
        "## Target Mapping\n\n"
        f"- `0`: {bundle.target_names[0]}\n"
        f"- `1`: {bundle.target_names[1]}\n"
        f"- Malignant rows: {int(class_counts[LABEL_TO_RAW_TARGET['malignant']])}\n"
        f"- Benign rows: {int(class_counts[LABEL_TO_RAW_TARGET['benign']])}\n"
        f"- Safety-relevant positive class: `{RAW_TARGET_TO_LABEL[0]}` (`0`)\n"
        f"- Shared contract: `{label_contract()}`\n\n"
        "## Features\n\n"
        f"{feature_lines}\n\n"
        "Each row is an educational dataset record, not a current patient or a "
        "general-user symptom questionnaire. The dataset is small, clean, and not "
        "clinically representative.\n\n"
        f"{EDUCATIONAL_LIMITATION}\n"
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
