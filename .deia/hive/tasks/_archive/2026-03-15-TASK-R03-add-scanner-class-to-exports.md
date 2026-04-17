# TASK-R03: Add Scanner class to RAG indexer exports + fix indexer_service imports

**Priority:** P0.15
**Model:** Haiku
**Original:** TASK-152 (RAG scanner port)

---

## Objective

Restore the Scanner class export from `hivenode/rag/indexer/__init__.py` and fix the broken imports in `indexer_service.py`. The scanner file (`scanner.py`) was created and survived, but the modifications to `__init__.py` and `indexer_service.py` were lost.

---

## Context

A `git reset --hard HEAD` wiped tracked-file modifications. The scanner.py file survived (new untracked file), but:
1. The `__init__.py` export of the `Scanner` class was lost (it only imports `scan` function now)
2. The `indexer_service.py` integration was lost (it imports a non-existent standalone function)

**Current broken state:**
- `__init__.py` imports `scan` function but NOT the `Scanner` class
- `__init__.py` exports `scan` in `__all__` but NOT `Scanner`
- `indexer_service.py` line 163 tries to import `from hivenode.rag.indexer.scanner import _detect_type` (private function, wrong approach)
- `indexer_service.py` does not create a Scanner instance in __init__

**Correct state (to restore):**
- `__init__.py` imports both `scan` function AND `Scanner` class
- `__init__.py` exports both in `__all__`
- `indexer_service.py` creates `self.scanner = Scanner(str(self.repo_path))` in __init__
- `indexer_service.py` uses `self.scanner._detect_type()` (instance method) in index_file()

---

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py` (surviving module — check Scanner class and scan function exist)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` (current broken state — only imports scan function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` (current broken imports — line 163 imports private function)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-152-RESPONSE.md` (original work record)

---

## Deliverables

- [ ] Update `hivenode/rag/indexer/__init__.py`:
  - Change line 21: `from hivenode.rag.indexer.scanner import scan` → `from hivenode.rag.indexer.scanner import scan, Scanner`
  - Add `"Scanner"` to the `__all__` list (after `"scan"`)
- [ ] Update `hivenode/rag/indexer/indexer_service.py`:
  - Add `self.scanner = Scanner(str(self.repo_path))` to the `__init__` method (around line 82, after `self.embedder = ...`)
  - Remove the broken import at line 163: `from hivenode.rag.indexer.scanner import _detect_type`
  - Update line 165 (in `index_file()` method): `artifact_type = _detect_type(file_path)` → `artifact_type = self.scanner._detect_type(file_path)`
  - Verify that the Scanner is also used in Pass 1 of `index_repository()` — but based on the current code (line 101), it already uses `scan()` function correctly, so no change needed there
- [ ] Run `python -m pytest tests/hivenode/rag/indexer/test_scanner.py -v` to verify 32 tests pass

---

## Test Requirements

- [ ] All 32 tests in `tests/hivenode/rag/indexer/test_scanner.py` must pass
- [ ] Verify import works: `python -c "from hivenode.rag.indexer import Scanner; print(Scanner)"`
- [ ] Verify IndexerService can be instantiated without errors

---

## Constraints

- No file over 500 lines
- No stubs
- Follow the exact pattern from the original TASK-152 response file

---

## Implementation Guidance

1. **__init__.py changes:**
   - Line 21: Add `Scanner` to the import
   - Line 36 (in `__all__`): Add `"Scanner"` after `"scan"`

2. **indexer_service.py changes:**
   - Import is already at top: Scanner is available from `hivenode.rag.indexer.scanner` but we need to import it at top OR use the exported one from `__init__.py`. Since the code already has `from hivenode.rag.indexer.scanner import scan` at line 31, change it to import Scanner too.
   - Actually, looking at the current code more carefully: line 31 has `from hivenode.rag.indexer.scanner import scan`. This should become: `from hivenode.rag.indexer.scanner import scan, Scanner` (if not already imported from models import).
   - Wait, let me re-check the actual imports. The file currently does NOT import Scanner at all. So:
     - Option A: Add Scanner to the existing import at line 31
     - Option B: Import from the __init__.py after we fix it
   - Recommended: Use option A (import directly from scanner.py at line 31) since that's cleaner

3. **Scanner instance:**
   - In `__init__` method (around line 82), add:
     ```python
     self.scanner = Scanner(str(self.repo_path))
     ```

4. **Fix index_file() method:**
   - Remove the broken import at line 163
   - Change line 165 to use instance method: `self.scanner._detect_type(file_path)`

5. **Verification:** Run scanner tests to confirm.

---

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R03-RESPONSE.md`

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
