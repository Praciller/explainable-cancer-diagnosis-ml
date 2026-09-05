from __future__ import annotations

import json
from math import exp, log
from pathlib import Path

import joblib
import numpy as np

CASE_PATH = Path(__file__).parents[1] / "frontend" / "src" / "data" / "explainability_case.json"


def test_case_study_provenance_and_reconstruction() -> None:
    from src.config import MODELS_DIR
    from src.contracts import SAFETY_POSITIVE_RAW_TARGET
    from src.data.load_dataset import load_dataset_frame
    from src.features.preprocess import split_dataset

    artifact = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    bundle = load_dataset_frame()
    metadata = json.loads((MODELS_DIR / "model_metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((MODELS_DIR / "artifact_manifest.json").read_text(encoding="utf-8"))
    splits = split_dataset(bundle.features, bundle.target, seed=42)
    model = joblib.load(MODELS_DIR / "best_model.joblib")
    sample = bundle.features.loc[[102]]

    assert artifact["schema_version"] == 1
    assert artifact["dataset_row_id"] == 102
    assert 102 in splits.X_test.index
    assert artifact["raw_target"] == int(bundle.target.loc[102]) == 1
    assert artifact["known_label"] == "benign"
    assert artifact["model_name"] == metadata["model_name"] == "logistic_regression"
    assert artifact["model_version"] == manifest["model_version"]
    assert artifact["positive_class"] == "malignant"
    assert artifact["output_space"] == "malignant_class_log_odds"
    assert artifact["threshold"] == metadata["decision_threshold"] == 0.5
    assert artifact["calibration_status"] == metadata["calibration_status"] == "uncalibrated"
    assert artifact["feature_order"] == bundle.feature_names
    assert artifact["feature_count"] == len(bundle.feature_names) == 30
    assert len(artifact["contributions"]) == 30
    assert "model_score_logit" not in artifact

    contributions = artifact["contributions"]
    assert [item["rank"] for item in contributions] == list(range(1, 31))
    assert [item["feature"] for item in contributions] == [
        item["feature"]
        for item in sorted(
            contributions,
            key=lambda item: (-item["absolute_contribution"], item["rank"]),
        )
    ]
    assert all(
        item["direction"]
        == (
            "toward_malignant"
            if item["contribution"] > 0
            else "away_from_malignant"
            if item["contribution"] < 0
            else "neutral"
        )
        for item in contributions
    )
    finite_values = [
        artifact["base_value"],
        artifact["contribution_sum"],
        artifact["reconstructed_log_odds"],
        artifact["model_score"],
        artifact["reconstruction_error"],
        *[value for item in contributions for value in item.values() if isinstance(value, float)],
    ]
    assert np.isfinite(finite_values).all()

    reconstructed = artifact["base_value"] + artifact["contribution_sum"]
    assert np.isclose(artifact["reconstructed_log_odds"], reconstructed, atol=1e-9)

    probabilities = model.predict_proba(sample)
    malignant_column = list(model.classes_).index(SAFETY_POSITIVE_RAW_TARGET)
    model_score = float(probabilities[0, malignant_column])
    expected_log_odds = log(model_score / (1.0 - model_score))
    assert np.isclose(artifact["reconstructed_log_odds"], expected_log_odds, atol=1e-9)
    assert np.isclose(
        artifact["model_score"],
        1.0 / (1.0 + exp(-artifact["reconstructed_log_odds"])),
        atol=1e-9,
    )
    assert artifact["reconstruction_error"] <= artifact["reconstruction_tolerance"]
