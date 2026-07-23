# Explainability contract

Global linear importance uses absolute standardized coefficients. Local contributions preserve sign and state whether a feature moved the selected model toward malignant or benign output.

`shap.LinearExplainer` returns the binary Logistic Regression class-1 direction, which is benign in this dataset. The project explicitly negates SHAP values and the expected value to reconstruct malignant-class (`0`) log-odds. Tests verify class selection, canonical feature order, sign, and `expected_value + sum(SHAP)`.

Generated outputs:

- `feature_importance.png`;
- `shap_summary.png`, explicitly labeled malignant-class log-odds;
- `shap_example_prediction.png`, dataset row 102;
- `explainability_summary.md`.

These explanations describe how the model used the supplied measurements. They do not prove biological causality, medical importance, or why cancer develops. Correlated measurements can divide or redistribute importance.

> This project is an educational machine-learning portfolio demonstration. It is not intended for diagnosis, screening, treatment, medical advice, or clinical decision-making.
