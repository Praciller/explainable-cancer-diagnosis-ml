from __future__ import annotations

import argparse
import csv
import json
from math import log
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.artifacts.manifest import validate_artifact_manifest
from src.config import MODELS_DIR, PROJECT_ROOT
from src.contracts import (
    CALIBRATION_STATUS,
    DECISION_THRESHOLD,
    EDUCATIONAL_LIMITATION,
    RAW_TARGET_TO_LABEL,
    SAFETY_POSITIVE_LABEL,
    SAFETY_POSITIVE_RAW_TARGET,
    malignant_scores,
    predictions_from_malignant_scores,
    score_for_raw_target,
)
from src.data.load_dataset import load_dataset_frame
from src.explainability.explain_model import _shap_values
from src.features.preprocess import split_dataset

CASE_SCHEMA_VERSION = 1
DATASET_ROW_ID = 102
RECONSTRUCTION_TOLERANCE = 1e-9
REPLAY_ATOL = 1e-9
REPLAY_RTOL = 0.0
LOCKED_TEST_ROW_COUNT = 86
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "frontend" / "src" / "data" / "explainability_case.json"
DEFAULT_SHOWCASE_PATH = PROJECT_ROOT / "frontend" / "src" / "data" / "showcase_contract.json"
DEFAULT_LOCKED_TEST_PATH = PROJECT_ROOT / "reports" / "locked_test_predictions.csv"
LOCKED_TEST_COLUMNS = (
    "row_id",
    "actual_raw_target",
    "predicted_raw_target",
    "malignant_class_score",
)


def _direction(contribution: float) -> str:
    if contribution > 0:
        return "toward_malignant"
    if contribution < 0:
        return "away_from_malignant"
    return "neutral"


def build_case_study_artifact() -> dict[str, Any]:
    metadata_path = MODELS_DIR / "model_metadata.json"
    manifest_path = MODELS_DIR / "artifact_manifest.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if metadata["model_name"] != "logistic_regression":
        raise ValueError("The explainability case study requires logistic_regression.")
    if manifest["selected_model"]["name"] != metadata["model_name"]:
        raise ValueError("Model metadata and artifact manifest selection disagree.")
    if metadata["decision_threshold"] != DECISION_THRESHOLD:
        raise ValueError("Model metadata decision threshold disagrees with the contract.")
    if metadata["calibration_status"] != CALIBRATION_STATUS:
        raise ValueError("Model metadata calibration status disagrees with the contract.")

    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed=int(metadata["random_seed"]))
    if metadata["feature_names"] != bundle.feature_names:
        raise ValueError("Model metadata feature order disagrees with the dataset contract.")
    if manifest["feature_names"] != bundle.feature_names:
        raise ValueError("Artifact manifest feature order disagrees with the dataset contract.")
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
        "threshold": float(DECISION_THRESHOLD),
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
    return artifact


def write_case_study_artifact(
    artifact: dict[str, Any],
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")


def generate_case_study_artifact(
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> dict[str, Any]:
    artifact = build_case_study_artifact()
    write_case_study_artifact(artifact, output_path)
    return artifact


def _require_equal(actual: object, expected: object, message: str) -> None:
    if actual != expected:
        raise ValueError(f"{message}: expected {expected!r}, got {actual!r}.")


def _require_close(actual: object, expected: object, message: str) -> float:
    actual_value = float(actual)
    expected_value = float(expected)
    if not np.isclose(actual_value, expected_value, rtol=REPLAY_RTOL, atol=REPLAY_ATOL):
        raise ValueError(
            f"{message}: expected {expected_value!r}, got {actual_value!r}; "
            f"delta={abs(actual_value - expected_value)!r}."
        )
    return abs(actual_value - expected_value)


def verify_canonical_case_identity(
    case: dict[str, Any],
    showcase: dict[str, Any],
) -> None:
    model_info = showcase["model_info"]
    evaluation = showcase["evaluation"]
    dataset = showcase["dataset"]
    split = evaluation["split"]

    exact_pairs = {
        "model name": (case["model_name"], model_info["model_name"]),
        "model version": (case["model_version"], model_info["model_version"]),
        "positive class": (case["positive_class"], model_info["positive_class"]),
        "threshold": (case["threshold"], model_info["decision_threshold"]),
        "calibration status": (
            case["calibration_status"],
            model_info["calibration_status"],
        ),
        "feature count": (case["feature_count"], model_info["features"]),
    }
    for label, (actual, expected) in exact_pairs.items():
        _require_equal(actual, expected, f"Canonical {label} parity failed")

    _require_equal(
        model_info["dataset_fingerprint"],
        dataset["fingerprint_sha256"],
        "Canonical dataset fingerprint parity failed",
    )
    _require_equal(
        model_info["model_name"],
        evaluation["selected_model"],
        "Canonical selected model parity failed",
    )
    _require_equal(
        split["assignment_sha256"],
        showcase["evaluation"]["split"]["assignment_sha256"],
        "Canonical split assignment parity failed",
    )
    _require_equal(
        evaluation["threshold"]["value"],
        model_info["decision_threshold"],
        "Canonical threshold parity failed",
    )
    _require_equal(
        evaluation["calibration_status"],
        model_info["calibration_status"],
        "Canonical calibration parity failed",
    )


def verify_semantic_manifest_replay(
    manifest: dict[str, Any],
    showcase: dict[str, Any],
) -> None:
    model_info = showcase["model_info"]
    evaluation = showcase["evaluation"]
    expected_split = evaluation["split"]
    actual_split = manifest["split"]

    exact_pairs = {
        "dataset fingerprint": (
            manifest["dataset"]["fingerprint_sha256"],
            model_info["dataset_fingerprint"],
        ),
        "feature count": (manifest["dataset"]["features"], model_info["features"]),
        "selected model": (
            manifest["selected_model"]["name"],
            evaluation["selected_model"],
        ),
        "split seed": (actual_split["seed"], expected_split["seed"]),
        "split row counts": (actual_split["row_counts"], expected_split["row_counts"]),
        "split assignment": (
            actual_split["assignment_sha256"],
            expected_split["assignment_sha256"],
        ),
        "threshold": (manifest["threshold"]["value"], model_info["decision_threshold"]),
        "calibration status": (
            manifest["calibration_status"],
            model_info["calibration_status"],
        ),
        "class counts": (
            manifest["dataset"]["class_counts"],
            showcase["dataset"]["class_counts"],
        ),
    }
    for label, (actual, expected) in exact_pairs.items():
        _require_equal(actual, expected, f"Semantic manifest {label} parity failed")

    _require_close(
        manifest["selected_model"]["validation_value"],
        evaluation["selection"]["value"],
        "Semantic manifest validation selection parity failed",
    )
    _require_equal(
        manifest["selected_model"]["selection_metric"],
        evaluation["selection"]["metric"],
        "Semantic manifest selection metric parity failed",
    )


def _verify_contributions(
    committed: list[dict[str, Any]],
    generated: list[dict[str, Any]],
) -> float:
    _require_equal(len(generated), len(committed), "SHAP contribution count parity failed")
    _require_equal(len(generated), 30, "SHAP contribution count contract failed")
    _require_equal(
        [item["rank"] for item in generated],
        list(range(1, len(generated) + 1)),
        "Generated SHAP ranks are invalid",
    )
    _require_equal(
        [item["rank"] for item in committed],
        list(range(1, len(committed) + 1)),
        "Canonical SHAP ranks are invalid",
    )

    committed_by_feature = {item["feature"]: item for item in committed}
    generated_by_feature = {item["feature"]: item for item in generated}
    _require_equal(
        set(generated_by_feature),
        set(committed_by_feature),
        "SHAP feature identity parity failed",
    )

    max_delta = 0.0
    numeric_fields = ("contribution", "absolute_contribution")
    for feature, saved in committed_by_feature.items():
        current = generated_by_feature[feature]
        _require_equal(current["value"], saved["value"], f"Dataset value drift for {feature}")
        for field in numeric_fields:
            max_delta = max(
                max_delta,
                _require_close(current[field], saved[field], f"SHAP {field} drift for {feature}"),
            )
        if (
            abs(float(saved["contribution"])) > REPLAY_ATOL
            and abs(float(current["contribution"])) > REPLAY_ATOL
        ):
            _require_equal(
                current["direction"],
                saved["direction"],
                f"SHAP direction drift for {feature}",
            )

    saved_order = [item["feature"] for item in committed]
    current_positions = {item["feature"]: position for position, item in enumerate(generated)}
    saved_magnitudes = [float(item["absolute_contribution"]) for item in committed]
    for left, left_feature in enumerate(saved_order):
        for right in range(left + 1, len(saved_order)):
            right_feature = saved_order[right]
            if saved_magnitudes[left] - saved_magnitudes[right] > 2 * REPLAY_ATOL:
                if current_positions[left_feature] >= current_positions[right_feature]:
                    raise ValueError("SHAP rank order changed beyond replay tolerance.")
    return max_delta


def _read_locked_predictions(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        _require_equal(reader.fieldnames, list(LOCKED_TEST_COLUMNS), "Locked-test columns differ")
        rows = list(reader)
    if any(row is None for row in rows):
        raise ValueError("Locked-test CSV contains an incomplete row.")
    return [
        {
            "row_id": int(row["row_id"]),
            "actual_raw_target": int(row["actual_raw_target"]),
            "predicted_raw_target": int(row["predicted_raw_target"]),
            "malignant_class_score": float(row["malignant_class_score"]),
        }
        for row in rows
    ]


def _current_locked_predictions() -> list[dict[str, object]]:
    metadata = json.loads((MODELS_DIR / "model_metadata.json").read_text(encoding="utf-8"))
    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed=int(metadata["random_seed"]))
    model = joblib.load(MODELS_DIR / "best_model.joblib")
    scores = malignant_scores(model.classes_, model.predict_proba(splits.X_test))
    predictions = predictions_from_malignant_scores(scores, DECISION_THRESHOLD)
    order = np.argsort(splits.X_test.index.to_numpy())
    return [
        {
            "row_id": int(splits.X_test.index.to_numpy()[index]),
            "actual_raw_target": int(splits.y_test.to_numpy()[index]),
            "predicted_raw_target": int(predictions[index]),
            "malignant_class_score": float(scores[index]),
        }
        for index in order
    ]


def _compare_locked_predictions(
    expected: list[dict[str, object]],
    actual: list[dict[str, object]],
    label: str,
) -> float:
    _require_equal(len(expected), LOCKED_TEST_ROW_COUNT, f"{label} row count is invalid")
    _require_equal(len(actual), LOCKED_TEST_ROW_COUNT, f"{label} replay row count is invalid")
    _require_equal(
        [row["row_id"] for row in actual],
        [row["row_id"] for row in expected],
        f"{label} row IDs differ",
    )
    max_delta = 0.0
    for saved, current in zip(expected, actual, strict=True):
        _require_equal(
            current["actual_raw_target"],
            saved["actual_raw_target"],
            f"{label} target parity failed for row {saved['row_id']}",
        )
        _require_equal(
            current["predicted_raw_target"],
            saved["predicted_raw_target"],
            f"{label} classification parity failed for row {saved['row_id']}",
        )
        max_delta = max(
            max_delta,
            _require_close(
                current["malignant_class_score"],
                saved["malignant_class_score"],
                f"{label} score parity failed for row {saved['row_id']}",
            ),
        )
    return max_delta


def verify_locked_test_replay(
    canonical_path: Path,
    current_path: Path = DEFAULT_LOCKED_TEST_PATH,
) -> dict[str, object]:
    canonical = _read_locked_predictions(canonical_path)
    current_report = _read_locked_predictions(current_path)
    reproduced = _current_locked_predictions()
    report_delta = _compare_locked_predictions(canonical, current_report, "Locked-test report")
    model_delta = _compare_locked_predictions(canonical, reproduced, "Locked-test model")
    return {
        "rows": len(canonical),
        "target_parity": True,
        "classification_parity": True,
        "max_score_delta": max(report_delta, model_delta),
    }


def verify_case_study_artifact(
    committed_path: Path = DEFAULT_OUTPUT_PATH,
    showcase_path: Path = DEFAULT_SHOWCASE_PATH,
) -> dict[str, object]:
    committed = json.loads(committed_path.read_text(encoding="utf-8"))
    showcase = json.loads(showcase_path.read_text(encoding="utf-8"))
    verify_canonical_case_identity(committed, showcase)
    manifest = validate_artifact_manifest()
    verify_semantic_manifest_replay(manifest, showcase)
    generated = build_case_study_artifact()

    exact_fields = (
        "schema_version",
        "dataset_row_id",
        "raw_target",
        "known_label",
        "model_name",
        "positive_class",
        "output_space",
        "threshold",
        "calibration_status",
        "feature_order",
        "feature_count",
        "reconstruction_tolerance",
        "global_explanation",
        "local_explanation",
        "educational_limitation",
    )
    for field in exact_fields:
        _require_equal(committed[field], generated[field], f"Case {field} parity failed")

    numeric_fields = (
        "base_value",
        "contribution_sum",
        "reconstructed_log_odds",
        "model_score",
        "reconstruction_error",
    )
    deltas = [
        _require_close(generated[field], committed[field], f"Case {field} replay failed")
        for field in numeric_fields
    ]
    contribution_delta = _verify_contributions(
        committed["contributions"], generated["contributions"]
    )
    return {
        "canonical_model_version": committed["model_version"],
        "replay_model_version": manifest["model_version"],
        "binary_identity_match": committed["model_version"] == manifest["model_version"],
        "max_case_numeric_delta": max([*deltas, contribution_delta]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the static explainability case study.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the committed case artifact without writing to it.",
    )
    parser.add_argument(
        "--canonical-locked-test",
        type=Path,
        help="Compare generated locked-test predictions with a preserved canonical copy.",
    )
    args = parser.parse_args()
    if args.check:
        report = verify_case_study_artifact()
        print(f"CANONICAL_MODEL_VERSION={report['canonical_model_version']}")
        print(f"REPLAY_MODEL_VERSION={report['replay_model_version']}")
        print(f"BINARY_IDENTITY_MATCH={'YES' if report['binary_identity_match'] else 'NO'}")
        print("SEMANTIC_REPLAY_MATCH=YES")
        if args.canonical_locked_test is not None:
            locked_report = verify_locked_test_replay(args.canonical_locked_test)
            print(f"LOCKED_TEST_ROWS={locked_report['rows']}")
            print(f"LOCKED_TEST_TARGET_PARITY={'YES' if locked_report['target_parity'] else 'NO'}")
            print(
                "LOCKED_TEST_CLASSIFICATION_PARITY="
                f"{'YES' if locked_report['classification_parity'] else 'NO'}"
            )
            print(f"LOCKED_TEST_MAX_SCORE_DELTA={locked_report['max_score_delta']!r}")
            print(f"LOCKED_TEST_SCORE_TOLERANCE={REPLAY_ATOL!r}")
        print("Verified the committed explainability case artifact.")
        return
    artifact = generate_case_study_artifact()
    print(
        f"Generated row {artifact['dataset_row_id']} explainability case "
        f"for {artifact['model_name']} ({artifact['model_version']})."
    )


if __name__ == "__main__":
    main()
