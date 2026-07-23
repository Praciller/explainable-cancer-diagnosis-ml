# Modeling approach

## Governed split

Seed `42` creates a stratified 398/85/86 train/validation/governed-test split. Row IDs and assignment SHA-256 `497e9350c039abd8f56c26e0fd3d6abf962bb8008fce5379f0b1790a9684df9c` preserve lineage and make overlap checks reproducible.

Preprocessing is fitted after splitting. Logistic Regression uses `StandardScaler` inside its pipeline. The PyTorch scaler is fitted on training rows only. Tree candidates use raw features. No resampling or feature selection occurs.

## Candidate protocol

- Majority `DummyClassifier` establishes a meaningful floor.
- Regularized Logistic Regression, Random Forest, and Gradient Boosting are scikit-learn candidates.
- A compact CPU PyTorch MLP is retained as a challenger.

All candidates use the same train and validation rows, malignant-positive contract, threshold `0.50`, and deterministic seeds where supported. The MLP uses validation loss for checkpoint selection.

Candidate selection uses validation ROC-AUC. Exact ties prefer Logistic Regression, then Random Forest, then Gradient Boosting for lower complexity and interpretability. Test results do not choose the model.

The frozen selected model is evaluated once by the pipeline on the governed test rows. Those rows were exposed during earlier portfolio work, so the result is described as a governed regression artifact rather than a pristine scientific holdout.

Scores are uncalibrated. Threshold trade-off plots use validation labels only.
