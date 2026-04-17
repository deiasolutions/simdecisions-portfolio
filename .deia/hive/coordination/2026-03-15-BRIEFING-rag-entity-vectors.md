# BRIEFING: Port RAG Entity Vectors + Complete BOK/Voyage Integration

**From:** Q33NR (regent)
**To:** Q33N (queen coordinator)
**Date:** 2026-03-15
**Spec:** 2026-03-15-1305-SPEC-w1-11-rag-entity-vectors
**Model:** sonnet
**Priority:** P0.55

---

## Objective

Port remaining RAG entity vector computation logic from platform repo to shiftcenter. Complete integration of Voyage AI adapter and BOK services which have already been partially ported.

---

## Context and Current State

### What's Already Ported (from previous work)

**Voyage AI Adapter:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\voyage_embedding.py` (171 lines) ✓
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_voyage_embedding.py` ✓
- Status: COMPLETE

**Bot Embeddings:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\embeddings.py` (314 lines) ✓
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_embeddings.py` ✓
- Features: BotEmbeddingStore, drift detection, pi computation
- Status: COMPLETE

**Entity Vector Core:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_core.py` (428 lines) ✓
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_vectors.py` ✓
- Features: EntityProfile, EntityComponent ORM models, helper functions
- Status: COMPLETE

**Entity Vector Compute:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\vectors_compute.py` (490 lines) ✓
- Features: alpha, sigma, rho computation with 30-day decay
- Status: COMPLETE (check if all functions from platform are present)

**Entity Routes:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\routes.py` (215 lines) ✓
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\test_routes.py` ✓
- Status: COMPLETE (verify all endpoints present)

**BOK Service:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\rag_service.py` (107 lines) ✓
- Tests: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\bok\test_bok_services.py` ✓
- Features: search_bok, format_bok_for_prompt, enrich_prompt
- Status: COMPLETE

### What Needs To Be Ported/Completed

Based on platform source files, we need to check and port:

**1. Entity Archetypes (if missing)**
   - Platform: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetypes.py` (432 lines)
   - Target: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\archetypes.py`
   - Features: domain archetype management, archetype embeddings, cosine similarity helpers

**2. Entity Updates (if missing)**
   - Platform: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\updates.py` (419 lines)
   - Target: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\updates.py`
   - Features: scheduled vector updates, background refresh, update tracking

**3. Entity Scheduler (if missing)**
   - Platform: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\scheduler.py` (232 lines)
   - Target: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\scheduler.py`
   - Features: background scheduler for periodic vector recomputation

**4. Additional Routes (if missing)**
   - Platform archetype routes: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\archetype_routes.py` (123 lines)
   - Platform embedding routes: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\embedding_routes.py` (143 lines)
   - Platform update routes: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\update_routes.py` (112 lines)
   - Platform vector routes: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\vector_routes.py` (81 lines)

**5. BOK Additional Files (if needed)**
   - Platform: `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\bok\` (878 lines total)
   - Check if models.py, routes.py, embedding_service.py, file_ingest.py, spec_reviewer.py, submission.py need porting

---

## Source Material

**Platform entity files (2,935 lines total):**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\entities\`
  - archetypes.py (432 lines)
  - archetype_routes.py (123 lines)
  - embeddings.py (299 lines) — likely already ported
  - embedding_routes.py (143 lines)
  - models.py (183 lines)
  - routes.py (235 lines)
  - scheduler.py (232 lines)
  - updates.py (419 lines)
  - update_routes.py (112 lines)
  - vectors.py (685 lines) — partially ported
  - vector_routes.py (81 lines)
  - voyage_embedding.py (165 lines) — already ported

**Platform BOK files (878 lines total):**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\bok\`
  - embedding_service.py (112 lines)
  - file_ingest.py (117 lines)
  - models.py (69 lines)
  - rag_service.py (64 lines) — already ported (simpler version)
  - routes.py (356 lines)
  - spec_reviewer.py (102 lines)
  - submission.py (91 lines)

**Platform tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\tests\`
  - test_entity_profiles.py
  - test_e2e_entity_lifecycle.py

---

## Target Structure

**Destination (entity vectors):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\entities\`
  - archetypes.py (NEW)
  - updates.py (NEW)
  - scheduler.py (NEW)
  - archetype_routes.py (NEW, or merge into routes.py)
  - embedding_routes.py (NEW, or merge into routes.py)
  - update_routes.py (NEW, or merge into routes.py)
  - vector_routes.py (NEW, or merge into routes.py)

**Destination (BOK):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\bok\`
  - models.py (verify complete)
  - routes.py (verify complete)
  - embedding_service.py (NEW if needed)
  - file_ingest.py (NEW if needed)
  - spec_reviewer.py (NEW if needed)
  - submission.py (NEW if needed)

**Tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\entities\`
  - test_archetypes.py (NEW)
  - test_updates.py (NEW)
  - test_scheduler.py (NEW)
  - (verify existing: test_embeddings.py, test_routes.py, test_vectors.py, test_voyage_embedding.py)

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\bok\`
  - (verify existing: test_bok_services.py)
  - test_bok_routes.py (NEW if routes expanded)

---

## Acceptance Criteria (from spec)

- [ ] Entity vector extraction ported
- [ ] Voyage AI adapter ported (**already complete**)
- [ ] BOK service ported (**already complete**)
- [ ] Tests written and passing

**Expanded mechanical criteria:**
- [ ] All missing entity files ported from platform
- [ ] All files under 500 lines (split if needed)
- [ ] No hardcoded colors (N/A — backend only)
- [ ] TDD: tests first
- [ ] No stubs
- [ ] All routes registered in `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py`
- [ ] Response file with all 8 sections

---

## Task Breakdown for Q33N

### Phase 1: Inventory and Gap Analysis (Q33N only)

1. **Read all existing hivenode/entities files** to understand what's already ported
2. **Compare with platform source** to identify gaps
3. **Read all existing hivenode/rag/bok files** to understand BOK state
4. **Compare with platform BOK source** to identify BOK gaps
5. **Create gap analysis report** listing exactly what needs to be ported

### Phase 2: Port Missing Entity Files

Based on gap analysis, create bee tasks for:

**TASK-158: Port entity archetypes (if missing)**
- Port archetypes.py from platform
- Domain archetype management
- Archetype embeddings
- Tests: archetype CRUD, embedding generation, cosine similarity

**TASK-159: Port entity updates (if missing)**
- Port updates.py from platform
- Scheduled vector updates
- Background refresh logic
- Tests: update scheduling, refresh triggers, state tracking

**TASK-160: Port entity scheduler (if missing)**
- Port scheduler.py from platform
- Background scheduler setup
- Periodic vector recomputation
- Tests: schedule registration, execution, error handling

**TASK-161: Consolidate or port entity routes (if needed)**
- Check if archetype_routes, embedding_routes, update_routes, vector_routes exist
- If missing, port or consolidate into main routes.py (keep under 500 lines)
- Register all routes in hivenode/routes/__init__.py
- Tests: all endpoint coverage

### Phase 3: Complete BOK Integration (if gaps found)

**TASK-162: Port missing BOK files (if needed)**
- Port models.py, routes.py, embedding_service.py, file_ingest.py, spec_reviewer.py, submission.py
- Only port what's missing
- Consolidate if possible to reduce file count
- Tests: BOK CRUD, file ingestion, spec review, submission workflow

### Phase 4: Integration Testing

**TASK-163: End-to-end entity lifecycle tests**
- Port test_e2e_entity_lifecycle.py from platform
- Test full entity profile creation → vector computation → update cycle
- Verify drift detection works
- Verify BOK enrichment works with entity embeddings

---

## Constraints from Spec

- Max 500 lines per file (hard limit 1,000)
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only (N/A — backend only)
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  ```json
  {"task_id": "2026-03-15-1305-SPEC-w1-11-rag-entity-vectors", "status": "running", "model": "sonnet", "message": "working"}
  ```

---

## Smoke Test (from spec)

```bash
python -m pytest tests/hivenode/test_rag*.py -v
python -m pytest tests/hivenode/entities/ -v
```

Expected: No new test failures, all new tests passing.

---

## Dependencies

**Backend:**
- SQLAlchemy (already present)
- FastAPI (already present)
- Voyage AI API (already present)
- Event Ledger (already ported — engine/events/)
- Database base (already present — engine/database.py)

**Python packages:**
- requests (for Voyage API) — already in pyproject.toml
- numpy (for vector math) — check if present, add if missing

---

## Q33N: Action Items

1. **Read existing files** in hivenode/entities/ and hivenode/rag/bok/
2. **Read platform source files** in platform/efemera/src/efemera/entities/ and platform/efemera/src/efemera/bok/
3. **Create gap analysis** (which functions/classes are missing)
4. **Write bee task files** for missing components (TASK-158 through TASK-163)
5. **Return task files to Q33NR for review** (do NOT dispatch bees yet)

---

## Q33NR Review Checklist

When Q33N returns task files, I (Q33NR) will verify:

- [ ] Gap analysis shows exactly what's missing vs already ported
- [ ] All acceptance criteria covered
- [ ] File paths absolute
- [ ] Test requirements specified (TDD)
- [ ] No files over 500 lines
- [ ] No stubs allowed
- [ ] Response file template included
- [ ] Dependencies identified
- [ ] Routes registration plan included

---

## Key Architectural Patterns (from MEMORY.md)

- **Event Ledger integration** — entity vectors read from event ledger (EventRecord table)
- **SQLAlchemy ORM** — use engine.database.Base for all models
- **30-day decay window** — vectors computed from events within last 30 days
- **Confidence formula** — `(sample_size / (sample_size + 10)) * source_multiplier`
- **Cold-start cascade** — local profile → domain default → neutral baseline (0.5, 0.0)
- **Absolute paths** — all file paths in task files must be absolute

---

## Next Steps

1. Q33N reads this briefing
2. Q33N performs gap analysis (what's ported vs what's missing)
3. Q33N writes task files (TASK-158 through TASK-163, or fewer if some components already complete)
4. Q33N returns to Q33NR for review
5. Q33NR reviews and approves (or requests corrections)
6. Q33N dispatches bees
7. Bees complete work
8. Q33N reports results to Q33NR
9. Q33NR reports to Q88N

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-1305-SPE
**Briefing complete. Awaiting Q33N gap analysis and task files.**
