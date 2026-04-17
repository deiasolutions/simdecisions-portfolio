---
id: REFACTOR-020
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-013
---
# SPEC-REFACTOR-020: Test Every System — Kanban, Inventory, DES, Canvas, Auth, Primitives

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-013

## Intent
Run every existing test suite and manually probe every system. Record what passes, what fails, what's untestable. This creates the pre-refactor functionality baseline.

## Files to Read First
- `.deia/hive/refactor/FEATURE-MANIFEST.json` — know what to test
- `tests/` — all test directories
- `browser/e2e/` — E2E tests

## Acceptance Criteria
- [ ] Run: `python -m pytest tests/ -v --tb=short` — capture full output
- [ ] Run: `npx vitest run` (if configured) — capture output
- [ ] For each system in FEATURE-MANIFEST.json, record:
  - Has tests? (yes/no, with file paths)
  - Tests pass? (pass/fail/error, with details)
  - Manual probe result (if no tests — can the route be hit? does the component render?)
- [ ] File created: `.deia/hive/refactor/test-results-systems.json`
- [ ] Summary: X systems tested, Y passing, Z failing, W untestable

## Constraints
- You are in EXECUTE mode. Run tests and write results. Do NOT enter plan mode.
- Read-only — no code changes. Only run tests and record output.
- If a test suite requires a running server, note it as "requires-server" and skip gracefully
- No git operations
