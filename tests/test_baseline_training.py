import json
from pathlib import Path


def test_train_baselines_persists_models_metrics_and_best_alias(tmp_path: Path) -> None:
    from src.models.train_baseline import train_baseline_models

    result = train_baseline_models(
        seed=9,
        models_dir=tmp_path / "models",
        reports_dir=tmp_path / "reports",
        mlflow_enabled=False,
    )

    assert set(result.metrics) == {
        "dummy_majority",
        "logistic_regression",
        "random_forest",
        "gradient_boosting",
    }
    assert result.best_model_name in result.metrics
    assert (tmp_path / "models" / "best_model.joblib").exists()
    for model_name in result.metrics:
        assert (tmp_path / "models" / f"{model_name}.joblib").exists()
        assert 0 <= result.metrics[model_name]["roc_auc"] <= 1

    saved = json.loads((tmp_path / "reports" / "baseline_metrics.json").read_text())
    assert saved["selected_model"] == result.best_model_name
    assert saved["selection_metric"] == "validation_roc_auc"
    assert saved["decision_threshold"] == 0.5
    assert saved["calibration_status"] == "uncalibrated"
    assert set(saved["validation_models"]) == set(result.metrics)
    assert "locked_test" not in saved
    assert len(saved["feature_names"]) == 30
