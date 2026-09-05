# ADR 0003: Evidence-driven maintenance gates

## Context

The repository had 14 simultaneous Dependabot pull requests and a working but incomplete quality signal: backend/frontend tests and builds existed, while coverage, assembled accessibility, bundle size, and dependency inventory were not consistently reported. Several updates were major transitions with different risk profiles: MLflow 2 to 3, TypeScript 6 to 7, jest-dom 6 to 7, and pytest-cov 6 to 7.

## Options considered

1. Merge or group every open update. This reduces the queue but obscures breakage and mixes optional MLflow and compiler migrations with application maintenance.
2. Freeze all dependency maintenance. This avoids immediate migration work but leaves routine fixes and CI action maintenance stale.
3. Apply verified patch/minor and CI-only maintenance, add measured gates, and hold major transitions for dedicated migrations. This keeps the maintenance PR reviewable and makes evidence the release decision.

## Decision

Choose option 3. Dependabot groups only routine minor/patch version updates per ecosystem; major MLflow, TypeScript, jest-dom, and pytest-cov updates remain standalone and are ignored for version updates while security updates remain visible. FastAPI, Pydantic, pytest, React paired with react-dom, user-event, Tailwind, and the CI Actions updates are accepted only with full local/CI/browser verification.

The backend gate measures the API and artifact-validation surfaces with a 90% threshold; it is not a model-quality claim. Frontend coverage is reported using the compatible V8 provider but has no arbitrary threshold. Playwright runs maintained axe checks for serious/critical findings on the hosted route set. A small JS/CSS bundle budget is enforced from the measured build baseline. CI emits npm CycloneDX and Python package inventory artifacts, retains least-privilege permissions, and disables checkout credential persistence.

Visual regression remains evidence-driven: stable snapshots may be added only after cross-environment verification; otherwise screenshot/browser evidence is reported as partial. Production verification is read-only and owner-gated. No model evidence, artifact, API schema, terminology, target orientation, feature order, or split is changed.

## Consequences

Routine dependency noise is reduced without hiding security updates, and the draft PR has reproducible evidence for quality and supply chain. The repository still has explicit follow-up work for four major transitions and visual baselines. Coverage numbers describe exercised code paths only. CI artifacts are generated and ignored, so they do not pollute the governed source tree.
