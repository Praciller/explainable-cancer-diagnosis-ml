# Error Analysis

Best baseline model: `logistic_regression`.

- False negatives (malignant predicted benign): 1
- False positives (benign predicted malignant): 0
- Other near-threshold rows: 4

Rows are identified by stable dataset indices. This review does not tune the model or threshold after inspecting the governed test set. A few errors do not support biological or medical conclusions.

This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
