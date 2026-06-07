# Portfolio Review

## Implemented Features

- Offline scikit-learn dataset loading with verified class mapping.
- Raw, processed, sample, metadata, validation, and EDA outputs.
- Reusable stratified 70/15/15 split with train-only standardization.
- Logistic Regression, Random Forest, Gradient Boosting, and PyTorch MLP.
- Shared test metrics, ROC, precision-recall, confusion matrix, and training curve.
- SHAP summary and local waterfall explanation.
- False-positive, false-negative, low-confidence, and threshold analysis.
- Strict FastAPI single and batch inference plus feature and sample discovery.
- Responsive React dashboard with sample-first prediction.
- Optional local MLflow, Docker Compose, and secret-free CI.

## Data Science Skills Demonstrated

- Dataset validation and EDA.
- Leakage prevention and fair model comparison.
- Binary classification metrics beyond accuracy.
- Threshold and error trade-off interpretation.
- Clear separation of validation selection and held-out test reporting.

## ML Engineering Skills Demonstrated

- Importable training and inference modules.
- Deterministic seeds and persisted artifacts.
- CPU PyTorch training with early stopping.
- Startup-loaded model service and strict transport validation.
- Independent local Python, API, and frontend workflows.
- CI, Docker, and generated-artifact hygiene.

## Explainability Skills Demonstrated

- Model-family-aware feature importance.
- Global SHAP summary.
- Local SHAP waterfall.
- Plain-language caveats about correlation, causality, and clinical relevance.

## Reviewer Path

1. Read the measured table in `README.md`.
2. Run `python -m pytest`.
3. Open `reports/model_comparison.md` and `reports/error_analysis.md`.
4. Start FastAPI and inspect `/docs`, `/features`, and `/predict`.
5. Start the React dashboard and run a sample prediction.
6. Review `src/explainability/explain_model.py` and the generated SHAP figures.

## Remaining Gaps

- No independent clinical dataset or external validation.
- No probability calibration study.
- No hosted public demo.
- Frontend batch CSV upload is not implemented.
- Docker startup trains demo artifacts and is not optimized for minimal image size.

## Resume and LinkedIn Positioning

Lead with fair model comparison, explainability, and delivery beyond notebooks. State that the project is an educational portfolio system. Do not describe it as a diagnostic product or imply clinical validation.

Suggested headline:

> Explainable tabular ML system with PyTorch, SHAP, FastAPI, and React
