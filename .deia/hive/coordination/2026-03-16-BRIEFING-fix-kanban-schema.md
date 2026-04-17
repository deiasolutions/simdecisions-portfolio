# BRIEFING: Fix Kanban Schema Mismatch (SPEC-fix-R18-kanban-schema)

**From:** Q33NR-bot (REGENT-QUEUE-TEMP-2026-03-16-1102-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-16
**Priority:** P0.92

---

## Objective

Dispatch BEE to complete TASK-R18: Fix SQLAlchemy insert error in kanban routes test caused by schema mismatch.

## Context

- **Source spec:** `.deia/hive/queue/2026-03-16-1102-SPEC-fix-R18-kanban-schema.md`
- **Task file:** `.deia/hive/tasks/2026-03-16-TASK-R18-fix-kanban-schema.md` (already exists)
- **Issue:** 1 error in `tests/hivenode/test_kanban_routes.py` — SQLAlchemy insert fails on `inv_backlog` table
- **Root cause:** TASK-159 (entity archetypes port) may have modified shared database model

## What Q33N Must Do

1. **Review the existing task file** at `.deia/hive/tasks/2026-03-16-TASK-R18-fix-kanban-schema.md`
2. **Verify task file completeness** against the checklist:
   - [ ] Deliverables match spec acceptance criteria
   - [ ] File paths are absolute
   - [ ] Test requirements present
   - [ ] CSS uses var(--sd-*) only (N/A for backend fix)
   - [ ] No file over 500 lines mentioned
   - [ ] No stubs or TODOs
   - [ ] Response file template present
3. **If task file is complete:** Dispatch a Haiku BEE with the task file
4. **If task file has issues:** Fix and return to me for review
5. **After BEE completes:** Review the response file and report results to me

## Model Assignment

**Haiku** (spec says haiku, task is small fix)

## Dispatch Command (once approved)

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-R18-fix-kanban-schema.md --model haiku --role bee --inject-boot --timeout 600
```

## Acceptance Criteria (from spec)

- [ ] All kanban route tests pass
- [ ] No regressions

## Next Steps

Q33N: Review the task file and report back whether it's ready for dispatch or needs corrections.
