# SPEC: Register RAG routes + canvas chat routes in __init__.py

## Priority
P0.35

## Model Assignment
haiku

## Objective
Restore route registrations for `rag_routes.py` and `canvas_chat.py` in `hivenode/routes/__init__.py`.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R07-register-rag-canvas-routes.md`

## Acceptance Criteria
- [ ] RAG routes registered with prefix `/api/rag` and tag `rag-indexer`
- [ ] Canvas chat routes registered with tag `canvas-chat`
- [ ] All 16 RAG route tests pass
- [ ] All canvas chat tests pass (if test file exists)
