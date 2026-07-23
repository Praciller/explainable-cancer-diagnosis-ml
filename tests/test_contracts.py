from __future__ import annotations

import numpy as np


def test_label_contract_is_explicit_and_malignant_positive() -> None:
    from src.contracts import label_contract

    contract = label_contract()

    assert contract["labels"][0] == {
        "raw_target": 0,
        "normalized_label": "malignant",
        "display_label": "Malignant",
        "safety_relevant_positive": True,
    }
    assert contract["metric_pos_label"] == 0
    assert contract["confusion_matrix_order"] == [0, 1]
    assert contract["shap_output_class"] == "malignant"
    assert contract["frontend_display_order"] == ["malignant", "benign"]


def test_malignant_score_resolves_model_classes_instead_of_column_position() -> None:
    from src.contracts import malignant_scores

    scores = malignant_scores(
        model_classes=np.array([1, 0]),
        probabilities=np.array([[0.8, 0.2], [0.1, 0.9]]),
    )

    assert scores.tolist() == [0.2, 0.9]


def test_metric_orientation_uses_malignant_as_positive_class() -> None:
    from src.utils.metrics import classification_metrics

    metrics = classification_metrics(
        y_true=np.array([0, 0, 1, 1]),
        y_pred=np.array([0, 1, 0, 1]),
        malignant_score=np.array([0.9, 0.4, 0.6, 0.1]),
    )

    assert metrics["confusion_matrix"] == [[1, 1], [1, 1]]
    assert metrics["sensitivity"] == 0.5
    assert metrics["specificity"] == 0.5
    assert metrics["false_negative_count"] == 1
    assert metrics["false_positive_count"] == 1
    assert metrics["sample_count"] == 4
