# Gap Analysis and Task Breakdown: RAG Entity Vectors + BOK Integration

**From:** Q33N (queen coordinator)
**To:** Q33NR (regent)
**Date:** 2026-03-15
**Bot ID:** QUEEN-2026-03-15-BRIEFING-rag-entity
**Spec:** 2026-03-15-1305-SPEC-w1-11-rag-entity-vectors

---

## Executive Summary

I have completed the gap analysis comparing shiftcenter's current entity vectors and BOK implementation with the platform source repo. Below is my assessment and proposed task breakdown.

**Key Finding:** Most core entity vector computation is already ported. The missing pieces are:
1. **Entity archetypes** (domain archetype management, tribunal consensus)
2. **Entity updates** (incremental updates, nightly recalculation, cold-start cascade)
3. **Entity scheduler** (APScheduler background job for nightly recalc)
4. **Additional routes** (archetype, update, vector routes — currently only bot embedding routes exist)
5. **BOK advanced features** (file ingest, spec reviewer, submission workflows — currently only basic search/enrich)

**Line Count Summary:**

| Area | Platform (lines) | Shiftcenter (lines) | Gap |
|------|-----------------|---------------------|-----|
| Entity files | 2,935 | 1,672 | 1,263 missing |
| BOK files | 878 | 306 | 572 missing |
| **Total** | **3,813** | **1,978** | **1,835 missing** |

---

## Gap Analysis: Entity Vectors

### ✅ Already Ported (COMPLETE)

**File:** `hivenode/entities/voyage_embedding.py` (171 lines)
- Voyage AI client with caching
- Status: COMPLETE ✓

**File:** `hivenode/entities/embeddings.py` (314 lines)
- BotEmbeddingStore
- Drift detection
- Pi computation
- Status: COMPLETE ✓

**File:** `hivenode/entities/vectors_core.py` (428 lines)
- EntityProfile, EntityComponent, EntitySLAConfig, EntityVectorHistory ORM models
- Helper functions for event queries, SLA lookups
- Cold-start cascade
- Confidence computation
- Global vector aggregation
- Status: COMPLETE ✓

**File:** `hivenode/entities/vectors_compute.py` (490 lines)
- Alpha, sigma, rho computation
- 30-day decay logic
- Status: COMPLETE (needs verification that all platform functions are present) ✓

**File:** `hivenode/entities/routes.py` (215 lines)
- Bot embedding routes only (`/api/bots/*`)
- 3 endpoints: register, pi, check-drift
- Status: PARTIAL (missing archetype, update, vector routes)

**Tests:**
- `tests/hivenode/entities/test_embeddings.py` ✓
- `tests/hivenode/entities/test_routes.py` ✓
- `tests/hivenode/entities/test_vectors.py` ✓
- `tests/hivenode/entities/test_voyage_embedding.py` ✓

### ❌ Missing (NEEDS PORTING)

**1. Entity Archetypes**
- Platform file: `platform/efemera/src/efemera/entities/archetypes.py` (432 lines)
- Target file: `hivenode/entities/archetypes.py` (NEW)
- Features:
  - DomainArchetype ORM model
  - ArchetypeCandidate, ConsensusResult dataclasses
  - Four consensus methods (majority, weighted avg, LLM synthesis, human select)
  - generate_archetype, get_current_archetype, check_drift functions
  - hash_embedding, cosine_similarity helpers
- Dependencies: engine/database.py (already ported), LLM provider integration

**2. Entity Updates**
- Platform file: `platform/efemera/src/efemera/entities/updates.py` (419 lines)
- Target file: `hivenode/entities/updates.py` (NEW)
- Features:
  - incremental_update (lightweight update after single event, <100ms target)
  - nightly_recalculation (full batch recalc for all entities with decay)
  - cold_start_cascade (multi-level fallback for new entities)
  - get_cold_start_status (diagnostic function)
- Dependencies: vectors_core.py (ported), vectors_compute.py (ported), engine/events/ledger.py (ported)

**3. Entity Scheduler**
- Platform file: `platform/efemera/src/efemera/entities/scheduler.py` (232 lines)
- Target file: `hivenode/entities/scheduler.py` (NEW)
- Features:
  - APScheduler BackgroundScheduler wrapper
  - Cron job for nightly recalculation (default: 02:00 UTC)
  - API endpoints: start, stop, status, trigger-now
- Dependencies: updates.py (not yet ported), APScheduler library (needs pyproject.toml addition)

**4. Archetype Routes**
- Platform file: `platform/efemera/src/efemera/entities/archetype_routes.py` (123 lines)
- Target: merge into `hivenode/entities/routes.py` OR create separate file
- Endpoints:
  - POST `/api/domains/{domain}/archetype/refresh` (generate new archetype via tribunal)
  - GET `/api/domains/{domain}/archetype` (get current archetype)
  - GET `/api/domains/{domain}/archetype/history` (get archetype history)
  - POST `/api/domains/{domain}/archetype/check-drift` (check embedding drift)

**5. Embedding Routes**
- Platform file: `platform/efemera/src/efemera/entities/embedding_routes.py` (143 lines)
- Status: ALREADY IN routes.py (bot embedding routes exist)
- Action: VERIFY completeness, no new porting needed ✓

**6. Update Routes**
- Platform file: `platform/efemera/src/efemera/entities/update_routes.py` (112 lines)
- Target: merge into `hivenode/entities/routes.py` OR create separate file
- Endpoints:
  - POST `/api/entities/{entity_id}/events/{event_type}` (trigger incremental update)
  - POST `/api/admin/nightly-recalc` (trigger nightly recalculation)
  - GET `/api/entities/{entity_id}/cold-start-status` (get cold start status)

**7. Vector Routes**
- Platform file: `platform/efemera/src/efemera/entities/vector_routes.py` (81 lines)
- Target: merge into `hivenode/entities/routes.py` OR create separate file
- Endpoints:
  - POST `/api/entities/{entity_id}/recalc` (full recalculation, optional domain query)
  - POST `/api/entities/{entity_id}/domains/{domain}/recalc` (domain-specific recalc)

---

## Gap Analysis: BOK (Body of Knowledge)

### ✅ Already Ported (COMPLETE)

**File:** `hivenode/rag/bok/rag_service.py` (107 lines)
- search_bok (keyword search)
- format_bok_for_prompt
- enrich_prompt
- Status: COMPLETE ✓

**File:** `hivenode/rag/bok/embedding_service.py` (44 lines)
- generate_embedding (Voyage AI)
- Status: COMPLETE ✓

**File:** `hivenode/rag/bok/models.py` (28 lines)
- BokEntry ORM model
- Status: COMPLETE (but missing Pydantic schemas from platform) ⚠️

**File:** `hivenode/rag/bok/routes.py` (partial)
- GET `/rag/bok/search` (search BOK)
- POST `/rag/bok/enrich` (enrich prompt)
- Status: PARTIAL (missing ingest, review, submission endpoints)

**Tests:**
- `tests/hivenode/rag/bok/test_bok_services.py` ✓

### ❌ Missing (NEEDS PORTING)

**1. BOK Models (Pydantic Schemas)**
- Platform file: `platform/efemera/src/efemera/bok/models.py` (69 lines)
- Target: add to `hivenode/rag/bok/models.py` (expand existing file)
- Features:
  - BokEntryCreate, BokEntryUpdate, BokEntryResponse Pydantic schemas
  - Entry type enums
  - Validation rules

**2. BOK File Ingest**
- Platform file: `platform/efemera/src/efemera/bok/file_ingest.py` (117 lines)
- Target: `hivenode/rag/bok/file_ingest.py` (NEW)
- Features:
  - scan_bok_directory (scans filesystem for markdown/text files)
  - parse BOK entries from files
  - bulk ingestion with deduplication

**3. BOK Spec Reviewer**
- Platform file: `platform/efemera/src/efemera/bok/spec_reviewer.py` (102 lines)
- Target: `hivenode/rag/bok/spec_reviewer.py` (NEW)
- Features:
  - review_bok_entry (checks for duplicates and contradictions)
  - ReviewResult dataclass
  - Uses vector similarity to detect near-duplicates

**4. BOK Submission**
- Platform file: `platform/efemera/src/efemera/bok/submission.py` (91 lines)
- Target: `hivenode/rag/bok/submission.py` (NEW)
- Features:
  - submit_from_chat (create BOK entry from chat message)
  - Approval workflow integration

**5. BOK Routes (Extended)**
- Platform file: `platform/efemera/src/efemera/bok/routes.py` (356 lines)
- Target: expand `hivenode/rag/bok/routes.py` (current: ~80 lines)
- Missing endpoints:
  - POST `/api/bok/ingest` (trigger file ingestion, requires ADMIN)
  - POST `/api/bok/review` (review entry before creation)
  - POST `/api/bok/entries` (create BOK entry with auto-review)
  - GET `/api/bok/entries` (list all entries)
  - GET `/api/bok/entries/{id}` (get single entry)
  - PUT `/api/bok/entries/{id}` (update entry)
  - DELETE `/api/bok/entries/{id}` (delete entry)

---

## Proposed Task Breakdown

### Phase 1: Entity Core Logic (Priority Order)

**TASK-159: Port entity archetypes**
- Port `archetypes.py` from platform
- Domain archetype management
- Archetype tribunal consensus (4 methods)
- Tests: archetype CRUD, consensus methods, drift detection
- Estimated lines: ~450 (split if needed to stay under 500)
- Model: Haiku (straightforward port, no complex logic)
- Test count target: 15-20 tests

**TASK-160: Port entity updates**
- Port `updates.py` from platform
- Incremental updates (lightweight, <100ms)
- Nightly recalculation (batch processing with decay)
- Cold-start cascade (multi-level fallback)
- Tests: incremental update speed, nightly batch, cold-start fallback
- Estimated lines: ~420 (may need split into 2 files to stay under 500)
- Model: Sonnet (complex decay logic, batch processing)
- Test count target: 20-25 tests

**TASK-161: Port entity scheduler**
- Port `scheduler.py` from platform
- APScheduler integration
- Cron job setup for nightly recalc
- API endpoints for scheduler control
- Tests: job registration, execution, error handling
- Estimated lines: ~240
- Model: Haiku (straightforward scheduler wrapper)
- Test count target: 8-10 tests
- **Dependency:** TASK-160 must complete first (needs updates.py)

### Phase 2: Entity Routes (Consolidation)

**TASK-162: Extend entity routes**
- Consolidate archetype_routes, update_routes, vector_routes into existing routes.py
- OR create separate route files if consolidation exceeds 500 lines
- Add archetype endpoints (4 routes)
- Add update endpoints (3 routes)
- Add vector endpoints (2 routes)
- Register all routes in `hivenode/routes/__init__.py`
- Tests: all endpoint coverage (request validation, response formats, auth)
- Estimated lines: +300 to routes.py (total ~515 — SPLIT REQUIRED)
- Model: Haiku (route wiring, no complex logic)
- Test count target: 15-18 tests (3 per route group)
- **Dependency:** TASK-159, TASK-160, TASK-161 must complete first

**Recommended Split Strategy for Routes:**
- Keep `hivenode/entities/routes.py` (bot embedding routes only, ~215 lines)
- Create `hivenode/entities/archetype_routes.py` (~150 lines)
- Create `hivenode/entities/update_routes.py` (~130 lines)
- Create `hivenode/entities/vector_routes.py` (~100 lines)

### Phase 3: BOK Advanced Features (Optional — Depends on Priority)

**TASK-163: Port BOK advanced features**
- Expand `models.py` with Pydantic schemas from platform
- Port `file_ingest.py` (file scanner, bulk ingestion)
- Port `spec_reviewer.py` (duplicate/contradiction detection)
- Port `submission.py` (chat-to-BOK workflow)
- Expand `routes.py` with CRUD endpoints
- Tests: file ingestion, review workflow, CRUD operations
- Estimated lines: ~380 total across 4 files (all under 150 each)
- Model: Sonnet (vector similarity logic in reviewer)
- Test count target: 20-25 tests
- **Note:** This phase is OPTIONAL — only if BOK advanced features are needed for MVP

### Phase 4: Integration Testing

**TASK-164: Entity lifecycle E2E tests**
- Port `test_e2e_entity_lifecycle.py` from platform
- Test full entity profile creation → vector computation → update cycle
- Verify drift detection works end-to-end
- Verify BOK enrichment works with entity embeddings
- Model: Haiku (test porting)
- Test count target: 5-8 E2E scenarios

---

## Dependencies to Add

### Python Packages (pyproject.toml)

```toml
[tool.poetry.dependencies]
apscheduler = "^3.10.4"  # For entity scheduler (TASK-161)
numpy = "^1.26.0"        # For vector math (may already be present)
```

**Action:** Check if numpy already in pyproject.toml. Add APScheduler.

### Route Registration

All new routes must be registered in:
- `hivenode/routes/__init__.py`

**Action:** After TASK-162 completes, bee must add:
```python
from hivenode.entities.archetype_routes import router as archetype_router
from hivenode.entities.update_routes import router as update_router
from hivenode.entities.vector_routes import router as vector_router

app.include_router(archetype_router)
app.include_router(update_router)
app.include_router(vector_router)
```

---

## File Size Compliance (500-line rule)

### Files That Will Exceed 500 Lines

**Problem:** Consolidating all entity routes into `routes.py` would create ~515-line file.

**Solution:** Split routes into 4 files:
1. `routes.py` (bot embedding routes, keep as-is, 215 lines) ✓
2. `archetype_routes.py` (new, ~150 lines) ✓
3. `update_routes.py` (new, ~130 lines) ✓
4. `vector_routes.py` (new, ~100 lines) ✓

**Problem:** `updates.py` from platform is 419 lines — close to limit.

**Solution:** Port as-is first. If shiftcenter version grows >450 during port, split into:
- `updates_core.py` (incremental update logic)
- `updates_batch.py` (nightly recalculation logic)

---

## Test Strategy (TDD)

All tasks follow TDD:
1. Write tests first (based on platform test files)
2. Run tests (they should fail initially)
3. Port implementation
4. Run tests (they should pass)
5. No stubs allowed

**Test Files to Create:**
- `tests/hivenode/entities/test_archetypes.py` (TASK-159)
- `tests/hivenode/entities/test_updates.py` (TASK-160)
- `tests/hivenode/entities/test_scheduler.py` (TASK-161)
- `tests/hivenode/entities/test_archetype_routes.py` (TASK-162)
- `tests/hivenode/entities/test_update_routes.py` (TASK-162)
- `tests/hivenode/entities/test_vector_routes.py` (TASK-162)
- `tests/hivenode/rag/bok/test_file_ingest.py` (TASK-163)
- `tests/hivenode/rag/bok/test_spec_reviewer.py` (TASK-163)
- `tests/hivenode/rag/bok/test_submission.py` (TASK-163)
- `tests/hivenode/rag/bok/test_bok_routes.py` (TASK-163)
- `tests/hivenode/entities/test_e2e_lifecycle.py` (TASK-164)

---

## Acceptance Criteria Checklist (from spec)

- [ ] Entity vector extraction ported (TASK-159, TASK-160)
- [x] Voyage AI adapter ported (ALREADY COMPLETE)
- [x] BOK service ported (ALREADY COMPLETE — basic search/enrich)
- [ ] BOK advanced features ported (TASK-163 — file ingest, review, submission)
- [ ] Tests written and passing (all tasks, TDD)
- [ ] All files under 500 lines (routes split, updates monitored)
- [ ] No stubs (enforced in all task files)
- [ ] All routes registered in `hivenode/routes/__init__.py`

---

## Recommended Task Sequence

**Critical Path (Must Complete):**
1. TASK-159 (archetypes) — no dependencies
2. TASK-160 (updates) — no dependencies
3. TASK-161 (scheduler) — depends on TASK-160
4. TASK-162 (routes) — depends on TASK-159, TASK-160, TASK-161

**Optional Path (BOK Advanced):**
5. TASK-163 (BOK advanced) — only if needed for MVP

**Integration:**
6. TASK-164 (E2E tests) — depends on all prior tasks

**Estimated Total Time:**
- Critical path: ~6-8 hours (4 tasks, Haiku/Sonnet mix)
- With BOK advanced: ~8-10 hours
- With E2E tests: ~10-12 hours

---

## Q33N Recommendation

**Proceed with Critical Path (TASK-159 through TASK-162) ONLY.**

Skip TASK-163 (BOK advanced features) unless Q33NR or Q88N explicitly requests it. The basic BOK search/enrich is already functional. File ingest, review, and submission are "nice-to-have" but not required for entity vector MVP.

**Rationale:**
- Entity vectors are the primary objective (per briefing title)
- BOK is already functional for RAG enrichment
- Advanced BOK features add 380 lines + 20-25 tests but low immediate value
- Focus effort on core entity logic first

**If Q33NR approves:**
- I will write task files for TASK-159, TASK-160, TASK-161, TASK-162
- Return to Q33NR for review
- Dispatch after approval

**If Q33NR wants BOK advanced features:**
- I will also write task file for TASK-163
- Return to Q33NR for review

---

## Q33NR: Decision Required

Please confirm:

1. **Do you approve the critical path (TASK-159 through TASK-162)?** YES / NO
2. **Do you want BOK advanced features (TASK-163)?** YES / NO / DEFER
3. **Do you want E2E lifecycle tests (TASK-164)?** YES / NO / DEFER
4. **Route file split strategy approved?** (4 separate route files vs consolidated)

Once confirmed, I will write the task files and return for final review before dispatch.

---

**Q33N signature:** QUEEN-2026-03-15-BRIEFING-rag-entity
**Awaiting Q33NR approval to proceed with task file creation.**
