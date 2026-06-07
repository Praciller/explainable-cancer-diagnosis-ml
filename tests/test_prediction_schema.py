import math

import pytest
from pydantic import ValidationError

from src.data.load_dataset import load_dataset_frame


def _valid_features() -> dict[str, float]:
    return load_dataset_frame().features.iloc[0].to_dict()


def test_prediction_schema_accepts_exactly_30_finite_numeric_features() -> None:
    from src.api.schemas import PredictionRequest

    request = PredictionRequest(features=_valid_features())

    assert len(request.features) == 30


@pytest.mark.parametrize("mutation", ["missing", "extra", "string", "infinite"])
def test_prediction_schema_rejects_invalid_feature_maps(mutation: str) -> None:
    from src.api.schemas import PredictionRequest

    features = _valid_features()
    if mutation == "missing":
        features.pop(next(iter(features)))
    elif mutation == "extra":
        features["unknown feature"] = 1.0
    elif mutation == "string":
        features["mean radius"] = "17.99"  # type: ignore[assignment]
    else:
        features["mean radius"] = math.inf

    with pytest.raises(ValidationError):
        PredictionRequest(features=features)
