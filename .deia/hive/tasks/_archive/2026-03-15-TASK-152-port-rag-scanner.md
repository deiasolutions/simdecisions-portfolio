# TASK-152: Port RAG Scanner Module

## Objective
Port the file scanner module that walks repository directory trees, identifies artifact types per file extension/path, and returns scan results for indexing.

## Context
The Scanner class is responsible for discovering indexable artifacts in a repository. It walks the filesystem, skips excluded directories (node_modules, .git, etc.), and classifies files by artifact type based on extension and filename patterns.

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\scanner.py` (164 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`

**Dependencies:** TASK-151 (models.py) must be complete.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\scanner.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (from TASK-151)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\scanner.py`
- [ ] Port Scanner class with methods:
  - `__init__(root_path)` — validate repository root exists
  - `scan()` → Iterator[tuple[Path, ArtifactType]] — walk tree, yield (file, type)
  - `scan_single(file_path)` → ArtifactType | None — classify single file
  - `_detect_type(file_path)` → ArtifactType | None — type detection logic
  - `_is_phase_ir_file(file_path)` → bool — check if JSON is PHASE-IR format
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` to export Scanner
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_scanner.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test Scanner initialization with valid directory
- [ ] Test Scanner initialization with invalid directory (raises ValueError)
- [ ] Test scan() yields correct artifact types for known extensions:
  - .py → CODE
  - .js/.jsx/.ts/.tsx → CODE
  - .json with PHASE-IR structure → PHASE_IR
  - .json without PHASE-IR structure → None (skip)
  - ADR-*.md → ADR
  - SPEC-*.md → SPEC
  - Other .md → DOCUMENT
- [ ] Test scan() skips excluded directories (node_modules, .git, __pycache__, etc.)
- [ ] Test scan_single() for individual file classification
- [ ] Test _is_phase_ir_file() detects PHASE-IR JSON format
- [ ] Edge cases:
  - Empty directory
  - Directory with only excluded files
  - Symlinks (should follow or skip?)
  - Malformed JSON (should not crash)
  - Unicode filenames

**Target test count:** 12+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_scanner.py -v
```

## Constraints
- No file over 500 lines (scanner.py is 164 lines, well under limit)
- No stubs — all methods fully implemented
- TDD: tests first
- Port verbatim — do NOT modify logic from platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-152-RESPONSE.md`

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

---

**Priority:** P0.50
**Model:** haiku
**Estimated time:** 25 minutes
**Dependency:** TASK-151
