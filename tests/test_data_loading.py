from pathlib import Path


def test_load_dataset_verifies_shape_and_target_mapping() -> None:
    from src.data.load_dataset import load_dataset_frame

    bundle = load_dataset_frame()

    assert bundle.feature_names == list(bundle.features.columns)
    assert all(type(name) is str for name in bundle.feature_names)
    assert len(bundle.feature_names) == 30
    assert bundle.target_names == ["malignant", "benign"]
    assert bundle.frame.shape == (569, 32)
    assert set(bundle.frame["label"]) == {"malignant", "benign"}


def test_save_dataset_assets_writes_csv_and_metadata(tmp_path: Path) -> None:
    from src.data.load_dataset import save_dataset_assets

    raw_path = tmp_path / "data" / "raw.csv"
    metadata_path = tmp_path / "reports" / "metadata.md"

    save_dataset_assets(raw_path=raw_path, metadata_path=metadata_path)

    assert raw_path.exists()
    metadata = metadata_path.read_text(encoding="utf-8")
    assert "569" in metadata
    assert "30" in metadata
    assert "malignant" in metadata
    assert "mean radius" in metadata


def test_save_portfolio_data_writes_processed_and_sample_csvs(tmp_path: Path) -> None:
    from src.data.load_dataset import save_portfolio_data

    processed_path = tmp_path / "processed.csv"
    sample_path = tmp_path / "sample.csv"

    save_portfolio_data(processed_path=processed_path, sample_path=sample_path, sample_rows=6)

    assert processed_path.exists()
    assert sample_path.exists()
    assert len(sample_path.read_text(encoding="utf-8").splitlines()) == 7
