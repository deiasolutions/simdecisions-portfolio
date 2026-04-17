# SPEC: Rebuild sim integration (routes, schema, app registration)

## Priority
P0.25

## Model Assignment
sonnet

## Objective
Re-apply sim integration changes from TASK-140 and TASK-141 that were lost in a git reset.

### TASK-140 changes (sim shell integration)
- `browser/src/apps/index.ts` — add SimAdapter import and registerApp('sim', ...) call
- `eggs/sim.egg.md` — sim EGG definition (may need recreation if the untracked version was also affected)

### TASK-141 changes (sim engine integration)
- `hivenode/routes/sim.py` — replace stubs with real engine calls (479 → 496 lines), add asyncio import, remove ImportError handling
- `hivenode/schemas_sim.py` — add checkpoint_id field to ForkRequest (215 → 217 lines)
- `tests/hivenode/test_sim_routes.py` — unskip 3 tests, update fixtures (290 → 292 lines)
- `engine/des/engine.py` — add QueueDiscipline import + dict-to-resource conversion in load()

## Recovery Sources
- `.deia/hive/responses/20260315-TASK-140-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-141-RESPONSE.md`
- `.deia/hive/tasks/2026-03-15-TASK-140-sim-shell-integration.md`
- `.deia/hive/tasks/2026-03-15-TASK-141-sim-engine-integration.md`

Feature inventory: `FEAT-140` (126 tests), `FEAT-141` (36 tests)
Platform source: `platform/efemera/src/efemera/des/` and `platform/simdecisions-2/`

**CRITICAL: Read the surviving test files — they define the expected behavior:**
- `browser/src/apps/__tests__/simModeStripAdapter.test.tsx` — shows sim adapter registration pattern
- `browser/src/apps/sim/components/flow-designer/__tests__/canvas.test.tsx` — shows FlowDesigner integration
- `browser/src/apps/sim/components/__tests__/` — all sim component tests survived
- `tests/hivenode/test_des_routes.py` — shows DES endpoint behavior
- Check `tests/hivenode/test_sim_routes.py` for the 3 tests that were unskipped

## Acceptance Criteria
- [ ] SimAdapter registered in browser/src/apps/index.ts
- [ ] sim.egg.md is correct and complete
- [ ] hivenode/routes/sim.py has real engine calls (no stubs)
- [ ] ForkRequest has checkpoint_id field
- [ ] All sim route tests pass (including previously-skipped 3)
- [ ] engine/des/engine.py has QueueDiscipline import
- [ ] No import errors

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-05-sim-integration", "status": "running", "model": "sonnet", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-05-sim-integration", "files": ["browser/src/apps/index.ts", "eggs/sim.egg.md", "hivenode/routes/sim.py", "hivenode/schemas_sim.py", "tests/hivenode/test_sim_routes.py", "engine/des/engine.py"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
