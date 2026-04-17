# BRIEFING: Fix REQUEUE-BUG030 — Dispatch the Approved Bee

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Priority:** P0
**Bot ID:** REGENT-QUEUE-TEMP-2026-03-18-2007-SPE

---

## Problem

The REQUEUE-BUG030 spec processing got interrupted after you created and I approved TASK-BUG030B. The bee was **never dispatched**. The task file exists and is approved, but no bee ran.

---

## What Needs to Happen

**Dispatch the bee NOW using the already-approved task file.**

### Task File (already created, already approved)
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`

### Approval File (already exists)
`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\coordination\2026-03-18-APPROVAL-BUG030B.md`

---

## Your Instructions

1. **Dispatch the bee immediately:**
   ```bash
   python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md --model sonnet --role bee --inject-boot
   ```

2. **Wait for bee to complete**

3. **Read bee response file:**
   - Expected location: `.deia/hive/responses/20260318-TASK-BUG030B-RESPONSE.md`
   - Verify all 8 sections present
   - Verify tests pass

4. **Report results to Q33NR**

---

## Context

This is a fix cycle (1 of 2) for the original REQUEUE-BUG030 spec. The problem is clear:
- Adapter code is correct
- Test mocks are broken (wrong expectations)
- Bee needs to fix test file only

Task file already contains:
- Specific fixes needed (dynamic conversationId, correct volume defaults, badge fixes)
- Test commands
- All constraints
- 8-section response template

---

## Expected Outcome

After bee completes:
- All 30 chatHistoryAdapter tests pass
- No regressions in tree-browser suite (163+ tests still passing)
- 8-section response file written
- Ready for commit

---

## Model Assignment
**sonnet** — Bee task already assigned sonnet model

---

## Constraints

- Do NOT rewrite the task file (it's already approved)
- Do NOT modify the spec (it's correct)
- Just dispatch the bee and report results

---

**This is a mechanical execution. No planning needed. Just dispatch.**
