# TASK-153: Port RAG Chunker Module

## Objective
Port the artifact chunker that breaks documents into logical chunks based on artifact type (code per function, PHASE-IR per node, markdown per section, etc.).

## Context
The Chunker class implements type-aware chunking logic per harness spec §6.3. Different artifact types have different chunking boundaries:
- Code: per function/method (AST for Python, regex for JS/TS)
- PHASE-IR: per node
- ADR: per decision section (## Decision N)
- Spec: per capability claim (## headings)
- Document: per section heading

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\chunker.py` (324 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py`

**Dependencies:** TASK-151 (models.py) must be complete.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\indexer\chunker.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\models.py` (from TASK-151)

## Deliverables
- [ ] Create `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py`
- [ ] Port Chunker class with methods:
  - `chunk(content, artifact_type, file_path)` → list[Chunk] — main chunking dispatcher
  - `_chunk_code(content, file_path)` → list[Chunk] — code chunking (delegates to Python or JS)
  - `_chunk_python(content)` → list[Chunk] — Python AST-based chunking
  - `_chunk_javascript(content)` → list[Chunk] — JS/TS regex-based chunking
  - `_chunk_phase_ir(content)` → list[Chunk] — PHASE-IR per-node chunking
  - `_chunk_adr(content)` → list[Chunk] — ADR per decision section
  - `_chunk_spec(content)` → list[Chunk] — Spec per capability claim
  - `_chunk_document(content)` → list[Chunk] — Document per section heading
  - `_chunk_by_headings(content, heading_level)` → list[Chunk] — generic markdown chunking
  - `_create_chunk(content, start_line, end_line)` → Chunk — chunk factory
- [ ] Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` to export Chunker
- [ ] Create test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_chunker.py`
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test _chunk_python() with valid Python code (2+ functions)
- [ ] Test _chunk_python() with syntax error (fallback to single chunk)
- [ ] Test _chunk_python() with class definitions
- [ ] Test _chunk_python() with async functions
- [ ] Test _chunk_javascript() with function declarations
- [ ] Test _chunk_javascript() with arrow functions
- [ ] Test _chunk_javascript() with class methods
- [ ] Test _chunk_phase_ir() with valid PHASE-IR JSON
- [ ] Test _chunk_phase_ir() with invalid JSON (fallback)
- [ ] Test _chunk_adr() with multiple decision sections
- [ ] Test _chunk_adr() with no decision sections (fallback)
- [ ] Test _chunk_spec() chunks by ## headings
- [ ] Test _chunk_document() chunks by ## headings
- [ ] Test _chunk_by_headings() with various heading levels
- [ ] Test _create_chunk() generates correct token estimates
- [ ] Test chunk.ir_pairs are populated with correct intent
- [ ] Edge cases:
  - Empty content
  - Single-line files
  - Files with no functions/headings/sections
  - Very long functions (>1000 lines)
  - Unicode content

**Target test count:** 20+ tests

**Smoke test command:**
```bash
python -m pytest tests/hivenode/rag/test_chunker.py -v
```

## Constraints
- No file over 500 lines (chunker.py is 324 lines, under limit)
- No stubs — all methods fully implemented
- TDD: tests first
- Port verbatim — do NOT modify logic from platform

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-153-RESPONSE.md`

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
**Estimated time:** 30 minutes
**Dependency:** TASK-151
