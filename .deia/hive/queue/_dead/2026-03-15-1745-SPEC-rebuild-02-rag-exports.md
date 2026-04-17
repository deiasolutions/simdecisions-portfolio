# SPEC: Rebuild RAG indexer __init__.py exports

## Priority
P0.10

## Model Assignment
haiku

## Objective
Re-add all imports and exports to `hivenode/rag/indexer/__init__.py` that were lost in a git reset. Five tasks layered changes onto this file:

1. TASK-151: Model exports (IRPair, Chunk, EmbeddingRecord, etc.)
2. TASK-152: Scanner import + export
3. TASK-153: Chunker import + export
4. TASK-155: IndexStorage + compute_content_hash exports
5. TASK-161: IndexerService import + __all__

## Recovery Sources
Read these response files for exact changes:
- `.deia/hive/responses/20260315-TASK-151-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-152-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-153-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-155-RESPONSE.md`
- `.deia/hive/responses/20260315-TASK-161-RESPONSE.md`

Also check what modules exist in `hivenode/rag/indexer/` directory — all the .py files survived as untracked. The __init__.py just needs its imports updated to expose them.

**CRITICAL: Read the surviving test files — they show exactly what imports must work:**
- `tests/hivenode/rag/indexer/test_storage.py` — shows IndexStorage imports
- `tests/hivenode/rag/indexer/test_scanner.py` — shows Scanner imports
- `tests/hivenode/rag/indexer/test_indexer_service.py` — shows IndexerService imports
- `tests/hivenode/rag/indexer/test_models.py` — shows all model class imports
- `tests/hivenode/rag/indexer/conftest.py` — shows shared fixtures and imports
- `tests/hivenode/rag/test_chunker.py` — shows Chunker imports
- `tests/hivenode/rag/indexer/test_embedder.py` — shows Embedder imports

**Also read the source modules directly** — each .py file in `hivenode/rag/indexer/` has its own exports at the top. Collect them all into __init__.py.

## Acceptance Criteria
- [ ] All RAG submodules importable: models, scanner, chunker, embedder, storage, indexer_service
- [ ] __all__ list includes all public exports
- [ ] `python -m pytest tests/hivenode/rag/indexer/ -v` passes (core tests)
- [ ] `python -c "from hivenode.rag.indexer import Scanner, Chunker, IndexStorage, IndexerService"` works
- [ ] No import errors

## Constraints
- Max 500 lines per file
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-02-rag-exports", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-02-rag-exports", "files": ["hivenode/rag/indexer/__init__.py"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
