# BRIEFING: Fix RAG Indexer Import Errors

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-15
**Time:** 14:35
**Priority:** P0
**Model:** Sonnet

---

## Decision from Q33NR

You correctly identified that the RAG indexer code has already been ported but is currently broken due to import errors.

**I approve your fix approach.** Write the 3 fix tasks as you outlined:

1. **TASK-158**: Fix RAG indexer import errors
2. **TASK-159**: Verify RAG indexer end-to-end  
3. **TASK-160**: Smoke-test RAG routes

---

## Instructions

1. Write 3 task files to `.deia/hive/tasks/` (use next available TASK-### numbers)
2. Include all standard task sections (Objective, Context, Deliverables, Test Requirements, Constraints, Response Requirements)
3. Make file paths absolute
4. Specify haiku model for all 3 tasks
5. Return task files to me for mechanical review before dispatch

---

## Known Issues to Fix

**Import errors in `indexer_service.py`:**
- Line 17: `from hivenode.rag.chunkers` → should be `from hivenode.rag.indexer.chunker`
- Line 18: `from hivenode.rag.embedder` → should be `from hivenode.rag.indexer.embedder`

**Missing exports in `__init__.py`:**
- `IndexerService` class not exported (needed by routes)

**Test execution blocked:**
- Cannot run `pytest tests/hivenode/rag/indexer/` due to import errors in conftest

---

## Acceptance Criteria (from original spec)

After fixes, these should all pass:
- [ ] Indexer service ported with document chunking
- [ ] Embedding generation working
- [ ] Vector storage using SQLite
- [ ] Similarity search API endpoint
- [ ] Tests written and passing

---

**Q33NR signature:** REGENT-QUEUE-TEMP-2026-03-15-1238-SPE
**Status:** Awaiting Q33N fix task files
