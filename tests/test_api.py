import asyncio
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.artifacts.manifest import build_artifact_manifest
from src.data.load_dataset import load_dataset_frame
from src.evaluation.error_analysis import generate_error_analysis
from src.evaluation.evaluate_models import evaluate_models
from src.explainability.explain_model import explain_best_model
from src.models.train_baseline import train_baseline_models
from src.models.train_pytorch_mlp import train_pytorch_mlp


@pytest.fixture(scope="module")
def client(tmp_path_factory: pytest.TempPathFactory) -> TestClient:
    from src.api.main import create_app

    root = tmp_path_factory.mktemp("api-artifacts")
    models_dir = root / "models"
    reports_dir = root / "reports"
    train_baseline_models(models_dir=models_dir, reports_dir=reports_dir)
    train_pytorch_mlp(
        epochs=3,
        patience=2,
        models_dir=models_dir,
        reports_dir=reports_dir,
    )
    evaluate_models(models_dir=models_dir, reports_dir=reports_dir)
    generate_error_analysis(models_dir=models_dir, reports_dir=reports_dir)
    explain_best_model(models_dir=models_dir, reports_dir=reports_dir, max_shap_samples=20)
    build_artifact_manifest(models_dir=models_dir, reports_dir=reports_dir)
    with TestClient(create_app(models_dir=models_dir, reports_dir=reports_dir)) as test_client:
        yield test_client


def test_health_model_info_features_and_samples(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}

    model_info = client.get("/model-info").json()
    assert model_info["features"] == 30
    assert model_info["classes"] == ["malignant", "benign"]
    assert model_info["positive_class"] == "malignant"
    assert model_info["decision_threshold"] == 0.5
    assert model_info["calibration_status"] == "uncalibrated"
    assert len(model_info["model_version"]) == 20

    readiness = client.get("/ready").json()
    assert readiness["status"] == "ready"
    assert readiness["manifest_validated"] is True

    features = client.get("/features").json()
    assert len(features["features"]) == 30
    assert features["features"][0]["name"]
    assert "digitized" in features["features"][0]["measurement_context"]

    samples = client.get("/samples?limit=3").json()
    assert len(samples["samples"]) == 3
    assert len(samples["samples"][0]["features"]) == 30
    assert isinstance(samples["samples"][0]["dataset_row_id"], int)
    assert {sample["known_label"] for sample in samples["samples"]} == {
        "malignant",
        "benign",
    }


def test_default_cors_allows_localhost_and_loopback_frontends(client: TestClient) -> None:
    for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
        response = client.get("/health", headers={"Origin": origin})
        assert response.headers["access-control-allow-origin"] == origin


def test_compose_cors_allows_localhost_and_loopback_frontends() -> None:
    compose = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert ("FRONTEND_ORIGINS: http://localhost:5173,http://127.0.0.1:5173") in compose


def test_predict_returns_bounded_score_contract_and_disclaimer(client: TestClient) -> None:
    features = load_dataset_frame().features.iloc[0].to_dict()

    response = client.post("/predict", json={"features": features})

    assert response.status_code == 200
    body = response.json()
    assert body["model_classification"] in {"malignant", "benign"}
    assert 0 <= body["malignant_class_score"] <= 1
    assert body["decision_threshold"] == 0.5
    assert body["calibration_status"] == "uncalibrated"
    assert "not an individual clinical probability" in body["score_interpretation"]
    assert body["top_feature_contributions"]
    assert {item["direction"] for item in body["top_feature_contributions"]} <= {
        "toward_malignant",
        "toward_benign",
        "magnitude_only",
    }
    assert "not intended for diagnosis" in body["educational_limitation"]


def test_predict_rejects_missing_features_and_batch_over_100(client: TestClient) -> None:
    features = load_dataset_frame().features.iloc[0].to_dict()
    features.pop(next(iter(features)))

    assert client.post("/predict", json={"features": features}).status_code == 422
    valid = load_dataset_frame().features.iloc[0].to_dict()
    response = client.post("/predict-batch", json={"items": [{"features": valid}] * 101})
    assert response.status_code == 422


def test_predict_flags_outside_observed_range_without_hard_rejection(
    client: TestClient,
) -> None:
    bundle = load_dataset_frame()
    features = bundle.features.iloc[0].to_dict()
    features["mean radius"] = float(bundle.features["mean radius"].max() + 1)

    response = client.post("/predict", json={"features": features})

    assert response.status_code == 200
    assert "outside_observed_training_range:mean radius" in response.json()["warning_flags"]


def test_predict_rejects_oversized_request_body(client: TestClient) -> None:
    response = client.post(
        "/predict",
        content=b"{}",
        headers={"Content-Type": "application/json", "Content-Length": str(300_000)},
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "Request body exceeds the configured size limit."}


def test_predict_rejects_oversized_chunked_request_body() -> None:
    from src.api.main import MAX_REQUEST_BODY_BYTES, RequestBodyLimitMiddleware

    messages = iter(
        [
            {"type": "http.request", "body": b"x" * 200_000, "more_body": True},
            {"type": "http.request", "body": b"x" * 100_000, "more_body": False},
        ]
    )
    sent: list[dict] = []

    async def downstream(scope: dict, receive, send) -> None:
        while (await receive()).get("more_body", False):
            pass
        await send({"type": "http.response.start", "status": 204, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    async def receive() -> dict:
        return next(messages)

    async def send(message: dict) -> None:
        sent.append(message)

    middleware = RequestBodyLimitMiddleware(downstream, MAX_REQUEST_BODY_BYTES)
    asyncio.run(middleware({"type": "http", "headers": []}, receive, send))

    assert sent[0]["status"] == 413
    assert json.loads(sent[1]["body"]) == {
        "detail": "Request body exceeds the configured size limit."
    }
