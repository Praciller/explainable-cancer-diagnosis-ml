from __future__ import annotations

import hashlib
import json
import platform
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

import joblib

from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import EDUCATIONAL_LIMITATION, label_contract
from src.data.load_dataset import dataset_fingerprint, load_dataset_frame

MANIFEST_FILENAME = "artifact_manifest.json"
MANIFEST_SCHEMA_VERSION = 1
ARTIFACT_PATHS = {
    "model": "models/best_model.joblib",
    "model_metadata": "models/model_metadata.json",
    "pytorch_checkpoint": "models/pytorch_mlp.pt",
    "validation_metrics": "reports/baseline_metrics.json",
    "pytorch_validation_metrics": "reports/pytorch_mlp_metrics.json",
    "evaluation": "reports/evaluation_metrics.json",
    "locked_test_predictions": "reports/locked_test_predictions.csv",
    "error_analysis": "reports/error_analysis.csv",
    "confusion_matrix": "reports/figures/confusion_matrix.png",
    "roc_curve": "reports/figures/roc_curve.png",
    "precision_recall_curve": "reports/figures/precision_recall_curve.png",
    "feature_importance": "reports/figures/feature_importance.png",
    "shap_summary": "reports/figures/shap_summary.png",
    "shap_example": "reports/figures/shap_example_prediction.png",
    "threshold_analysis": "reports/figures/threshold_analysis.png",
    "training_curve": "reports/figures/training_curve.png",
}


class ArtifactValidationError(RuntimeError):
    """Raised when generated artifact provenance is incomplete or inconsistent."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as artifact:
        for chunk in iter(lambda: artifact.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


def _artifact_file(
    logical_path: str,
    models_dir: Path,
    reports_dir: Path,
) -> Path:
    normalized = Path(logical_path)
    if normalized.is_absolute() or ".." in normalized.parts:
        raise ArtifactValidationError("Artifact paths must be repository-relative.")
    if normalized.parts[:1] == ("models",):
        return models_dir / Path(*normalized.parts[1:])
    if normalized.parts[:1] == ("reports",):
        return reports_dir / Path(*normalized.parts[1:])
    raise ArtifactValidationError("Artifact path must be rooted at models/ or reports/.")


def _model_version(
    *,
    dataset_fingerprint_value: str,
    model_sha256: str,
    selected_model: str,
    feature_names: list[str],
    split_assignment_sha256: str,
    threshold: float,
    calibration_status: str,
) -> str:
    identity_payload = {
        "dataset_fingerprint": dataset_fingerprint_value,
        "model_sha256": model_sha256,
        "selected_model": selected_model,
        "feature_names": feature_names,
        "label_contract": label_contract(),
        "split_assignment_sha256": split_assignment_sha256,
        "threshold": threshold,
        "calibration_status": calibration_status,
    }
    return hashlib.sha256(
        json.dumps(identity_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:20]


def build_artifact_manifest(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, Any]:
    metadata_path = models_dir / "model_metadata.json"
    evaluation_path = reports_dir / "evaluation_metrics.json"
    if not metadata_path.exists() or not evaluation_path.exists():
        raise ArtifactValidationError(
            "Model metadata and governed evaluation must exist before manifest generation."
        )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    evaluation = json.loads(evaluation_path.read_text(encoding="utf-8"))
    bundle = load_dataset_frame()
    fingerprint = dataset_fingerprint(bundle)
    if metadata.get("dataset_fingerprint") != fingerprint:
        raise ArtifactValidationError("Model metadata dataset fingerprint is stale.")
    if evaluation.get("dataset_fingerprint") != fingerprint:
        raise ArtifactValidationError("Evaluation dataset fingerprint is stale.")
    if metadata.get("model_name") != evaluation.get("selected_model"):
        raise ArtifactValidationError("Model metadata and evaluation selection disagree.")

    artifacts: dict[str, dict[str, str]] = {}
    for name, logical_path in ARTIFACT_PATHS.items():
        path = _artifact_file(logical_path, models_dir, reports_dir)
        if not path.is_file():
            raise ArtifactValidationError(f"Required artifact is missing: {logical_path}")
        artifacts[name] = {"path": logical_path, "sha256": sha256_file(path)}

    model_version = _model_version(
        dataset_fingerprint_value=fingerprint,
        model_sha256=artifacts["model"]["sha256"],
        selected_model=metadata["model_name"],
        feature_names=bundle.feature_names,
        split_assignment_sha256=metadata["split_assignment_sha256"],
        threshold=metadata["decision_threshold"],
        calibration_status=metadata["calibration_status"],
    )
    model = joblib.load(models_dir / "best_model.joblib")
    manifest: dict[str, Any] = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "model_version": model_version,
        "generated_at": datetime.now(UTC).isoformat(),
        "dataset": {
            "loader": "sklearn.datasets.load_breast_cancer(as_frame=True)",
            "fingerprint_sha256": fingerprint,
            "rows": len(bundle.frame),
            "features": len(bundle.feature_names),
            "class_counts": {
                str(key): int(value)
                for key, value in bundle.target.value_counts().sort_index().items()
            },
            "scikit_learn_version": _package_version("scikit-learn"),
        },
        "feature_names": bundle.feature_names,
        "label_contract": label_contract(),
        "split": evaluation["split"],
        "preprocessing": {
            "logistic_regression": "StandardScaler fitted inside the training-only pipeline",
            "tree_models": "No scaling",
            "pytorch_mlp": "StandardScaler fitted on training rows only",
        },
        "selected_model": {
            "name": metadata["model_name"],
            "parameters": {
                key: value
                for key, value in model.get_params(deep=True).items()
                if isinstance(value, (str, int, float, bool, type(None)))
            },
            "selection_metric": metadata["selection_metric"],
            "validation_value": metadata["selection_value"],
        },
        "threshold": evaluation["threshold"],
        "calibration_status": metadata["calibration_status"],
        "locked_test": evaluation["locked_test"],
        "artifacts": artifacts,
        "runtime": {
            "python": platform.python_version(),
            "numpy": _package_version("numpy"),
            "pandas": _package_version("pandas"),
            "scikit_learn": _package_version("scikit-learn"),
            "shap": _package_version("shap"),
            "torch": _package_version("torch"),
            "fastapi": _package_version("fastapi"),
            "joblib": _package_version("joblib"),
        },
        "trust_boundary": (
            "Load only artifacts produced by this repository. joblib and PyTorch "
            "artifacts are code-bearing formats and must not come from users."
        ),
        "educational_limitation": EDUCATIONAL_LIMITATION,
    }
    models_dir.mkdir(parents=True, exist_ok=True)
    (models_dir / MANIFEST_FILENAME).write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    return manifest


def validate_artifact_manifest(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
) -> dict[str, Any]:
    manifest_path = models_dir / MANIFEST_FILENAME
    if not manifest_path.is_file():
        raise ArtifactValidationError("Artifact manifest is missing.")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactValidationError("Artifact manifest is unreadable.") from exc

    required = {
        "schema_version",
        "model_version",
        "dataset",
        "feature_names",
        "label_contract",
        "split",
        "selected_model",
        "threshold",
        "calibration_status",
        "locked_test",
        "artifacts",
        "educational_limitation",
    }
    if not required <= set(manifest):
        raise ArtifactValidationError("Artifact manifest schema is incomplete.")
    if manifest["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise ArtifactValidationError("Artifact manifest schema version is unsupported.")
    bundle = load_dataset_frame()
    if manifest["feature_names"] != bundle.feature_names:
        raise ArtifactValidationError("Artifact feature order does not match the dataset.")
    if manifest["label_contract"] != label_contract():
        raise ArtifactValidationError("Artifact label contract does not match the application.")
    if manifest["dataset"]["fingerprint_sha256"] != dataset_fingerprint(bundle):
        raise ArtifactValidationError("Artifact dataset fingerprint does not match.")
    if set(manifest["artifacts"]) != set(ARTIFACT_PATHS):
        raise ArtifactValidationError("Artifact inventory is incomplete.")

    for name, expected_path in ARTIFACT_PATHS.items():
        artifact = manifest["artifacts"][name]
        if artifact.get("path") != expected_path:
            raise ArtifactValidationError("Artifact path does not match the governed inventory.")
        path = _artifact_file(expected_path, models_dir, reports_dir)
        if not path.is_file() or sha256_file(path) != artifact.get("sha256"):
            raise ArtifactValidationError(f"Artifact checksum validation failed: {name}")

    metadata = json.loads((models_dir / "model_metadata.json").read_text(encoding="utf-8"))
    evaluation = json.loads((reports_dir / "evaluation_metrics.json").read_text(encoding="utf-8"))
    if metadata.get("model_name") != manifest["selected_model"]["name"]:
        raise ArtifactValidationError("Selected-model provenance disagrees.")
    if metadata.get("split_assignment_sha256") != manifest["split"]["assignment_sha256"]:
        raise ArtifactValidationError("Split provenance disagrees.")
    if manifest["selected_model"].get("selection_metric") != metadata.get("selection_metric"):
        raise ArtifactValidationError("Selection-metric provenance disagrees.")
    if manifest["selected_model"].get("validation_value") != metadata.get("selection_value"):
        raise ArtifactValidationError("Selection-value provenance disagrees.")
    if manifest["threshold"] != evaluation.get("threshold"):
        raise ArtifactValidationError("Decision-threshold provenance disagrees.")
    if manifest["calibration_status"] != metadata.get("calibration_status"):
        raise ArtifactValidationError("Calibration provenance disagrees.")
    if manifest["locked_test"] != evaluation.get("locked_test"):
        raise ArtifactValidationError("Governed evaluation provenance disagrees.")

    expected_version = _model_version(
        dataset_fingerprint_value=dataset_fingerprint(bundle),
        model_sha256=manifest["artifacts"]["model"]["sha256"],
        selected_model=metadata["model_name"],
        feature_names=bundle.feature_names,
        split_assignment_sha256=metadata["split_assignment_sha256"],
        threshold=metadata["decision_threshold"],
        calibration_status=metadata["calibration_status"],
    )
    if manifest["model_version"] != expected_version:
        raise ArtifactValidationError("Artifact model version does not match its identity.")
    return manifest
