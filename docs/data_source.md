# Data source and row contract

The project loads the Breast Cancer Wisconsin (Diagnostic) dataset with `sklearn.datasets.load_breast_cancer(as_frame=True)`. The data ships with scikit-learn, so the reviewer path requires no login, scraping, or network download.

The bundled description attributes the dataset to Wolberg, Street, and Mangasarian and the University of Wisconsin. Each of the 569 rows contains 30 real-valued measurements computed from a digitized image of a fine-needle aspirate sample. These fields are not ordinary symptoms or values a general user can safely measure. Physical units are not specified by the bundled documentation.

Verified with scikit-learn `1.6.1`:

- 569 rows;
- 30 ordered numeric features;
- 212 malignant rows (`0`);
- 357 benign rows (`1`);
- no missing, non-finite, duplicate-feature, duplicate-column, or constant-feature observations;
- canonical CSV SHA-256 `f721302d723688b8cce20f5f9b5c1bfcd654703234c137b9df575fca7fe7e218`.

Malignant (`0`) is the safety-relevant positive class for metrics, class-score extraction, confusion matrices, SHAP, and frontend order. Probability columns are resolved from `model.classes_`.

Generated local outputs:

- `data/raw/breast_cancer_raw.csv`;
- `data/processed/breast_cancer_processed.csv`;
- `data/sample/sample_features.csv`;
- `reports/dataset_metadata.md`;
- `reports/data_validation_report.md`.

The first two CSVs and generated JSON/figures are ignored. No patient, hospital, or private medical data is used.

> This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
