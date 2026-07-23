# Dataset Metadata

## Source

`sklearn.datasets.load_breast_cancer(as_frame=True)` using the Breast Cancer Wisconsin (Diagnostic) dataset. The source measurements were computed from digitized images of fine-needle aspirate samples. The bundled scikit-learn description attributes the data to Wolberg, Street, and Mangasarian and the University of Wisconsin.

- scikit-learn version: `1.6.1`
- Canonical CSV SHA-256: `f721302d723688b8cce20f5f9b5c1bfcd654703234c137b9df575fca7fe7e218`
- Physical units: not specified by the bundled dataset documentation

## Shape

- Rows: 569
- Numeric features: 30
- Saved columns: 32

## Target Mapping

- `0`: malignant
- `1`: benign
- Malignant rows: 212
- Benign rows: 357
- Safety-relevant positive class: `malignant` (`0`)
- Shared contract: `{'labels': [{'raw_target': 0, 'normalized_label': 'malignant', 'display_label': 'Malignant', 'safety_relevant_positive': True}, {'raw_target': 1, 'normalized_label': 'benign', 'display_label': 'Benign', 'safety_relevant_positive': False}], 'probability_column_mapping': 'resolved from model.classes_', 'metric_pos_label': 0, 'confusion_matrix_order': [0, 1], 'shap_output_class': 'malignant', 'frontend_display_order': ['malignant', 'benign']}`

## Features

- `mean radius`
- `mean texture`
- `mean perimeter`
- `mean area`
- `mean smoothness`
- `mean compactness`
- `mean concavity`
- `mean concave points`
- `mean symmetry`
- `mean fractal dimension`
- `radius error`
- `texture error`
- `perimeter error`
- `area error`
- `smoothness error`
- `compactness error`
- `concavity error`
- `concave points error`
- `symmetry error`
- `fractal dimension error`
- `worst radius`
- `worst texture`
- `worst perimeter`
- `worst area`
- `worst smoothness`
- `worst compactness`
- `worst concavity`
- `worst concave points`
- `worst symmetry`
- `worst fractal dimension`

Each row is an educational dataset record, not a current patient or a general-user symptom questionnaire. The dataset is small, clean, and not clinically representative.

This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
