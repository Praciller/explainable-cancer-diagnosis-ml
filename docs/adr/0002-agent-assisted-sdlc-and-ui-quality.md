# ADR 0002: Agent-assisted SDLC and UI quality

## Context

The repository has governed ML evidence, explicit educational limitations, a read-only public showcase, a local FastAPI path, and an existing React/Vite interface. It did not yet expose those decisions as one agent-ready operating contract, nor did it have isolated component verification, deterministic browser integration, frontend lint/typecheck, or complete security/dependency workflow documentation.

## Options considered

1. Rewrite the frontend around a new design framework and replace the current dashboard structure. This would increase visual and contract risk without improving the ML evidence boundary.
2. Add disconnected tooling and broad dependencies around the current app. This would create gates without clear component ownership or an explicit source of truth.
3. Formalize the existing identity and contracts with a lean repository contract, tokenized CSS-first primitives, Storybook, Playwright, and deterministic CI/security gates. This preserves the working product while making its quality process inspectable.

## Decision

Choose option 3. `AGENTS.md` is the concise repository-local operating entry point and points to `PRODUCT.md`, `CONTEXT.md`, root `DESIGN.md`, and the canonical SDLC. Root `DESIGN.md` is the design source of truth; CSS custom properties implement its tokens. Work follows progressive skill loading and a spec → tickets → implementation workflow.

The frontend keeps its React/Vite page composition, lazy pages, runtime boundary, and hosted read-only behavior. Shared UI semantics use small typed primitives; model-specific copy and data remain in domain components. Storybook verifies component states in isolation. Playwright verifies assembled hosted behavior and a primary local flow against the real FastAPI service, with route mocks limited to impractical edge states. CI runs deterministic backend, frontend, browser, packaging, CodeQL, audit, Dependabot, and supported dependency-review gates.

Development remains branch/PR based with no direct main development. The public showcase remains read-only. ML evidence contracts, target orientation, feature ordering, split governance, artifact checksums, generated showcase evidence, and FastAPI contracts remain authoritative and unchanged.

## Consequences

The repository gains visible agent context, reviewable UI boundaries, component state coverage, real browser evidence, and clearer quality/security gates. Storybook and browser dependencies increase install time and lockfile size, and fast-moving tool versions require explicit pinning and CI verification. The design system remains intentionally CSS-first and recognizable rather than becoming a new framework. GitHub rulesets and production deployment remain owner-gated until checks stabilize and separate authorization is provided.
