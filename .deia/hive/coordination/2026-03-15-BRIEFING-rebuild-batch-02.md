# BRIEFING: Rebuild Batch 02 — RAG Service Fixes + Route Registration + Shell CSS

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Context:** Continuation of rebuild after `git reset --hard HEAD`. These 5 tasks cover RAG service repairs, route registration, shell CSS fixes, and test additions. All depend on Batch 01 completing first (shared `__init__.py`).

---

## Your Job

Write 5 official task files to `.deia/hive/tasks/`. Priorities continue from Batch 01.

---

## REBUILD-TASK-R06 (P0.30): Fix RAG indexer_service.py imports + storage.py methods

**Original:** TASK-156 (RAG indexer service port)
**Purpose:** The indexer_service.py file had extensive import fixes and model schema alignment done. storage.py had new public methods added. These modifications are lost.

**What the bee must do:**
1. In `hivenode/rag/indexer/indexer_service.py`:
   - Fix imports: change `from hivenode.rag.chunkers import CodeChunk, chunk_file` to use `from hivenode.rag.indexer.chunker import Chunker`
   - Fix imports: change `from hivenode.rag.embedder import TFIDFEmbedder` to use `from hivenode.rag.indexer.embedder import TFIDFEmbedder`
   - Update model field usage: StorageTier.WARM → StorageTier.EDGE, add content_preview/char_count/token_estimate to IndexRecord creation
   - Fix StalenessInfo fields to use `content_hash`, `last_modified`
   - Fix ProvenanceInfo to use only `created_by` field
   - Fix ReliabilityMetrics fields: `availability`, `hit_rate`, `failure_count`, `consecutive_failures`
   - Fix RelevanceMetrics fields: `user_feedback_helpful`, `user_feedback_not_helpful`
   - Add `_convert_code_chunks_to_chunks()` method
   - Fix `_compute_ir_summary()` to use Chunk model objects
   - Fix storage interaction: remove invalid kwargs from `storage.insert()`
2. In `hivenode/rag/indexer/storage.py`:
   - Add `get_chunks()` public method
   - Add `get_embeddings()` public method
   - Add `limit` parameter to `list_all()`
3. In `tests/hivenode/rag/indexer/test_indexer_service.py`:
   - Fix test assertions to match actual model schema

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (current broken state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (model definitions)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-156-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1418-BEE-HAIKU-2026-03-15-TASK-156-PORT-RAG-INDEXER-SERVICE-RAW.txt`

**Test:** `python -m pytest tests/hivenode/rag/indexer/test_indexer_service.py -v`
**Model:** Sonnet (complex multi-file repair)

---

## REBUILD-TASK-R07 (P0.35): Register RAG routes + canvas chat routes in __init__.py

**Original:** TASK-157 (RAG routes) + TASK-165 (canvas chatbot dialect)
**Purpose:** Two route modules were created and survived (`hivenode/routes/rag_routes.py`, `hivenode/routes/canvas_chat.py`), but their registrations in `__init__.py` were lost.

**What the bee must do:**
1. In `hivenode/routes/__init__.py`:
   - Add import: `from hivenode.routes import rag_routes as new_rag_routes` (rename to avoid collision with existing `rag_routes` from `hivenode.rag`)
   - Add import: `from hivenode.routes import canvas_chat`
   - Add registration: `router.include_router(new_rag_routes.router, prefix='/api/rag', tags=['rag-indexer'])`
   - Add registration: `router.include_router(canvas_chat.router, tags=['canvas-chat'])`
2. Run tests:
   - `python -m pytest tests/hivenode/test_rag_routes.py -v`
   - `python -m pytest tests/hivenode/test_canvas_chat.py -v` (if exists)

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\rag_routes.py` (surviving file — check router name)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\canvas_chat.py` (surviving file — check router name)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-157-RESPONSE.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-165-COMPLETION-REPORT.md`

**Test:** 16 RAG route tests + 8 canvas chat tests
**Model:** Haiku

---

## REBUILD-TASK-R08 (P0.40): Fix CSS var violations in ShellTabBar + WorkspaceBar

**Original:** TASK-158 (shell chrome CSS fixes)
**Purpose:** Hardcoded rgba() values in ShellTabBar.tsx and WorkspaceBar.tsx were replaced with CSS variables, but those changes are lost.

**What the bee must do:**
1. In `browser/src/shell/components/ShellTabBar.tsx`:
   - Line ~150: Replace `boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'` with `boxShadow: 'var(--sd-shadow-sm)'`
2. In `browser/src/shell/components/WorkspaceBar.tsx`:
   - Line ~57: Replace `e.currentTarget.style.background = 'rgba(139,92,246,0.06)'` with `e.currentTarget.style.background = 'var(--sd-accent-subtle)'`
   - Line ~146: Replace `background: 'rgba(139,92,246,0.06)'` with `background: 'var(--sd-accent-subtle)'`
   - Line ~230: Replace `boxShadow: '0 8px 28px rgba(0,0,0,0.5)'` with `boxShadow: 'var(--sd-shadow-xl)'`
3. Verify NO hex/rgb/rgba values remain: `grep -n -E "(#[0-9a-fA-F]{3,6}|rgb\(|rgba\()" ShellTabBar.tsx WorkspaceBar.tsx` should return nothing.
4. Run shell component tests.

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ShellTabBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\WorkspaceBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-158-RESPONSE.md`

**Test:** `cd browser && npx vitest run src/shell/components/__tests__/ShellTabBar.test.tsx src/shell/components/__tests__/WorkspaceBar.test.tsx`
**Model:** Haiku

---

## REBUILD-TASK-R09 (P0.45): Add IndexerService export to RAG __init__.py

**Original:** TASK-161 (RAG init fixes)
**Purpose:** The IndexerService class was not exported from `__init__.py`. This was a simple one-line fix that's now lost.

**What the bee must do:**
1. In `hivenode/rag/indexer/__init__.py`:
   - Add `from hivenode.rag.indexer.indexer_service import IndexerService`
   - Add `"IndexerService"` to `__all__`
2. Verify: `python -c "from hivenode.rag.indexer import IndexerService; print('OK')"`
3. Run `python -m pytest tests/hivenode/rag/indexer/test_storage.py tests/hivenode/rag/indexer/test_scanner.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-161-RESPONSE.md`

**Test:** 54 tests (22 storage + 32 scanner)
**Model:** Haiku

---

## REBUILD-TASK-R10 (P0.50): Add 2 smoke tests to RAG routes test file

**Original:** TASK-163 (RAG routes smoke test)
**Purpose:** Two new test methods were added to the RAG routes test file. The test file itself was tracked (not new), so those additions are lost.

**What the bee must do:**
1. In `tests/hivenode/rag/test_rag_routes.py`:
   - Add `TestQueryRoute` class with:
     - `test_query_endpoint_exists` — verifies `/query` endpoint responds (200 or 503)
     - `test_query_missing_query_param` — validates required query parameter (422 or 400)
2. Run `python -m pytest tests/hivenode/rag/test_rag_routes.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_rag_routes.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-163-RESPONSE.md`

**Test:** 14 total tests expected
**Model:** Haiku

---

## NOTES FOR Q33N

1. R06 depends on Batch 01 (R02-R05) completing first — needs correct __init__.py exports.
2. R07 depends on R01 completing first (DES routes already registered).
3. R08 is independent of all other tasks (browser-side CSS).
4. R09 depends on R06 completing (IndexerService needs fixed imports first).
5. R06 is Sonnet-level. All others are Haiku.
6. Write task files to `.deia/hive/tasks/2026-03-15-TASK-R06-*.md` through `R10`.
7. Do NOT dispatch bees. Return task files to Q33NR for review.
