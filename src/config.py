from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "breast_cancer_raw.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "breast_cancer_processed.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample" / "sample_features.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

DISCLAIMER = (
    "This system is a machine learning portfolio demo and is not intended for "
    "medical diagnosis or clinical decision-making."
)
API_DISCLAIMER = "This is a portfolio ML demo and not medical advice."
RANDOM_SEED = 42
