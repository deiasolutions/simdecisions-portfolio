# Dispatch Instruction: Fix Sim EGG Tests

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Regent)
**Date:** 2026-03-18

---

## Status

Your task file `.deia/hive/tasks/2026-03-18-TASK-FIX-SIM-EGG-TESTS.md` has been **APPROVED** for dispatch.

---

## Action Required

Dispatch the bee NOW using this exact command:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-FIX-SIM-EGG-TESTS.md --model haiku --role bee --inject-boot
```

---

## Expected Result

- Haiku bee makes 3 file edits
- Runs 4 test files
- All 11 tests pass
- Writes response file to `.deia/hive/responses/20260318-FIX-SIM-EGG-TESTS-RESPONSE.md`

---

## After Dispatch

1. Wait for bee completion
2. Read bee response file
3. Verify all 8 sections present
4. Verify test results (11 passes, 0 failures)
5. Report completion to Q33NR with summary

---

## DO NOT

- Do NOT create new task files
- Do NOT modify the existing task file
- Do NOT dispatch multiple bees
- Just dispatch the ONE haiku bee for the approved task file
