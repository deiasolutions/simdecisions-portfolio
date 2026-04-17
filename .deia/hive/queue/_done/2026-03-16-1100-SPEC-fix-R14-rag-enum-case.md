# SPEC: Fix RAG models enum case mismatch (43 failures)

## Priority
P0.90

## Model Assignment
haiku

## Objective
Change enum string values in models.py from uppercase to lowercase to match API contract.

## Task File
`.deia/hive/tasks/2026-03-16-TASK-R14-fix-rag-models-enum-case.md`

## Acceptance Criteria
- [ ] All enum string values lowercase in models.py
- [ ] All 50 tests in test_models.py pass
- [ ] No regressions in other RAG tests
