# Explainability

## Global Importance

Linear-model importance uses absolute standardized coefficients. Tree-model importance uses native feature importance values.

## SHAP

The explainability command uses `LinearExplainer` for the selected Logistic Regression pipeline and `TreeExplainer` for supported tree models.

Outputs:

- `feature_importance.png`
- `shap_summary.png`
- `shap_example_prediction.png`
- `explainability_summary.md`

## Interpretation Limits

SHAP attributes a model output relative to a background dataset. It does not prove:

- a feature causes malignancy;
- a feature is clinically actionable;
- the model will generalize to other populations or acquisition systems.

Strongly correlated measurements may divide or redistribute attribution.
