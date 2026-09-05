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

### PR #15 preview evidence

The current final-head PR preview is non-production and was created automatically by the Vercel Git integration:

- Preview alias: [explainable-cancer-diag-git-5a5f1c-pracillatlove-3370s-projects.vercel.app](https://explainable-cancer-diag-git-5a5f1c-pracillatlove-3370s-projects.vercel.app/)
- Direct deployment URL: [explainable-cancer-diagnosis-82c94u7uq.vercel.app](https://explainable-cancer-diagnosis-82c94u7uq.vercel.app/)
- GitHub deployment record: `6279879317`
- Vercel deployment inspector: `2rUohN2n7rxZeZBNbM36MvkZfzxW`
- Verified source commit: `2d7b0834de0396e4812bc65964c45da9baa006d5`
- Target: Preview (non-production)

The earlier owner-supplied preview snapshot for the pre-polish head remains useful for audit history: [explainable-cancer-diagnosis-lhoystgqn.vercel.app](https://explainable-cancer-diagnosis-lhoystgqn.vercel.app/) at Vercel deployment `dpl_CVMRKnnuQWpFCGD6vErtzhbWiHUy`, before the final-head polish. Preview aliases and deployment IDs can change when the branch receives a new commit.

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

Use the Vercel project’s owner-approved deployment workflow for a preview or production deployment. Do not invent project IDs, deployment IDs, environment values, or credentials in documentation. No production deployment or promotion was manually triggered. Vercel Git integration automatically created PR preview deployments.

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
