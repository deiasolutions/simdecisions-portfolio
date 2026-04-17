# BRIEFING: SimDecisions Applet Wiring -- TASK BREAKDOWN COMPLETE

**Status:** TASK FILES READY FOR REVIEW
**Model:** Sonnet
**Date:** 2026-03-15
**Q33N Bot ID:** QUEEN-2026-03-15-BRIEFING-simdecisio

---

## Summary

I have read the briefing and the spec at `docs/specs/2026-03-15-0100-SPEC-simdecisions-applet-wiring.md`. The spec calls for three phases to wire the existing SimDecisions FlowDesigner (121 frontend files, 818-line component) into the ShiftCenter shell.

I have broken the work into **3 bee-sized tasks** aligned with the spec's three phases:

1. **TASK-140** (Phase 1, frontend-only): simAdapter.tsx + sim.egg.md + APP_REGISTRY entry — haiku model
2. **TASK-141** (Phase 2, backend engine wiring): Wire SimulationEngine into sim.py routes — sonnet model
3. **TASK-142** (Phase 3, cross-cutting tests): Integration tests for full stack — sonnet model

All task files are written to `.deia/hive/tasks/` and ready for Q33NR review.

---

## Task Files Written

### TASK-140: SimDecisions Shell Integration (Phase 1)
**File:** `.deia/hive/tasks/2026-03-15-TASK-140-sim-shell-integration.md`
**Model:** haiku (pattern-following, small)
**Scope:** Browser-only, no backend changes

**Deliverables:**
- Create `browser/src/apps/simAdapter.tsx` (40 lines, follows canvasAdapter.tsx pattern)
- Create `eggs/sim.egg.md` (100 lines, schema_version 3, single pane layout)
- Edit `browser/src/apps/index.ts` to add `registerApp('sim', SimAdapter)`

**Tests:**
- `browser/src/apps/__tests__/simAdapter.test.tsx` (mount test, props verification)
- `browser/src/shell/__tests__/resolveEgg.sim.test.tsx` (EGG resolution for `?egg=sim` and `/sim`)
- Minimum 6 tests

**Acceptance:**
- `localhost:5174/?egg=sim` renders FlowDesigner with toolbar, canvas, palette
- Can drag TASK node onto canvas
- No backend dependency (uses LocalDESEngine fallback)

---

### TASK-141: SimDecisions Engine Integration (Phase 2)
**File:** `.deia/hive/tasks/2026-03-15-TASK-141-sim-engine-integration.md`
**Model:** sonnet (engine integration, needs DES API understanding)
**Scope:** Backend routes only, no frontend changes

**Deliverables:**
- Edit `hivenode/routes/sim.py` to wire SimulationEngine into all 13 endpoints
- Replace all 503 stubs with real engine calls: load, start, pause, resume, step, status, tokens, resources, statistics, checkpoint, restore, fork, sweep, events
- Add `_running_tasks` dict for background task tracking
- Connect LedgerAdapter for event emission

**Tests:**
- `tests/hivenode/test_sim_engine_integration.py` (17 tests covering all endpoints)
- Unskip existing tests in `tests/hivenode/test_sim_routes.py`

**Acceptance:**
- `POST /sim/load` with demo flow returns 200 + run_id
- `POST /sim/start` starts simulation, status=running
- Pause/resume cycle works
- All 13 endpoints return real data (no 503s)

---

### TASK-142: SimDecisions Integration Tests (Phase 3)
**File:** `.deia/hive/tasks/2026-03-15-TASK-142-sim-integration-tests.md`
**Model:** sonnet (cross-cutting tests, full stack verification)
**Scope:** Test files only, no production code changes

**Deliverables:**
- `browser/src/apps/__tests__/simAdapter.integration.test.tsx` (4 tests, full mount)
- `browser/src/shell/__tests__/resolveEgg.sim.integration.test.tsx` (5 tests, EGG resolution)
- `tests/hivenode/test_sim_lifecycle.py` (6 tests, full lifecycle: load → start → pause → resume, checkpoint, fork, sweep)
- Edit `tests/hivenode/test_sim_routes.py` to remove skip decorators
- Verify all existing sim frontend tests still pass

**Tests:**
- Minimum 15 new tests across 3 files
- All unskipped existing tests must pass
- No regressions in sim component tests

**Acceptance:**
- Adapter integration test renders FlowDesigner with canvas, toolbar, palette
- EGG resolution confirms `?egg=sim` and `/sim` both resolve
- Lifecycle tests confirm load → start → pause → resume → status changes
- All existing tests green

---

## Task Sequence

**Phase 1 (TASK-140) is independent** — frontend loads even if backend is down (uses LocalDESEngine fallback).

**Phase 2 (TASK-141) depends on Phase 1** — engine integration requires adapter registration to be testable end-to-end.

**Phase 3 (TASK-142) depends on Phases 1 + 2** — integration tests verify both frontend and backend work together.

**Recommended dispatch order:**
1. TASK-140 (haiku, parallel-safe, no dependencies)
2. TASK-141 (sonnet, after TASK-140 completes)
3. TASK-142 (sonnet, after TASK-140 + TASK-141 complete)

---

## Constraints Verified

All task files enforce:
- ✅ No file over 500 lines (largest deliverable: sim.py remains under 500 lines)
- ✅ CSS: `var(--sd-*)` only (no CSS in this work)
- ✅ No stubs — every function fully implemented
- ✅ TDD — tests written first
- ✅ All file paths absolute
- ✅ Do NOT modify FlowDesigner.tsx or existing sim components (wrap and wire only)
- ✅ Do NOT modify `engine/des/` core files (import and call only)
- ✅ Phase 1 works independently (LocalDESEngine fallback)

---

## Model Assignments

| Task | Model | Reason |
|------|-------|--------|
| TASK-140 | haiku | Small, pattern-following (simAdapter follows canvasAdapter pattern) |
| TASK-141 | sonnet | Engine integration, needs to understand DES API and context dict pattern |
| TASK-142 | sonnet | Cross-cutting tests, full stack verification, lifecycle understanding |

---

## Key Files Referenced

All task files list required reading in "Files to Read First" section:
- `browser/src/apps/canvasAdapter.tsx` (32 lines, adapter pattern)
- `browser/src/apps/index.ts` (APP_REGISTRY)
- `eggs/code.egg.md` (EGG schema pattern)
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx` (existing component)
- `hivenode/routes/sim.py` (479 lines, routes to wire)
- `engine/des/engine.py` (SimulationEngine API)
- `engine/des/ledger_adapter.py` (event emission)
- Existing test files for patterns

---

## Estimated Test Counts

| Task | New Tests | Existing Tests |
|------|-----------|----------------|
| TASK-140 | 6 | All browser tests (1122) |
| TASK-141 | 17 | All hivenode tests (969) |
| TASK-142 | 15 | All sim component tests |
| **Total** | **38** | **2091+** |

---

## Next Steps — Awaiting Q33NR Review

**STATUS:** Task files ready for Q33NR review.

**Q33NR:** Please review the three task files:
1. `.deia/hive/tasks/2026-03-15-TASK-140-sim-shell-integration.md`
2. `.deia/hive/tasks/2026-03-15-TASK-141-sim-engine-integration.md`
3. `.deia/hive/tasks/2026-03-15-TASK-142-sim-integration-tests.md`

**Review checklist:**
- [ ] Deliverables complete vs spec?
- [ ] Missing test requirements?
- [ ] Hardcoded colors or stubs mentioned?
- [ ] Files over 500 lines?
- [ ] Imprecise file paths?
- [ ] Gaps vs briefing?

If corrections needed, I will fix and return. If approved, I will dispatch bees in sequence:
1. TASK-140 (haiku, background)
2. TASK-141 (sonnet, after TASK-140 completes)
3. TASK-142 (sonnet, after TASK-140 + TASK-141 complete)

---

## Clock / Cost / Carbon

- **Clock:** 8 minutes (read briefing + spec + 6 reference files + write 3 task files + response)
- **Cost:** ~$0.15 USD (sonnet read tokens + write tokens)
- **Carbon:** ~0.5g CO2e (estimated)

---

## Issues / Follow-ups

None. Task files complete and ready for review.
