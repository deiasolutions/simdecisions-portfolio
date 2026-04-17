# SPEC: Add Scanner class to RAG indexer exports + fix indexer_service imports

## Priority
P0.15

## Model Assignment
haiku

## Objective
Add Scanner class import/export to `__init__.py`. Fix `indexer_service.py` imports to use correct model names and Scanner class.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R03-add-scanner-class-to-exports.md`

## Acceptance Criteria
- [ ] Scanner class exported from `hivenode.rag.indexer`
- [ ] indexer_service.py imports use correct model names
- [ ] All 32 tests in `tests/hivenode/rag/indexer/test_scanner.py` pass
