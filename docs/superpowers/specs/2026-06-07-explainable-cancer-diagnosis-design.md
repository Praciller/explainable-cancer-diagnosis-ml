# Explainable Cancer Diagnosis ML Design

## Goal

Build a local-first educational portfolio system that trains and compares tabular classifiers, explains model outputs, serves strict inference contracts, and presents evidence in a responsive dashboard.

## Architecture

Production logic lives in importable Python modules under `src/`. Deterministic dataset splits are shared by baseline, PyTorch, evaluation, explainability, and error-analysis commands. FastAPI owns transport validation and delegates inference to a reusable prediction service. React consumes API metadata, feature schema, samples, prediction results, and generated report assets.

## Data Flow

`load_breast_cancer` -> raw/processed CSV -> stratified train/validation/test split -> baseline and PyTorch training -> shared test evaluation -> best-model metadata -> explainability/error reports -> FastAPI -> React dashboard.

## Contracts

- Dataset mapping must equal `["malignant", "benign"]`.
- Prediction requests contain exactly 30 finite numeric features.
- `/features` is the source of truth for frontend form fields and sample ranges.
- Models load once during FastAPI lifespan startup.
- Every prediction response includes the portfolio medical disclaimer.
- Docker and MLflow failures cannot block normal local commands.

## UI Direction

Restrained light product UI with aubergine navigation, coral malignant semantics, sage benign semantics, open report-like layouts, and system typography. Sample selection leads the prediction workflow; the full feature form is progressively disclosed.

## Testing

Vertical TDD slices cover data loading, split leakage prevention, model training contracts, strict request validation, API behavior, and frontend build/runtime smoke paths.
