import json
from pathlib import Path


def test_train_pytorch_mlp_saves_reloadable_cpu_checkpoint(tmp_path: Path) -> None:
    from src.models.train_pytorch_mlp import load_mlp_checkpoint, train_pytorch_mlp

    result = train_pytorch_mlp(
        seed=3,
        epochs=3,
        batch_size=64,
        patience=2,
        models_dir=tmp_path / "models",
        reports_dir=tmp_path / "reports",
        mlflow_enabled=False,
    )

    checkpoint_path = tmp_path / "models" / "pytorch_mlp.pt"
    assert checkpoint_path.exists()
    model, checkpoint = load_mlp_checkpoint(checkpoint_path)
    assert model.training is False
    assert checkpoint["feature_names"]
    assert len(result.history["train_loss"]) >= 1
    metrics = json.loads(
        (tmp_path / "reports" / "pytorch_mlp_metrics.json").read_text(encoding="utf-8")
    )
    assert 0 <= metrics["test"]["roc_auc"] <= 1
    assert (tmp_path / "reports" / "figures" / "training_curve.png").exists()
