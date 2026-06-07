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
