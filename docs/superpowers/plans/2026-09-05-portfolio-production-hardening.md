# Portfolio production-quality hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Harden dependency maintenance, quality evidence, supply-chain controls, and portfolio documentation around the existing governed ML/FastAPI/React system without changing its ML, artifact, API, terminology, accessibility, or hosted read-only contracts.

**Architecture:** Keep the Python pipeline, optional MLflow adapter, FastAPI schemas, generated evidence, React/Vite page composition, lazy loading, and hosted/local runtime boundary unchanged. Add measured CI gates and governance docs around those surfaces. Apply only verified safe dependency updates; record and hold dedicated major migrations.

**Tech Stack:** Python 3.10+, pytest/Ruff, FastAPI, React/Vite, TypeScript 6 baseline, Vitest, Storybook, Playwright, GitHub Actions, CodeQL, Dependabot, npm/pip lockfiles, and Docker Compose.

**Spec:** `docs/superpowers/specs/2026-09-05-portfolio-production-hardening.md`

## Global constraints

- Re-fetch `origin` before branch creation and before ship; rebase if `origin/main` advances.
- Never edit or regenerate `reports/`, locked predictions, model artifacts, or `frontend/src/data/showcase_contract.json`.
- Preserve target orientation, canonical features, split governance, FastAPI contracts, terminology, accessibility behavior, lazy loading, and hosted read-only mode.
- Use the real FastAPI service for the primary local Playwright path; mocks only for deterministic edge states.
- Do not merge or manually deploy production; push only the feature branch and create a draft PR.
- Do not enable main branch protection/rulesets or change required check names.
- Use TDD for behavior changes: write a failing focused test, implement the smallest change, then refactor and run the relevant gate.

## Task 1: Baseline evidence and dependency decision record

**Files:** Create `docs/verification/2026-09-05-portfolio-production-hardening-baseline.md`; modify only if needed after inventory.

- [ ] Capture current branch/base SHA, manifests, runtime versions, workflow permissions/check names, open Dependabot PRs/checks, main protection/ruleset read-only state, and production URL state.
- [ ] Measure backend coverage and frontend coverage capability without changing thresholds or generated evidence.
- [ ] Record bundle sizes from the current production build and whether stable visual snapshots are feasible in CI.
- [ ] Record MLflow, TypeScript, jest-dom, pytest-cov, and Actions major-version findings with links to PR diffs and official current documentation.

**Acceptance criteria:**

- Given the repository is clean, when the baseline commands run, then the baseline SHA and all observed statuses are recorded without modifying governed evidence.
- Given open Dependabot PRs #16–#29, when the inventory is compared to GitHub, then all 14 are accounted for with current checks and a safe/hold/dedicated classification.

## Task 2: Dependabot grouping and safe dependency maintenance

**Files:** Modify `.github/dependabot.yml`, `requirements.txt`, `requirements-dev.txt`, `requirements-mlflow.txt`, `frontend/package.json`, `frontend/package-lock.json`, `.github/workflows/ci.yml`, `.github/workflows/codeql.yml` only for verified safe updates.

- [ ] Add conservative routine groups for npm, pip, and Actions; preserve security-update visibility and exclude dedicated major migrations from groups.
- [ ] Apply safe patch/minor updates supported by fresh local tests and the existing required CI check names.
- [ ] Verify Actions 6→7 candidates individually for inputs, permissions, artifact behavior, runtime selection, and CI compatibility before applying any.
- [ ] Do not update MLflow 2→3, TypeScript 6→7, jest-dom 6→7, or pytest-cov 6→7 in this PR unless dedicated evidence proves the transition is isolated and safe; default is hold.

**Acceptance criteria:**

- Given a routine dependency update, when `npm ci`, backend install, lint/typecheck/tests/build, and packaging gates run, then they pass without evidence-contract changes.
- Given a dedicated-major dependency, when the maintenance PR is reviewed, then it is held with a named follow-up decision and no compatibility claim is implied.

## Task 3: Coverage governance

**Files:** Modify `pyproject.toml`, `requirements-dev.txt`, `.github/workflows/ci.yml`; add focused tests only if baseline exposes an unprotected critical path; optionally modify frontend test config/scripts if a useful report is already supported.

- [ ] Add backend coverage reporting for critical `src` modules and inspect the measured baseline.
- [ ] Choose a realistic threshold only from evidence; do not add a cosmetic global threshold or call it model-quality coverage.
- [ ] Decide frontend coverage as PASS, PARTIAL, or NOT_APPLICABLE based on stable tooling and report usefulness.
- [ ] Upload coverage evidence where supported without leaking secrets or committing reports.

**Acceptance criteria:**

- Given the same test corpus, when the coverage gate runs twice, then it produces a deterministic report and threshold result.
- Given ML pipeline code, when coverage is reported, then it measures code paths only and does not alter metrics, splits, artifacts, or model behavior.

## Task 4: Automated accessibility checks

**Files:** Modify `frontend/package.json`, `frontend/package-lock.json`, `frontend/playwright.config.ts`, `frontend/e2e/*.spec.ts`, `.github/workflows/ci.yml`.

- [ ] Add the maintained Playwright axe integration only if current Playwright/browser versions support it without unsafe transitive changes.
- [ ] Add route/state checks for Overview, Evaluation, Explainability, Prediction hosted read-only, local prediction result, loading, and error.
- [ ] Inspect violations; fix serious/critical issues with semantic markup or named design tokens, and document any reviewed non-actionable result.
- [ ] Keep the claim scoped to automated accessibility checks; do not claim full WCAG conformance.

**Acceptance criteria:**

- Given a major route/state, when the browser accessibility check runs, then actionable serious/critical findings fail the test and report the affected selector/rule.
- Given hosted mode, when the axe check runs, then it does not trigger inference, expose clinical terminology, or require production credentials.

## Task 5: Visual and responsive evidence

**Files:** Modify `frontend/e2e/*.spec.ts`, `frontend/playwright.config.ts`, `.github/workflows/ci.yml`, `docs/deployment.md` or verification docs as needed.

- [ ] Verify desktop, 390px mobile, and 320–334px narrow behavior for no horizontal overflow, navigation, charts, focus, disclaimers, and read-only prediction messaging.
- [ ] Add a small visual snapshot set only if screenshots are stable across CI and local Chromium; otherwise keep explicit screenshot evidence and document visual regression as PARTIAL.
- [ ] Do not add medical imagery, color-only semantics, or arbitrary CSS tokens while fixing visual findings.

**Acceptance criteria:**

- Given the hosted showcase, when it is opened at desktop/mobile/narrow widths, then body and major evidence regions remain usable without horizontal overflow.
- Given visual verification is marked PASS, when the same suite reruns in CI, then the selected snapshots are deterministic; otherwise the final report states why it remains PARTIAL.

## Task 6: Bundle baseline and performance guard

**Files:** Modify `frontend/package.json`, `.github/workflows/ci.yml`; add a small checked-in budget script/config only if measurements are stable.

- [ ] Capture production JS/CSS asset sizes after build and document the baseline.
- [ ] Set a budget with a justified tolerance only if repeated builds show stable output.
- [ ] Investigate imports/lazy loading only when the baseline identifies a material regression; preserve existing route lazy loading.

**Acceptance criteria:**

- Given a production build, when the bundle check runs, then it reports named asset sizes and fails only on an evidence-backed budget breach.
- Given route-level chunks, when bundle verification completes, then lazy-loaded pages remain split and no evidence or API files change.

## Task 7: Supply-chain and CI hardening

**Files:** Modify `.github/workflows/ci.yml`, `.github/workflows/codeql.yml`, `.github/dependabot.yml`, `docker-compose.yml`, `README.md`, and add SBOM workflow/config only where supported.

- [ ] Keep workflow permissions least-privileged and add `persist-credentials: false` to checkout steps where no git push is required.
- [ ] Use repository-compatible action pinning/versioning; do not claim immutable SHA pinning if it would break Dependabot or current policy without a recorded choice.
- [ ] Verify lockfile integrity, npm high-severity audit, CodeQL, Compose config, and Docker build/provenance boundaries.
- [ ] Produce an SBOM or dependency inventory as a CI artifact if tooling is available; report unsupported platform features as UNVERIFIED/BLOCKED rather than suppressing them.

**Acceptance criteria:**

- Given a pull request, when CI executes, then no job has write permissions beyond its documented need and audit/security failures remain actionable.
- Given an SBOM is produced, when it is inspected, then it describes the actual lockfiles/environment and contains no credentials or machine paths.

## Task 8: Portfolio UX, Model/Data card, and documentation

**Files:** Modify `README.md`, `docs/modeling_approach.md` or add a concise Model/Data card document, `docs/deployment.md`, `.github/PULL_REQUEST_TEMPLATE.md`, issue forms, and `docs/adr/0003-portfolio-production-hardening.md` if a new durable decision is needed.

- [ ] Review production-facing copy for fast answers to what the project is, engineering depth, ML workflow, evidence, explainability, deployment boundary, and next click.
- [ ] Make every Model/Data card number traceable to repository evidence; do not duplicate conflicting values.
- [ ] Document local, preview, and production verification, rollback, owner-gated deployment, and known limitations.
- [ ] Ensure PR governance asks for GWT acceptance, tests, browser evidence, ML/data impact, terminology, security, deployment, rollback, and docs.

**Acceptance criteria:**

- Given a recruiter opens the README or hosted site, when they scan the primary path, then the educational scope, engineering workflow, authoritative evidence, and read-only boundary are clear without clinical claims.
- Given a PR author fills the template, when it renders, then all required evidence and rollback fields are present.

## Task 9: Reproducibility rehearsal and full verification

**Files:** Add/update verification evidence only; no governed ML artifacts.

- [ ] Run backend format/lint/compile/test/coverage gates.
- [ ] Run frontend clean install, audit, lint, typecheck, unit tests, build, Storybook build, and bundle check.
- [ ] Start the actual FastAPI service against repository-generated artifacts and run local Playwright; run hosted Playwright against the public URL or a production-like preview separately.
- [ ] Run accessibility checks, responsive checks, packaging, CodeQL-compatible local checks, and SBOM/inventory.
- [ ] Rehearse a bounded clean clone/worktree and compare governed evidence checksums before/after.
- [ ] Perform independent diff review for ML, API, terminology, a11y, security, dependency, docs, and CI regressions.

**Acceptance criteria:**

- Given the final branch, when the complete matrix runs from a clean environment, then every applicable gate has fresh evidence or an explicit limitation status.
- Given a before/after evidence comparison, when hashes and contract tests are checked, then `GOVERNED_ML_EVIDENCE_CHANGED=NO`, `LOCKED_ARTIFACTS_CHANGED=NO`, and the API contract is unchanged.

## Task 10: GitHub draft PR and safe Dependabot cleanup

**Files:** No repository files beyond final documentation/evidence updates.

- [ ] Confirm `origin/main` again and rebase if advanced; rerun affected gates after any rebase.
- [ ] Push only `chore/portfolio-production-hardening`.
- [ ] Create one draft PR with the exact scope, triage table, commands, evidence paths, statuses, limitations, decisions, rollback, and production boundary.
- [ ] If authenticated, create the Epic plus 5–8 meaningful issues with GWT acceptance criteria.
- [ ] After the controlled PR exists and its local/CI evidence is verified, close only justified superseded routine Dependabot PRs with concise comments; leave held/dedicated-major PRs open and record their decisions.
- [ ] Do not merge, deploy production, or enable main protection/rulesets.

**Acceptance criteria:**

- Given the draft PR exists, when its checks and body are inspected, then it is draft, targets `main`, preserves required check names, and makes no merge/deployment claim.
- Given a held major Dependabot PR, when cleanup is performed, then it remains open or has an explicit owner-approved follow-up record; it is never silently closed.

## Final response evidence fields

Return the exact requested fields from the user, including base/head SHA, branch, PR, Dependabot counts, dependency decisions, all test/gate statuses, unchanged ML/artifact/API fields, preview/production URLs, blockers, limitations, recommended next step, exact commands, issue/PR links, and screenshot/evidence paths. Use `COMPLETE_WITH_LIMITATIONS` when applicable gates are intentionally partial; use `BLOCKED` when a safe required action cannot proceed.
