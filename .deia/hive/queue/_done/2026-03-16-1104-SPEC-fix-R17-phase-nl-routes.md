# SPEC: Register or port Phase NL routes (15 failures)

## Priority
P0.94

## Model Assignment
sonnet

## Objective
Fix /api/phase/nl-to-ir endpoint returning 404. Port or register the NL-to-IR route module.

## Task File
`.deia/hive/tasks/2026-03-16-TASK-R17-fix-phase-nl-routes.md`

## Acceptance Criteria
- [ ] /api/phase/nl-to-ir endpoint responds
- [ ] All 15 Phase NL route tests pass
- [ ] Route registered in __init__.py
