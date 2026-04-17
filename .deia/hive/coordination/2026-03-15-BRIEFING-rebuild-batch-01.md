# BRIEFING: Rebuild Batch 01 — Route Registration + RAG Indexer Exports

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Context:** A `git reset --hard HEAD` wiped all uncommitted tracked-file modifications. New files survived (untracked). Tracked-file edits are lost. These 5 tasks reconstruct the earliest lost changes.

---

## Your Job

Write 5 official task files to `.deia/hive/tasks/`. Each task reconstructs ONE original task's lost tracked-file modifications. Read the source files listed to understand exactly what changed, then write a task file that tells a bee how to redo it.

**Priorities:** Start at P0.05, increment by P0.05.

---

## REBUILD-TASK-R01 (P0.05): Re-register DES routes in __init__.py

**Original:** TASK-146 (DES engine routes port)
**Purpose:** The DES routes module (`hivenode/routes/des_routes.py`) was created and survived, but its registration in `__init__.py` was lost.

**What the bee must do:**
- Add `from hivenode.routes import des_routes` to the import line at the top of `hivenode/routes/__init__.py`
- Add `router.include_router(des_routes.router, prefix='/api/des', tags=['des'])` inside `create_router()`
- Run `python -m pytest tests/hivenode/test_des_routes.py -v` to verify

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\__init__.py` (current state — missing DES)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py` (surviving module)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-146-RESPONSE.md` (original work record)

**Test:** 22 existing tests in `tests/hivenode/test_des_routes.py` must pass.

---

## REBUILD-TASK-R02 (P0.10): Restore RAG models exports + CCC_PER_FILE fix

**Original:** TASK-151 (RAG models port)
**Purpose:** The models file (`models.py`) was created and survived. But `__init__.py` exports were updated and `indexer_service.py` had a CCC_PER_FILE constant fixed — both lost.

**What the bee must do:**
1. Update `hivenode/rag/indexer/__init__.py` to export ALL 17 models + compatibility aliases from models.py (not just the 12 currently there). The canonical names are: `ProvenanceMetadata`, `ReliabilityMetadata`, `RelevanceMetadata`, `StalenessMetadata`. The aliases `ProvenanceInfo`, `ReliabilityMetrics`, `RelevanceMetrics`, `StalenessInfo` should ALSO be exported.
2. Fix `CCC_PER_FILE` constant in `hivenode/rag/indexer/indexer_service.py` to use correct field names: `coin_usd_per_load`, `carbon_kg_per_load`, add `token_estimate`
3. Run `python -m pytest tests/hivenode/rag/test_models.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current broken state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (surviving module — check actual class names)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (find CCC_PER_FILE)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-151-RESPONSE.md`

**Test:** 50 tests in `tests/hivenode/rag/test_models.py`

---

## REBUILD-TASK-R03 (P0.15): Add Scanner class to RAG indexer exports + fix indexer_service imports

**Original:** TASK-152 (RAG scanner port)
**Purpose:** The scanner file (`scanner.py`) was created and survived. But `__init__.py` only imports the `scan` function — the `Scanner` class import is missing. Also, `indexer_service.py` needs its imports updated to use Scanner and correct model names.

**What the bee must do:**
1. Add `Scanner` class import to `hivenode/rag/indexer/__init__.py` (currently only imports `scan` function)
2. Add `Scanner` to `__all__` list
3. Fix `hivenode/rag/indexer/indexer_service.py`:
   - Update model imports to use canonical names (ProvenanceMetadata not ProvenanceInfo, etc.)
   - Add `self.scanner = Scanner(str(self.repo_path))` to IndexerService.__init__
   - Update `index_file()` to use `self.scanner._detect_type()` instead of standalone function
4. Run `python -m pytest tests/hivenode/rag/indexer/test_scanner.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py` (surviving module — check Scanner class and scan function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (current broken imports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-152-RESPONSE.md`

**Test:** 32 tests in `tests/hivenode/rag/indexer/test_scanner.py`

---

## REBUILD-TASK-R04 (P0.20): Add Chunker to RAG indexer exports

**Original:** TASK-153 (RAG chunker port)
**Purpose:** The chunker file (`chunker.py`) was created and survived. But the export from `__init__.py` was lost.

**What the bee must do:**
1. Add `from hivenode.rag.indexer.chunker import Chunker` to `hivenode/rag/indexer/__init__.py`
2. Add `"Chunker"` to `__all__` list
3. Run `python -m pytest tests/hivenode/rag/test_chunker.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py` (surviving module — verify class name)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-153-RESPONSE.md`

**Test:** 43 tests in `tests/hivenode/rag/test_chunker.py`

---

## REBUILD-TASK-R05 (P0.25): Add TFIDFEmbedder export + models compatibility aliases

**Original:** TASK-154 (RAG embedder port) + TASK-155 (RAG storage port — models.py aliases)
**Purpose:** The embedder file (`embedder.py`) and storage file (`storage.py`) survived. But the exports in `__init__.py` and the compatibility aliases in `models.py` were lost.

**What the bee must do:**
1. Add `from hivenode.rag.indexer.embedder import TFIDFEmbedder` to `hivenode/rag/indexer/__init__.py`
2. Add `"TFIDFEmbedder"` to `__all__`
3. Add `from hivenode.rag.indexer.storage import IndexStorage, compute_content_hash` to `__init__.py`
4. Add `"IndexStorage"`, `"compute_content_hash"` to `__all__`
5. Add compatibility aliases to the END of `hivenode/rag/indexer/models.py`:
   ```python
   # Compatibility aliases
   ProvenanceInfo = ProvenanceMetadata
   ReliabilityMetrics = ReliabilityMetadata
   RelevanceMetrics = RelevanceMetadata
   StalenessInfo = StalenessMetadata
   ```
6. Run tests:
   - `python -m pytest tests/hivenode/rag/indexer/test_embedder.py -v` (34 tests)
   - `python -m pytest tests/hivenode/rag/indexer/test_storage.py -v`

**Files to read:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py` (surviving module)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (surviving module)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (needs aliases at end)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1418-BEE-HAIKU-2026-03-15-TASK-154-PORT-RAG-EMBEDDER-RAW.txt` (no response file — use RAW)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-155-RESPONSE.md`

**Test:** 34 embedder tests + storage tests

---

## IMPORTANT NOTES FOR Q33N

1. **These tasks share `__init__.py`.** R02 through R05 all modify the same file. They MUST be dispatched SEQUENTIALLY, not in parallel.
2. **Read the current state of each file BEFORE writing the task.** The files are in a partially broken state.
3. **Each task file must include the response template** per BOOT.md (8 sections).
4. **Model assignment:** Haiku for all 5 (these are small, targeted modifications).
5. **Write task files to:** `.deia/hive/tasks/2026-03-15-TASK-R01-*.md` through `R05`.
6. **Do NOT dispatch bees.** Return the 5 task files to Q33NR for review.
