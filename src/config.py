from pathlib import Path

from src.contracts import EDUCATIONAL_LIMITATION

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "breast_cancer_raw.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed" / "breast_cancer_processed.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample" / "sample_features.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

DISCLAIMER = EDUCATIONAL_LIMITATION
API_DISCLAIMER = EDUCATIONAL_LIMITATION
RANDOM_SEED = 42
