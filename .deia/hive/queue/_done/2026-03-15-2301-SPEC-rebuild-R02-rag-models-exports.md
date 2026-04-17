# SPEC: Restore RAG models exports + CCC_PER_FILE fix

## Priority
P0.10

## Model Assignment
haiku

## Objective
Add compatibility aliases to `models.py` and fix CCC_PER_FILE constant in `indexer_service.py`. Update `__init__.py` exports to include all model classes.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R02-restore-rag-models-exports-ccc-fix.md`

## Acceptance Criteria
- [ ] Compatibility aliases added to models.py
- [ ] CCC_PER_FILE constant uses correct field names
- [ ] All 50 tests in `tests/hivenode/rag/test_models.py` pass
