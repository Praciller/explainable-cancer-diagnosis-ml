from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.data.load_dataset import load_dataset_frame
from src.models.train_baseline import train_baseline_models


@pytest.fixture(scope="module")
def client(tmp_path_factory: pytest.TempPathFactory) -> TestClient:
    from src.api.main import create_app

    root = tmp_path_factory.mktemp("api-artifacts")
    models_dir = root / "models"
    reports_dir = root / "reports"
    train_baseline_models(models_dir=models_dir, reports_dir=reports_dir)
    with TestClient(create_app(models_dir=models_dir, reports_dir=reports_dir)) as test_client:
        yield test_client


def test_health_model_info_features_and_samples(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}

    model_info = client.get("/model-info").json()
    assert model_info["features"] == 30
    assert model_info["classes"] == ["malignant", "benign"]

    features = client.get("/features").json()
    assert len(features["features"]) == 30
    assert features["features"][0]["name"]

    samples = client.get("/samples?limit=3").json()
    assert len(samples["samples"]) == 3
    assert len(samples["samples"][0]["features"]) == 30
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

    assert (
        "FRONTEND_ORIGINS: "
        "http://localhost:5173,http://127.0.0.1:5173"
    ) in compose


def test_predict_returns_probabilities_explanation_and_disclaimer(client: TestClient) -> None:
    features = load_dataset_frame().features.iloc[0].to_dict()

    response = client.post("/predict", json={"features": features})

    assert response.status_code == 200
    body = response.json()
    assert body["predicted_class"] in {"malignant", "benign"}
    assert set(body["probabilities"]) == {"malignant", "benign"}
    assert body["top_features"]
    assert "not medical advice" in body["disclaimer"]


def test_predict_rejects_missing_features_and_batch_over_100(client: TestClient) -> None:
    features = load_dataset_frame().features.iloc[0].to_dict()
    features.pop(next(iter(features)))

    assert client.post("/predict", json={"features": features}).status_code == 422
    valid = load_dataset_frame().features.iloc[0].to_dict()
    response = client.post("/predict-batch", json={"items": [{"features": valid}] * 101})
    assert response.status_code == 422
