# SPEC: Add 2 smoke tests to RAG routes test file

## Priority
P0.50

## Model Assignment
haiku

## Objective
Restore two test methods added to `tests/hivenode/rag/test_rag_routes.py` that were lost in the git reset.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R10-add-rag-routes-smoke-tests.md`

## Acceptance Criteria
- [ ] `test_query_endpoint_exists` added to TestQueryRoute class
- [ ] `test_query_missing_query_param` added to TestQueryRoute class
- [ ] All RAG route tests pass
