from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.api.schemas import (
    FeatureContribution,
    FeatureDefinition,
    PredictionResponse,
    SampleRecord,
)
from src.config import API_DISCLAIMER, MODELS_DIR
from src.data.load_dataset import DatasetBundle, load_dataset_frame
from src.utils.importance import model_feature_importance


class PredictionService:
    def __init__(self, model: Any, metadata: dict[str, Any], dataset: DatasetBundle) -> None:
        self.model = model
        self.metadata = metadata
        self.dataset = dataset
        self._global_importance = model_feature_importance(model, dataset.feature_names)

    @classmethod
    def from_artifacts(cls, models_dir: Path = MODELS_DIR) -> "PredictionService":
        model_path = models_dir / "best_model.joblib"
        metadata_path = models_dir / "model_metadata.json"
        if not model_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(
                "Model artifacts are missing. Run `python -m src.models.train_baseline` first."
            )
        return cls(
            model=joblib.load(model_path),
            metadata=json.loads(metadata_path.read_text(encoding="utf-8")),
            dataset=load_dataset_frame(),
        )

    def model_info(self) -> dict[str, Any]:
        return {
            "model_name": self.metadata["model_name"],
            "problem_type": "binary_classification",
            "features": len(self.dataset.feature_names),
            "classes": self.dataset.target_names,
            "dataset_version": self.metadata["dataset_version"],
        }

    def feature_definitions(self) -> list[FeatureDefinition]:
        return [
            FeatureDefinition(
                name=name,
                minimum=float(self.dataset.features[name].min()),
                maximum=float(self.dataset.features[name].max()),
                mean=float(self.dataset.features[name].mean()),
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
            row = self.dataset.frame.iloc[index]
            records.append(
                SampleRecord(
                    id=index,
                    known_label=str(row["label"]),
                    features={name: float(row[name]) for name in self.dataset.feature_names},
                )
            )
        return records

    def _local_importance(self, frame: pd.DataFrame) -> pd.Series:
        if isinstance(self.model, Pipeline) and "scaler" in self.model.named_steps:
            scaled = self.model.named_steps["scaler"].transform(frame)[0]
            classifier = self.model.named_steps["classifier"]
            if hasattr(classifier, "coef_"):
                values = np.abs(classifier.coef_[0] * scaled)
                return pd.Series(values, index=self.dataset.feature_names).sort_values(
                    ascending=False
                )
        return self._global_importance

    def predict(self, features: dict[str, float]) -> PredictionResponse:
        frame = pd.DataFrame([features], columns=self.dataset.feature_names)
        class_id = int(self.model.predict(frame)[0])
        raw_probabilities = self.model.predict_proba(frame)[0]
        probabilities = {
            self.dataset.target_names[int(class_value)]: float(raw_probabilities[position])
            for position, class_value in enumerate(self.model.classes_)
        }
        importance = self._local_importance(frame).head(8)
        return PredictionResponse(
            predicted_class=self.dataset.target_names[class_id],
            predicted_class_id=class_id,
            confidence=max(probabilities.values()),
            probabilities=probabilities,
            top_features=[
                FeatureContribution(feature=name, importance=float(value))
                for name, value in importance.items()
            ],
            disclaimer=API_DISCLAIMER,
        )
