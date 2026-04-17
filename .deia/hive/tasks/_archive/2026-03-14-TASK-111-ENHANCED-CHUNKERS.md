# TASK-111: Enhanced Chunkers (AST Python + JS + PHASE-IR + ADR + SPEC)

**Wave:** 1
**Model:** sonnet
**Role:** bee
**Depends on:** None

---

## Objective

Extend existing `hivenode/rag/chunkers.py` with production-grade chunking for Python (AST-based), JavaScript/TypeScript, PHASE-IR JSON, ADR documents, and SPEC documents. Add IR pair extraction from Python docstrings.

## Source Spec

Port from: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-PORT-RAG-001-rag-pipeline-port.md`
Decomposition: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-Q33N-BRIEFING-PORT-RAG-PIPELINE-TASK-DECOMPOSITION.md`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py` (existing chunkers — DO NOT replace, EXTEND)
- Source files in `platform/efemera/src/efemera/indexer/chunker.py` (reference for algorithms)

## Files to Modify

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py` (extend with new chunking methods)

## Files to Create

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\test_enhanced_chunkers.py`

## Deliverables

### Extensions to chunkers.py (324 lines added)

**1. Extend `CodeChunk` dataclass:**
```python
@dataclass
class CodeChunk:
    content: str
    start_line: int
    end_line: int
    char_count: int
    token_estimate: int
    ir_pairs: list[dict] = field(default_factory=list)  # NEW FIELD
```

**2. Replace `_chunk_python()` with AST-based implementation:**
- Use Python `ast` module to parse source
- Extract functions, methods, and classes as chunks
- Each chunk = 1 function/method OR 1 class definition
- Include docstrings in chunk content
- Call `_extract_ir_pairs_from_docstring()` for each chunk
- Handle syntax errors gracefully (return empty list + log warning)

**3. Add `_chunk_javascript(content: str) -> list[CodeChunk]`:**
- Regex + brace-matching for JS/TS function scope
- Patterns: `function foo()`, `const foo = () =>`, `class Foo`, `foo() {`
- Track braces to find function/class end
- Handle nested functions (outer scope only)
- Token estimate: `len(content) // 4`

**4. Add `_chunk_phase_ir(content: str) -> list[CodeChunk]`:**
- Parse JSON
- Each "node" in `nodes` array becomes a chunk
- Chunk content = JSON.stringify(node)
- Extract IR pairs from `node.metadata.ir_pairs` if present
- Handle invalid JSON gracefully

**5. Add `_chunk_adr(content: str) -> list[CodeChunk]`:**
- Split by `## Decision N` headings (regex: `^## Decision \d+`)
- Each decision section = 1 chunk
- Include decision number in chunk metadata
- Preserve markdown formatting

**6. Add `_chunk_spec(content: str) -> list[CodeChunk]`:**
- Split by `##` headings (top-level sections)
- Each section = 1 chunk (capability claim)
- Preserve heading in chunk content
- Track section title for metadata

**7. Refactor `_chunk_by_headings(content: str, heading_pattern: str) -> list[CodeChunk]`:**
- Generic heading-based chunker (used by ADR + SPEC + existing markdown chunker)
- Regex pattern parameter for heading detection
- Split content at heading boundaries
- Return chunks with start/end line numbers

**8. Add `_create_chunk(content: str, start_line: int, end_line: int, ir_pairs: Optional[list] = None) -> CodeChunk`:**
- Factory function for creating CodeChunk instances
- Compute `char_count = len(content)`
- Compute `token_estimate = len(content) // 4`
- Attach ir_pairs if provided

**9. Add `_extract_ir_pairs_from_docstring(docstring: str) -> list[dict]`:**
- Regex pattern: `# IR: (.+?) → (.+?)(?:\n|$)`
- Extract intent → result pairs
- Return list of dicts: `[{"intent": "...", "result": "...", "status": "UNTESTED"}]`
- Default status = UNTESTED (no verification yet)

**10. Update `chunk_code()` dispatcher:**
- Add cases for `.js`, `.ts`, `.tsx`, `.jsx` → `_chunk_javascript()`
- Keep existing `.py` → `_chunk_python()` (now AST-based)
- Add case for `.json` with PHASE-IR detection → `_chunk_phase_ir()`
- Fallback: existing simple chunker

**11. Add `chunk_document()` dispatcher:**
- Route ADR files → `_chunk_adr()`
- Route SPEC files → `_chunk_spec()`
- Route other markdown → `_chunk_by_headings()` with `^##` pattern
- Route `.txt` → simple line-based chunking (500 lines per chunk)

### test_enhanced_chunkers.py (20+ tests)

**Python AST chunking (5 tests):**
- Test chunking Python file with 3 functions → 3 chunks
- Test chunking Python class with 2 methods → 1 class chunk or 3 chunks (class + 2 methods)
- Test IR pair extraction from docstring with `# IR: intent → result`
- Test syntax error handling (invalid Python) → empty list + warning
- Test empty file → empty list

**JavaScript chunking (4 tests):**
- Test chunking JS file with `function foo()` and `const bar = () =>`
- Test nested functions (only outer scope chunked)
- Test class chunking with `class Foo { method() {} }`
- Test edge case: unmatched braces → skip malformed code

**PHASE-IR chunking (3 tests):**
- Test valid PHASE-IR JSON with 5 nodes → 5 chunks
- Test IR pairs extracted from node metadata
- Test invalid JSON → empty list

**ADR chunking (3 tests):**
- Test ADR with 3 decisions → 3 chunks
- Test decision numbering preserved
- Test single decision → 1 chunk

**SPEC chunking (3 tests):**
- Test SPEC with 4 sections → 4 chunks
- Test heading preserved in chunk content
- Test nested headings (only `##` splits, not `###`)

**Helpers (2 tests):**
- Test `_create_chunk()` computes char_count and token_estimate correctly
- Test `_extract_ir_pairs_from_docstring()` with multiple IR pairs

## Acceptance Criteria

- [ ] All listed files modified/created
- [ ] All tests pass (`python -m pytest tests/hivenode/rag/test_enhanced_chunkers.py -v`)
- [ ] No file exceeds 500 lines
- [ ] PORT not rewrite — same AST approach, same IR pair extraction as platform/efemera
- [ ] TDD: tests written first
- [ ] 20+ tests covering all new chunkers, IR pair extraction, edge cases (empty files, syntax errors)
- [ ] Existing chunker tests still pass (backward compatibility)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260314-TASK-111-RESPONSE.md`

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
