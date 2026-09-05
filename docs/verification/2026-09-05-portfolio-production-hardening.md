# Portfolio production hardening verification

## Classification

`COMPLETE_WITH_LIMITATIONS` for the draft PR stage. The implementation and all applicable local/PR gates passed. The PR is intentionally unmerged; production deployment, main branch protection, and four dedicated major migrations remain owner-gated follow-up work.

## Repository and GitHub state

- Base: `origin/main` `5a463b12bf64678a0359b8c384dd0248a7a30e94`
- Branch: `chore/portfolio-production-hardening`
- Draft PR: [#37](https://github.com/Praciller/explainable-cancer-diagnosis-ml/pull/37)
- Issues: [Epic #30](https://github.com/Praciller/explainable-cancer-diagnosis-ml/issues/30), child issues [#31](https://github.com/Praciller/explainable-cancer-diagnosis-ml/issues/31)–[#36](https://github.com/Praciller/explainable-cancer-diagnosis-ml/issues/36)
- Dependabot: 14 open before; 4 open after (#21, #24, #25, #26); 10 routine/safe PRs closed as superseded after PR #37 checks passed.
- PR checks: 13 successful, 0 failing, 0 pending, including push and pull-request CI, CodeQL Python/JavaScript, Vercel preview, and preview comments.

## Gate evidence

| Gate | Result | Evidence |
|---|---|---|
| Backend format/lint | PASS | `ruff format --check src tests`; `ruff check src tests` |
| Backend tests | PASS | 34 tests |
| Critical backend coverage | PASS | 91.29%, threshold 90%, `src/api` + `src/artifacts` |
| Compile | PASS | `python -m compileall -q src tests` |
| Frontend install/audit | PASS | clean `npm ci`; 391 audited; 0 vulnerabilities |
| Frontend lint/typecheck | PASS | `npm run lint`; `npm run typecheck` |
| Frontend tests/coverage | PASS | 12 tests; 94.11% statements on exercised modules; no global threshold |
| Production build/bundle | PASS | 537,531 JS bytes / 17,646 CSS bytes under 600,000 / 30,000 |
| Storybook | PASS | `npm run build-storybook` |
| Hosted browser | PASS | Playwright desktop/mobile: 6 passed; hosted navigation/read-only/keyboard checks |
| Local browser | PASS | Playwright desktop/mobile: 4 passed against real FastAPI; sample prediction/disclaimer verified |
| Automated accessibility | PASS | axe serious/critical checks on major hosted routes; contrast finding fixed and rerun |
| Packaging | PASS | `docker compose config --quiet` |
| CodeQL | PASS | PR Python and JavaScript/TypeScript analyses |
| SBOM/inventory | PASS in CI design | npm CycloneDX and Python package inventory artifacts wired; not committed |
| Python pip-audit | UNVERIFIED | command unavailable locally; not represented as a passing gate |
| Pixel visual regression | PARTIAL | stable browser screenshots/evidence; no brittle pixel baseline added |

## Contract review

`GOVERNED_ML_EVIDENCE_CHANGED=NO`, `LOCKED_ARTIFACTS_CHANGED=NO`, and `API_CONTRACT_CHANGED=NO`. The diff contains no `reports/`, model, API, feature, contract, or showcase-contract paths. Before/after hashes for locked predictions, the showcase contract, reports, and explainability summary were unchanged after the local artifact-generation rehearsal.

## Browser and deployment boundary

- Local screenshots/reports are under ignored `frontend/test-results/` and `frontend/playwright-report/`.
- The production URL [explainable-cancer-diagnosis-ml.vercel.app](https://explainable-cancer-diagnosis-ml.vercel.app/) was inspected read-only in Chrome. Overview, Evaluation, Explainability, Prediction, disclaimer, metrics, charts, and hosted local-inference messaging rendered.
- `PRODUCTION_MANUALLY_DEPLOYED=NO`; the PR’s natural Vercel preview check passed. No promotion, production setting, main protection/ruleset, or secret was changed.

## Major-version decisions

- MLflow 2→3: HOLD; optional local adapter and major API/storage transition need a dedicated migration.
- TypeScript 6→7: HOLD; dedicated compiler/toolchain compatibility work required.
- jest-dom 6→7: HOLD; dedicated matcher/test-environment compatibility work required.
- pytest-cov 6→7: HOLD; dedicated coverage configuration/report semantics work required.
- GitHub Actions 6/4→7: APPLIED after individual CI verification; checkout credential persistence is disabled.
