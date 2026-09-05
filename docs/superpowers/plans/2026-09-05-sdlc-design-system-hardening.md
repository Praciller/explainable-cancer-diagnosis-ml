# Agent-assisted SDLC and UI quality hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the existing governed ML showcase into a reviewable SDLC reference implementation with explicit repository context, tokenized UI foundations, component/browser verification, deterministic CI/security gates, and honest deployment/governance documentation.

**Architecture:** Keep the current Python pipeline, generated evidence, FastAPI contracts, React/Vite page composition, lazy loading, runtime mode boundary, and hosted read-only behavior unchanged. Add a CSS-first UI primitive layer below existing domain components, Storybook for isolated state verification, Playwright for hosted and real-FastAPI integration flows, and repository/GitHub documentation around those surfaces.

**Tech Stack:** Python 3.10+, pytest, Ruff, FastAPI, React 19, TypeScript 6, Vite 8, Vitest 4, Storybook 10.6.0, `@storybook/react-vite` 10.6.0, `@storybook/addon-a11y` 10.6.0, ESLint 10.10.0, `typescript-eslint` 8.69.0, Playwright Test 1.63.0, GitHub Actions, CodeQL, Dependabot, and dependency review.

**Spec:** `docs/superpowers/specs/2026-09-05-sdlc-design-system-hardening-design.md`

## Global Constraints

- Preserve target orientation, feature ordering, split governance, artifact checksums/contracts, generated showcase evidence, and FastAPI contracts.
- Preserve the educational-only boundary: use “model prediction,” “model output,” and “malignant-class model score”; never imply diagnosis, risk, confidence, clinical probability, treatment, screening, or clinical decision support.
- Preserve public Vercel read-only mode and local FastAPI inference mode.
- Do not manually edit generated evidence, retrain models, change dataset/splits, add secrets, or add paid services.
- Keep `DESIGN.md` as the design source of truth and use named tokens for new styling.
- Use real FastAPI for the primary local Playwright integration flow; route mocks are only for deterministic loading/failure/unusual-response states.
- Do not push to `main`, merge the PR, enable branch protection/rulesets, or trigger production deployment.
- Run focused tests after each vertical task and the complete verification gate before any completion claim.

---

### Task 1: Establish repository context, design contract, ADR, deployment, and contribution governance

**Files:**
- Create: `AGENTS.md`
- Modify: `DESIGN.md`
- Create: `docs/adr/0002-agent-assisted-sdlc-and-ui-quality.md`
- Create: `docs/deployment.md`
- Modify: `README.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/ISSUE_TEMPLATE/feature.yml`
- Create: `.github/ISSUE_TEMPLATE/bug.yml`
- Create: `.github/dependabot.yml`
- Test: repository documentation scans and `git diff --check`

**Interfaces:**
- Consumes: `PRODUCT.md`, `CONTEXT.md`, the new spec, existing `docs/frontend.md`, current Vercel behavior, and current scripts.
- Produces: a concise agent entry point, machine-readable design tokens, durable ADR, actual deployment runbook, PR/issue governance, and README links. Later tasks use the token names and command names defined here.

- [ ] **Step 1: Write the repository operating contract**

  `AGENTS.md` must point to `PRODUCT.md`, `CONTEXT.md`, `DESIGN.md`, the canonical SDLC index, and the relevant stage documents. It must state the repository map, Python/frontend/package commands, generated-file rules, terminology/safety constraints, ML invariants, design-system rules, testing expectations, dependency policy, branch/PR rules, secret handling, and definition of done without copying the source documents.

- [ ] **Step 2: Rewrite the design contract without changing the product identity**

  Put YAML front matter at the top of `DESIGN.md` with explicit values for `canvas`, `surface`, `surface_strong`, `text`, `muted`, `border`, `accent`, `accent_dark`, `malignant`, `malignant_soft`, `benign`, `benign_soft`, `warning`, `error`, `focus`, `space`, `radius`, `container`, `sidebar`, and `breakpoints`. Follow it with exactly these sections: Visual Theme & Atmosphere; Color Palette & Roles; Typography Rules; Component Stylings; Layout Principles; Depth & Elevation; Interaction & Motion; Responsive Behavior; Agent Prompt Guide. Include chart/table/metric rules, warning/error/disclaimer rules, empty/loading behavior, reduced-motion behavior, 44px target guidance, and every listed anti-pattern.

- [ ] **Step 3: Record the durable architecture decision**

  `docs/adr/0002-agent-assisted-sdlc-and-ui-quality.md` must contain Context, Options considered, Decision, and Consequences. The Decision must name `AGENTS.md`, root `DESIGN.md`, progressive skill loading, spec → tickets → implementation, Storybook, Playwright, deterministic CI/security, no direct-main development, hosted read-only mode, and authoritative ML evidence contracts.

- [ ] **Step 4: Document actual deployment and rollback behavior**

  `docs/deployment.md` must distinguish local, preview, and production. Document `npm run build`, Vercel’s no-`VITE_API_URL` read-only behavior, configured `VITE_API_URL` behavior, preview expectations, the existing live URL, read-only verification, owner-gated production deployment, rollback by reverting the PR, and the known limits of static evidence and local inference. Include no credentials or invented deployment IDs.

- [ ] **Step 5: Add review and issue templates**

  The PR template must require Summary, Scope/linked issue, Given/When/Then acceptance criteria, tests, UI/browser evidence, ML/data contract impact, safety terminology review, security impact, deployment impact, rollback notes, and documentation. The feature and bug forms must collect reproducible context and testable acceptance criteria. Dependabot must cover npm, pip, and GitHub Actions with a weekly schedule and bounded pull-request limits.

- [ ] **Step 6: Add concise README references**

  Keep recruiter content near the top. Add links to `AGENTS.md`, `DESIGN.md`, ADRs, frontend quality commands, Storybook, Playwright, CI/security, and `docs/deployment.md`; do not duplicate the internal runbook.

- [ ] **Step 7: Verify documentation contracts**

  Run:

  ```powershell
  rg -n "PRODUCT.md|CONTEXT.md|DESIGN.md|plan before|no direct|generated|VITE_API_URL|Storybook|Playwright|rollback" AGENTS.md DESIGN.md docs README.md .github
  rg -n "TBD|TODO|FIXME|diagnosis|clinical probability|confidence|risk" AGENTS.md DESIGN.md docs/adr/0002-agent-assisted-sdlc-and-ui-quality.md docs/deployment.md
  git diff --check
  ```

  Expected: required references and safety language are present; no placeholder remains; the second scan may match only explicitly documented anti-patterns or boundary language, never user-facing claims.

- [ ] **Step 8: Commit the documentation vertical**

  ```powershell
  git add AGENTS.md DESIGN.md docs/adr/0002-agent-assisted-sdlc-and-ui-quality.md docs/deployment.md README.md .github
  git commit -m "docs: establish agent SDLC and design contracts"
  ```

**Acceptance criteria:**

- Given an agent starts in the repository, when it reads `AGENTS.md`, then it is directed to authoritative product/context/design/SDLC files and the required commands/rules.
- Given a reviewer reads `DESIGN.md`, when they inspect the front matter and nine sections, then every required token, semantic role, responsive/accessibility rule, and anti-pattern is explicit and the aubergine/coral/sage identity remains intact.
- Given a contributor opens a PR or issue, when the template renders, then the required acceptance, evidence, safety, security, deployment, rollback, and documentation fields are present.
- Given a maintainer follows `docs/deployment.md`, when they verify local/preview/production, then the instructions do not claim local code is deployed or require credentials to be committed.

---

### Task 2: Add tokenized UI primitives and migrate shared states

**Files:**
- Create: `frontend/src/components/ui/Button.tsx`
- Create: `frontend/src/components/ui/Surface.tsx`
- Create: `frontend/src/components/ui/Metric.tsx`
- Create: `frontend/src/components/ui/StatusBadge.tsx`
- Create: `frontend/src/components/ui/Callout.tsx`
- Create: `frontend/src/components/ui/Skeleton.tsx`
- Create: `frontend/src/components/ui/index.ts`
- Modify: `frontend/src/components/MetricCard.tsx`
- Modify: `frontend/src/components/LoadingState.tsx`
- Modify: `frontend/src/components/ErrorMessage.tsx`
- Modify: `frontend/src/components/DisclaimerBanner.tsx`
- Modify: `frontend/src/components/FeatureInputForm.tsx`
- Modify: `frontend/src/components/SampleSelector.tsx`
- Modify: `frontend/src/components/PredictionPage.tsx`
- Modify: `frontend/src/pages/OverviewPage.tsx`
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/styles.css`
- Test: focused component tests under `frontend/src/components/*.test.tsx`

**Interfaces:**
- Consumes: design tokens from `DESIGN.md` and existing component props/copy.
- Produces: typed UI primitives with no API calls. `Button` accepts native button props plus `variant?: "primary" | "secondary" | "text"`; `Metric` accepts `label`, `value`, and `detail`; `StatusBadge` accepts `status?: "malignant" | "benign" | "warning" | "neutral"`; `Callout` accepts `tone?: "disclaimer" | "error" | "warning" | "info"`, `title`, and children; `Skeleton` accepts `label` and `variant?: "title" | "line" | "short"`; `Surface` accepts children and an optional `as` element. Existing domain components remain compatible.

- [ ] **Step 1: Add failing primitive tests**

  Add tests that render each primitive and assert role/name, disabled state, visible text, status text, and reduced-motion-safe class semantics. Test `Button` variants and `disabled`, `Callout` error/disclaimer roles, `Metric` value/detail, and `Skeleton`’s visually hidden loading label.

- [ ] **Step 2: Implement the primitives with semantic HTML**

  Use `<button>`, `<section>`, `<output>`/`<div>` as appropriate, and preserve native props. Do not add API imports, model data, new colors, or clinical terms. Export all primitives from `ui/index.ts`.

- [ ] **Step 3: Add token-backed CSS**

  Replace repeated literal values in the touched styles with custom properties. Keep compatibility classes while migrating. Define one focus ring, one target minimum, one status treatment, one radius scale, and one spacing scale. Preserve the existing responsive breakpoints and reduced-motion media query.

- [ ] **Step 4: Migrate shared call sites**

  Replace repeated buttons with `Button`, `MetricCard` internals with `Metric`, loading markup with `Skeleton`, and disclaimer/error markup with `Callout`. Migrate only call sites where the rendered semantics remain identical; keep `PredictionResult`’s domain copy and `App`’s navigation behavior.

- [ ] **Step 5: Run focused red-green verification**

  ```powershell
  cd frontend
  npm test -- src/components/DisclaimerBanner.test.tsx src/components/PredictionResult.test.tsx src/components/MetricCard.test.tsx
  npm run build
  cd ..
  ```

  Expected: focused tests and the TypeScript/Vite build pass; no `showcase_contract.json`, reports, models, or backend files change.

- [ ] **Step 6: Commit the primitive vertical**

  ```powershell
  git add frontend/src/components frontend/src/pages frontend/src/App.tsx frontend/src/styles.css
  git commit -m "feat(frontend): formalize shared UI primitives"
  ```

**Acceptance criteria:**

- Given any primitive is rendered, when a keyboard user interacts with it, then its native role, visible focus, disabled state, and 44px target are preserved.
- Given the existing pages render, when the migration is applied, then page copy, lazy loading, hosted/local mode, navigation, aria-live behavior, and ML terminology are unchanged.
- Given a visual token is needed, when a touched component is styled, then it resolves through a named CSS custom property rather than a duplicated literal.
- Given the frontend suite runs, when focused tests and `npm run build` complete, then they pass without changing generated ML evidence.

---

### Task 3: Audit charts and make evidence alternatives explicit

**Files:**
- Modify: `frontend/src/components/ModelScoreChart.tsx`
- Modify: `frontend/src/components/FeatureImportanceChart.tsx`
- Modify: `frontend/src/components/RocCurveViewer.tsx`
- Modify: `frontend/src/components/ConfusionMatrixViewer.tsx`
- Modify: `frontend/src/components/ReportFigure.tsx`
- Modify: `frontend/src/components/PredictionResult.tsx`
- Modify: `frontend/src/styles.css`
- Test: chart/component tests in `frontend/src/components/*.test.tsx`

**Interfaces:**
- Consumes: existing generated report images, `PredictionResponse`, and `ModelScoreChart` props.
- Produces: visible chart headings/captions, stable `aria-describedby` relationships, and textual/semantic alternatives that explain score/threshold or link the existing evidence without inventing values.

- [ ] **Step 1: Write failing chart accessibility tests**

  Assert that `ModelScoreChart` exposes a named region plus visible score/threshold text, and that report figures expose a figure caption and non-empty alt text. Assert `PredictionResult` retains malignant-class terminology and its live region.

- [ ] **Step 2: Add a textual score alternative**

  Keep Recharts for visual presentation, add a visible heading or `aria-labelledby`, preserve the fixed threshold line, and ensure the visible caption states the score and threshold to three/two decimal places as the existing UI does. Do not add animation.

- [ ] **Step 3: Strengthen report figure semantics**

  Make `ReportFigure` accept an optional `title`/description only if all callers can provide truthful content; otherwise use its existing `alt`/caption contract. Keep generated PNGs as the source evidence and do not hand-edit or regenerate them.

- [ ] **Step 4: Run chart-focused verification**

  ```powershell
  cd frontend
  npm test -- src/components/PredictionResult.test.tsx src/components/ModelScoreChart.test.tsx src/components/ReportFigure.test.tsx
  npm run build
  cd ..
  ```

- [ ] **Step 5: Commit chart accessibility**

  ```powershell
  git add frontend/src/components frontend/src/styles.css
  git commit -m "feat(frontend): add accessible evidence alternatives"
  ```

**Acceptance criteria:**

- Given a reader cannot perceive color, when they inspect a chart, then labels, order, visible text, and a nearby alternative still communicate the evidence.
- Given a report figure is rendered, when assistive technology reads it, then the image has meaningful alt text and the figure has a caption.
- Given prediction output is rendered, when the live region is announced, then it uses existing model-output terminology and does not imply clinical certainty.

---

### Task 4: Add Storybook component verification

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json`
- Create: `frontend/.storybook/main.ts`
- Create: `frontend/.storybook/preview.ts`
- Create: `frontend/src/components/ui/Button.stories.tsx`
- Create: `frontend/src/components/ui/Surface.stories.tsx`
- Create: `frontend/src/components/ui/Metric.stories.tsx`
- Create: `frontend/src/components/ui/StatusBadge.stories.tsx`
- Create: `frontend/src/components/ui/Callout.stories.tsx`
- Create: `frontend/src/components/ui/Skeleton.stories.tsx`
- Create: `frontend/src/components/DisclaimerBanner.stories.tsx`
- Create: `frontend/src/components/ErrorMessage.stories.tsx`
- Create: `frontend/src/components/LoadingState.stories.tsx`
- Create: `frontend/src/components/MetricCard.stories.tsx`
- Create: `frontend/src/components/PredictionResult.stories.tsx`
- Create: `frontend/src/components/ModelComparisonTable.stories.tsx`
- Modify: `frontend/.gitignore` or root `.gitignore` if needed for `storybook-static/`
- Test: Storybook test/build commands

**Interfaces:**
- Consumes: typed primitives/domain props and local fixture data from `frontend/src/data/showcase_contract.json`.
- Produces: deterministic Storybook stories, a11y addon configuration, `storybook` and `build-storybook` scripts, and no network dependency.

- [ ] **Step 1: Install the pinned official Storybook packages**

  ```powershell
  cd frontend
  npm install --save-dev storybook@10.6.0 @storybook/react-vite@10.6.0 @storybook/addon-a11y@10.6.0
  cd ..
  ```

  Verify the lockfile contains the exact direct versions and no unrelated major upgrade.

- [ ] **Step 2: Configure React + Vite Storybook**

  `main.ts` must use `@storybook/react-vite`, discover `src/**/*.stories.tsx`, and include no app bootstrapping or API calls. `preview.ts` must import the production stylesheet and register `@storybook/addon-a11y` through the supported current configuration.

- [ ] **Step 3: Add state-focused stories**

  Each requested component must cover applicable default, focus, disabled, loading, error, warning, malignant, benign, empty, and responsive states. `PredictionResult` uses a typed local fixture; `ModelComparisonTable` covers a real contract fixture and null report; no story uses clinical claims or random/time-dependent values.

- [ ] **Step 4: Add scripts and ignore generated output**

  Add:

  ```json
  "storybook": "storybook dev -p 6006",
  "build-storybook": "storybook build"
  ```

  Keep `test`, `build`, and existing scripts intact. Ignore `frontend/storybook-static/`.

- [ ] **Step 5: Verify Storybook**

  ```powershell
  cd frontend
  npm ci
  npm run build-storybook
  npm test
  cd ..
  ```

  Expected: Storybook build and existing tests pass; generated output is untracked and no ML evidence changes.

- [ ] **Step 6: Commit Storybook**

  ```powershell
  git add frontend/package.json frontend/package-lock.json frontend/.storybook frontend/src/components .gitignore frontend/.gitignore
  git commit -m "test(frontend): add Storybook component states"
  ```

**Acceptance criteria:**

- Given Storybook is started from a clean install, when the catalog is opened, then the requested core/domain components render from local typed props and the a11y addon is available.
- Given an applicable state is selected, when the story is viewed, then default/focus/disabled/loading/error/warning/malignant/benign/empty/responsive behavior is represented without network calls or unsafe medical copy.
- Given CI runs `npm run build-storybook`, when the build completes, then it passes and generated `storybook-static` is not committed.

---

### Task 5: Add frontend lint and typecheck gates

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json`
- Create: `frontend/eslint.config.js`
- Modify: `frontend/tsconfig.app.json` only if the typecheck boundary needs an explicit no-emit project setting
- Test: lint/typecheck commands

**Interfaces:**
- Consumes: existing TypeScript/Vite source and Storybook TypeScript files.
- Produces: one minimal ESLint flat config, `lint` and `typecheck` scripts, and no duplicate formatter.

- [ ] **Step 1: Install the pinned lint packages**

  ```powershell
  cd frontend
  npm install --save-dev eslint@10.10.0 typescript-eslint@8.69.0 eslint-plugin-react-hooks eslint-plugin-react-refresh globals
  cd ..
  ```

  Keep versions compatible with the installed React/TypeScript/Vite stack; if the official package peer range rejects a version, stop and record the concrete error before choosing the smallest compatible patch version.

- [ ] **Step 2: Add the flat config**

  Configure TypeScript-aware recommended rules, browser globals, React Hooks rules, React Refresh rules, ignored generated directories, and test globals. Do not add formatting rules or a second formatter. Keep rule overrides minimal and document any disabled rule inline.

- [ ] **Step 3: Add scripts**

  Add:

  ```json
  "lint": "eslint .",
  "typecheck": "tsc -b --pretty false"
  ```

  Keep `build` as the production compile/build gate.

- [ ] **Step 4: Run gates and fix only confirmed findings**

  ```powershell
  cd frontend
  npm run lint
  npm run typecheck
  npm run build
  cd ..
  ```

  Resolve actual source findings without broad formatting churn or weakening rules to hide errors.

- [ ] **Step 5: Commit lint/typecheck**

  ```powershell
  git add frontend/package.json frontend/package-lock.json frontend/eslint.config.js frontend/tsconfig.app.json
  git commit -m "chore(frontend): add lint and typecheck gates"
  ```

**Acceptance criteria:**

- Given a clean frontend install, when `npm run lint` and `npm run typecheck` run, then both pass with the source, stories, and tests included.
- Given a lint rule is not applicable, when it is disabled, then the config records the narrow reason and does not suppress real correctness/security findings.
- Given the build runs after lint/typecheck, then the existing production build remains passing.

---

### Task 6: Add real-FastAPI Playwright integration and edge-state coverage

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json`
- Create: `frontend/playwright.config.ts`
- Create: `frontend/e2e/showcase.spec.ts`
- Create: `frontend/e2e/local-prediction.spec.ts`
- Create: `frontend/e2e/edge-states.spec.ts`
- Modify: `.gitignore`
- Test: Playwright HTML report, screenshots, and traces on failure

**Interfaces:**
- Consumes: production Vite preview, hosted no-`VITE_API_URL` mode, real FastAPI endpoints, repository-generated artifacts, existing public copy, and Playwright 1.63.0.
- Produces: `e2e:hosted`, `e2e:local`, and `e2e:report` scripts plus deterministic desktop Chromium/mobile Chromium projects. The local project points `VITE_API_URL` at `http://127.0.0.1:8000`.

- [ ] **Step 1: Install Playwright Test**

  ```powershell
  cd frontend
  npm install --save-dev @playwright/test@1.63.0
  npx playwright install chromium
  cd ..
  ```

- [ ] **Step 2: Configure isolated browser projects**

  Configure a hosted and local mode selected by `E2E_MODE`, `baseURL` on port `4173`, Chromium desktop, and a mobile Chromium device. Use `trace: "retain-on-failure"`, `screenshot: "only-on-failure"`, and HTML reporting to an ignored output directory. The preview server must inherit `VITE_API_URL` only in local mode.

- [ ] **Step 3: Write hosted showcase tests first**

  Assert app load, skip link, visible primary navigation, Overview heading/evidence, Evaluation table/figure, Explainability heading/figure, Prediction read-only message, disclaimer, no horizontal overflow at desktop/mobile, and no unsafe clinical implication in visible text. Use role/name locators and `page.screenshot()` for stable selected evidence.

- [ ] **Step 4: Write the real local integration flow**

  Before the test, generate artifacts with `python -m src.pipeline --seed 42 --mlp-epochs 100`, start `uvicorn src.api.main:app --host 127.0.0.1 --port 8000`, and start the Vite preview with `VITE_API_URL=http://127.0.0.1:8000`. Assert samples load, a sample can be selected, `Run model prediction` returns a result, malignant-class score/threshold/copy render, the disclaimer remains, and the live result region is present.

- [ ] **Step 5: Add route-mocked edge states**

  Mock only `/model-info`/`/samples`/`/features` or `/predict` responses needed to prove loading and API failure UI. Assert the visible error message and retry-safe state; do not use mocks for the primary success path.

- [ ] **Step 6: Add scripts and ignore artifacts**

  Add:

  ```json
  "e2e:hosted": "cross-env E2E_MODE=hosted playwright test",
  "e2e:local": "cross-env E2E_MODE=local playwright test",
  "e2e:report": "playwright show-report playwright-report"
  ```

  Add `cross-env` only if Windows/CI environment assignment cannot remain portable without it. Otherwise use a checked-in PowerShell/Node wrapper. Ignore `frontend/playwright-report/`, `frontend/test-results/`, and browser caches.

- [ ] **Step 7: Run browser verification**

  ```powershell
  cd frontend
  npm run e2e:hosted
  cd ..
  python -m src.pipeline --seed 42 --mlp-epochs 100
  uvicorn src.api.main:app --host 127.0.0.1 --port 8000
  cd frontend
  npm run e2e:local
  cd ..
  ```

  Expected: hosted and real-FastAPI local tests pass at desktop/mobile projects; HTML report and screenshots exist under ignored paths. Stop the temporary API process after the run.

- [ ] **Step 8: Commit E2E**

  ```powershell
  git add frontend/package.json frontend/package-lock.json frontend/playwright.config.ts frontend/e2e .gitignore frontend/.gitignore
  git commit -m "test(frontend): add browser integration coverage"
  ```

**Acceptance criteria:**

- Given the hosted build has no `VITE_API_URL`, when Playwright visits the showcase, then all four pages and read-only prediction messaging work at desktop and mobile sizes.
- Given the real FastAPI service has repository-generated artifacts, when a sample-based prediction runs in the browser, then the actual frontend/API response renders with existing terminology, disclaimer, and live announcement behavior.
- Given an API edge response is mocked, when loading or failure occurs, then the corresponding UI is testable without changing the success-path contract.
- Given the browser suite completes, then HTML results and selected screenshots are available and no pixel-diff baseline is introduced.

---

### Task 7: Wire CI, CodeQL, dependency review, and packaging gates

**Files:**
- Modify: `.github/workflows/ci.yml`
- Create: `.github/workflows/codeql.yml`
- Create: `.github/workflows/dependency-review.yml`
- Modify: `.github/dependabot.yml` if Task 1 created it
- Modify: `README.md` only for final command references
- Test: local workflow command equivalents and YAML parsing

**Interfaces:**
- Consumes: all package scripts and Playwright commands from Tasks 4–6, backend baseline commands, and GitHub-native actions.
- Produces: deterministic PR/push quality gates with least-privilege permissions. CodeQL covers Python and JavaScript/TypeScript; dependency review runs on pull requests and fails high/critical introduced vulnerabilities without warning-only behavior.

- [ ] **Step 1: Extend the existing CI workflow without removing baseline gates**

  Keep backend format, lint, pytest, compileall; frontend `npm ci`, high-severity audit, unit tests, and production build; packaging Compose config. Add frontend lint, typecheck, Storybook build, and browser jobs. The browser job installs Chromium, installs Python dependencies, runs the pipeline to create local artifacts, starts FastAPI, and runs the real local Playwright suite; run hosted mode separately against a no-API build.

- [ ] **Step 2: Add least-privilege security workflows**

  Configure `permissions: contents: read` by default. CodeQL uses the official `github/codeql-action` with Python and JavaScript/TypeScript matrices. Dependency review uses `actions/dependency-review-action@v5` on `pull_request` with `contents: read`, `fail-on-severity: high`, and no `warn-only`.

- [ ] **Step 3: Validate workflow syntax and command parity**

  ```powershell
  docker compose config --quiet
  git diff --check
  rg -n "ruff format|ruff check|pytest|compileall|npm ci|npm audit|npm run lint|npm run typecheck|npm test|npm run build|npm run build-storybook|playwright|dependency-review|CodeQL" .github/workflows
  ```

  If a dedicated YAML parser is already available, use it; do not add one only for this check. Verify every referenced npm script exists in `frontend/package.json`.

- [ ] **Step 4: Commit CI/security**

  ```powershell
  git add .github/workflows .github/dependabot.yml README.md
  git commit -m "ci: add frontend browser and security gates"
  ```

**Acceptance criteria:**

- Given a pull request changes frontend code, when CI runs, then lint, typecheck, unit tests, production build, Storybook build, hosted E2E, and real-FastAPI local E2E are defined.
- Given a pull request changes Python or dependency files, when CI/security runs, then backend gates, CodeQL, audit, and supported dependency review run with least privilege.
- Given a real audit/security failure occurs, when CI reports it, then the workflow does not suppress or downgrade it to obtain green status.
- Given packaging is checked, when `docker compose config --quiet` runs, then the existing Compose contract remains valid.

---

### Task 8: Create GitHub traceability, perform independent review, verify live/read-only behavior, and create the draft PR

**Files:**
- Create if needed: `docs/governance/epic-and-issues.md` with ready-to-paste issue bodies when GitHub CLI is unavailable
- Create: `docs/verification/2026-09-05-sdlc-design-system-hardening.md`
- Modify: none in ML/artifact/API surfaces unless a verification test proves regression
- Test/evidence: complete command log, Playwright report/screenshots, live URL browser checks, `gh auth status`, diff review

**Interfaces:**
- Consumes: approved spec, this plan, all preceding commits, current `origin/main`, live URL, GitHub CLI state, and installed review/verification skills.
- Produces: 5–8 meaningful GitHub issues plus Epic when authorized, a final governance issue describing future ruleset checks, verification report, pushed feature branch, and a DRAFT PR against `main`. Never merges or enables rulesets.

- [ ] **Step 1: Verify current GitHub authority before mutation**

  ```powershell
  gh auth status
  gh repo view Praciller/explainable-cancer-diagnosis-ml --json nameWithOwner,defaultBranchRef
  ```

  If authenticated with issue/PR write permission, create the Epic titled `Epic: Agent-assisted SDLC and frontend design-system hardening`, 5–8 child issues matching plan verticals, and `Enable main branch ruleset after quality-gate stabilization`. If not, write the exact issue bodies to `docs/governance/epic-and-issues.md` and report the owner-gated blocker.

- [ ] **Step 2: Run the complete local verification gate**

  ```powershell
  ruff format --check src tests
  ruff check src tests
  python -m compileall -q src tests
  python -m pytest
  cd frontend
  npm ci
  npm audit --audit-level=high
  npm run lint
  npm run typecheck
  npm test
  npm run build
  npm run build-storybook
  npm run e2e:hosted
  cd ..
  python -m src.pipeline --seed 42 --mlp-epochs 100
  uvicorn src.api.main:app --host 127.0.0.1 --port 8000
  cd frontend
  npm run e2e:local
  cd ..
  docker compose config --quiet
  ```

  Record exit codes and counts; distinguish baseline, local seeded, browser, and live evidence. Do not claim generated evidence is production evidence.

- [ ] **Step 3: Verify the actual live public showcase read-only**

  Use a real browser to inspect `https://explainable-cancer-diagnosis-ml.vercel.app/` at desktop and mobile sizes. Check load, navigation, Overview/Evaluation/Explainability, Prediction read-only messaging, disclaimer, focus/skip link, no horizontal overflow, charts/tables, and absence of clinical implication. Save screenshots under the visualization/evidence workspace or another ignored evidence path; do not deploy or alter Vercel settings.

- [ ] **Step 4: Run standards/spec/security/verification reviews**

  Review `git diff origin/main...HEAD` against the spec and repo conventions. Run the installed `code-review`, `codex-security:security-diff-scan` or narrow security review available in this environment, and `superpowers:verification-before-completion` workflow. Resolve confirmed issues and rerun affected gates.

- [ ] **Step 5: Write the evidence report**

  `docs/verification/2026-09-05-sdlc-design-system-hardening.md` must list baseline SHA, branch, changed files by vertical, exact commands and exit results, Storybook/browser artifacts, accessibility checks, GitHub issue/PR state, live URL state, deployment non-action, known limitations, and blockers. Use `PASS`, `PARTIAL`, `UNVERIFIED`, or `BLOCKED`; never use “secure,” “accessible,” “deployed,” or “production-ready” without direct evidence.

- [ ] **Step 6: Push only the feature branch and create the draft PR**

  ```powershell
  git status --short --branch
  git log --oneline origin/main..HEAD
  git push -u origin chore/sdlc-design-system-hardening
  gh pr create --draft --base main --head chore/sdlc-design-system-hardening --title "chore: harden agent-assisted SDLC and frontend quality" --body-file docs/verification/2026-09-05-sdlc-design-system-hardening.md
  ```

  The PR body must include problem, design decisions, exact files, screenshots, commands/results, CI status, security findings, dependency changes, deployment implications, limitations, rollback, and linked Epic/issues. Do not merge. Do not enable branch protection/rulesets.

**Acceptance criteria:**

- Given the final branch is reviewed, when `git diff origin/main...HEAD` and the verification report are inspected, then every spec requirement is mapped to evidence or an explicit limitation.
- Given GitHub authentication is available, when issue creation runs, then one Epic, 5–8 meaningful child issues, and the final ruleset-stabilization issue exist; otherwise the repository contains ready-to-paste issue content and a clear blocker.
- Given the live URL is inspected, when desktop/mobile read-only checks complete, then the public deployment is reported separately from local/preview state and no deployment mutation occurs.
- Given the branch is ready to hand off, when the draft PR is created, then it targets `main`, contains the required evidence, and remains unmerged with rulesets unchanged.

---

## Plan self-review checklist

- [ ] Every spec section maps to Tasks 1–8.
- [ ] No ML, artifact, API, dataset, or generated evidence mutation is planned.
- [ ] Real FastAPI is the primary local browser success path; mocks are edge-state-only.
- [ ] Storybook, Playwright, lint/typecheck, CI/security, governance, deployment, accessibility, and live verification are all covered.
- [ ] Each task has exact files, interfaces, focused tests, Given/When/Then acceptance criteria, and a logical commit.
- [ ] No task requires direct `main` mutation, production deployment, credentials, or branch-protection activation.
