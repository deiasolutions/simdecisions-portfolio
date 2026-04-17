# BRIEFING: Add TFIDFEmbedder and IndexStorage exports

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-15-2304-SPEC-rebuild-R05-embedder-storage-exports.md`
**Priority:** P0.25
**Model:** haiku

---

## Objective

Add missing exports to `hivenode/rag/indexer/__init__.py`:
- `TFIDFEmbedder` (from embedder.py)
- `IndexStorage` (from storage.py)
- `compute_content_hash` (from storage.py)

## Context

These exports are needed to complete the RAG indexer module public API. All three items already exist in their respective files:
- `TFIDFEmbedder` at `hivenode/rag/indexer/embedder.py:16`
- `IndexStorage` at `hivenode/rag/indexer/storage.py:47`
- `compute_content_hash` at `hivenode/rag/indexer/storage.py:35`

Current `__init__.py` exports Scanner and scan (from scanner.py) and various model classes, but is missing the embedder and storage exports.

## Acceptance Criteria (from spec)

- [ ] TFIDFEmbedder exported from `hivenode.rag.indexer`
- [ ] IndexStorage and compute_content_hash exported from `hivenode.rag.indexer`
- [ ] All 34 embedder tests pass
- [ ] All storage tests pass

## Files Involved

**Primary file to modify:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py`

**Files to read first:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\embedder.py` (to confirm TFIDFEmbedder)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` (to confirm IndexStorage, compute_content_hash)

**Test files to run:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_embedder.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\rag\indexer\test_storage.py`

## Constraints

- Follow existing import/export pattern in `__init__.py`
- Maintain alphabetical ordering in `__all__` list
- No file over 500 lines (not applicable — `__init__.py` is 38 lines)
- No stubs
- TDD (tests already exist — this is just exporting existing code)

## Next Steps for Q33N

1. Read this briefing
2. Write a single task file for a BEE (haiku)
3. Return to Q33NR for review (do NOT dispatch yet)
4. After Q33NR approval, dispatch the bee
5. Review bee response and report results to Q33NR
