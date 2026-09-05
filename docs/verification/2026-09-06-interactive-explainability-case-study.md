# Interactive Explainability Case Study Verification

## Classification

`PASS` — the Draft PR remains owner-gated, while local gates, current-head
CI/CodeQL, Vercel Preview, and real Chromium verification are green.

## Source and artifact evidence

- Baseline: `origin/main=0467ffabcff8d2c17de38e3a4fbaa1abaee64c1`
- Branch: `feat/interactive-explainability-case-study`
- Current head: `637c6c288724921a0558ef1517bcc32af6189288`
- Draft PR: [#48](https://github.com/Praciller/explainable-cancer-diagnosis-ml/pull/48)
- The final delivery head adds this evidence report as a docs-only commit; the
  resulting SHA is reported in the delivery response.
- Artifact: `frontend/src/data/explainability_case.json`
- Artifact schema: `1`
- Dataset row: `102`, locked test split, raw target `1`, known label `benign`
- Model: `logistic_regression`, version `bbb5977c47501cd9a962`
- Positive class: `malignant` (raw target `0`)
- Output space: `malignant_class_log_odds`
- Base value: `-0.5770589234377406`
- Contribution count: `30`
- Contribution sum: `-4.199147683081785`
- Reconstructed log-odds: `-4.776206606519525`
- Reconstructed score: `0.008357472762137497`
- Model score: `0.008357472762137497`
- Reconstruction error: `2.6645352591003757e-15`
- Reconstruction tolerance: `1e-9`

The generator `python -m src.explainability.case_study` derives the artifact
from the existing model, manifest, dataset, seed-42 split, training background,
SHAP orientation, and malignant-class score mapping. No training or API change
is part of this feature.

Governed file Git object hashes, unchanged from `origin/main`:

| File | Git object hash |
| --- | --- |
| `reports/locked_test_predictions.csv` | `763f61ebb151e07734ddadbf857f0f9d40887476` |
| `frontend/src/data/showcase_contract.json` | `10776b05b550618bb8c2a18d07a53d3128ad0c73` |
| `reports/model_comparison.md` | `33fc84ca27c80406beee54794e6d2573671142e0` |
| `reports/error_analysis.md` | `b39d9ef980e10df274fdf73c74622da0fdb262e7` |
| `reports/explainability_summary.md` | `91d6b45f2c43742cf35acc5752e65cc52629db37` |

`git diff --quiet origin/main...HEAD` for all five files exited `0`. The API
contract diff for `src/api` and `src/contracts.py` is empty.

## UI and browser evidence

- Case summary: row 102, selected model/version, malignant-class model score,
  threshold, model classification, and calibration status are visible.
- Reconstruction: base value plus contribution sum, reconstructed log-odds,
  sigmoid score, and threshold comparison are visible.
- Contributions: top 8 default; native `Show all 30 contributions` expands to
  all 30; feature selection works with pointer and keyboard.
- Global/local explanation: recurring global model behavior is distinguished
  from this supplied row’s local contribution; correlation and non-causality
  limits are stated.
- Limitation: existing educational-use disclaimer is retained.
- Hosted behavior: case data is static JSON; no FastAPI or inference request is
  made in hosted mode.
- Responsive checks: final Vercel Preview was inspected in authenticated real
  Chromium at 1440px, 1024px, 640px, 390px, and 332px. At every width the
  case study, reconstruction, disclaimer, and active Explainability state were
  present. At 332px, document `clientWidth` and `scrollWidth` both measured
  317px.
- Accessibility: hosted axe scan has zero serious/critical findings across the
  five widths and both Chromium projects; the real-browser keyboard flow
  focused the skip link on Tab and `main#main-content` after Enter.
- Interaction: real Chromium expanded all 30 contributions and selected
  `mean compactness` by keyboard; the selected detail panel was visible.
- Console: final-preview Chromium inspection collected zero console `error`
  messages.
- Local E2E: real FastAPI sample prediction passed in both Chromium projects.
  The local preview was run on port 5173 because the unchanged API CORS contract
  allows `127.0.0.1:5173` and not the default 4173.

Final Vercel Preview: https://explainable-cancer-diagnosis-fhy3c5fxu.vercel.app
for head `637c6c288724921a0558ef1517bcc32af6189288`. Reviewer captures were
made in real Chromium for `explainability-case-desktop.png`,
`explainability-case-mobile-390.png`, `explainability-case-mobile-332.png`,
and `explainability-case-feature-selected.png`; they are task evidence rather
than committed browser output, per repository policy.

## Verification commands

Passing local results:

- `ruff format --check src tests`
- `ruff check src tests`
- `python -m compileall -q src tests`
- `python -m pytest` — `35 passed`
- `docker compose config --quiet`
- `frontend/npm ci`
- `frontend/npm audit --audit-level=high` — `0 vulnerabilities`
- `frontend/npm run lint`
- `frontend/npm run typecheck`
- `frontend/npm test -- --coverage` — `8 files, 17 tests passed`, `96.1%` statements
- `frontend/npm run build`
- `frontend/npm run check:bundle` — JS `544114/600000` bytes, CSS `20924/30000` bytes
- `frontend/npm run build-storybook`
- `frontend/npm run e2e:hosted -- showcase.spec.ts` — `6 passed`
- `frontend/npm run e2e:hosted -- accessibility.spec.ts` — `6 passed`
- `frontend/PLAYWRIGHT_PORT=5173 npm run e2e:local` — `8 passed, 8 skipped`

Remote CI run `33983122818`: backend, frontend, browser, and packaging pass.
- Remote CodeQL run `33983122821`: Analyze (python), Analyze
  (javascript-typescript), and CodeQL pass.
- Vercel Preview deployment `6284160551`: success.

## Contracts and non-goals

- `GOVERNED_ML_EVIDENCE_CHANGED=NO`
- `LOCKED_ARTIFACTS_CHANGED=NO`
- `SHOWCASE_CONTRACT_CHANGED=NO`
- `API_CONTRACT_CHANGED=NO`
- `DEPENDENCIES_CHANGED=NO`
- `BRANCH_PROTECTION_CHANGED=NO`
- `PRODUCTION_CHANGED=NO`
- Held migrations remain held: MLflow `3`, TypeScript `7`, jest-dom `7`, and
  pytest-cov `7`.
- Dependabot PRs `#45` and `#46` were not modified.

## Limitations and owner review

The case study is one static educational dataset row and does not provide live
inference, calibration, biological causality, clinical interpretation, or
production evidence. The preview is not production; production remains
owner-gated through the existing Git integration.

`READY_FOR_OWNER_REVIEW=YES`
