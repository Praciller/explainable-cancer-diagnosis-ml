from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import PROCESSED_DATA_PATH, RANDOM_SEED
from src.data.load_dataset import load_dataset_frame


@dataclass(frozen=True)
class DatasetSplits:
    X_train: pd.DataFrame
    X_validation: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_validation: pd.Series
    y_test: pd.Series


@dataclass(frozen=True)
class ScaledSplits:
    X_train: np.ndarray
    X_validation: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_validation: np.ndarray
    y_test: np.ndarray
    scaler: StandardScaler
    feature_names: list[str]


def split_dataset(
    features: pd.DataFrame,
    target: pd.Series,
    seed: int = RANDOM_SEED,
) -> DatasetSplits:
    X_train, X_remaining, y_train, y_remaining = train_test_split(
        features,
        target,
        test_size=0.30,
        random_state=seed,
        stratify=target,
    )
    X_validation, X_test, y_validation, y_test = train_test_split(
        X_remaining,
        y_remaining,
        test_size=0.50,
        random_state=seed,
        stratify=y_remaining,
    )
    return DatasetSplits(
        X_train=X_train,
        X_validation=X_validation,
        X_test=X_test,
        y_train=y_train,
        y_validation=y_validation,
        y_test=y_test,
    )


def prepare_scaled_splits(splits: DatasetSplits) -> ScaledSplits:
    scaler = StandardScaler()
    X_train = scaler.fit_transform(splits.X_train)
    return ScaledSplits(
        X_train=X_train,
        X_validation=scaler.transform(splits.X_validation),
        X_test=scaler.transform(splits.X_test),
        y_train=splits.y_train.to_numpy(),
        y_validation=splits.y_validation.to_numpy(),
        y_test=splits.y_test.to_numpy(),
        scaler=scaler,
        feature_names=list(splits.X_train.columns),
    )


def save_processed_dataset(output_path: Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    bundle = load_dataset_frame()
    processed = bundle.frame.copy()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(output_path, index=False)
    return processed
