# Interactive Explainability Case Study

**Status:** Approved for implementation

**Date:** 2026-09-06

**Baseline:** `origin/main` at `0467ffabcff8d2c17de38e3a4fbaa1abaee64c1a`

## Problem

The Explainability page currently presents global importance, a SHAP summary,
one static waterfall image, and threshold analysis. Those artifacts establish
the explanation contract but do not let a recruiter or learner inspect one
complete model output, see how the score is reconstructed, or select a feature
to read its value and directional contribution. Add one deterministic,
portfolio-facing case study that makes the existing explanation evidence
inspectable without changing model behavior or exposing hosted inference.

## Goal

Supplement the Explainability page with a keyboard-accessible interactive case
study for governed dataset row `102` and selected model `logistic_regression`.
The case study must show the model output, its malignant-class log-odds
reconstruction, the complete local contribution set, and the distinction
between global and local explanation while preserving the existing static
figures and all repository contracts.

## Non-goals

- Do not retrain, recalibrate, retune, or replace any model.
- Do not change the dataset, target orientation, feature order, split
  assignment, threshold, calibration status, locked predictions, comparison
  metrics, error analysis, or existing SHAP figures.
- Do not change FastAPI routes, request schemas, response schemas, or API
  terminology.
- Do not expose live inference or add an inference endpoint to hosted Vercel.
- Do not upgrade or add npm/Python dependencies.
- Do not start held major migrations: MLflow `3`, TypeScript `7`, jest-dom `7`,
  or pytest-cov `7`.
- Do not enable branch protection/rulesets, deploy production manually, merge
  the feature PR, or modify Dependabot PR `#45` or `#46`.
- Do not replace the existing visual identity with medical imagery, gradients,
  color-only class meaning, or a generic dashboard pattern.

## Governed explanation contract

The derived case artifact is generated from the repository's existing model and
explainability semantics. It is not a new source of ML truth.

| Field | Required value or rule |
| --- | --- |
| Dataset row | `102` from `load_breast_cancer(as_frame=True)` |
| Row split | Locked test split under seed `42` |
| Raw target | `1` |
| Known label | `benign` |
| Selected model | `logistic_regression` |
| Model version | Read from the current artifact manifest; expected baseline value `bbb5977c47501cd9a962` |
| Feature count | `30` |
| Feature order | Exact `bundle.feature_names` order, unchanged |
| SHAP orientation | Existing `_shap_values` malignant-class orientation |
| Positive class | `malignant`, raw target `0` |
| Output space | `malignant_class_log_odds` for base value and contributions |
| Threshold | Existing governed threshold `0.5` |
| Calibration | Existing status `uncalibrated` |
| Score | Existing malignant-class probability selected by `score_for_raw_target` |
| Classification | Existing threshold rule: score `>= 0.5` is `malignant`, otherwise `benign` |

The expected reference calculation at the approved baseline is:

```text
base_value                         = -0.5770589234377406
contribution_count                 = 30
contribution_sum                   = -4.199147683081785
reconstructed_log_odds             = -4.776206606519525
malignant_class_model_score        = 0.008357472762137497
sigmoid(reconstructed_log_odds)    = 0.008357472762137474
```

The generator must calculate these values rather than embed them as hand-authored
constants. The provenance test must verify finite values, exact feature order,
30 contributions, `base + sum(contributions)` reconstruction, sigmoid-to-score
agreement, selected model/version, positive class, threshold, calibration, row
membership, and raw target. The test must use a tolerance no looser than
`1e-9` for the reconstruction and score comparisons unless the actual numeric
implementation requires a narrower documented tolerance.

## Derived artifact

Create `frontend/src/data/explainability_case.json` as a generated,
presentation-ready artifact. Add a documented generator entry point that loads
the existing model, manifest, dataset, and split definitions, then writes the
artifact deterministically. The generator may reuse `_shap_values`,
`score_for_raw_target`, and the model's existing prediction methods; it must not
change their semantics.

The artifact must include:

- `schema_version`.
- `dataset_row_id`, `raw_target`, and `known_label`.
- `model_name`, `model_version`, `positive_class`, `output_space`, `threshold`,
  and `calibration_status`.
- `feature_order` and `feature_count`.
- `base_value`, `contribution_sum`, `reconstructed_log_odds`, `model_score`,
  `reconstruction_error`, and `reconstruction_tolerance`.
- All 30 contributions, each containing feature name, exact row value,
  malignant-class log-odds contribution, absolute contribution, and a
  sign-consistent human-readable direction label.
- A deterministic ranking by absolute contribution for the default top eight
  view.
- Existing educational limitation text and explicit global/local explanation
  notes.

The artifact is derived evidence and must be regenerated through the documented
command. It must not be edited manually to satisfy a test. Existing locked
artifacts and `showcase_contract.json` remain byte-for-byte unchanged.

## UI behavior

Add a focused domain component, preferably
`frontend/src/components/ExplainabilityCaseStudy.tsx`, and render it from the
existing Explainability page before or alongside the current figures. Keep the
static SHAP waterfall, summary, global importance, and threshold figures.

The case study must provide:

1. A concise summary identifying row `102`, selected model, artifact version,
   malignant-class score, fixed threshold, resulting model classification, and
   uncalibrated status. Use “model output”, “model score”, and “dataset row”;
   never clinical claims.
2. A visible reconstruction line equivalent to
   `base value + all local contributions = malignant-class log-odds`, plus the
   sigmoid-derived score and the existing threshold comparison. Values must use
   bounded, readable precision.
3. A contribution list/table showing the top eight by absolute contribution by
   default and a 44px-or-larger native button labeled `Show all 30
   contributions`. The expanded state must expose all 30 contributions without
   horizontal page overflow.
4. Selectable contribution rows implemented with actual keyboard-operable
   buttons. The selected feature detail must expose the feature name, exact
   dataset-row value, signed contribution, direction label, and an explanation
   that direction is model behavior rather than causality. Selection must work
   with mouse and keyboard and remain visible at mobile widths.
5. A global-versus-local explanation section: global importance summarizes
   recurring model behavior across governed rows; local contributions describe
   this one supplied row. State that correlated measurements can share or
   redistribute importance and that contributions do not prove biological
   causality.
6. A visible educational limitation using the repository's existing limitation
   language. The case study must not use diagnosis, risk, confidence, clinical
   probability, screening, treatment, medical advice, or clinical-decision
   support language.

Use existing UI primitives and named DESIGN.md tokens. Use semantic headings,
table/list structure as appropriate, visible focus, `aria-expanded`, a selected
state that is not color-only, textual alternatives for any visual encoding, and
reduced-motion behavior. The component must be statically driven in hosted mode
and must make no fetch or API request.

## Testing and verification

### Backend/provenance

- Add a focused Python test for the generated case artifact and its model/data
  provenance.
- Verify the current backend/API contract tests still pass without source or
  schema changes.
- Verify no governed ML evidence, locked artifact hash, or showcase-contract
  hash changes.

### Frontend

- Add component tests for summary fields, reconstruction math, top-eight default,
  `Show all 30 contributions`, keyboard feature selection, selected detail, and
  global/local copy.
- Add Storybook stories for default, selected-feature, expanded-all, and mobile
  states where the current Storybook setup supports viewport parameters.
- Keep frontend lint, typecheck, unit test, production build, Storybook build,
  and bundle-budget checks green.

### Browser

- Extend Playwright hosted coverage to assert the case study is visible without
  FastAPI, has the expected row/model/score semantics, expands to all 30, and
  supports keyboard selection.
- Verify exact viewports `1440px`, `390px`, and `332px` (the required narrow
  mobile width between 320px and 334px).
- Run serious/critical axe checks with zero violations at each required width,
  check the skip link/navigation active state, no horizontal overflow, and no
  material console errors.
- Keep the existing real-FastAPI local E2E success path unchanged.
- Capture clean PR-preview screenshots at the named widths after the preview
  deployment is available. Do not use a local or production screenshot as
  preview evidence.

### Deployment and review

- Push only `feat/interactive-explainability-case-study`.
- Create a Draft PR titled `feat: add interactive explainability case study`
  against `main`.
- Verify the Vercel Preview generated by Git integration in a real Chromium
  browser. Do not trigger or promote production.
- Do not mark production complete; production remains owner-gated and
  unchanged.

## Acceptance criteria

- Given the repository is at the approved baseline and the documented generator
  runs, when the case artifact is produced, then it contains row 102, the
  selected logistic-regression model, all 30 ordered finite contributions, and
  a reconstruction matching the model score within the documented tolerance.
- Given a reader opens the hosted Explainability page without FastAPI, when the
  page loads, then the interactive case study renders entirely from the checked-
  in derived artifact and no inference request is made.
- Given the case study is in its default state, when the reader inspects it,
  then the row/model/score/threshold/calibration summary and visible
  reconstruction are understandable without selecting a feature.
- Given the reader activates `Show all 30 contributions`, when the expanded
  list renders, then all 30 feature contributions are present and the page has
  no horizontal overflow at 1440px, 390px, or 332px.
- Given the reader selects a contribution row with mouse or keyboard, when the
  selection changes, then the selected feature's value, signed contribution,
  direction, and non-causal explanation are visible and announced by structure
  rather than color alone.
- Given the reader compares global and local explanation text, when they read
  the case study, then the difference between recurring global importance and
  this-row local contribution is explicit, including correlation limitations.
- Given the existing Explainability figures and Prediction page are rendered,
  when the feature branch is tested, then those artifacts, hosted read-only
  behavior, API schemas, terminology, accessibility contracts, and local real
  inference flow remain unchanged.
- Given CI and the PR preview are available, when lint, typecheck, unit,
  backend, packaging, Storybook, Playwright, accessibility, security, and
  bundle gates run, then they pass without dependency migration or governed
  evidence mutation.

## Rollback

Revert the feature branch/PR commits. The rollback removes the derived case
artifact, generator, component, tests, and documentation while leaving the
existing ML artifacts, API, showcase contract, and production deployment
unchanged.
