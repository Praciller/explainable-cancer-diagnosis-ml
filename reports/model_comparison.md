# Governed Model Evaluation

## Validation-only candidate comparison

| Model | ROC-AUC | PR-AUC | Balanced accuracy | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|
| dummy_majority | 0.5000 | 0.3765 | 0.5000 | 0.0000 | 1.0000 |
| logistic_regression (selected) | 1.0000 | 1.0000 | 0.9906 | 1.0000 | 0.9811 |
| random_forest | 1.0000 | 1.0000 | 0.9906 | 1.0000 | 0.9811 |
| gradient_boosting | 0.9994 | 0.9991 | 0.9749 | 0.9688 | 0.9811 |
| pytorch_mlp | 1.0000 | 1.0000 | 0.9811 | 1.0000 | 0.9623 |

## Governed test result

- Selected model: `logistic_regression`
- Selection metric: `validation_roc_auc`
- Fixed threshold: `0.5`
- Calibration status: `uncalibrated`
- Sample count: 86
- Confusion matrix order: malignant, benign; values: `[[31, 1], [0, 54]]`
- Malignant-to-benign errors: 1
- Benign-to-malignant errors: 0
- ROC-AUC: 0.9954
- PR-AUC: 0.9938

This 86-row test artifact has been exposed during prior portfolio development. It is retained as a governed regression set, not represented as a pristine scientific benchmark.

This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
