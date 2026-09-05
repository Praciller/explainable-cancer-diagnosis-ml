# Deployment runbook

## Prerequisites

- Node.js and npm compatible with the checked-in frontend lockfile.
- Python dependencies installed for local API/inference verification.
- Vercel access only when an owner explicitly authorizes preview or production deployment.
- No secret, credential, deployment ID, or machine-specific path is required in this repository.

## Local workflow

From the repository root, generate trusted local artifacts when inference is needed:

```powershell
python -m src.pipeline --seed 42 --mlp-epochs 100
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Without `VITE_API_URL`, a production frontend build is the read-only showcase. With `VITE_API_URL=http://localhost:8000`, the frontend connects to the local FastAPI service and enables dataset-row inference. The local API is an educational service with no authentication; it exposes only repository dataset rows.

## Vercel behavior

The public showcase is a Vite frontend deployed at [explainable-cancer-diagnosis-ml.vercel.app](https://explainable-cancer-diagnosis-ml.vercel.app/). Production builds without `VITE_API_URL` use checked-in `frontend/src/data/showcase_contract.json` and remain read-only. They do not expose the FastAPI inference service. A preview can be inspected separately; local code and a successful build do not establish that a preview or production deployment contains the same commit.

## Build and deployment commands

```powershell
cd frontend
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run build-storybook
```

Use the Vercel project’s owner-approved deployment workflow for a preview or production deployment. Do not invent project IDs, deployment IDs, environment values, or credentials in documentation. This runbook does not trigger a deployment.

## Verification checklist

- Confirm the deployed URL returns the expected app shell.
- Confirm Overview, Evaluation, Explainability, and Prediction render in a real browser.
- Confirm Prediction explicitly says live inference remains local and no general-purpose hosted inference is exposed.
- Confirm the educational disclaimer, model-score terminology, charts/tables, keyboard focus, mobile layout, and no-horizontal-overflow behavior.
- Check the deployed source/commit through the hosting provider when access is available; otherwise report deployment identity as unverified.
- Keep live, preview, local, seeded, and mock evidence separate in the verification report.

## Rollback

For a PR or branch change, revert the responsible commit or PR and rerun the relevant local/browser checks. For a deployed version, use the owner-approved Vercel rollback or redeploy workflow for the last verified deployment. No production setting, branch ruleset, or public deployment is changed by this repository workflow.

## Known limitations

The public showcase is static/read-only evidence. Local inference requires generated trusted artifacts and a running FastAPI service. The dataset, governed test set, model scores, and explainability outputs retain the limitations in `docs/limitations.md`; none are evidence of clinical validity, safety, or production readiness.
