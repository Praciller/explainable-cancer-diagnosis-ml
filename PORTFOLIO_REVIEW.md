# Portfolio review

## What this project demonstrates

- Deterministic packaged-dataset loading, validation, fingerprinting, and row lineage.
- One explicit malignant-positive contract across metrics, score extraction, SHAP, API, and React.
- Leakage-safe train-only preprocessing and 398/85/86 split governance.
- Majority baseline plus Logistic Regression, Random Forest, Gradient Boosting, and CPU PyTorch challenger.
- Validation-only selection with an explicit complexity tie-break.
- Selected-model governed-test evaluation with exact confusion counts, ROC-AUC, PR-AUC, and raw saved predictions.
- Malignant-oriented SHAP reconstruction with sign and feature-order tests.
- Fail-closed artifact manifest and checksum validation.
- Strict FastAPI transport contracts and a generated, accessible, read-only evidence dashboard.
- Optional local MLflow, deterministic Docker build artifacts, and secret-free CI.

## Reviewer path

1. Read the first two screens of `README.md`.
2. Inspect `src/contracts.py`, `src/features/preprocess.py`, and `src/artifacts/manifest.py`.
3. Run `python -m pytest`.
4. Run `python -m src.pipeline --seed 42 --mlp-epochs 100`.
5. Confirm `/ready`, inspect one `/predict` response, then open the local React dashboard.

## Honest remaining limits

- The test artifact was previously exposed.
- Scores are uncalibrated.
- No external or prospective validation exists.
- No fairness or representativeness claim is made.
- Live inference remains local.
- Docker builds are deterministic in configuration but still depend on pinned package indexes and base-image availability.

The repository is suitable as an educational ML engineering portfolio project when these boundaries remain visible. It is not a clinical product.
