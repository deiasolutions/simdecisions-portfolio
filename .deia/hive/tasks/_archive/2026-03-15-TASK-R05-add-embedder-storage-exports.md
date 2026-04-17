# TASK-R05: Add TFIDFEmbedder and IndexStorage exports to RAG indexer

**Priority:** P0.25
**Model:** Haiku
**Original:** TASK-154 (RAG embedder port) + TASK-155 (RAG storage port)

---

## Objective

Add exports for `TFIDFEmbedder`, `IndexStorage`, and `compute_content_hash` to `hivenode/rag/indexer/__init__.py`. The embedder and storage files (`embedder.py` and `storage.py`) were created and survived, but the exports from `__init__.py` were lost.

---

## Context

A `git reset --hard HEAD` wiped tracked-file modifications. The embedder.py and storage.py files survived (new untracked files) with complete implementations, but the modifications to `__init__.py` to export them were lost.

**Current state:**
- `embedder.py` exists at `hivenode/rag/indexer/embedder.py` with TFIDFEmbedder class
- `storage.py` exists at `hivenode/rag/indexer/storage.py` with IndexStorage class and compute_content_hash function
- `__init__.py` does NOT import or export these classes/functions

**What needs to be restored:**
- Import TFIDFEmbedder from embedder.py
- Import IndexStorage and compute_content_hash from storage.py
- Add all three to __all__ exports list

**NOTE:** The briefing mentioned adding compatibility aliases to models.py, but those were already handled in TASK-R02. This task only deals with the exports.

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py` (surviving module — verify TFIDFEmbedder exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (surviving module — verify IndexStorage and compute_content_hash exist)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state — missing these exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1418-BEE-HAIKU-2026-03-15-TASK-154-PORT-RAG-EMBEDDER-RAW.txt` (if accessible — original work record)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-155-RESPONSE.md` (if exists — original work record)

---

## Deliverables

- [ ] Add `from hivenode.rag.indexer.embedder import TFIDFEmbedder` to `hivenode/rag/indexer/__init__.py`
- [ ] Add `from hivenode.rag.indexer.storage import IndexStorage, compute_content_hash` to `hivenode/rag/indexer/__init__.py`
- [ ] Add `"TFIDFEmbedder"`, `"IndexStorage"`, and `"compute_content_hash"` to the `__all__` list in `__init__.py`
- [ ] Run `python -m pytest tests/hivenode/rag/indexer/test_embedder.py -v` to verify embedder tests pass (34 tests expected)
- [ ] Run `python -m pytest tests/hivenode/rag/indexer/test_storage.py -v` to verify storage tests pass
- [ ] Verify imports work:
  ```bash
  python -c "from hivenode.rag.indexer import TFIDFEmbedder, IndexStorage, compute_content_hash; print('OK')"
  ```

---

## Test Requirements

- [ ] All embedder tests pass (34 tests in `tests/hivenode/rag/indexer/test_embedder.py`)
- [ ] All storage tests pass (in `tests/hivenode/rag/indexer/test_storage.py`)
- [ ] Manual import verification successful

---

## Constraints

- No file over 500 lines (__init__.py is currently ~38 lines, will grow by 2-3 lines)
- No stubs
- Follow the existing import pattern in __init__.py

---

## Implementation Guidance

1. **Add import statements:** Add these two import lines in the imports section of `__init__.py`:
   ```python
   from hivenode.rag.indexer.embedder import TFIDFEmbedder
   from hivenode.rag.indexer.storage import IndexStorage, compute_content_hash
   ```
   Place them in alphabetical order with other imports (after chunker, before models, or in appropriate alphabetical position).

2. **Update __all__ list:** Add these three items to the `__all__` list:
   - `"TFIDFEmbedder"`
   - `"IndexStorage"`
   - `"compute_content_hash"`

   Place them in alphabetical order within the list.

3. **Verification:** Run both test suites to confirm all classes/functions are accessible via the module's public API.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R05-RESPONSE.md`

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
