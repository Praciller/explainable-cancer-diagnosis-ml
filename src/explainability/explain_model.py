from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.pipeline import Pipeline

from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import EDUCATIONAL_LIMITATION, SAFETY_POSITIVE_RAW_TARGET
from src.data.load_dataset import load_dataset_frame
from src.features.preprocess import split_dataset
from src.utils.importance import model_feature_importance


def _shap_values(
    model: Any,
    background: pd.DataFrame,
    samples: pd.DataFrame,
    explained_raw_target: int = SAFETY_POSITIVE_RAW_TARGET,
) -> tuple[np.ndarray, np.ndarray, float]:
    if isinstance(model, Pipeline):
        scaler = model.named_steps["scaler"]
        classifier = model.named_steps["classifier"]
        background_values = scaler.transform(background)
        sample_values = scaler.transform(samples)
        explainer = shap.LinearExplainer(classifier, background_values)
        values = np.asarray(explainer.shap_values(sample_values))
        expected = float(np.asarray(explainer.expected_value).reshape(-1)[0])
        classes = np.asarray(classifier.classes_)
        target_index = int(np.flatnonzero(classes == explained_raw_target)[0])
        if len(classes) == 2 and target_index == 0:
            values = -values
            expected = -expected
        elif len(classes) != 2 or target_index != 1:
            raise ValueError("Unsupported linear SHAP class orientation.")
        return values, sample_values, expected

    explainer = shap.TreeExplainer(model)
    values = np.asarray(explainer.shap_values(samples))
    expected_values = np.asarray(explainer.expected_value).reshape(-1)
    if values.ndim == 3:
        target_index = int(np.flatnonzero(np.asarray(model.classes_) == explained_raw_target)[0])
        values = values[:, :, target_index]
        expected = float(expected_values[target_index])
    else:
        classes = np.asarray(model.classes_)
        target_index = int(np.flatnonzero(classes == explained_raw_target)[0])
        expected = float(expected_values[0])
        if len(classes) == 2 and target_index == 0:
            values = -values
            expected = -expected
    return values, samples.to_numpy(), expected


def explain_best_model(
    models_dir: Path = MODELS_DIR,
    reports_dir: Path = REPORTS_DIR,
    max_shap_samples: int = 100,
) -> None:
    metadata = json.loads((models_dir / "model_metadata.json").read_text(encoding="utf-8"))
    model = joblib.load(models_dir / "best_model.joblib")
    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, int(metadata["random_seed"]))
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    importance = model_feature_importance(model, bundle.feature_names)
    top = importance.head(12).sort_values()
    figure, axis = plt.subplots(figsize=(8, 6))
    axis.barh(top.index, top.values, color="#713c78")
    axis.set(title="Global feature importance", xlabel="Absolute model importance")
    figure.tight_layout()
    figure.savefig(figures_dir / "feature_importance.png", dpi=160)
    plt.close(figure)

    samples = splits.X_test.iloc[:max_shap_samples]
    background = splits.X_train.sample(min(100, len(splits.X_train)), random_state=42)
    shap_values, display_values, expected = _shap_values(model, background, samples)
    shap.summary_plot(
        shap_values,
        display_values,
        feature_names=bundle.feature_names,
        show=False,
        max_display=12,
        rng=np.random.default_rng(42),
    )
    plt.gcf().tight_layout()
    plt.gca().set_xlabel("SHAP value for malignant-class log-odds")
    plt.gcf().savefig(figures_dir / "shap_summary.png", dpi=160, bbox_inches="tight")
    plt.close(plt.gcf())

    explanation = shap.Explanation(
        values=shap_values[0],
        base_values=expected,
        data=display_values[0],
        feature_names=bundle.feature_names,
    )
    shap.plots.waterfall(explanation, max_display=12, show=False)
    plt.gcf().suptitle(
        f"Malignant-class explanation for dataset row {int(samples.index[0])}",
        y=1.01,
    )
    plt.gcf().tight_layout()
    plt.gcf().savefig(
        figures_dir / "shap_example_prediction.png",
        dpi=160,
        bbox_inches="tight",
    )
    plt.close(plt.gcf())

    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "explainability_summary.md").write_text(
        "# Explainability Summary\n\n"
        f"The selected baseline model is `{metadata['model_name']}`. Its strongest global "
        "importance signals are:\n\n"
        + "\n".join(f"- `{name}`: {value:.4f}" for name, value in importance.head(10).items())
        + "\n\nThe SHAP output class is explicitly `malignant` (`raw target 0`). "
        f"The local waterfall uses dataset row `{int(samples.index[0])}` and reconstructs "
        "the malignant-class log-odds relative to the training-background expectation.\n\n"
        "These explanations describe how the model used the supplied measurements. "
        "They do not prove biological causality, medical importance, or why cancer develops. "
        "Correlated measurements can divide or redistribute importance.\n\n"
        f"{EDUCATIONAL_LIMITATION}\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Explain the selected baseline model.")
    parser.add_argument("--max-shap-samples", type=int, default=100)
    args = parser.parse_args()
    explain_best_model(max_shap_samples=args.max_shap_samples)
    print("Generated feature importance and SHAP reports.")


if __name__ == "__main__":
    main()
