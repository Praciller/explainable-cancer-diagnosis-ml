# Portfolio production-quality hardening

## Status

Approved for implementation on `chore/portfolio-production-hardening`.

## Problem and finish line

The governed ML portfolio is on `origin/main` at `5a463b12bf64678a0359b8c384dd0248a7a30e94`. The product and its evidence contracts are healthy, but dependency maintenance is fragmented across 14 open Dependabot pull requests and quality gates do not yet measure coverage, assembled accessibility, visual stability, bundle size, or supply-chain inventory in a consistent way.

The finish line is one reviewable draft PR that hardens those engineering gates, applies only verified safe dependency maintenance, records explicit major-version decisions, improves portfolio-facing documentation, and produces reproducible local/browser evidence. The PR must not merge, deploy production, alter branch protection/rulesets, retrain models, regenerate locked evidence, or change API behavior.

## Baseline and constraints

- Base: current `origin/main` SHA `5a463b12bf64678a0359b8c384dd0248a7a30e94`; re-fetch before ship and rebase if it advances.
- Open Dependabot baseline: PRs #16–#29, 14 total; each was inspected for changed files and current check state. #23 and #25 are blocked by frontend/browser failures; the others report clean checks at inventory time.
- Preserve target orientation, canonical feature order, split governance, model/artifact checksums, generated reports, `frontend/src/data/showcase_contract.json`, FastAPI request/response contracts, existing terminology, hosted read-only mode, and local FastAPI inference.
- Keep the existing aubergine/coral/sage evidence-first visual identity and named tokens. No clinical framing, color-only semantics, arbitrary design tokens, or broad formatting churn.
- Use one feature branch and one integrated draft PR with logical commits and approximately 5–8 meaningful GitHub issues if authenticated. Do not merge the PR.
- Use the real FastAPI service for primary local Playwright integration; mocks are limited to deterministic loading/failure/unusual-response states.
- Verify the production URL read-only. Preview inspection is allowed; no manual deployment or promotion.

## Dependency triage

| PR | Dependency | Current → proposed | Ecosystem | Class | Decision and reason |
|---:|---|---|---|---|---|
| 16 | actions/checkout | 6 → 7 | Actions | SAFE_CANDIDATE after CI verification | CI-only major; review action inputs and keep least-privilege permissions. |
| 17 | FastAPI | 0.139.2 → 0.141.1 | pip | SAFE_CANDIDATE | Minor runtime update; run API, backend, and real local-browser checks. |
| 18 | @testing-library/user-event | 14.6.1 → 14.6.7 | npm | SAFE_CANDIDATE | Patch test dependency; run Vitest and browser gates. |
| 19 | pytest | 9.0.3 → 9.1.1 | pip dev | SAFE_CANDIDATE | Minor test-runner update; run the complete backend suite. |
| 20 | pydantic | 2.11.5 → 2.13.5 | pip | SAFE_CANDIDATE | Minor validation dependency; API contract tests are mandatory. |
| 21 | pytest-cov | 6.1.1 → 7.1.0 | pip dev | REQUIRES_DEDICATED_MIGRATION | Major plugin transition; hold until coverage configuration and report semantics are separately verified. |
| 22 | tailwindcss | 4.3.0 → 4.3.3 | npm dev | SAFE_CANDIDATE | Patch build dependency; run lint, build, Storybook, and browser checks. |
| 23 | React and @types/react | 19.2.7/19.2.14 → 19.2.8/19.2.18 | npm | SAFE_CANDIDATE after rebase verification | Patch runtime/types update; the existing PR is blocked, so apply only after reproducing and explaining the failure. |
| 24 | MLflow | 2.22.0 → 3.15.2 | pip optional | REQUIRES_DEDICATED_MIGRATION | Optional local adapter with a major API/storage transition; do not change governed training or tracking behavior here. |
| 25 | TypeScript | 6.0.3 → 7.0.2 | npm dev | REQUIRES_DEDICATED_MIGRATION | Major compiler/toolchain transition; current PR is blocked. Hold for a dedicated compatibility branch. |
| 26 | @testing-library/jest-dom | 6.9.1 → 7.0.1 | npm dev | REQUIRES_DEDICATED_MIGRATION | Major matcher/test-environment transition; hold pending focused migration and compatibility evidence. |
| 27 | actions/upload-artifact | 4 → 7 | Actions | SAFE_CANDIDATE after CI verification | CI-only major; inspect retention/hidden-file behavior and verify browser artifacts remain available. |
| 28 | actions/setup-node | 6 → 7 | Actions | SAFE_CANDIDATE after CI verification | CI-only major; verify Node selection and npm lockfile installation. |
| 29 | actions/setup-python | 6 → 7 | Actions | SAFE_CANDIDATE after CI verification | CI-only major; verify Python selection and pip install. |

The exact final set is determined by fresh branch verification. A failed or security-sensitive update is held and recorded, not forced through by suppressing checks. Dependabot grouping will reduce routine PR noise while preserving separate security visibility and never grouping the four dedicated migrations with routine updates.

## Architecture and quality-gate design

The repository remains a Python ML package plus FastAPI adapter and React/Vite evidence dashboard. This work adds governance around those existing boundaries:

1. Dependency policy groups routine npm, pip, and Actions maintenance; major MLflow and TypeScript transitions remain explicit standalone decisions.
2. Backend coverage is measured first. A threshold is introduced only if it is justified by the baseline and protects critical modules without pretending to measure model quality. Frontend coverage is optional unless the existing Vitest environment supports a useful, stable report without a new disproportionate dependency.
3. Playwright gains assembled axe checks for major routes/states if the maintained integration is compatible. The gate fails only actionable serious/critical findings after false-positive inspection. Results are called accessibility checks, not WCAG conformance.
4. Visual regression is added only if stable in CI with a small, high-value surface set. Otherwise the PR documents `PARTIAL` coverage and retains screenshot/browser evidence without brittle pixel baselines.
5. Bundle size is baselined from the production build. A budget is enforced only where measured output is stable and the limit is recorded from evidence; lazy loading remains intact.
6. Supply-chain evidence includes lockfile integrity, npm high-severity audit, CodeQL, least-privilege Actions, `persist-credentials: false` where applicable, pinned or repository-compatible action references, and an SBOM/inventory artifact. Unsupported enterprise-only controls are reported as unavailable rather than simulated.
7. Model/Data card and README changes link to authoritative repository evidence and preserve the distinction between static hosted evidence and local inference.
8. A clean-clone rehearsal uses a temporary bounded worktree/directory and never overwrites locked artifacts or the working checkout.

## Pressure-test findings resolved

- One integrated PR is retained for coherent review; implementation issues provide traceability without splitting independent major migrations into unsafe mixed changes.
- Real FastAPI is the primary local browser contract; route mocks remain edge-state tools only.
- GitHub issues are created only if authenticated and permissioned; no issue or PR claims success when GitHub is unavailable.
- Production verification is read-only; a natural preview may be inspected, but production deployment remains owner-gated.
- “Production-quality” is defined as measured gates and explicit limitations, not arbitrary 100% coverage, full WCAG claims, universal visual snapshots, or an empty Dependabot queue.
- Generated ML evidence is a protected input to verification, never a maintenance output.

## Acceptance criteria

1. Given a fresh fetch, when the branch is compared with `origin/main`, then the base SHA and any rebase are reported accurately.
2. Given the 14 Dependabot PRs, when triage is reviewed, then every PR has a class, reason, and explicit safe/hold/dedicated decision; no PR is blindly merged or closed.
3. Given routine maintenance, when CI runs, then backend, frontend, browser, packaging, CodeQL, audit, coverage, accessibility, bundle, and supported SBOM gates are reproducible with required check names preserved.
4. Given a model or artifact contract, when the complete verification runs, then target orientation, feature order, split, checksums, generated reports, showcase contract, FastAPI schema, terminology, and hosted-read-only behavior are unchanged.
5. Given the local browser flow, when FastAPI is running against repository-generated artifacts, then a sample produces the existing model output, malignant-class score wording, disclaimer, and no clinical implication at desktop and mobile sizes.
6. Given the hosted production URL, when it is inspected read-only, then the evidence pages load, navigation/keyboard behavior works, and no hosted inference or deployment mutation is claimed.
7. Given the draft PR, when a reviewer reads it, then scope, Given/When/Then acceptance, exact commands, evidence paths, dependency decisions, known limitations, rollback, ML impact, security impact, and deployment boundary are present.

## Explicit non-goals

No model retraining, data/split/metric change, artifact/showcase regeneration, API contract change, persistent hosted inference, production deployment, main protection/ruleset change, force push, self-merge, secret addition, or forced major migration.

## Evidence and status vocabulary

Every final field uses `PASS`, `FAIL`, `BLOCKED`, `PARTIAL`, `NOT_APPLICABLE`, or `UNVERIFIED` where applicable. Local, seeded, preview, and production evidence are reported separately. No completion claim is made without fresh command output and browser-visible evidence.
