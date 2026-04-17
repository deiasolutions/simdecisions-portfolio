# SPEC-RAG-DEDUP-001-fix-dual-routing: Fix Dual RAG Route Registration

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

The RAG system has two separate route registrations that collide: `hivenode/routes/rag_routes.py` (mounted via `routes/__init__.py` line 34) and `hivenode/rag/routes.py` (mounted in `main.py` line 619 at `/api/rag`). Both serve similar endpoints, causing "last-mounted wins" ambiguity. Consolidate to a single RAG router with one mount point.

## Files to Read First

- hivenode/main.py
- hivenode/routes/__init__.py
- hivenode/routes/rag_routes.py
- hivenode/rag/routes.py
- hivenode/rag/bok/routes.py
- hivenode/rag/indexer/routes.py

## Acceptance Criteria

- [ ] RAG endpoints are served from exactly ONE router registration, not two
- [ ] All RAG functionality (search, index, query, status) is preserved — no endpoints lost
- [ ] The kept implementation is the more complete one (compare endpoint counts and features between the two files)
- [ ] The removed implementation's file is deleted (not left as dead code)
- [ ] `routes/__init__.py` and `main.py` have no duplicate RAG router mounts
- [ ] BOK and indexer sub-routers remain correctly mounted as children of the RAG router
- [ ] All existing RAG tests still pass
- [ ] 2+ new tests: verify no duplicate route paths, verify all expected RAG endpoints respond

## Smoke Test

- [ ] `curl -s http://127.0.0.1:8420/api/rag/status` returns 200
- [ ] `curl -s http://127.0.0.1:8420/api/rag/search?q=test` returns 200
- [ ] No duplicate route warnings in hivenode startup logs

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Preserve all existing RAG functionality — this is a dedup, not a rewrite
- Keep the `/api/rag` prefix
