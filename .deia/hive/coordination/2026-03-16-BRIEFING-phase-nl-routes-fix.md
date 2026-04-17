# BRIEFING: Fix Phase NL Routes (R17)

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Priority:** P0.94 (part of rebuild verification cycle)

## Objective

Dispatch TASK-R17 to fix 15 test failures where `/api/phase/nl-to-ir` endpoint returns 404.

## Context

This is part of the R13 full integration verification cycle. After the git reset recovery, 15 tests in `test_phase_nl_routes.py` are failing because the NL-to-IR route module is missing or unregistered.

The task file already exists at:
- `.deia/hive/tasks/2026-03-16-TASK-R17-fix-phase-nl-routes.md`

The task was created but not yet dispatched to a bee.

## What Q33N Must Do

1. **Review the task file** — verify it's complete and ready for dispatch
2. **Dispatch TASK-R17 to a sonnet bee** using:
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-R17-fix-phase-nl-routes.md --model sonnet --role bee --inject-boot
   ```
3. **Wait for bee completion** and check the response file
4. **Report results to Q33NR**

## Model Assignment

**sonnet** — The spec explicitly assigns sonnet for this task.

## Files Referenced

- Task: `.deia/hive/tasks/2026-03-16-TASK-R17-fix-phase-nl-routes.md`
- Tests: `tests/hivenode/test_phase_nl_routes.py`
- Routes init: `hivenode/routes/__init__.py`
- Expected response: `.deia/hive/responses/20260316-TASK-R17-RESPONSE.md`

## Acceptance Criteria

- [ ] TASK-R17 dispatched to sonnet bee
- [ ] Bee completes and writes response file with all 8 sections
- [ ] All 15 Phase NL route tests pass
- [ ] `/api/phase/nl-to-ir` endpoint responds (not 404)
- [ ] No regressions in other tests

## Notes

This is a straightforward dispatch task. The task file is already written and reviewed. Q33N should dispatch immediately and monitor for completion.
