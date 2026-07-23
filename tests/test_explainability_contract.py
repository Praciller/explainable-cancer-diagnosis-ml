from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def test_linear_shap_reconstructs_malignant_class_log_odds() -> None:
    from src.data.load_dataset import load_dataset_frame
    from src.explainability.explain_model import _shap_values
    from src.features.preprocess import split_dataset

    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed=42)
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    ).fit(splits.X_train, splits.y_train)
    sample = splits.X_test.iloc[:1]
    background = splits.X_train.iloc[:100]

    values, _, expected = _shap_values(model, background, sample)
    benign_log_odds = float(model.decision_function(sample)[0])

    assert list(sample.columns) == bundle.feature_names
    assert np.isclose(expected + values[0].sum(), -benign_log_odds)
