from pathlib import Path


def test_analysis_commands_generate_required_reports(tmp_path: Path) -> None:
    from src.artifacts.manifest import build_artifact_manifest
    from src.evaluation.error_analysis import generate_error_analysis
    from src.evaluation.evaluate_models import evaluate_models
    from src.evaluation.generate_eda import generate_eda
    from src.explainability.explain_model import explain_best_model
    from src.models.train_baseline import train_baseline_models
    from src.models.train_pytorch_mlp import train_pytorch_mlp

    models_dir = tmp_path / "models"
    reports_dir = tmp_path / "reports"
    train_baseline_models(models_dir=models_dir, reports_dir=reports_dir)
    train_pytorch_mlp(
        epochs=3,
        patience=3,
        models_dir=models_dir,
        reports_dir=reports_dir,
    )

    evaluate_models(models_dir=models_dir, reports_dir=reports_dir)
    generate_eda(reports_dir=reports_dir)
    generate_error_analysis(models_dir=models_dir, reports_dir=reports_dir)
    explain_best_model(models_dir=models_dir, reports_dir=reports_dir, max_shap_samples=30)
    build_artifact_manifest(models_dir=models_dir, reports_dir=reports_dir)

    required = [
        "evaluation_metrics.json",
        "locked_test_predictions.csv",
        "eda_summary.md",
        "error_analysis.md",
        "error_analysis.csv",
        "explainability_summary.md",
        "figures/confusion_matrix.png",
        "figures/roc_curve.png",
        "figures/precision_recall_curve.png",
        "figures/target_distribution.png",
        "figures/correlation_heatmap.png",
        "figures/top_feature_distributions.png",
        "figures/threshold_analysis.png",
        "figures/feature_importance.png",
        "figures/shap_summary.png",
        "figures/shap_example_prediction.png",
    ]
    for relative_path in required:
        assert (reports_dir / relative_path).exists(), relative_path
    assert (models_dir / "artifact_manifest.json").exists()
