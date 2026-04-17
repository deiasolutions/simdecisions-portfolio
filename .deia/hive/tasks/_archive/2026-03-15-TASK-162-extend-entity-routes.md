# TASK-162: Extend entity routes

## Objective
Add archetype, update, and vector API routes to entity module. Create 3 new route files (archetype_routes.py, update_routes.py, vector_routes.py) to avoid exceeding 500-line limit. Register all routes in hivenode app.

## Context
Currently, only bot embedding routes exist in `hivenode/entities/routes.py` (3 endpoints: register, pi, drift check). This task adds 9 new endpoints across 3 route files:

**Archetype routes** (4 endpoints):
- POST `/api/domains/{domain}/archetype/refresh` — generate new archetype via tribunal
- GET `/api/domains/{domain}/archetype` — get current archetype
- GET `/api/domains/{domain}/archetype/history` — get archetype history
- POST `/api/domains/{domain}/archetype/check-drift` — check embedding drift

**Update routes** (3 endpoints):
- POST `/api/entities/{entity_id}/events/{event_type}` — trigger incremental update
- POST `/api/admin/nightly-recalc` — trigger nightly recalculation
- GET `/api/entities/{entity_id}/cold-start-status` — get cold start status

**Vector routes** (2 endpoints):
- POST `/api/entities/{entity_id}/recalc` — full recalculation
- POST `/api/entities/{entity_id}/domains/{domain}/recalc` — domain-specific recalc

**Platform sources:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetype_routes.py` (123 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\update_routes.py` (112 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\vector_routes.py` (81 lines)

**Target files:** (NEW)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetype_routes.py` (~150 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\update_routes.py` (~130 lines)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vector_routes.py` (~100 lines)

**Existing file to keep as-is:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py` (215 lines, bot embedding routes only)

**Dependencies:**
- `hivenode.entities.archetypes` (TASK-159)
- `hivenode.entities.updates` (TASK-160)
- `hivenode.entities.scheduler` (TASK-161)
- `hivenode.dependencies` (verify_jwt_or_local for auth)
- `engine.database` (get_db for session injection)

**Important:** This task depends on TASK-159, TASK-160, and TASK-161 completing first. All business logic functions must exist before wiring routes.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetype_routes.py` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\update_routes.py` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\vector_routes.py` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py` (existing pattern reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetypes.py` (TASK-159)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\updates.py` (TASK-160)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\scheduler.py` (TASK-161)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (for route registration pattern)

## Deliverables
- [ ] `hivenode\entities\archetype_routes.py` created with 4 endpoints (no stubs)
- [ ] `hivenode\entities\update_routes.py` created with 3 endpoints (no stubs)
- [ ] `hivenode\entities\vector_routes.py` created with 2 endpoints (no stubs)
- [ ] All Pydantic request/response schemas defined in each route file
- [ ] Proper HTTP status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Server Error)
- [ ] Error handling for business logic failures (missing archetype, invalid entity_id, etc.)
- [ ] Auth enforcement via `verify_jwt_or_local` dependency (local bypasses, cloud requires JWT)
- [ ] Database session injection via `Depends(get_db)`
- [ ] Route registration in `hivenode\routes\__init__.py` (add all 3 routers)
- [ ] OpenAPI tags for route grouping ("archetype", "entity-updates", "entity-vectors")
- [ ] File sizes under 500 lines each (archetype ~150, update ~130, vector ~100)
- [ ] All endpoints return proper JSON responses (use Pydantic response models)

### Archetype Routes Deliverables
- [ ] POST `/api/domains/{domain}/archetype/refresh` — returns `ArchetypeResponse` (archetype_id, domain, embedding_hash, consensus_method, created_at)
- [ ] GET `/api/domains/{domain}/archetype` — returns `ArchetypeResponse` or 404 if none exists
- [ ] GET `/api/domains/{domain}/archetype/history` — returns `List[ArchetypeResponse]`
- [ ] POST `/api/domains/{domain}/archetype/check-drift` — accepts `CheckDriftRequest(entity_id)`, returns `DriftResponse(similarity: float, drift_detected: bool)`

### Update Routes Deliverables
- [ ] POST `/api/entities/{entity_id}/events/{event_type}` — triggers incremental update, returns `UpdateResponse(entity_id, updated_at, execution_time_ms)`
- [ ] POST `/api/admin/nightly-recalc` — triggers nightly recalc (admin only via auth), returns `RecalcResponse(entities_updated: int, execution_time_ms)`
- [ ] GET `/api/entities/{entity_id}/cold-start-status` — returns `ColdStartStatus(entity_id, fallback_level: str, source: str)`

### Vector Routes Deliverables
- [ ] POST `/api/entities/{entity_id}/recalc` — full recalc (optional query param `domain`), returns `RecalcResponse(entity_id, domains_updated: List[str])`
- [ ] POST `/api/entities/{entity_id}/domains/{domain}/recalc` — domain-specific recalc, returns `RecalcResponse`

### Route Registration Deliverable
- [ ] Update `hivenode\routes\__init__.py`:
  ```python
  from hivenode.entities.archetype_routes import router as archetype_router
  from hivenode.entities.update_routes import router as update_router
  from hivenode.entities.vector_routes import router as vector_router

  app.include_router(archetype_router)
  app.include_router(update_router)
  app.include_router(vector_router)
  ```

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test files:
  - `tests\hivenode\entities\test_archetype_routes.py`
  - `tests\hivenode\entities\test_update_routes.py`
  - `tests\hivenode\entities\test_vector_routes.py`
- [ ] All tests pass
- [ ] Test count target: 15-18 tests minimum (5-6 per route file)
- [ ] Edge cases per route group:
  - **Archetype routes:**
    - Refresh with no candidates → 400 Bad Request
    - Get archetype for nonexistent domain → 404 Not Found
    - Check drift with invalid entity_id → 404 Not Found
    - History for domain with no archetypes → returns empty list
  - **Update routes:**
    - Incremental update with missing entity → creates new entity
    - Nightly recalc with no entities → returns 0 entities updated
    - Cold-start status for entity with full history → returns "full_history"
    - Admin route without auth (cloud mode) → 401 Unauthorized
  - **Vector routes:**
    - Recalc with invalid domain → 400 Bad Request
    - Recalc for entity with no events → falls back to cold-start
- [ ] Test request validation (invalid JSON, missing required fields)
- [ ] Test response schemas (verify Pydantic models serialize correctly)
- [ ] Mock business logic functions (archetypes.py, updates.py functions)
- [ ] Use FastAPI TestClient for endpoint testing
- [ ] Verify database transactions (session commit/rollback)

## Constraints
- No file over 500 lines (split into 3 route files to stay under limit)
- CSS: var(--sd-*) only (not applicable, backend only)
- No stubs — every endpoint fully implemented
- TDD: tests first, then implementation
- All routes must enforce auth via `verify_jwt_or_local` (local bypasses, cloud requires JWT)
- Admin routes (nightly-recalc) require additional permission check if admin role system exists
- All imports must use absolute paths (`from hivenode.entities.archetypes import ...`)
- Follow existing route file patterns (see `hivenode/entities/routes.py`, `hivenode/routes/des_routes.py`)
- Use Pydantic BaseModel for request/response schemas (not dataclasses — those are for internal logic)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-162-RESPONSE.md`

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
# Run archetype route tests
python -m pytest tests/hivenode/entities/test_archetype_routes.py -v

# Run update route tests
python -m pytest tests/hivenode/entities/test_update_routes.py -v

# Run vector route tests
python -m pytest tests/hivenode/entities/test_vector_routes.py -v

# Run all entity tests (verify no regressions)
python -m pytest tests/hivenode/entities/ -v

# Verify route registration (check hivenode startup)
python -m pytest tests/hivenode/test_routes.py -v
```

## Model Assignment
Haiku (route wiring, no complex logic — business logic already in TASK-159, 160, 161)

## Priority
P0.55 (critical path for entity vectors MVP)

## Dependencies
**BLOCKED BY:**
- TASK-159 (archetypes.py must exist)
- TASK-160 (updates.py must exist)
- TASK-161 (scheduler.py must exist)

## Additional Notes
After this task completes, the entity vector system will have full API coverage:
- Bot embedding routes (existing)
- Archetype management routes (new)
- Entity update routes (new)
- Vector computation routes (new)

The scheduler (TASK-161) needs to be started on app init. If not already done in TASK-161, add to `hivenode/main.py`:
```python
from hivenode.entities.scheduler import EntityScheduler

@app.on_event("startup")
async def startup_scheduler():
    EntityScheduler().start()

@app.on_event("shutdown")
async def shutdown_scheduler():
    EntityScheduler().stop()
```
