from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class LabelDefinition:
    raw_target: int
    normalized_label: str
    display_label: str
    safety_relevant_positive: bool


LABEL_DEFINITIONS = (
    LabelDefinition(
        raw_target=0,
        normalized_label="malignant",
        display_label="Malignant",
        safety_relevant_positive=True,
    ),
    LabelDefinition(
        raw_target=1,
        normalized_label="benign",
        display_label="Benign",
        safety_relevant_positive=False,
    ),
)
RAW_TARGET_TO_LABEL = {
    definition.raw_target: definition.normalized_label for definition in LABEL_DEFINITIONS
}
LABEL_TO_RAW_TARGET = {label: target for target, label in RAW_TARGET_TO_LABEL.items()}
CONFUSION_MATRIX_ORDER = tuple(definition.raw_target for definition in LABEL_DEFINITIONS)
FRONTEND_DISPLAY_ORDER = tuple(definition.normalized_label for definition in LABEL_DEFINITIONS)
SAFETY_POSITIVE_RAW_TARGET = 0
SAFETY_POSITIVE_LABEL = RAW_TARGET_TO_LABEL[SAFETY_POSITIVE_RAW_TARGET]
DECISION_THRESHOLD = 0.5
CALIBRATION_STATUS = "uncalibrated"

EDUCATIONAL_LIMITATION = (
    "This project is an educational machine-learning portfolio demonstration. "
    "It is not intended for diagnosis, screening, treatment, medical advice, "
    "or clinical decision-making."
)


def label_contract() -> dict[str, Any]:
    return {
        "labels": [asdict(definition) for definition in LABEL_DEFINITIONS],
        "probability_column_mapping": "resolved from model.classes_",
        "metric_pos_label": SAFETY_POSITIVE_RAW_TARGET,
        "confusion_matrix_order": list(CONFUSION_MATRIX_ORDER),
        "shap_output_class": SAFETY_POSITIVE_LABEL,
        "frontend_display_order": list(FRONTEND_DISPLAY_ORDER),
    }


def score_for_raw_target(
    model_classes: Any,
    probabilities: Any,
    raw_target: int,
) -> np.ndarray:
    classes = np.asarray(model_classes)
    matches = np.flatnonzero(classes == raw_target)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one probability column for raw target {raw_target}.")
    values = np.asarray(probabilities)
    if values.ndim != 2:
        raise ValueError("Probability output must be a two-dimensional array.")
    return values[:, int(matches[0])]


def malignant_scores(model_classes: Any, probabilities: Any) -> np.ndarray:
    return score_for_raw_target(
        model_classes,
        probabilities,
        SAFETY_POSITIVE_RAW_TARGET,
    )


def predictions_from_malignant_scores(
    scores: Any,
    threshold: float = DECISION_THRESHOLD,
) -> np.ndarray:
    values = np.asarray(scores, dtype=float)
    return np.where(
        values >= threshold,
        SAFETY_POSITIVE_RAW_TARGET,
        LABEL_TO_RAW_TARGET["benign"],
    )
