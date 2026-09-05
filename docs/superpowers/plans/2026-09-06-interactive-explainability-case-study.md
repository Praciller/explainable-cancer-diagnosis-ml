# Interactive Explainability Case Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic, keyboard-accessible Explainability case study for governed dataset row 102 while preserving ML, API, hosted-read-only, terminology, accessibility, and visual-evidence contracts.

**Architecture:** Generate one static JSON artifact from the existing logistic-regression artifact, seed-42 split, feature order, target contract, and `_shap_values` orientation. Import it into a focused React component with local expansion/selection state; retain the existing static figures. Prove the calculation in Python, UI in Vitest/Storybook, and hosted behavior in Playwright.

**Tech Stack:** Existing Python ML/SHAP stack; React 19, TypeScript 6.0.3, Vite 8.0.16, Vitest 4.1.11, Storybook 10.6.0, Playwright 1.63.0, Testing Library, existing CSS tokens and UI primitives.

**Spec:** `docs/superpowers/specs/2026-09-06-interactive-explainability-case-study.md`

## Global Constraints

- Base `origin/main=0467ffabcff8d2c17de38e3a4fbaa1abaee64c1`; branch `feat/interactive-explainability-case-study`.
- Fixed row `102`, selected model `logistic_regression`, malignant raw target `0`, benign raw target `1`, seed `42`, locked test split, threshold `0.5`, calibration `uncalibrated`.
- Preserve `src/api`, API schemas, `src/contracts.py`, locked predictions, comparison/error evidence, existing SHAP figures, and `frontend/src/data/showcase_contract.json`.
- No retraining, recalibration, retuning, dependency changes, held migrations, production deployment, branch-ruleset change, or Dependabot #45/#46 mutation.
- Hosted mode remains static/read-only and the new UI makes no API request. Use existing terminology and named DESIGN.md tokens; no clinical claims or color-only meaning.

## File map

- Create `src/explainability/case_study.py`: deterministic artifact generator and CLI `python -m src.explainability.case_study`.
- Create `frontend/src/data/explainability_case.json` only through that generator.
- Create `tests/test_explainability_case_study.py`: provenance and numerical reconstruction tests.
- Create `frontend/src/types/explainability.ts`, `frontend/src/components/ExplainabilityCaseStudy.tsx`, its test and Storybook story.
- Modify `frontend/src/pages/ExplainabilityPage.tsx`, `frontend/src/styles.css`, `frontend/e2e/showcase.spec.ts`, `frontend/e2e/accessibility.spec.ts`, `README.md`, and `docs/deployment.md`.
- Create `docs/verification/2026-09-06-interactive-explainability-case-study.md` after all evidence exists.

## Artifact interface

`CaseStudyArtifact` has `schema_version: 1`, `dataset_row_id`, `raw_target`,
`known_label`, `model_name`, `model_version`, `positive_class`, `output_space`,
`threshold`, `calibration_status`, `feature_order`, `feature_count`,
`base_value`, `contribution_sum`, `reconstructed_log_odds`, `model_score`,
`reconstruction_error`, `reconstruction_tolerance`, `contributions`,
`global_explanation`, `local_explanation`, and `educational_limitation`.
Each contribution has `rank`, `feature`, `value`, `contribution`,
`absolute_contribution`, and direction `toward_malignant`, `away_from_malignant`,
or `neutral`. Sort by descending absolute contribution and feature-order index.

---

### Task 1: Generate and verify the governed case artifact

**Files:** `src/explainability/case_study.py`, `tests/test_explainability_case_study.py`, generated `frontend/src/data/explainability_case.json`, `docs/deployment.md`.

**Interfaces:** `generate_case_study_artifact(output_path: Path = PROJECT_ROOT / "frontend" / "src" / "data" / "explainability_case.json") -> dict[str, Any]`; CLI has no required arguments.

- [ ] Write a failing Python test that reads the artifact, asserts row 102 is in `X_test`, raw target 1/label benign, logistic-regression selection, manifest model version, malignant positive class, `malignant_class_log_odds`, threshold/calibration, exact feature order/count, 30 finite contributions, sign-derived directions, and no NaN/Inf.
- [ ] Assert `reconstructed_log_odds == base_value + contribution_sum` and `sigmoid(reconstructed_log_odds) == score_for_raw_target(model.classes_, model.predict_proba(row), 0)` with `atol=1e-9`; assert there is no hand-authored `model_score_logit` field.
- [ ] Run `pytest tests/test_explainability_case_study.py -q`; expected red failure is missing generated JSON, not a test setup error.
- [ ] Implement the generator using `load_dataset_frame`, `split_dataset(seed=42)`, the existing model/manifest, training background `X_train.sample(min(100, len(X_train)), random_state=42)`, `_shap_values`, and `score_for_raw_target`; raise explicit errors for wrong model, split, feature count, non-finite data, or mismatch.
- [ ] Serialize UTF-8, two-space JSON with a terminal newline and write no existing ML/report artifact. Run `python -m src.explainability.case_study` and the focused test; expected green values match the spec reference.
- [ ] Document the generator and static hosted boundary, run `git diff --check`, then commit `feat(explainability): add governed case-study artifact`.

**Acceptance:** Given current governed artifacts, when the generator runs, then row 102 has 30 ordered finite contributions and malignant score reconstruction within `1e-9`; existing artifact bytes remain unchanged.

---

### Task 2: Implement the typed interactive component

**Files:** `frontend/src/types/explainability.ts`, `frontend/src/components/ExplainabilityCaseStudy.tsx`, `frontend/src/components/ExplainabilityCaseStudy.test.tsx`, `frontend/src/pages/ExplainabilityPage.tsx`, `frontend/src/styles.css`.

**Interfaces:** `ExplainabilityCaseStudy({ artifact }: { artifact: CaseStudyArtifact })`; local `expanded` and `selectedFeature` state only; no service/API import.

- [ ] Write failing Testing Library tests using the real JSON: summary row/model/version/score/threshold/classification/calibration, visible reconstruction, limitation, global/local copy, eight default native contribution buttons, expansion to 30 with `aria-expanded`, keyboard selection of `worst texture`, selected detail, and forbidden-term absence.
- [ ] Run `Set-Location frontend; npm test -- ExplainabilityCaseStudy.test.tsx; Set-Location ..`; expected red failure is missing component/type.
- [ ] Define exact TypeScript interfaces matching the artifact. Render semantic summary metrics, text-only reconstruction, native `Show all 30 contributions` button, full-width native contribution buttons, and selected-detail region with value, signed contribution, direction, and non-causal explanation. Display scores to 3 decimals, contributions to 3, log-odds to 4.
- [ ] Import JSON and render before the existing figure grid without removing/reordering the global importance, SHAP summary, waterfall, or threshold figures.
- [ ] Add only token-based styles: `min-width: 0`, wrapping/640px stacking, 44px controls, wrapped feature names, visible selected/focus states, no fixed viewport children, and existing reduced-motion behavior.
- [ ] Run focused tests, `npm run lint`, and `npm run typecheck`; then commit `feat(frontend): add interactive explainability case study`.

**Acceptance:** Given no FastAPI service, when the component renders, then all data comes from static JSON; default/expanded states expose 8/30 keyboard-operable contributions; Enter/Space selection exposes non-color-only detail.

---

### Task 3: Add deterministic Storybook state coverage

**Files:** `frontend/src/components/ExplainabilityCaseStudy.stories.tsx`, `frontend/src/components/ExplainabilityCaseStudy.test.tsx`.

- [ ] Add state assertions for `Default`, `FeatureSelected`, `AllContributions`, and `Mobile` using the same generated fixture; run the focused test and verify the new assertions fail for the absent story/state representation.
- [ ] Implement stories with no network calls or new dependencies; use Storybook `play` to select a feature and expand all contributions, and a supported mobile viewport parameter.
- [ ] Run `Set-Location frontend; npm run build-storybook; npm test; Set-Location ..`; expected both green and `storybook-static/` ignored.
- [ ] Commit `test(frontend): add explainability case-study stories`.

**Acceptance:** Given Storybook has no FastAPI, when each story loads, then the deterministic artifact renders its named state; existing static Explainability figures remain present.

---

### Task 4: Add hosted/local browser proof and preview screenshots

**Files:** `frontend/e2e/showcase.spec.ts`, `frontend/e2e/accessibility.spec.ts`, `frontend/e2e/local-prediction.spec.ts` only for a regression assertion; ignored evidence screenshots `explainability-case-desktop.png`, `explainability-case-mobile-390.png`, `explainability-case-mobile-332.png`, `explainability-case-feature-selected.png`.

- [ ] Write failing hosted assertions for navigation, row 102/model/score/reconstruction, expansion to 30, keyboard selection, absence of localhost API requests, no console errors, and `document.documentElement.scrollWidth <= window.innerWidth`.
- [ ] Run `Set-Location frontend; npm run e2e:hosted -- showcase.spec.ts; Set-Location ..`; expected red failure is the missing case-study locator.
- [ ] Parameterize hosted Explainability checks at 1440x1000, 1024x900, 640x900, 390x844, and 332x800. Extend axe coverage to all five widths and expect zero serious/critical violations. Keep local success backed by real FastAPI and do not mock success.
- [ ] Run `npm run e2e:hosted`, generate local artifacts, start FastAPI on `127.0.0.1:8000`, run `npm run e2e:local`, then stop only the temporary API. Expected hosted and real local flows green.
- [ ] Commit `test(browser): verify interactive explainability case study`.
- [ ] After push creates the Vercel Git-integration Preview, inspect that Preview in real Chromium at all exact widths, capture the four named screenshots, and record Preview URL/source SHA. Do not use local/production screenshots or manually deploy.

**Acceptance:** Given hosted mode has no API URL, when Explainability is visited, then the case study works without FastAPI or inference requests; at all required widths expansion/selection has no overflow and axe severe/critical is zero; local prediction remains unchanged.

---

### Task 5: Complete gates, evidence, and Draft PR

**Files:** `README.md`, `docs/verification/2026-09-06-interactive-explainability-case-study.md`.

- [ ] Add one recruiter-facing line: `The Explainability page includes an interactive row-102 case study that reconstructs a malignant-class model score from its governed SHAP contributions.` Run `git diff --check` and terminology review.
- [ ] Compare `origin/main...HEAD` for locked predictions, showcase contract, model comparison, error analysis, explainability summary, API/source surfaces, dependency files, and deployment/ruleset files; record unchanged hashes and exact diff paths.
- [ ] Run backend format/lint/compile/pytest, `docker compose config --quiet`, frontend `npm ci`, high-severity audit, lint, typecheck, coverage tests, build, bundle check, Storybook build, hosted E2E, and real-FastAPI local E2E. Record exit codes and counts.
- [ ] Review the full diff for API imports, held migrations, forbidden clinical copy, generated locked-file changes, and production mutations; run the installed narrow security-diff review and resolve only confirmed findings.
- [ ] Write the evidence report with baseline/head SHAs, artifact numerical values, UI/browser/axe/overflow/console results, screenshot paths, Preview URL/source SHA, commands, limitations, Dependabot #45/#46 untouched status, and owner-review state. Separate local, Preview, and production evidence.
- [ ] Commit `docs: document explainability case-study verification`, push only `feat/interactive-explainability-case-study`, and verify clean status.
- [ ] Run `gh auth status`; create one Draft PR against `main` titled `feat: add interactive explainability case study`, using the evidence report as body. Verify current head/base and checks with `gh pr checks <number> --watch` and `gh pr view <number> --json headRefOid,baseRefName,isDraft,statusCheckRollup,url`.

**Acceptance:** Given the clean feature branch, all applicable local/CI/browser/security gates pass; given the Draft PR, it targets `main`, Preview matches the feature head, and production remains untouched. Never mark ready, merge, deploy production, or change rulesets.

## Plan self-review

- [ ] Every spec requirement maps to Tasks 1–5.
- [ ] TDD red steps precede each production implementation task.
- [ ] Generated artifact uses existing ML semantics and is not hand-authored.
- [ ] Existing ML/API/terminology/accessibility/visual contracts and held migrations are protected.
- [ ] Exact 1440px, 1024px, 640px, 390px, and 332px browser checks plus Storybook, audit, bundle, and CI evidence are covered.
