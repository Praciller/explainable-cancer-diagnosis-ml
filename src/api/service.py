from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.pipeline import Pipeline

from src.api.schemas import (
    FeatureContribution,
    FeatureDefinition,
    ModelInfoResponse,
    PredictionResponse,
    SampleRecord,
)
from src.artifacts.manifest import validate_artifact_manifest
from src.config import MODELS_DIR, REPORTS_DIR
from src.contracts import (
    EDUCATIONAL_LIMITATION,
    RAW_TARGET_TO_LABEL,
    malignant_scores,
    predictions_from_malignant_scores,
)
from src.data.load_dataset import DatasetBundle, load_dataset_frame
from src.utils.importance import model_feature_importance


class PredictionService:
    def __init__(
        self,
        model: Any,
        metadata: dict[str, Any],
        manifest: dict[str, Any],
        dataset: DatasetBundle,
    ) -> None:
        self.model = model
        self.metadata = metadata
        self.manifest = manifest
        self.dataset = dataset
        self.threshold = float(manifest["threshold"]["value"])
        self._global_importance = model_feature_importance(model, dataset.feature_names)

    @classmethod
    def from_artifacts(
        cls,
        models_dir: Path = MODELS_DIR,
        reports_dir: Path = REPORTS_DIR,
    ) -> PredictionService:
        manifest = validate_artifact_manifest(models_dir, reports_dir)
        metadata = json.loads((models_dir / "model_metadata.json").read_text(encoding="utf-8"))
        model = joblib.load(models_dir / "best_model.joblib")
        if list(model.classes_) != metadata["raw_classes"]:
            raise ValueError("Loaded model classes disagree with the governed label contract.")
        dataset = load_dataset_frame()
        if metadata["feature_names"] != dataset.feature_names:
            raise ValueError("Loaded model feature order disagrees with the dataset contract.")
        return cls(
            model=model,
            metadata=metadata,
            manifest=manifest,
            dataset=dataset,
        )

    def model_info(self) -> ModelInfoResponse:
        return ModelInfoResponse(
            model_name=self.metadata["model_name"],
            problem_type="binary_classification",
            features=len(self.dataset.feature_names),
            classes=self.dataset.target_names,
            positive_class="malignant",
            dataset_fingerprint=self.metadata["dataset_fingerprint"],
            model_version=self.manifest["model_version"],
            decision_threshold=self.threshold,
            calibration_status=self.metadata["calibration_status"],
            educational_limitation=EDUCATIONAL_LIMITATION,
        )

    def feature_definitions(self) -> list[FeatureDefinition]:
        context = (
            "Observed educational dataset measurement from a digitized fine-needle "
            "aspirate image; the range is a warning reference, not a clinical validity bound."
        )
        return [
            FeatureDefinition(
                name=name,
                minimum=float(self.dataset.features[name].min()),
                maximum=float(self.dataset.features[name].max()),
                mean=float(self.dataset.features[name].mean()),
                measurement_context=context,
            )
            for name in self.dataset.feature_names
        ]

    def samples(self, limit: int) -> list[SampleRecord]:
        indices_by_label = {
            label: self.dataset.frame.index[self.dataset.frame["label"] == label].tolist()
            for label in self.dataset.target_names
        }
        records: list[SampleRecord] = []
        for position in range(min(limit, len(self.dataset.frame))):
            label = self.dataset.target_names[position % len(self.dataset.target_names)]
            index = indices_by_label[label][position // len(self.dataset.target_names)]
            row = self.dataset.frame.loc[index]
            records.append(
                SampleRecord(
                    dataset_row_id=int(index),
                    known_label=str(row["label"]),
                    features={name: float(row[name]) for name in self.dataset.feature_names},
                )
            )
        return records

    def _local_contributions(self, frame: pd.DataFrame) -> list[FeatureContribution]:
        if isinstance(self.model, Pipeline) and "scaler" in self.model.named_steps:
            scaled = self.model.named_steps["scaler"].transform(frame)[0]
            classifier = self.model.named_steps["classifier"]
            if hasattr(classifier, "coef_"):
                benign_contributions = classifier.coef_[0] * scaled
                malignant_contributions = -benign_contributions
                values = pd.Series(
                    malignant_contributions,
                    index=self.dataset.feature_names,
                )
                ordered = values.reindex(values.abs().sort_values(ascending=False).index).head(8)
                return [
                    FeatureContribution(
                        feature=name,
                        contribution=float(value),
                        direction=("toward_malignant" if value >= 0 else "toward_benign"),
                    )
                    for name, value in ordered.items()
                ]
        return [
            FeatureContribution(
                feature=name,
                contribution=float(value),
                direction="magnitude_only",
            )
            for name, value in self._global_importance.head(8).items()
        ]

    def _warning_flags(self, features: dict[str, float]) -> list[str]:
        flags: list[str] = []
        for name in self.dataset.feature_names:
            value = features[name]
            minimum = float(self.dataset.features[name].min())
            maximum = float(self.dataset.features[name].max())
            if value < minimum or value > maximum:
                flags.append(f"outside_observed_training_range:{name}")
        return flags

    def predict(self, features: dict[str, float]) -> PredictionResponse:
        frame = pd.DataFrame(
            [[features[name] for name in self.dataset.feature_names]],
            columns=self.dataset.feature_names,
        )
        malignant_score = float(
            malignant_scores(self.model.classes_, self.model.predict_proba(frame))[0]
        )
        raw_target = int(
            predictions_from_malignant_scores(
                [malignant_score],
                threshold=self.threshold,
            )[0]
        )
        return PredictionResponse(
            model_classification=RAW_TARGET_TO_LABEL[raw_target],
            raw_target=raw_target,
            malignant_class_score=malignant_score,
            decision_threshold=self.threshold,
            calibration_status="uncalibrated",
            score_interpretation=(
                "This is an uncalibrated malignant-class model score for a dataset-style "
                "feature vector. It is not an individual clinical probability or risk."
            ),
            warning_flags=self._warning_flags(features),
            model_version=self.manifest["model_version"],
            explanation_available=True,
            top_feature_contributions=self._local_contributions(frame),
            educational_limitation=EDUCATIONAL_LIMITATION,
        )
