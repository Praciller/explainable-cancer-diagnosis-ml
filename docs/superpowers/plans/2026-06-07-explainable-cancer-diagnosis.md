# Explainable Cancer Diagnosis ML Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete local-first ML portfolio system specified in `explainable-cancer-diagnosis-ml-requirements.md`.

**Architecture:** Importable Python modules own data, training, evaluation, explanation, and inference behavior. FastAPI and React are adapters around stable contracts. Generated artifacts are reproducible and ignored where large.

**Tech Stack:** Python 3.12, pandas, scikit-learn, PyTorch, SHAP, FastAPI, Pydantic, React, Vite, TypeScript, Tailwind CSS, Recharts, pytest, Vitest.

---

### Task 1: Data loading and validation

**Files:** `tests/test_data_loading.py`, `src/data/load_dataset.py`, `src/data/validate_dataset.py`

- [ ] Write a failing test asserting 569 rows, 30 features, verified target names, labels, and saved metadata.
- [ ] Run `pytest tests/test_data_loading.py -v` and confirm failure because modules do not exist.
- [ ] Implement dataset loading, CSV persistence, metadata, and markdown validation report.
- [ ] Re-run the focused test and full data tests.

### Task 2: Reusable preprocessing

**Files:** `tests/test_preprocess.py`, `src/features/preprocess.py`

- [ ] Write failing tests for deterministic stratified 70/15/15 splits and train-only scaling.
- [ ] Implement split and pipeline helpers with configurable seed.
- [ ] Verify focused tests pass.

### Task 3: Baseline training

**Files:** `tests/test_baseline_training.py`, `src/models/train_baseline.py`, `src/utils/metrics.py`, `src/utils/tracking.py`

- [ ] Write a failing contract test using a temporary artifact directory.
- [ ] Implement Logistic Regression, Random Forest, and Gradient Boosting training, validation selection, model persistence, and optional MLflow logging.
- [ ] Verify artifacts and metrics through public training function.

### Task 4: PyTorch MLP

**Files:** `tests/test_pytorch_training.py`, `src/models/train_pytorch_mlp.py`

- [ ] Write a failing short-epoch training test.
- [ ] Implement Dataset/DataLoader training, early stopping, checkpoint persistence, metrics, and curve output.
- [ ] Verify CPU training and checkpoint reload.

### Task 5: Evaluation, EDA, explainability, and error analysis

**Files:** `src/evaluation/evaluate_models.py`, `src/evaluation/generate_eda.py`, `src/evaluation/error_analysis.py`, `src/explainability/explain_model.py`

- [ ] Write failing report-generation tests.
- [ ] Implement shared-test evaluation metrics and required figures.
- [ ] Implement EDA figures/summary, SHAP outputs, feature importance, and threshold/error reports.
- [ ] Verify commands generate all required outputs.

### Task 6: Strict prediction service and FastAPI

**Files:** `tests/test_prediction_schema.py`, `tests/test_api.py`, `src/api/schemas.py`, `src/api/service.py`, `src/api/main.py`

- [ ] Write failing schema tests for missing, extra, string, non-finite, and valid 30-feature inputs.
- [ ] Implement strict Pydantic models and reusable loaded prediction service.
- [ ] Write failing endpoint tests for health, model info, features, samples, predict, and batch predict.
- [ ] Implement lifespan model loading, CORS, stable errors, and disclaimer responses.
- [ ] Verify API tests pass.

### Task 7: React dashboard

**Files:** `frontend/src/**`, `frontend/package.json`, `frontend/vite.config.ts`

- [ ] Scaffold React/Vite/TypeScript/Tailwind and write component tests for disclaimer and sample-first prediction.
- [ ] Implement app shell, Overview, Prediction, Evaluation, and Explainability pages.
- [ ] Add API service, loading/error states, responsive navigation, accessible form controls, Recharts visualizations, and report images.
- [ ] Verify tests, TypeScript, production build, desktop browser flow, and mobile layout.

### Task 8: Reproducibility and documentation

**Files:** `README.md`, `docs/*.md`, notebooks, Dockerfiles, `docker-compose.yml`, `.github/workflows/ci.yml`

- [ ] Add complete local setup, commands, API examples, architecture, results, limitations, disclaimer, and portfolio review.
- [ ] Add executable notebooks that call production modules.
- [ ] Add optional Docker and MLflow instructions plus secret-free CI.
- [ ] Run full backend tests, frontend tests/build, pipeline smoke, API smoke, and repository requirement audit.
