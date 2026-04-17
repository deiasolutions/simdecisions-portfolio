# TASK-160: Port entity updates

## Objective
Port entity update logic from platform to shiftcenter. Incremental updates (<100ms target), nightly recalculation (batch with 30-day decay), cold-start cascade (multi-level fallback for new entities).

## Context
Entity updates are the core of the entity vector system. Two update modes:

1. **Incremental update** — lightweight, triggered after a single event (e.g., bot sends message). Updates entity vectors quickly (<100ms) without full recomputation. Uses cached components where possible.

2. **Nightly recalculation** — batch process that recalculates all entity vectors from scratch, applying 30-day decay to event weights. Runs once per day via scheduler. Ensures vectors stay fresh and decay old signal.

3. **Cold-start cascade** — multi-level fallback for new entities with no event history. Falls back through: domain archetype → similar entities → global baseline.

**Platform source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\updates.py` (394 lines)

**Target file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\updates.py` (NEW)

**Key features to port:**
- `incremental_update(entity_id, event_type, db)` — lightweight update after single event
- `nightly_recalculation(db)` — batch recalc for all entities with 30-day decay
- `cold_start_cascade(entity_id, domain, db)` — multi-level fallback for new entities
- `get_cold_start_status(entity_id, db)` — diagnostic function, returns which fallback level was used
- Helper functions for event fetching, decay calculation, component aggregation

**Dependencies:**
- `hivenode.entities.vectors_core` (EntityProfile, EntityComponent, EntityVectorHistory models) — already ported
- `hivenode.entities.vectors_compute` (alpha, sigma, rho computation, decay logic) — already ported
- `engine.events.ledger` (event query functions) — already ported
- `hivenode.entities.archetypes` (for cold-start fallback to domain archetype) — **TASK-159 dependency**

**Important:** This task depends on TASK-159 (archetypes.py) completing first. The cold-start cascade needs `get_current_archetype()` from archetypes.py.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\updates.py` (source file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_core.py` (ORM models, helper functions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_compute.py` (alpha, sigma, rho computation, decay)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetypes.py` (newly created by TASK-159)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\events\ledger.py` (event query functions)

## Deliverables
- [ ] `hivenode\entities\updates.py` created with full implementation (no stubs)
- [ ] `incremental_update()` function fully implemented (target: <100ms execution time)
- [ ] `nightly_recalculation()` function fully implemented (batch processes all entities)
- [ ] `cold_start_cascade()` function fully implemented (domain archetype → similar entities → global baseline)
- [ ] `get_cold_start_status()` function fully implemented (returns diagnostic info)
- [ ] All helper functions ported (event fetching, decay calculation, component aggregation)
- [ ] Proper error handling (missing entity, missing domain archetype, database failures)
- [ ] Logging for batch operations (info level for progress, debug for details)
- [ ] File size under 500 lines (platform source is 394, should fit comfortably)
- [ ] All functions return proper types (no `Any`, no placeholders)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test file: `tests\hivenode\entities\test_updates.py`
- [ ] All tests pass
- [ ] Test count target: 20-25 tests minimum
- [ ] Edge cases:
  - Incremental update with no prior history → creates new EntityProfile
  - Incremental update with existing profile → updates in-place
  - Incremental update performance (<100ms target) → measure execution time
  - Nightly recalc with no entities → completes without error
  - Nightly recalc with 100 entities → processes all successfully
  - Cold-start cascade with no domain archetype → falls back to similar entities
  - Cold-start cascade with no similar entities → falls back to global baseline
  - Cold-start cascade with domain archetype → uses archetype
  - 30-day decay applied correctly (verify event weights decrease over time)
  - Database transaction rollback on error
  - Concurrent incremental updates (thread safety)
- [ ] Test incremental update speed (must be <100ms for single event)
- [ ] Test nightly recalc batch processing (verify all entities updated)
- [ ] Test cold-start fallback chain (mock missing archetype, verify next fallback)
- [ ] Mock event ledger queries for deterministic test data
- [ ] Verify EntityVectorHistory records created after each update

## Constraints
- No file over 500 lines (platform source is 394, port should be similar — if grows >450, split into updates_core.py + updates_batch.py)
- CSS: var(--sd-*) only (not applicable, backend only)
- No stubs — every function fully implemented
- TDD: tests first, then implementation
- Incremental update must target <100ms execution time (log warning if exceeds)
- Nightly recalc must handle large entity counts (batch process, don't load all into memory)
- Use SQLAlchemy session properly (commit after updates, rollback on error)
- All imports must use absolute paths (`from hivenode.entities.vectors_core import ...`)
- Follow existing entity file patterns (see `vectors_core.py`, `vectors_compute.py`)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-160-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Test Commands

```bash
# Run update tests only
python -m pytest tests/hivenode/entities/test_updates.py -v

# Run all entity tests (verify no regressions)
python -m pytest tests/hivenode/entities/ -v

# Performance test (incremental update speed)
python -m pytest tests/hivenode/entities/test_updates.py::test_incremental_update_performance -v
```

## Model Assignment
Sonnet (complex decay logic, batch processing, performance requirements)

## Priority
P0.55 (critical path for entity vectors MVP)

## Dependencies
**BLOCKED BY:** TASK-159 (archetypes.py must exist for cold-start cascade)
