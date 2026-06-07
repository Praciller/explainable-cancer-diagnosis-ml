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

SHAP values describe how this model's inputs move its output relative to a background expectation. They do not establish causality, biological mechanism, or clinical relevance. Correlated measurements can divide or redistribute importance.
