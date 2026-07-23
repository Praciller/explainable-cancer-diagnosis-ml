# Explainability Summary

The selected baseline model is `logistic_regression`. Its strongest global importance signals are:

- `worst texture`: 1.2263
- `worst concave points`: 0.9968
- `worst area`: 0.9550
- `worst radius`: 0.9411
- `area error`: 0.9375
- `radius error`: 0.8864
- `worst symmetry`: 0.8694
- `worst concavity`: 0.7860
- `worst smoothness`: 0.7490
- `worst perimeter`: 0.7310

The SHAP output class is explicitly `malignant` (`raw target 0`). The local waterfall uses dataset row `102` and reconstructs the malignant-class log-odds relative to the training-background expectation.

These explanations describe how the model used the supplied measurements. They do not prove biological causality, medical importance, or why cancer develops. Correlated measurements can divide or redistribute importance.

This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
