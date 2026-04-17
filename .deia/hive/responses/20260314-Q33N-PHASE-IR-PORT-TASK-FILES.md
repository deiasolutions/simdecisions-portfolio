# Q33N: PHASE-IR Port Task Files — Ready for Review

**Date:** 2026-03-14
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Briefing:** `.deia/hive/coordination/2026-03-14-BRIEFING-phase-ir-port.md`

---

## Summary

I have completed the survey and written **two task files** for the PHASE-IR + DES engine port:

1. **TASK-071:** Engine Port (PHASE-IR + DES) — copy source files, fix imports, port tests
2. **TASK-072:** Hivenode Sim Routes + Ledger Adapter — wire engine to ledger, write API routes, write tests

Both tasks are ready for Q33NR review and approval before dispatch.

---

## Survey Findings

### Old Repo Structure
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\`

**PHASE-IR Source:**
- Location: `src\efemera\phase_ir\`
- Key file: `primitives.py` (11 IR types: Flow, Node, Edge, Port, Token, Resource, Variable, Distribution, Timing, Group, Checkpoint)
- Other files: `bpmn_compiler.py`, `cli.py`, `formalism.py`, `mermaid.py`, `node_types.py`, `pie.py`, `schema.py`, `trace.py`, `validation.py` (NOT porting these per spec — v1.0 primitives only)

**DES Engine Source:**
- Location: `src\efemera\des\`
- **19 source files total** (excluding `engine_routes.py` which we'll rewrite):
  - Core engine: `core.py`, `engine.py`, `tokens.py`, `resources.py`, `statistics.py`, `variables.py`
  - Advanced features: `replay.py`, `sweep.py`, `replication.py`
  - Supporting modules: `checkpoints.py`, `dispatch.py`, `distributions.py`, `edges.py`, `generators.py`, `pools.py`, `loader_v2.py`, `trace_writer.py`
  - Package: `__init__.py`

**DES Tests:**
- Location: `tests\` (root level, NOT in `tests\des\` subdirectory)
- **20 test files** matching `test_des_*.py`:
  - `test_des_checkpoints.py`
  - `test_des_core.py`
  - `test_des_dispatch.py`
  - `test_des_durations.py`
  - `test_des_edges.py`
  - `test_des_engine.py`
  - `test_des_generators.py`
  - `test_des_guards.py`
  - `test_des_integration_phase_e.py`
  - `test_des_ledger_emission.py`
  - `test_des_loader_v2.py`
  - `test_des_pools.py`
  - `test_des_reneging.py`
  - `test_des_replay.py`
  - `test_des_replication.py`
  - `test_des_resources.py`
  - `test_des_statistics.py`
  - `test_des_sweep.py`
  - `test_des_tokens.py`
  - `test_des_trace_writer.py`
- **Estimated test count:** 270+ tests (spec states this, not verified per-file)

### New Repo Structure
**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\`

**Current state:**
- `engine\` directory exists, contains only `__init__.py` (1 byte)
- `tests\engine\` does not exist yet
- `hivenode\routes\__init__.py` — existing route registry, ready for sim routes
- `hivenode\ledger\writer.py` — existing ledger interface

---

## Task File 1: TASK-071 (Engine Port)

**File:** `.deia\hive\tasks\2026-03-14-TASK-071-engine-port-phase-ir-des.md`

**Bee:** Sonnet (mechanical but large file count)

**Deliverables:**
- Port PHASE-IR `primitives.py` → `engine\phase_ir\primitives.py`
- Port 19 DES source files → `engine\des\`
- Fix ALL imports: `from efemera.` → `from engine.`
- Write 3 package `__init__.py` files with exports
- Port 20 test files → `tests\engine\des\`
- Run tests: `cd tests/engine && python -m pytest des/ -v`
- **Target:** 270+ tests passing

**Key constraints:**
- DO NOT port `engine_routes.py` (TASK-072 rewrites this)
- DO NOT port any `ledger.py` (TASK-072 rewrites this)
- No modifications, pure copy + fix imports
- Document any test failures (expected if ledger interface changes)
- Flag any files over 500 lines

**Estimated effort:** 2 hours (mechanical, large file count, test verification)

---

## Task File 2: TASK-072 (Sim Routes + Adapter)

**File:** `.deia\hive\tasks\2026-03-14-TASK-072-hivenode-sim-routes-adapter.md`

**Bee:** Sonnet (design + implementation)

**Deliverables:**
- Write `engine\des\ledger_adapter.py` — bridges DES events to hivenode Event Ledger
  - 9 event type mappings (token_create → SIM_TOKEN_CREATED, etc.)
  - Three currencies: CLOCK (sim_time), COIN (0), CARBON (0.001 * events)
  - Universal entity ID format: actor=`sim:{run_id}`, target=`{type}:{id}`
- Write `hivenode\routes\sim.py` — 16 FastAPI routes:
  - /sim/load, /sim/start, /sim/pause, /sim/resume
  - /sim/step, /sim/step/{n}
  - /sim/status, /sim/inject
  - /sim/checkpoint, /sim/restore, /sim/fork
  - /sim/tokens, /sim/resources, /sim/statistics, /sim/events
  - /sim/sweep
- Write `hivenode\schemas_sim.py` — ~32 Pydantic models (request/response for each route)
- Register routes in `hivenode\routes\__init__.py`
- Write `tests\engine\des\test_ledger_adapter.py` — 10+ tests
- Write `tests\hivenode\test_sim_routes.py` — 10+ E2E tests
- **Target:** 20+ new tests passing

**Key constraints:**
- TDD: tests first, then implementation
- No file over 500 lines (split if needed)
- All events MUST include three currencies
- No stubs (every route functional)
- Use global dict for engine instances (MVP pattern, future: state manager)

**Estimated effort:** 1.5 hours (design + TDD + tests)

---

## Parallel Execution Strategy

**Independence:** The two tasks are independent:
- TASK-071 ports code, fixes imports, verifies tests
- TASK-072 writes new code (adapter + routes + tests)
- No file overlap
- TASK-072 can read old repo's engine files if TASK-071 not done yet

**Recommendation:** Dispatch both bees in parallel for ~2 hour wall time (instead of 3.5 hours sequential).

---

## Files Read During Survey

1. ✅ `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` — full technical spec (267 lines)
2. ✅ `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — ledger interface
3. ✅ `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` — route registry
4. ✅ `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` — app structure
5. ✅ Surveyed `platform\efemera\src\efemera\des\` — identified 19 source files
6. ✅ Surveyed `platform\efemera\tests\` — identified 20 test_des_*.py files
7. ✅ `.deia\BOOT.md` and `.deia\HIVE.md` — workflow rules

---

## Acceptance Criteria Distributed Across Tasks

From the spec's section 11 acceptance criteria:

**TASK-071 (Engine Port):**
- [ ] `from engine.des import SimulationEngine` works
- [ ] `from engine.phase_ir.primitives import Flow, Node, Edge` works
- [ ] 270+ existing DES tests pass in new location
- [ ] No file over 500 lines (flag if needed, document in response)

**TASK-072 (Routes + Adapter):**
- [ ] Sim can load a simple IR flow (3 nodes, 2 edges), run to completion
- [ ] Event Ledger receives SIM_* events during simulation
- [ ] All 16 hivenode sim routes respond correctly
- [ ] `/sim/load` + `/sim/start` + `/sim/status` E2E test passes
- [ ] 20+ new tests for ledger adapter and sim routes

**Both tasks:**
- [ ] No file over 500 lines (hard limit: 1,000)

---

## Critical Constraints Verified

✅ **PHASE-IR v1.0 ONLY** — task files specify no v2.0 features
✅ **Do NOT port:** production/tabletop/optimization engines — task files exclude these
✅ **Import paths:** All `from efemera.` → `from engine.` — task files enforce this
✅ **File size:** No file over 500 lines, hard limit 1,000 — task files enforce this
✅ **Parallel bees:** Two independent tasks — task files confirmed no overlap
✅ **Model assignment:** Both sonnet — correct per briefing
✅ **TDD:** TASK-072 enforces tests first — TASK-071 is pure port (tests already exist)
✅ **No stubs:** Task files enforce full implementation

---

## Known Risks / Issues

1. **Test failures expected in TASK-071:**
   - `test_des_ledger_emission.py` may fail if old repo's ledger interface differs
   - TASK-071 task file instructs bee to document failures, not block on them
   - TASK-072's E2E tests will verify the full system works

2. **Engine instance state management:**
   - TASK-072 uses global dict (MVP pattern)
   - Task file notes this should be Redis/DB in production (future task)
   - Adequate for alpha/beta

3. **Blocking I/O in sim routes:**
   - `engine.run()` is blocking
   - TASK-072 task file notes to use `asyncio.to_thread()` or remove `async`
   - Edge case for long simulations (future: background workers)

4. **File size risk:**
   - Some old repo files are large (e.g., `core.py` ~24KB, `tokens.py` ~21KB, `resources.py` ~22KB)
   - TASK-071 instructs bee to flag files over 500 lines, document for future refactor
   - Hard limit 1,000 lines — if exceeded, bee MUST split before committing

---

## Next Steps — Awaiting Q33NR Approval

**Q33NR:** Please review the two task files:
1. `.deia\hive\tasks\2026-03-14-TASK-071-engine-port-phase-ir-des.md`
2. `.deia\hive\tasks\2026-03-14-TASK-072-hivenode-sim-routes-adapter.md`

**Check for:**
- Missing deliverables
- Vague acceptance criteria
- Incomplete test requirements
- Missing file paths
- Gaps vs the briefing

**If approved:** I will dispatch both bees in parallel with these commands:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-TASK-071-engine-port-phase-ir-des.md --model sonnet --role bee --inject-boot --timeout 7200

python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-14-TASK-072-hivenode-sim-routes-adapter.md --model sonnet --role bee --inject-boot --timeout 5400
```

**If corrections needed:** Please specify what to fix and I will revise the task files.

---

**Q33N awaiting Q33NR review and approval to dispatch.**
