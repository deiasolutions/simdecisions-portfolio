# BRIEFING: Fix TASK-224 Dispatch Role Issue

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-17-1502-SPE)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Priority:** P0
**Original Spec:** 2026-03-17-1502-SPEC-fix-TASK-224-directory-state-machine.md

---

## Problem

TASK-224 (Directory State Machine) failed because it was dispatched with **role=regent** when it should have been dispatched with **role=bee**. The spec file contains implementation work (code, tests), not coordination work.

From the bee response (20260317-1500-BEE-SONNET-QUEUE-TEMP-2026-03-16-SPEC-TASK-224-DIRECTORY-STATE-MACHINE-RAW.txt):

> "This task appears to be addressed directly to me as if I'm a BEE worker, not as Q33NR. The task includes implementation deliverables like 'Create `_active/`, `_failed/`, etc.' and 'Implement pickup logic' and 'Create tests.'"
>
> "According to HIVE.md:
> - Q33NR NEVER writes code
> - Q33NR writes briefings for Q33N
> - Q33N writes task files
> - BEEs write code"

The bee correctly refused to execute because of role mismatch.

---

## Root Cause

The spec processor (`spec_processor.py`) or queue runner (`run_queue.py`) is incorrectly assigning **role=regent** to spec files that should be **role=bee** tasks.

Looking at the spec:
- It has `## Model Assignment: sonnet`
- It has implementation deliverables (create directories, implement logic, write tests)
- This is clearly **BEE WORK**, not regent work

---

## What Q33N Must Do

Create a task file that tells a BEE to:

1. **Investigate** why TASK-224 was dispatched with role=regent
   - Check `.deia/hive/scripts/queue/spec_processor.py` - does it have logic to determine role from spec content?
   - Check `.deia/hive/scripts/queue/run_queue.py` - how does it assign roles during dispatch?

2. **Fix the role assignment logic**
   - Specs with implementation deliverables → **role=bee**
   - Specs with coordination directives → **role=queen**
   - Specs asking for briefings/reviews → **role=regent**

3. **Re-dispatch TASK-224** with correct role=bee after fix

4. **Test the fix**
   - Create a test spec with implementation deliverables
   - Verify it gets dispatched with role=bee
   - Verify the bee executes it successfully

---

## Context Files

Read these first:
- `.deia/hive/scripts/queue/spec_processor.py` - spec parsing and role detection
- `.deia/hive/scripts/queue/run_queue.py` - dispatch logic
- `.deia/hive/queue/_done/2026-03-16-SPEC-TASK-224-directory-state-machine.md` - the original spec
- `.deia/hive/responses/20260317-1500-BEE-SONNET-QUEUE-TEMP-2026-03-16-SPEC-TASK-224-DIRECTORY-STATE-MACHINE-RAW.txt` - the failure response

---

## Acceptance Criteria

- [ ] Role assignment logic correctly identifies bee tasks vs regent tasks vs queen tasks
- [ ] TASK-224 is re-dispatched with role=bee
- [ ] TASK-224 completes successfully (implementation done, tests pass)
- [ ] No regression on existing queue processing

---

## Model Assignment

**haiku** - this is a targeted bug fix, not complex architecture

---

## Constraints

- Do not change the TASK-224 spec content (it's correct)
- Do not change HIVE.md role definitions (they're correct)
- Fix the dispatcher/processor logic that assigns roles
- Follow TDD (write tests for role detection first)

---

## Next Steps for Q33N

1. Read the context files
2. Write a task file for a BEE to fix the role assignment logic
3. Return the task file to Q33NR for review
4. After approval, dispatch the bee
5. Monitor completion
6. Report results

---

**Q33NR Note:** This is fix cycle 1 of 2 for TASK-224. If this fix doesn't work, we have one more cycle before escalating to NEEDS_DAVE.
