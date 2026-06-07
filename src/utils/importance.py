from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def model_feature_importance(model: Any, feature_names: list[str]) -> pd.Series:
    estimator = model
    if isinstance(model, Pipeline):
        estimator = model.named_steps["classifier"]
    if hasattr(estimator, "feature_importances_"):
        values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        values = np.abs(estimator.coef_[0])
    else:
        raise TypeError(f"Model {type(estimator).__name__} has no supported importance values.")
    return pd.Series(values, index=feature_names).sort_values(ascending=False)
