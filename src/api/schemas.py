from __future__ import annotations

import math
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.data.load_dataset import load_dataset_frame

FEATURE_NAMES = tuple(load_dataset_frame().feature_names)
FEATURE_SET = frozenset(FEATURE_NAMES)


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    features: dict[str, float]

    @field_validator("features", mode="before")
    @classmethod
    def validate_features(cls, value: Any) -> dict[str, float]:
        if not isinstance(value, dict):
            raise ValueError("features must be an object keyed by feature name")
        provided = set(value)
        missing = sorted(FEATURE_SET - provided)
        extra = sorted(provided - FEATURE_SET)
        if missing or extra:
            parts = []
            if missing:
                parts.append(f"missing features: {', '.join(missing)}")
            if extra:
                parts.append(f"unknown features: {', '.join(extra)}")
            raise ValueError("; ".join(parts))

        normalized: dict[str, float] = {}
        for name in FEATURE_NAMES:
            item = value[name]
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise ValueError(f"{name} must be a numeric value")
            number = float(item)
            if not math.isfinite(number):
                raise ValueError(f"{name} must be finite")
            normalized[name] = number
        return normalized


class BatchPredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[PredictionRequest] = Field(min_length=1, max_length=100)


class FeatureContribution(BaseModel):
    feature: str
    contribution: float
    direction: Literal["toward_malignant", "toward_benign", "magnitude_only"]


class PredictionResponse(BaseModel):
    model_classification: Literal["malignant", "benign"]
    raw_target: Literal[0, 1]
    malignant_class_score: float
    decision_threshold: float
    calibration_status: Literal["uncalibrated"]
    score_interpretation: str
    warning_flags: list[str]
    model_version: str
    explanation_available: bool
    top_feature_contributions: list[FeatureContribution]
    educational_limitation: str


class BatchPredictionResponse(BaseModel):
    results: list[PredictionResponse]


class FeatureDefinition(BaseModel):
    name: str
    minimum: float
    maximum: float
    mean: float
    measurement_context: str


class FeatureListResponse(BaseModel):
    features: list[FeatureDefinition]


class SampleRecord(BaseModel):
    dataset_row_id: int
    known_label: Literal["malignant", "benign"]
    features: dict[str, float]


class SampleListResponse(BaseModel):
    samples: list[SampleRecord]


class ModelInfoResponse(BaseModel):
    model_name: str
    problem_type: Literal["binary_classification"]
    features: int
    classes: list[str]
    positive_class: Literal["malignant"]
    dataset_fingerprint: str
    model_version: str
    decision_threshold: float
    calibration_status: Literal["uncalibrated"]
    educational_limitation: str


class ReadinessResponse(BaseModel):
    status: Literal["ready"]
    model_version: str
    manifest_validated: Literal[True]
