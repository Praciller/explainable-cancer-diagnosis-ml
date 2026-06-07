# Data Source

The project loads the Breast Cancer Wisconsin Diagnostic dataset with:

```python
from sklearn.datasets import load_breast_cancer

dataset = load_breast_cancer(as_frame=True)
```

The source is bundled with scikit-learn, so no Kaggle account, login, scraping, or runtime network download is required.

## Shape and Target

- 569 rows
- 30 numeric features
- `0 = malignant`
- `1 = benign`

The loader verifies `dataset.target_names` before saving any data. A human-readable `label` column is added beside the numeric `target`.

## Local Outputs

- `data/raw/breast_cancer_raw.csv`
- `data/processed/breast_cancer_processed.csv`
- `data/sample/sample_features.csv`
- `reports/dataset_metadata.md`
- `reports/data_validation_report.md`

The public dataset is educational and does not represent the complexity, prevalence, acquisition variation, or governance requirements of deployed clinical data.
