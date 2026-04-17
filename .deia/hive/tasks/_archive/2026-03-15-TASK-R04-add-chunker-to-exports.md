# TASK-R04: Add Chunker to RAG indexer exports

**Priority:** P0.20
**Model:** Haiku
**Original:** TASK-153 (RAG chunker port)

---

## Objective

Add the `Chunker` class export to `hivenode/rag/indexer/__init__.py`. The chunker file (`chunker.py`) was created and survived, but the export from `__init__.py` was lost.

---

## Context

A `git reset --hard HEAD` wiped tracked-file modifications. The chunker.py file survived (new untracked file) with the complete Chunker class implementation, but the modification to `__init__.py` to export it was lost.

**Current state:**
- `chunker.py` exists at `hivenode/rag/indexer/chunker.py` with full implementation
- `__init__.py` does NOT import or export the Chunker class

**What needs to be restored:**
- Import Chunker from chunker.py
- Add Chunker to __all__ exports list

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py` (surviving module — verify Chunker class exists)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current state — missing Chunker export)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-153-RESPONSE.md` (if exists — original work record)

---

## Deliverables

- [ ] Add `from hivenode.rag.indexer.chunker import Chunker` to `hivenode/rag/indexer/__init__.py`
- [ ] Add `"Chunker"` to the `__all__` list in `__init__.py`
- [ ] Run `python -m pytest tests/hivenode/rag/test_chunker.py -v` to verify 43 tests pass
- [ ] Verify import: `python -c "from hivenode.rag.indexer import Chunker; print(Chunker)"`

---

## Test Requirements

- [ ] All 43 tests in `tests/hivenode/rag/test_chunker.py` must pass (they already do, this verifies import works)
- [ ] Manual import verification successful

---

## Constraints

- No file over 500 lines (__init__.py is currently 38 lines, will grow by 1-2 lines)
- No stubs
- Follow the existing import pattern in __init__.py

---

## Implementation Guidance

1. **Add import statement:** Add a new import line in the imports section of `__init__.py`:
   ```python
   from hivenode.rag.indexer.chunker import Chunker
   ```
   Place it in alphabetical order with other imports (after `from hivenode.rag.indexer.models import ...` section).

2. **Update __all__ list:** Add `"Chunker"` to the `__all__` list. Place it in alphabetical order.

3. **Verification:** Run tests to confirm Chunker is accessible via the module's public API.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R04-RESPONSE.md`

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
