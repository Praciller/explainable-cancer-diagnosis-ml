import numpy as np


def test_split_dataset_is_deterministic_stratified_and_complete() -> None:
    from src.data.load_dataset import load_dataset_frame
    from src.features.preprocess import split_dataset

    bundle = load_dataset_frame()
    first = split_dataset(bundle.features, bundle.target, seed=17)
    second = split_dataset(bundle.features, bundle.target, seed=17)

    assert (len(first.X_train), len(first.X_validation), len(first.X_test)) == (398, 85, 86)
    assert first.X_train.index.equals(second.X_train.index)
    assert set(first.X_train.index).isdisjoint(first.X_validation.index)
    assert set(first.X_train.index).isdisjoint(first.X_test.index)
    assert abs(first.y_train.mean() - bundle.target.mean()) < 0.02


def test_standard_scaler_is_fit_on_training_data_only() -> None:
    from src.data.load_dataset import load_dataset_frame
    from src.features.preprocess import prepare_scaled_splits, split_dataset

    bundle = load_dataset_frame()
    splits = split_dataset(bundle.features, bundle.target, seed=42)
    scaled = prepare_scaled_splits(splits)

    assert np.allclose(scaled.X_train.mean(axis=0), 0, atol=1e-10)
    assert np.allclose(scaled.scaler.mean_, splits.X_train.mean(axis=0))
    assert scaled.X_validation.shape == splits.X_validation.shape
    assert scaled.X_test.shape == splits.X_test.shape
