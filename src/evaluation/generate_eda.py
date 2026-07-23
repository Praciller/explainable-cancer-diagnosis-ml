from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import REPORTS_DIR
from src.contracts import EDUCATIONAL_LIMITATION
from src.data.load_dataset import load_dataset_frame


def generate_eda(reports_dir: Path = REPORTS_DIR) -> None:
    bundle = load_dataset_frame()
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    palette = {"malignant": "#d36d5f", "benign": "#6c9b76"}

    figure, axis = plt.subplots(figsize=(6.5, 4.5))
    counts = bundle.frame["label"].value_counts().reindex(bundle.target_names)
    axis.bar(counts.index, counts.values, color=[palette[name] for name in counts.index])
    axis.set(title="Target distribution", ylabel="Samples")
    figure.tight_layout()
    figure.savefig(figures_dir / "target_distribution.png", dpi=160)
    plt.close(figure)

    correlations = bundle.frame[bundle.feature_names + ["target"]].corr()
    figure, axis = plt.subplots(figsize=(13, 11))
    sns.heatmap(correlations, cmap="vlag", center=0, ax=axis, xticklabels=True, yticklabels=True)
    axis.set_title("Feature correlation heatmap")
    figure.tight_layout()
    figure.savefig(figures_dir / "correlation_heatmap.png", dpi=150)
    plt.close(figure)

    top_features = (
        correlations["target"].drop("target").abs().sort_values(ascending=False).head(3).index
    )
    figure, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    for axis, feature in zip(axes, top_features, strict=True):
        for label in bundle.target_names:
            values = bundle.frame.loc[bundle.frame["label"] == label, feature]
            axis.hist(values, bins=20, alpha=0.55, label=label, color=palette[label])
        axis.set(title=feature, ylabel="Samples")
    axes[0].legend(frameon=False)
    figure.suptitle("Top target-correlated feature distributions")
    figure.tight_layout()
    figure.savefig(figures_dir / "top_feature_distributions.png", dpi=160)
    plt.close(figure)

    target_correlations = correlations["target"].drop("target").sort_values()
    summary = (
        "# EDA Summary\n\n"
        f"The dataset contains {len(bundle.frame)} samples and {len(bundle.feature_names)} "
        "numeric features. Benign samples are more common, but the class ratio is mild and "
        "stratified splitting preserves both classes.\n\n"
        "## Strongest Relationships\n\n"
        + "\n".join(
            f"- `{name}`: target correlation {value:.3f}"
            for name, value in target_correlations.abs()
            .sort_values(ascending=False)
            .head(8)
            .items()
        )
        + "\n\n## Leakage and Overfitting Risks\n\n"
        "Features are measurements from the same digitized image and several are strongly "
        "correlated. Splitting must happen by row before fitting scalers. The small, clean "
        "dataset can overstate real-world performance and does not provide external "
        "clinical validation.\n\n"
        f"{EDUCATIONAL_LIMITATION}\n"
    )
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "eda_summary.md").write_text(summary, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EDA reports.")
    parser.parse_args()
    generate_eda()
    print("Generated EDA report and figures.")


if __name__ == "__main__":
    main()
