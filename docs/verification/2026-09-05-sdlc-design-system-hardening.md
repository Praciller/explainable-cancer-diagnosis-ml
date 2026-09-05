# Verification record: SDLC and design-system hardening

Date: 2026-09-05

Baseline: `9a20bcb10f4d5c7a94017e9313ab41bef73a201d` (`origin/main`)

Feature branch: `chore/sdlc-design-system-hardening`

## Baseline evidence

- `python -m pytest`: PASS, 34 passed.
- `ruff format --check src tests`: PASS, 40 files already formatted.
- `ruff check src tests`: PASS.
- `python -m compileall -q src tests`: PASS.
- `frontend/npm ci`: PASS, 173 packages installed, 0 vulnerabilities.
- `frontend/npm audit --audit-level=high`: PASS, 0 vulnerabilities.
- `frontend/npm test`: PASS, 5 files and 6 tests passed.
- `frontend/npm run build`: PASS.
- `docker compose config --quiet`: PASS.

## Final local evidence

- `python -m pytest`: PASS, 34 passed after removing machine-specific path literals from new documentation.
- `ruff format --check src tests`: PASS, 40 files already formatted.
- `ruff check src tests`: PASS.
- `python -m compileall -q src tests`: PASS.
- `frontend/npm ci`: PASS.
- `frontend/npm audit --audit-level=high`: PASS, 0 vulnerabilities.
- `frontend/npm run lint`: PASS.
- `frontend/npm run typecheck`: PASS.
- `frontend/npm test -- --run`: PASS, 7 files and 12 tests passed.
- `frontend/npm run build`: PASS.
- `frontend/npm run build-storybook`: PASS with only the existing large-chunk warning.
- `docker compose config --quiet`: PASS.
- Impeccable detector over changed UI targets: PASS, no findings.

## Browser evidence

- `frontend/npm run e2e:hosted`: PASS, 4 tests passed and 4 deterministic local-only tests skipped across Chromium and mobile Chromium.
- Hosted Chromium-only screenshot run: PASS, 2 tests passed.
- `frontend/npm run e2e:local`: PASS, 4 tests passed and 4 hosted-only tests skipped across Chromium and mobile Chromium.
- Local E2E used freshly generated artifacts from `python -m src.pipeline --seed 42 --mlp-epochs 100` and a real FastAPI service. Server logs recorded successful `GET /model-info`, `GET /features`, `GET /samples`, `POST /predict`, and report requests.
- Browser-visible hosted checks confirmed primary navigation, evidence content, disclaimers, hosted local-only prediction messaging, keyboard skip navigation, and mobile layout.
- Mobile viewport measurement: `innerWidth=390`, `scrollWidth=375`, `bodyScrollWidth=375`; no horizontal overflow.

## Security evidence

- Codex Security diff scan: scan `95e81da1-7071-42c3-a8d1-ca677981be74`, range `9a20bcb10f4d5c7a94017e9313ab41bef73a201d...78b6a7c`.
- Complete compact inventory: 41 changed files reviewed by the parent process because delegated workers were unavailable.
- Findings: 0 reportable findings; coverage complete.
- `npm audit --audit-level=high`: PASS, 0 vulnerabilities.
- GitHub Dependency Review: UNAVAILABLE because the repository Dependency Graph is disabled; the unsupported workflow was removed rather than treated as a passing gate.
- TAC status was not available because the security-access connector was not connected; this is an advisory limitation and not a code finding.

## Release boundary

The public Vercel URL was verified read-only. No deployment, promotion, merge, main push, or main branch protection/ruleset change was performed.
