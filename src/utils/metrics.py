from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    malignant_probability: np.ndarray,
) -> dict[str, Any]:
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    true_malignant, false_benign = matrix[0]
    false_malignant, true_benign = matrix[1]
    sensitivity = true_malignant / max(true_malignant + false_benign, 1)
    specificity = true_benign / max(true_benign + false_malignant, 1)

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, pos_label=0, zero_division=0)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro")),
        "roc_auc": float(roc_auc_score(y_true == 0, malignant_probability)),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
        "confusion_matrix": matrix.tolist(),
    }
