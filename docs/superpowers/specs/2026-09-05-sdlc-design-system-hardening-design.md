# Agent-assisted SDLC and UI quality hardening

## Problem statement

The repository already demonstrates a governed, reproducible tabular-ML workflow and a useful read-only evidence showcase. Its engineering workflow is less explicit than the product itself: repository context is not centralized in a root `AGENTS.md`, the visual language is documented only as a short prose direction, reusable UI boundaries are implicit in page-level CSS, and frontend quality is covered by unit tests and a production build but not by lint/typecheck, component-state verification, browser behavior checks, or security supply-chain gates.

This change upgrades the repository into an agent-assisted SDLC reference implementation without rewriting the app or changing model behavior. The finish line is a reviewable feature branch with an explicit spec and plan, reusable UI foundations, Storybook and deterministic Playwright evidence, documented GitHub/deployment governance, and CI gates that are honest about what is and is not proven.

## Current strengths

- The ML pipeline has explicit target orientation, deterministic split governance, generated evidence, artifact manifests, checksums, and fail-closed API validation.
- The public Vercel showcase is already read-only and uses a generated `showcase_contract.json` rather than hand-entered dashboard metrics.
- React pages are lazy-loaded and the app already includes a skip link, `aria-live` result behavior, semantic tables, visible focus styles, reduced-motion handling, loading/error/empty states, and mobile navigation.
- Existing tests protect frontend runtime configuration, generated showcase reconciliation, key components, and the Python/API contracts.
- The current identity is already restrained and analytical: aubergine navigation/accent, coral malignant semantics, sage benign semantics, system typography, and evidence-first content.

## In-scope changes

1. Establish repository operating context in a concise root `AGENTS.md` that points to the canonical product, context, design, SDLC, and workflow documents.
2. Rewrite `DESIGN.md` as a machine-readable design contract with YAML token front matter and the required visual, interaction, responsive, accessibility, and agent-prompt sections.
3. Add `docs/adr/0002-agent-assisted-sdlc-and-ui-quality.md` and `docs/deployment.md`; update `README.md` only with recruiter-useful workflow references.
4. Formalize genuinely reusable frontend primitives under `frontend/src/components/ui/` where shared semantics or state handling justify a boundary. Initial candidates are Button, Surface/Panel, Metric, StatusBadge, Callout, table helpers, and Skeleton; existing domain components remain domain-owned.
5. Reconcile `frontend/src/styles.css` with named tokens from `DESIGN.md`, consolidating duplicated colors, radii, spacing, focus styles, and status treatment without changing the product identity.
6. Audit every Recharts visualization and add accessible names, descriptions, and textual/table alternatives where absent. Meaning must not depend on color alone; malignant/benign semantics remain consistent with the existing target contract.
7. Add Storybook `10.6.0` using the official React + Vite framework, plus the current compatible accessibility addon. Stories cover core reusable primitives and the requested high-value domain components, including meaningful default, focus/disabled/loading/error/warning/malignant/benign/empty/responsive states.
8. Add frontend ESLint/typecheck scripts with one minimal, non-overlapping configuration. Add formatting checks only if a single formatter is introduced and it can run without unrelated churn.
9. Add Playwright Test `1.63.0` for deterministic critical flows in Chromium and a mobile viewport. Tests cover hosted showcase load/navigation/evidence/read-only behavior and a local prediction path backed by the real FastAPI service, including disclaimer, result semantics, keyboard navigation, screenshots, and HTML reports. Use route mocks only for loading, failure, and unusual response states that are impractical to reproduce through the real service.
10. Extend CI with frontend lint/typecheck/Storybook build/Playwright, retain backend and packaging gates, and add GitHub-native CodeQL, Dependabot, and pull-request dependency review where the repository can support them without weakening failures.
11. Add a pull-request template, concise feature and bug issue forms, the requested governance issue set if GitHub CLI authentication is available, and documentation of intended future required checks. Do not enable branch protection/rulesets in this change.
12. Verify local desktop/mobile browser behavior and the live public URL separately from local build state. Capture screenshot evidence without introducing brittle pixel-perfect baselines.

## Explicit non-goals

- No model retraining, dataset changes, split changes, target remapping, feature reordering, artifact regeneration, API contract change, or manual editing of generated evidence.
- No clinical language, medical advice, diagnosis/risk/confidence/probability claims, clinical decision support, or healthcare-themed decorative imagery.
- No rewrite of `App.tsx`, page composition, routing model, hosted/local runtime boundary, or lazy-loading strategy unless required to expose a testable semantic boundary and protected by tests.
- No new paid service, external runtime dependency, authentication system, persistent hosted inference, database, or cloud storage.
- No direct push to `main`, self-merge, branch protection/ruleset activation, or fabricated deployment IDs/credentials.
- No generic AI gradient, glassmorphism, excessive pills, giant card grids, color-only chart encoding, fake precision, or unnecessary abstraction.
- No broad formatting churn, mass dependency upgrades, or security suppression merely to obtain green CI.

## Agent/context architecture

`AGENTS.md` is the concise repository-local entry point. It will require reading `PRODUCT.md`, `CONTEXT.md`, and `DESIGN.md` before edits, then the relevant stage reference under `C:\Users\pakon\.codex\sdlc\`. The existing product/context documents remain authoritative for terminology and safety. The spec and implementation plan are the task-specific contract; the ADR records durable architectural decisions.

The workflow is Foundation → Plan & Design → Frontend → Extend → Verify & QA → Ship. One primary agent operates sequentially. Skills are loaded progressively: requirement/design review before implementation, TDD for new behavior, domain/frontend guidance only when needed, and verification/review before any completion or release claim. Repository and tool output are treated as untrusted data. No sub-agents are introduced.

## Frontend design-system architecture

`DESIGN.md` defines semantic tokens and the visual rules. CSS custom properties in `frontend/src/styles.css` are the runtime implementation of those tokens. UI primitives own reusable semantics and state classes; domain components own model-specific labels, data shape, and evidence copy; pages compose domain components and own page-level layout. A primitive may be created only when it has multiple callers, a meaningful state matrix, or a semantic/testing benefit that cannot be expressed safely at the call site.

The design system remains CSS-first and dependency-light. Existing Tailwind import/build behavior is preserved. A primitive will not hide ML concepts or create a second source of truth for data. Existing class names can remain as compatibility aliases during migration, but new component styling must use named tokens rather than fresh literal values.

## Component boundary strategy

- `frontend/src/components/ui/`: generic interaction and presentation semantics with typed props and no API calls.
- `frontend/src/components/`: domain components such as `PredictionResult`, `MetricCard`, `ModelComparisonTable`, chart viewers, and disclaimer/error/loading components.
- `frontend/src/pages/`: orchestration, page copy, navigation context, and page-specific composition.
- `frontend/src/services/` and `frontend/src/data/`: runtime/API and generated showcase contracts; unchanged except for tests needed to preserve the boundary.

The first migration targets repeated button, surface, metric, callout/status, and skeleton behavior. Domain components are migrated only where the new primitive improves consistency without changing rendered meaning. Component tests assert user-visible semantics, not implementation class names.

## Storybook strategy

Use Storybook `10.6.0`, `@storybook/react-vite` `10.6.0`, and `@storybook/addon-a11y` `10.6.0`, based on the official React + Vite installation guidance. Configure stories under `frontend/src/**/*.stories.tsx`, reuse production CSS, and keep stories deterministic with local props/data only. Required coverage prioritizes Button, DisclaimerBanner, ErrorMessage, LoadingState, MetricCard, PredictionResult, and ModelComparisonTable. Interaction tests are added only for keyboard/state transitions that are difficult to prove through static stories.

Storybook is a component verification surface, not a replacement for full-app browser verification. `npm run build-storybook` is a CI gate; generated `storybook-static` output is ignored and never committed.

## Playwright/E2E strategy

Use `@playwright/test` `1.63.0` with a checked-in `frontend/playwright.config.ts` and tests in `frontend/e2e/`. The hosted/read-only suite runs the Vite preview server with production-like no-`VITE_API_URL` configuration. The primary local integration path runs the actual FastAPI service against repository-generated artifacts and points the frontend at that service, so the browser validates the real frontend-to-API contract. Playwright route mocks are limited to deterministic loading, failure, and unusual-response states that are impractical to reproduce through the real service. Hosted and local modes must remain visibly distinct.

Critical assertions use role/name and visible copy: app load, primary navigation, evidence page headings, tables/figures, hosted read-only prediction messaging, disclaimer presence, keyboard focus, and no clinical implication. Run desktop Chromium and a mobile Chromium project; capture HTML report, traces/screenshots on failure, and selected stable screenshots as evidence. Do not add pixel-diff baselines.

## Accessibility strategy

Automated checks cover semantic headings, accessible names, form labels, error/result association, keyboard navigation, visible focus, skip navigation, minimum 44px interactive targets, `aria-live` prediction output, reduced motion, chart alternatives, and absence of color-only meaning. Storybook a11y checks catch component-level violations; Playwright checks the assembled app. Findings are called accessibility checks, not WCAG conformance, unless a complete conformance audit exists.

Responsive verification covers desktop, tablet/mobile viewport, and zoom/reflow behavior without horizontal overflow. Native semantic elements remain preferred over ARIA reconstruction. Warnings, errors, and disclaimers use text and structure in addition to color.

## Data-visualization accessibility

Each Recharts visualization must have a useful visible title/caption or heading, an accessible name/description, and a nearby textual summary or semantic data table/fallback. Axes and units are explicit where the source evidence provides them. Malignant/benign meaning uses labels, order, and text in addition to coral/sage styling. Charts do not expose clinical interpretation, and values are not given extra precision beyond the generated evidence contract.

## CI/security gates

The existing backend, frontend install/audit/test/build, and Compose gates remain. Add frontend lint and typecheck, Storybook build, and deterministic Playwright. Add CodeQL for Python and JavaScript/TypeScript using least-privilege workflow permissions, Dependabot configuration for pip/npm/GitHub Actions, and dependency review for pull requests using the GitHub-maintained action. Existing audit failures remain actionable; no `continue-on-error`, warning-only, or allowlist is added without a documented, reviewed reason.

Workflow action versions are pinned to the repository's current major conventions where possible. Third-party dependencies are added only when official, current, and necessary: Storybook, its official a11y addon, Playwright Test, ESLint, and `typescript-eslint`. Browser binaries are installed explicitly in CI as required by Playwright's official guidance.

## GitHub governance

The PR template requires summary, scope/linked issue, Given/When/Then acceptance criteria, tests, browser evidence, ML/data contract impact, terminology/safety review, security/deployment impact, rollback notes, and documentation. Feature and bug issue forms use concise structured prompts. The Epic and approximately 5–8 child issues are created only if GitHub CLI authentication is available; otherwise the repository receives ready-to-paste issue documents or a clearly reported owner-gated blocker. A final governance issue documents the intended required checks and explicitly states that rulesets wait until this PR is merged and check names stabilize.

## Deployment verification

`docs/deployment.md` documents the actual Vite/Vercel workflow: production build, no-`VITE_API_URL` hosted read-only behavior, configured `VITE_API_URL` local/API behavior, preview expectations, production deployment, live smoke checks, rollback, and known limitations. Local passing tests do not establish deployment. The public URL `https://explainable-cancer-diagnosis-ml.vercel.app/` is checked separately with browser-visible evidence; no deployment mutation is performed without explicit owner intent.

## Rollback approach

All changes are isolated to the feature branch and grouped into logical commits. Rollback is a branch/PR revert; generated evidence and ML artifacts are not rewritten. If frontend dependency installation or CI proves incompatible, revert the dependency/configuration commit and preserve the existing baseline gates. If a browser or live check reveals hosted behavior drift, revert the UI/CI change before considering deployment. No main ruleset or production setting is changed, so the current public deployment remains the operational fallback.

## Testing strategy

Use red-green-refactor for new frontend behavior: write focused component or browser assertions, observe failure, implement the smallest boundary, then run the relevant test. The final gate is:

- Backend: Ruff format check, Ruff lint, compileall, pytest.
- Frontend: `npm ci`, high-severity audit, lint, typecheck, Vitest, production build, Storybook build.
- Browser: Playwright desktop/mobile hosted and real-FastAPI local flows, plus route-mocked edge states, screenshots/report.
- Packaging: `docker compose config --quiet`.
- Security/review: CodeQL/dependency workflow configuration inspection, dependency audit, standards/spec review, and evidence review.

Existing tests must continue to prove ML, artifact, API, terminology, generated showcase, and hosted-read-only invariants. New tests must not depend on network services, current time, random data, or production credentials.

## Risks and tradeoffs

- Storybook and Playwright increase install time and lockfile size, but provide isolated state coverage and assembled browser evidence that unit/build checks cannot provide.
- Current package versions are fast-moving. Exact versions are pinned after official documentation/registry verification, and CI install/build is the compatibility authority.
- A primitive migration can accidentally alter copy or responsive behavior. Keep migrations incremental, test user-visible behavior, and preserve existing page structure.
- Live deployment verification may be owner- or access-gated. Report local, seeded/mock, preview, and live evidence separately.
- GitHub security features may depend on repository settings or plan support. Configuration can be added only where the public repository supports it; unsupported activation is reported, not simulated.
- The existing CSS is a single stylesheet. A full CSS architecture rewrite would create more risk than value, so this change introduces tokens and focused primitives while keeping the stylesheet structure recognizable.

## Acceptance criteria

1. Given `origin/main` remains at `9a20bcb…`, when the feature branch is inspected, then it is based on that SHA and all baseline commands pass; if remote main moves, the branch is rebased onto the latest verified SHA and the new SHA is reported.
2. Given the repository context is needed by an agent, when `AGENTS.md` is read, then it points to authoritative product/context/design/SDLC documents and states planning, safety, dependency, testing, and PR rules without duplicating those documents.
3. Given a reviewer needs visual rules, when `DESIGN.md` is read, then it contains YAML tokens and all nine required sections, including semantic colors, focus, spacing/radii, layout, charts, responsive behavior, reduced motion, and anti-patterns.
4. Given a shared UI state is rendered, when its Storybook story is opened, then the component has typed semantics and the applicable default, disabled/loading/error/warning/malignant/benign/empty/focus/responsive states are represented without network or clinical copy.
5. Given the frontend is installed from the lockfile, when lint, typecheck, unit tests, production build, and Storybook build run, then each passes without changing generated ML evidence.
6. Given a user visits the hosted showcase in a real browser, when they navigate Overview, Evaluation, Explainability, and Prediction, then evidence renders, keyboard focus and skip navigation work, the prediction page clearly remains read-only, and no clinical inference implication appears.
7. Given the real FastAPI service is started with repository-generated artifacts, when a user selects a sample and runs the local flow, then the frontend receives the real prediction response, uses existing malignant-class terminology, preserves the disclaimer, announces the result, and remains usable at desktop and mobile viewports; route mocks cover only explicit loading/failure/unusual-response cases.
8. Given any chart is rendered, when a keyboard or non-color-dependent reader inspects it, then a meaningful label/description and textual/table alternative is available and the existing evidence orientation is unchanged.
9. Given a pull request changes this repository, when CI runs, then backend, frontend, browser, packaging, and supported security/dependency gates are defined with least privilege and no suppressed real failures.
10. Given the governance docs are reviewed, when GitHub and deployment instructions are followed, then no direct-main workflow, ruleset activation, secret fabrication, self-merge, or unsupported deployment claim is required; if `gh auth status` and repository permissions allow it, the Epic and 5–8 meaningful child issues are created; otherwise the blocker and ready-to-paste issue content are reported; the draft PR includes evidence, limitations, and rollback notes.

## Evidence sources

- Storybook React + Vite official docs: https://storybook.js.org/docs/get-started/frameworks/react-vite
- Storybook installation and current stable release guidance: https://storybook.js.org/docs/get-started/install and https://storybook.js.org/docs/releases
- Playwright installation and browser/CI guidance: https://playwright.dev/docs/intro and https://playwright.dev/docs/release-notes
- GitHub dependency review action documentation: https://github.com/actions/dependency-review-action
