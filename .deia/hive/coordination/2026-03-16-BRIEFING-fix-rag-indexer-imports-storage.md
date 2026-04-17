# BRIEFING: Fix RAG indexer_service.py imports + storage.py methods

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-15-2305-SPEC-rebuild-R06-indexer-service-imports.md`
**Priority:** P0.30
**Model:** sonnet

---

## Objective

Fix import errors blocking RAG indexer tests. The immediate blocker is:

```
ImportError: cannot import name 'Chunk' from 'hivenode.rag.indexer.models'
```

This is happening because `hivenode/rag/indexer/chunker.py:14` imports `Chunk` from `.models`, but the models file doesn't define it. The indexer should be using `CodeChunk` from `hivenode/rag/chunkers.py` instead.

## Root Cause Analysis

The repo has **two chunking systems**:

1. **Root RAG chunkers**: `hivenode/rag/chunkers.py` with `CodeChunk` dataclass (production)
2. **Indexer chunker**: `hivenode/rag/indexer/chunker.py` (trying to import non-existent `Chunk` model)

The indexer/chunker.py was likely ported from platform without proper import alignment. The indexer should delegate to the root chunkers.py (which `indexer_service.py` already does correctly at line 17).

## Files Involved

**Problem files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\chunker.py` — imports non-existent `Chunk` from `.models`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\__init__.py` — exports `Chunker` class (which is broken)

**Reference files (correct pattern):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\chunkers.py` — defines `CodeChunk` (working)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py:17` — correctly imports from `hivenode.rag.chunkers`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py:18` — correctly imports `CodeChunk` from `hivenode.rag.chunkers`

**Already working:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\storage.py` — has `get_chunks()`, `get_embeddings()`, `list_all()` methods (spec says "add" but they already exist)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\rag\indexer\indexer_service.py` — imports are correct

## Solution

**Option 1: Remove indexer/chunker.py entirely** (RECOMMENDED)

The indexer doesn't need its own Chunker class. `indexer_service.py` already uses `chunk_file()` from `hivenode.rag.chunkers` (line 226). The `indexer/chunker.py` file is dead code creating import conflicts.

**Option 2: Fix indexer/chunker.py imports**

Change line 14 from:
```python
from .models import ArtifactType, Chunk, IRPair, IRStatus
```

To:
```python
from hivenode.rag.chunkers import CodeChunk
from .models import ArtifactType, IRPair, IRStatus
```

Then replace all references to `Chunk` with `CodeChunk`.

**RECOMMEND Option 1** — remove dead code. But check if indexer/chunker.py is actually used anywhere first.

## Acceptance Criteria (from spec)

- [ ] All imports fixed (chunker, embedder, scanner)
- [ ] All model field mismatches corrected
- [ ] Storage API methods added: get_chunks(), get_embeddings(), list_all(limit=...)
- [ ] All 13 indexer service tests pass

## Test Command

```bash
cd C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter && python -m pytest tests/hivenode/rag/indexer/test_indexer_service.py -v
```

## Constraints

- No file over 500 lines
- No stubs
- TDD (tests already exist)
- Follow existing import patterns in `indexer_service.py` and `storage.py`

## Recovery Context

This is part of rebuild batch after git reset incident (2026-03-15). The RAG indexer module was partially ported from platform but lost import alignment fixes. See damage report: `.deia/hive/coordination/2026-03-15-DAMAGE-REPORT-git-reset.md`

## Next Steps for Q33N

1. Read this briefing
2. Check if `hivenode/rag/indexer/chunker.py` is used anywhere (grep for imports)
3. Write a single task file for a BEE (sonnet)
4. Return to Q33NR for review (do NOT dispatch yet)
5. After Q33NR approval, dispatch the bee
6. Review bee response and report results to Q33NR
