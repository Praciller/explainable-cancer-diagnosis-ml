# Modeling Approach

## Split

One deterministic stratified split is reused:

- 70% training: 398 rows
- 15% validation: 85 rows
- 15% test: 86 rows

The validation set selects the baseline model. The test set reports final comparisons.

## Models

- Logistic Regression uses `StandardScaler` inside a scikit-learn pipeline.
- Random Forest uses 300 trees and a minimum leaf size of 2.
- Gradient Boosting uses scikit-learn defaults with a fixed seed.
- PyTorch MLP uses 30 inputs, hidden layers of 64 and 32, ReLU, dropout, and one binary logit.

The MLP uses Adam, binary cross-entropy, train-only scaling, deterministic loading, and early stopping.

## Selection

Baseline selection uses validation ROC-AUC for the malignant class. Logistic Regression and Random Forest both reached 1.0 validation ROC-AUC at seed 42; deterministic insertion order selects Logistic Regression. The test table remains the honest comparison.

## Reproducibility

Every command accepts or uses seed 42. Metadata stores the seed, feature order, target names, training time, and a hash of the loaded dataset.
