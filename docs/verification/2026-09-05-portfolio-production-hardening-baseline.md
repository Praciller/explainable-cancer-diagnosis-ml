# Portfolio production hardening baseline

## Snapshot

- Captured: 2026-09-05
- Base branch: `origin/main`
- Base SHA: `5a463b12bf64678a0359b8c384dd0248a7a30e94`
- Work branch: `chore/portfolio-production-hardening`
- Open Dependabot PRs: 14 (`#16`–`#29`)
- Main required checks observed: `backend`, `frontend`, `browser`, `packaging`, `Analyze (python)`, `Analyze (javascript-typescript)`
- Main protection/rulesets: read-only inspection only; no ruleset mutation performed

## Measured local baseline

- Backend: 34 tests passed; total coverage 82% before the critical-surface gate.
- Critical backend surface (`src/api`, `src/artifacts`): 91.29% with the proposed 90% threshold.
- Frontend: 12 tests passed; V8 report 94.11% statements, 75% branches, 88.88% functions, and 93.93% lines over the exercised modules. This is reported evidence, not a global threshold.
- Production asset baseline before/after safe maintenance remains approximately 537,531 bytes JavaScript and 17,581 bytes CSS; enforced budgets are 600,000 and 30,000 bytes respectively.
- Frontend coverage initially failed because `@vitest/coverage-v8` was absent; adding the compatible pinned provider resolved that tooling gap.

## Dependency decisions

Safe candidates are FastAPI 0.141.1, Pydantic 2.13.5, pytest 9.1.1, React/react-dom 19.2.8, React types 19.2.18, user-event 14.6.7, Tailwind 4.3.3, and Actions checkout/setup-node/setup-python/upload-artifact 7 after local verification. Held dedicated migrations are MLflow 2.22.0→3.15.2, TypeScript 6.0.3→7.0.2, jest-dom 6.9.1→7.0.1, and pytest-cov 6.1.1→7.1.0.

## Evidence boundary

This baseline does not establish preview or production deployment identity. The public URL is verified separately and read-only. Generated ML reports, locked predictions, artifacts, and `frontend/src/data/showcase_contract.json` are not edited by this maintenance work.
