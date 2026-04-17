# SPEC: Re-register DES routes in __init__.py

## Priority
P0.05

## Model Assignment
haiku

## Objective
Re-register the DES routes module in `hivenode/routes/__init__.py`. The module (`des_routes.py`) survived the git reset but its registration was lost.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R01-re-register-des-routes.md`

## Acceptance Criteria
- [ ] `des_routes` imported in `hivenode/routes/__init__.py`
- [ ] Router registered with prefix `/api/des` and tag `des`
- [ ] All 22 tests in `tests/hivenode/test_des_routes.py` pass
- [ ] No regressions in other route tests
