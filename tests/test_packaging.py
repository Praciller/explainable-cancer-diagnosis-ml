from pathlib import Path


def test_docker_context_excludes_generated_artifacts() -> None:
    patterns = set(Path(".dockerignore").read_text(encoding="utf-8").splitlines())

    assert {
        "data/raw/*.csv",
        "data/processed/*.csv",
        "models/*.joblib",
        "models/*.pt",
        "models/*.json",
        "reports/*.json",
        "reports/*.csv",
        "reports/figures/*.png",
    } <= patterns


def test_vercel_ignore_does_not_exclude_frontend_source_or_assets() -> None:
    patterns = set(Path(".vercelignore").read_text(encoding="utf-8").splitlines())

    assert "src" not in patterns
    assert "reports" not in patterns
    assert {"/src", "/reports"} <= patterns


def test_api_image_builds_governed_artifacts_and_never_trains_at_startup() -> None:
    dockerfile = Path("Dockerfile.api").read_text(encoding="utf-8")

    assert "RUN python -m src.pipeline --seed 42 --mlp-epochs 100" in dockerfile
    assert "USER appuser" in dockerfile
    assert 'CMD ["uvicorn"' in dockerfile
    assert "if [ ! -f models/best_model.joblib ]" not in dockerfile


def test_compose_readiness_uses_validated_manifest_endpoint() -> None:
    compose = Path("docker-compose.yml").read_text(encoding="utf-8")

    assert "http://localhost:8000/ready" in compose
    assert '"5173:8080"' in compose
