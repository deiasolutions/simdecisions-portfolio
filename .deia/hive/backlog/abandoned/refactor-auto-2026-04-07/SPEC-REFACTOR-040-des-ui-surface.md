---
id: REFACTOR-040
priority: P0
model: sonnet
role: bee
depends_on:
  - REFACTOR-034
---
# SPEC-REFACTOR-040: DES — Build UI Surface If Missing

## Priority
P0

## Model Assignment
sonnet

## Depends On
- REFACTOR-034

## Intent
The DES (Discrete Event Simulation) engine exists in `engine/des/` with backend routes in `hivenode/routes/des_routes.py`. Check if it has a frontend UI surface. If not, build a minimal one as a primitive that can be loaded via a .set.md config.

## Files to Read First
- `engine/des/` — the DES engine
- `hivenode/routes/des_routes.py` — API routes
- `browser/src/primitives/` — check for existing DES primitive
- `.deia/hive/refactor/test-results-systems.json` — DES test results from Phase 1

## Acceptance Criteria
- [ ] If DES UI exists: verify it works, document in changes file
- [ ] If DES UI is missing: create `browser/src/primitives/des-pane/DesPaneApp.tsx`
  - Minimal but functional: form to configure simulation, run button, results display
  - Calls `/api/des/run` and `/api/des/status` endpoints
  - Registers in ShellNodeRenderer
- [ ] DES loadable as a .set.md primitive
- [ ] File created: `.deia/hive/refactor/changes-040.json`

## Constraints
- You are in EXECUTE mode. Build it if missing. Do NOT enter plan mode.
- Keep it minimal — functional UI, not beautiful. Ship it.
- Commit changes to `refactor/auto-2026-04-07` branch
