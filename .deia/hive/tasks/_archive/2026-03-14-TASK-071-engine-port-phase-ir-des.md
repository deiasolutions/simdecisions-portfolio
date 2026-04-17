# TASK-071: Engine Port — PHASE-IR + DES Runtime

## Objective

Port the PHASE-IR primitives and DES simulation engine from the legacy `platform/efemera` repository into the shiftcenter `engine/` directory. Fix all imports, write package inits, port tests, and verify 270+ existing tests pass.

## Context

ShiftCenter is porting the PHASE-IR v1.0 specification and DES (Discrete Event Simulation) execution engine from the old `platform/efemera` repo. This is a mechanical port: copy source files, fix import paths (`from efemera.` → `from engine.`), copy tests, verify all tests pass.

**Old Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\`
- PHASE-IR source: `src\efemera\phase_ir\`
- DES source: `src\efemera\des\` (19 .py files)
- DES tests: `tests\test_des_*.py` (20 test files)

**New Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\`
- Target directory: `engine\` (currently contains only `__init__.py`)
- Test directory: `tests\engine\` (will be created)

**DO NOT port:**
- `engine_routes.py` (will be rewritten in TASK-072)
- Any `ledger.py` (will be rewritten in TASK-072)
- Production engine (`efemera/production/`)
- Tabletop engine (`efemera/tabletop/`)
- Optimization/OR-Tools (`efemera/optimization/`)

**PHASE-IR v1.0 only:** No v2.0 features. The DES engine uses v1.0 primitives.

## Files to Read First

1. `C:\Users\davee\Downloads\SPEC-PHASE-IR-PORT-001.md` — full technical spec
2. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\primitives.py` — IR primitives
3. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\__init__.py` — DES exports
4. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\core.py` — event loop
5. `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\engine.py` — SimulationEngine
6. Survey all files in `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\des\` to identify what to port
7. Survey all files in `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\` matching `test_des_*.py`

## Deliverables

### Phase 1: PHASE-IR Primitives Port
- [ ] Copy `platform\efemera\src\efemera\phase_ir\primitives.py` → `shiftcenter\engine\phase_ir\primitives.py`
- [ ] Fix all imports in `primitives.py`: `from efemera.` → `from engine.`
- [ ] Write `engine\phase_ir\__init__.py` with exports: `Flow`, `Node`, `Edge`, `Port`, `Token`, `Resource`, `Variable`, `Distribution`, `Timing`, `Group`, `Checkpoint`
- [ ] Verify `from engine.phase_ir.primitives import Flow, Node, Edge` works

### Phase 2: DES Engine Port
- [ ] Create `engine\des\` directory
- [ ] Copy all DES source files from `platform\efemera\src\efemera\des\` to `shiftcenter\engine\des\` **EXCEPT:**
  - `engine_routes.py` (skip this, will be rewritten in TASK-072)
  - Any `ledger.py` (skip this, will be rewritten in TASK-072)
- [ ] Files to copy (verify each exists before copying):
  - `core.py` (event loop, priority queue, SimulationClock, SimConfig, EngineState)
  - `engine.py` (SimulationEngine class)
  - `tokens.py` (12-state token FSM, TokenRegistry)
  - `resources.py` (ResourceManager, queue disciplines)
  - `statistics.py` (Welford stats, Little's Law, time-weighted averages)
  - `variables.py` (VariableManager, watch expressions)
  - `replay.py` (trace replay from Event Ledger)
  - `sweep.py` (parameter sweep, sensitivity analysis)
  - `replication.py` (multi-replication runner, CI aggregation)
  - `checkpoints.py` (checkpoint save/restore)
  - `dispatch.py` (resource dispatch logic)
  - `distributions.py` (probability distributions)
  - `edges.py` (edge traversal logic)
  - `generators.py` (token generators)
  - `pools.py` (resource pools)
  - `loader_v2.py` (PHASE-IR loader)
  - `trace_writer.py` (trace writer)
- [ ] Fix ALL imports in all copied DES files:
  - `from efemera.des import X` → `from engine.des import X`
  - `from efemera.phase_ir import Y` → `from engine.phase_ir import Y`
  - `from efemera.X import Z` → (check if X was ported; if not, note in response file)
- [ ] Write `engine\des\__init__.py` with exports for all major classes (at minimum: `SimulationEngine`, `TokenRegistry`, `ResourceManager`, `SimConfig`, `EngineState`)
- [ ] Write `engine\__init__.py` as package root

### Phase 3: Test Port
- [ ] Create `tests\engine\des\` directory
- [ ] Copy ALL test files matching `test_des_*.py` from `platform\efemera\tests\` to `shiftcenter\tests\engine\des\`
- [ ] Expected test files (verify each exists):
  - `test_des_checkpoints.py`
  - `test_des_core.py`
  - `test_des_dispatch.py`
  - `test_des_durations.py`
  - `test_des_edges.py`
  - `test_des_engine.py`
  - `test_des_generators.py`
  - `test_des_guards.py`
  - `test_des_integration_phase_e.py`
  - `test_des_ledger_emission.py` (may need to skip/stub if ledger interface changes)
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
- [ ] Fix ALL imports in all test files:
  - `from efemera.des import X` → `from engine.des import X`
  - `from efemera.phase_ir import Y` → `from engine.phase_ir import Y`
- [ ] Copy `conftest.py` from old repo if DES tests depend on it (verify first)
- [ ] Write `tests\engine\__init__.py` (empty, just marks package)
- [ ] Write `tests\engine\des\__init__.py` (empty, just marks package)

### Phase 4: Test Execution
- [ ] Run: `cd tests/engine && python -m pytest des/ -v`
- [ ] **Target:** 270+ tests passing
- [ ] If any tests fail:
  - Document each failure in response file (test name, error message, root cause)
  - If failure is due to ledger interface changes, note in response (TASK-072 will fix)
  - If failure is due to missing imports, fix imports and rerun
  - If failure is unrelated to port, document as pre-existing (verify in old repo)

## Test Requirements

- [ ] Tests written FIRST (TDD) — **N/A for this task** (pure port, tests already exist)
- [ ] All ported tests pass (270+ target)
- [ ] Edge cases:
  - Test files that import ledger/routes should be noted if they fail
  - Test files that import other efemera modules (not ported) should be noted
  - Test files that depend on old repo fixtures should have fixtures copied

## Constraints

- **No file over 500 lines:** If any ported file exceeds 500 lines, document in response file. Do NOT split files in this task (flag for future refactor).
- **Hard limit: 1,000 lines:** If any file exceeds 1,000 lines, split it before committing.
- **PHASE-IR v1.0 only:** Do NOT add v2.0 features.
- **No stubs:** If a function is incomplete in the old repo, port it as-is. Document incomplete functions in response file.
- **Import paths:** ALL `from efemera.` must become `from engine.` or external imports.
- **No code modifications:** This is a mechanical port. Copy + fix imports only. Do NOT refactor, improve, or add features.

## Acceptance Criteria

- [ ] `from engine.des import SimulationEngine` works
- [ ] `from engine.phase_ir.primitives import Flow, Node, Edge` works
- [ ] All 19 DES source files copied (excluding `engine_routes.py` and `ledger.py`)
- [ ] All 20 test files copied
- [ ] 270+ existing DES tests pass in new location (or documented failures with root cause)
- [ ] All imports fixed (no `from efemera.` remains)
- [ ] `engine/__init__.py`, `engine/phase_ir/__init__.py`, `engine/des/__init__.py` exist with correct exports
- [ ] No file over 1,000 lines (flag files over 500 in response)
- [ ] Response file lists every ported file (source + tests)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-071-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts, failure details
5. **Build Verification** — pytest output summary (last 10 lines)
6. **Acceptance Criteria** — copy from above, mark [x] or [ ] with explanation
7. **Clock / Cost / Carbon** — all three currencies
8. **Issues / Follow-ups** — any files over 500 lines, any test failures, any missing imports

DO NOT skip any section.

## Notes

- **Parallel with TASK-072:** This task is independent of TASK-072. Both can run simultaneously.
- **Ledger interface:** TASK-072 will write `engine/des/ledger_adapter.py` to bridge to hivenode ledger. This task does NOT touch ledger code.
- **Routes:** TASK-072 will write `hivenode/routes/sim.py`. This task does NOT touch routes.
- **Test failures OK if documented:** If tests fail due to ledger interface changes, document them. TASK-072 integration tests will verify the full system.
