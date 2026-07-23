from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def test_manifest_validates_and_rejects_checksum_drift(tmp_path: Path) -> None:
    from src.artifacts.manifest import (
        ArtifactValidationError,
        build_artifact_manifest,
        validate_artifact_manifest,
    )
    from src.evaluation.error_analysis import generate_error_analysis
    from src.evaluation.evaluate_models import evaluate_models
    from src.explainability.explain_model import explain_best_model
    from src.models.train_baseline import train_baseline_models
    from src.models.train_pytorch_mlp import train_pytorch_mlp

    models_dir = tmp_path / "models"
    reports_dir = tmp_path / "reports"
    train_baseline_models(models_dir=models_dir, reports_dir=reports_dir)
    train_pytorch_mlp(
        epochs=3,
        patience=2,
        models_dir=models_dir,
        reports_dir=reports_dir,
    )
    evaluate_models(models_dir=models_dir, reports_dir=reports_dir)
    generate_error_analysis(models_dir=models_dir, reports_dir=reports_dir)
    explain_best_model(
        models_dir=models_dir,
        reports_dir=reports_dir,
        max_shap_samples=20,
    )
    manifest = build_artifact_manifest(models_dir=models_dir, reports_dir=reports_dir)

    assert (
        validate_artifact_manifest(models_dir, reports_dir)["model_version"]
        == manifest["model_version"]
    )

    manifest_path = models_dir / "artifact_manifest.json"
    original_manifest = manifest_path.read_text(encoding="utf-8")

    tampered = json.loads(original_manifest)
    tampered["schema_version"] = 999
    manifest_path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(ArtifactValidationError, match="schema version"):
        validate_artifact_manifest(models_dir, reports_dir)

    tampered = json.loads(original_manifest)
    tampered["model_version"] = "0" * 20
    manifest_path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(ArtifactValidationError, match="model version"):
        validate_artifact_manifest(models_dir, reports_dir)

    tampered = json.loads(original_manifest)
    tampered["locked_test"]["metrics"]["sensitivity"] = 0.0
    manifest_path.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(ArtifactValidationError, match="Governed evaluation"):
        validate_artifact_manifest(models_dir, reports_dir)

    from src.api.main import create_app

    with pytest.raises(ArtifactValidationError):
        with TestClient(create_app(models_dir=models_dir, reports_dir=reports_dir)):
            pass

    manifest_path.write_text(original_manifest, encoding="utf-8")
    training_curve = reports_dir / "figures" / "training_curve.png"
    training_curve_bytes = training_curve.read_bytes()
    training_curve.unlink()
    with pytest.raises(ArtifactValidationError, match="checksum"):
        validate_artifact_manifest(models_dir, reports_dir)

    training_curve.write_bytes(training_curve_bytes)
    build_artifact_manifest(models_dir=models_dir, reports_dir=reports_dir)
    model_path = models_dir / "best_model.joblib"
    model_path.write_bytes(model_path.read_bytes() + b"checksum-drift")
    with pytest.raises(ArtifactValidationError, match="checksum"):
        validate_artifact_manifest(models_dir, reports_dir)
