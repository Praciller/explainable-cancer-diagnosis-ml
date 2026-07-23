from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.contracts import (
    CONFUSION_MATRIX_ORDER,
    DECISION_THRESHOLD,
    SAFETY_POSITIVE_RAW_TARGET,
)


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    malignant_score: np.ndarray,
    threshold: float = DECISION_THRESHOLD,
) -> dict[str, Any]:
    matrix = confusion_matrix(y_true, y_pred, labels=CONFUSION_MATRIX_ORDER)
    true_malignant, false_negative = matrix[0]
    false_positive, true_benign = matrix[1]
    sensitivity = true_malignant / max(true_malignant + false_negative, 1)
    specificity = true_benign / max(true_benign + false_positive, 1)
    malignant_truth = np.asarray(y_true) == SAFETY_POSITIVE_RAW_TARGET
    malignant_precision = precision_score(
        y_true,
        y_pred,
        pos_label=SAFETY_POSITIVE_RAW_TARGET,
        zero_division=0,
    )
    malignant_recall = recall_score(
        y_true,
        y_pred,
        pos_label=SAFETY_POSITIVE_RAW_TARGET,
        zero_division=0,
    )

    return {
        "sample_count": int(len(y_true)),
        "threshold": float(threshold),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "malignant_precision": float(malignant_precision),
        "malignant_recall": float(malignant_recall),
        "malignant_f1": float(
            f1_score(
                y_true,
                y_pred,
                pos_label=SAFETY_POSITIVE_RAW_TARGET,
                zero_division=0,
            )
        ),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "roc_auc": float(roc_auc_score(malignant_truth, malignant_score)),
        "pr_auc": float(average_precision_score(malignant_truth, malignant_score)),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "true_malignant_count": int(true_malignant),
        "false_negative_count": int(false_negative),
        "false_positive_count": int(false_positive),
        "true_benign_count": int(true_benign),
        "confusion_matrix": matrix.tolist(),
    }
