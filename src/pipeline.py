from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from src.artifacts.manifest import build_artifact_manifest
from src.config import PROJECT_ROOT, RANDOM_SEED, REPORTS_DIR
from src.data.load_dataset import save_dataset_assets, save_portfolio_data
from src.data.validate_dataset import save_validation_report
from src.evaluation.error_analysis import generate_error_analysis
from src.evaluation.evaluate_models import evaluate_models
from src.evaluation.generate_eda import generate_eda
from src.explainability.explain_model import explain_best_model
from src.models.train_baseline import train_baseline_models
from src.models.train_pytorch_mlp import train_pytorch_mlp


def publish_showcase_snapshot(
    manifest: dict[str, Any],
    reports_dir: Path = REPORTS_DIR,
    project_root: Path = PROJECT_ROOT,
) -> None:
    contract = {
        "schema_version": 1,
        "model_info": {
            "model_name": manifest["selected_model"]["name"],
            "problem_type": "binary_classification",
            "features": manifest["dataset"]["features"],
            "classes": ["malignant", "benign"],
            "dataset_fingerprint": manifest["dataset"]["fingerprint_sha256"],
            "model_version": manifest["model_version"],
            "positive_class": "malignant",
            "decision_threshold": manifest["threshold"]["value"],
            "calibration_status": manifest["calibration_status"],
            "educational_limitation": manifest["educational_limitation"],
        },
        "dataset": manifest["dataset"],
        "evaluation": {
            "selected_model": manifest["selected_model"]["name"],
            "selection": {
                "metric": manifest["selected_model"]["selection_metric"],
                "value": manifest["selected_model"]["validation_value"],
            },
            "split": {
                "seed": manifest["split"]["seed"],
                "row_counts": manifest["split"]["row_counts"],
                "assignment_sha256": manifest["split"]["assignment_sha256"],
            },
            "threshold": manifest["threshold"],
            "calibration_status": manifest["calibration_status"],
            "validation_models": json.loads(
                (reports_dir / "evaluation_metrics.json").read_text(encoding="utf-8")
            )["validation_models"],
            "locked_test": manifest["locked_test"],
        },
    }
    contract_path = project_root / "frontend" / "src" / "data" / "showcase_contract.json"
    contract_path.parent.mkdir(parents=True, exist_ok=True)
    contract_path.write_text(json.dumps(contract, indent=2), encoding="utf-8")

    destination = project_root / "frontend" / "public" / "reports" / "figures"
    destination.mkdir(parents=True, exist_ok=True)
    for artifact in manifest["artifacts"].values():
        logical_path = Path(artifact["path"])
        if logical_path.parts[:2] == ("reports", "figures"):
            shutil.copy2(
                reports_dir / Path(*logical_path.parts[1:]), destination / logical_path.name
            )


def run_pipeline(
    seed: int = RANDOM_SEED,
    mlp_epochs: int = 100,
    publish_showcase: bool = False,
) -> dict[str, Any]:
    save_dataset_assets()
    save_portfolio_data()
    save_validation_report()
    generate_eda()
    train_baseline_models(seed=seed)
    train_pytorch_mlp(seed=seed, epochs=mlp_epochs)
    evaluate_models()
    generate_error_analysis()
    explain_best_model()
    manifest = build_artifact_manifest()
    if publish_showcase:
        publish_showcase_snapshot(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the governed local portfolio pipeline.")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--mlp-epochs", type=int, default=100)
    parser.add_argument("--publish-showcase", action="store_true")
    args = parser.parse_args()
    manifest = run_pipeline(
        seed=args.seed,
        mlp_epochs=args.mlp_epochs,
        publish_showcase=args.publish_showcase,
    )
    print(f"Generated governed artifact manifest {manifest['model_version']}.")


if __name__ == "__main__":
    main()
