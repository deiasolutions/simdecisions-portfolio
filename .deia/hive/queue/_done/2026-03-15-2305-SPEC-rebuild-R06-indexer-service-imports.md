# SPEC: Fix RAG indexer_service.py imports + storage.py methods

## Priority
P0.30

## Model Assignment
sonnet

## Objective
Restore lost import fixes and model schema alignments in `indexer_service.py`, add missing public methods to `storage.py`, and fix test assertions.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R06-fix-rag-indexer-imports-storage.md`

## Acceptance Criteria
- [ ] All imports fixed (chunker, embedder, scanner)
- [ ] All model field mismatches corrected
- [ ] Storage API methods added: get_chunks(), get_embeddings(), list_all(limit=...)
- [ ] All 13 indexer service tests pass
