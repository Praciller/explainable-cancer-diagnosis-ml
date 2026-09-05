from __future__ import annotations

import argparse
import json
from math import log
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.config import MODELS_DIR, PROJECT_ROOT
from src.contracts import (
    EDUCATIONAL_LIMITATION,
    RAW_TARGET_TO_LABEL,
    SAFETY_POSITIVE_LABEL,
    SAFETY_POSITIVE_RAW_TARGET,
    score_for_raw_target,
)
from src.data.load_dataset import load_dataset_frame
from src.explainability.explain_model import _shap_values
from src.features.preprocess import split_dataset

CASE_SCHEMA_VERSION = 1
DATASET_ROW_ID = 102
RECONSTRUCTION_TOLERANCE = 1e-9
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "frontend" / "src" / "data" / "explainability_case.json"


def _direction(contribution: float) -> str:
    if contribution > 0:
        return "toward_malignant"
    if contribution < 0:
        return "away_from_malignant"
    return "neutral"


def generate_case_study_artifact(
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    metadata_path = MODELS_DIR / "model_metadata.json"
    manifest_path = MODELS_DIR / "artifact_manifest.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if metadata["model_name"] != "logistic_regression":
        raise ValueError("The explainability case study requires logistic_regression.")
    if manifest["selected_model"]["name"] != metadata["model_name"]:
        raise ValueError("Model metadata and artifact manifest selection disagree.")

    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed=int(metadata["random_seed"]))
    if DATASET_ROW_ID not in splits.X_test.index:
        raise ValueError("Dataset row 102 must belong to the locked test split.")
    if len(bundle.feature_names) != 30:
        raise ValueError("The explainability case study requires exactly 30 features.")

    model = joblib.load(MODELS_DIR / "best_model.joblib")
    sample = bundle.features.loc[[DATASET_ROW_ID]]
    background = splits.X_train.sample(min(100, len(splits.X_train)), random_state=42)
    shap_values, _, base_value = _shap_values(model, background, sample)
    contributions_by_feature = np.asarray(shap_values[0], dtype=float)
    if contributions_by_feature.shape != (len(bundle.feature_names),):
        raise ValueError("SHAP contribution count does not match the feature contract.")

    model_score = float(
        score_for_raw_target(
            model.classes_,
            model.predict_proba(sample),
            SAFETY_POSITIVE_RAW_TARGET,
        )[0]
    )
    contribution_sum = float(contributions_by_feature.sum())
    reconstructed_log_odds = float(base_value + contribution_sum)
    expected_log_odds = float(log(model_score / (1.0 - model_score)))
    reconstruction_error = abs(reconstructed_log_odds - expected_log_odds)
    row_values = sample.iloc[0].to_numpy(dtype=float)
    finite_values = np.concatenate(
        ([base_value, model_score], row_values, contributions_by_feature)
    )
    if not np.isfinite(finite_values).all():
        raise ValueError("The explainability case study contains a non-finite value.")
    if reconstruction_error > RECONSTRUCTION_TOLERANCE:
        raise ValueError("SHAP contributions do not reconstruct the malignant-class score.")

    ranked_indices = sorted(
        range(len(bundle.feature_names)),
        key=lambda index: (-abs(float(contributions_by_feature[index])), index),
    )
    contributions = [
        {
            "rank": rank,
            "feature": bundle.feature_names[index],
            "value": float(row_values[index]),
            "contribution": float(contributions_by_feature[index]),
            "absolute_contribution": abs(float(contributions_by_feature[index])),
            "direction": _direction(float(contributions_by_feature[index])),
        }
        for rank, index in enumerate(ranked_indices, start=1)
    ]
    artifact: dict[str, Any] = {
        "schema_version": CASE_SCHEMA_VERSION,
        "dataset_row_id": DATASET_ROW_ID,
        "raw_target": int(bundle.target.loc[DATASET_ROW_ID]),
        "known_label": RAW_TARGET_TO_LABEL[int(bundle.target.loc[DATASET_ROW_ID])],
        "model_name": metadata["model_name"],
        "model_version": manifest["model_version"],
        "positive_class": SAFETY_POSITIVE_LABEL,
        "output_space": "malignant_class_log_odds",
        "threshold": float(metadata["decision_threshold"]),
        "calibration_status": metadata["calibration_status"],
        "feature_order": bundle.feature_names,
        "feature_count": len(bundle.feature_names),
        "base_value": float(base_value),
        "contribution_sum": contribution_sum,
        "reconstructed_log_odds": reconstructed_log_odds,
        "model_score": model_score,
        "reconstruction_error": reconstruction_error,
        "reconstruction_tolerance": RECONSTRUCTION_TOLERANCE,
        "contributions": contributions,
        "global_explanation": (
            "Global importance summarizes recurring model behavior across governed rows; "
            "contributions do not prove biological causality."
        ),
        "local_explanation": (
            "Local contributions describe how this supplied dataset row moved the selected "
            "model output in malignant-class log-odds space. Correlated measurements can "
            "share or redistribute importance."
        ),
        "educational_limitation": EDUCATIONAL_LIMITATION,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the static explainability case study.")
    parser.parse_args()
    artifact = generate_case_study_artifact()
    print(
        f"Generated row {artifact['dataset_row_id']} explainability case "
        f"for {artifact['model_name']} ({artifact['model_version']})."
    )


if __name__ == "__main__":
    main()
