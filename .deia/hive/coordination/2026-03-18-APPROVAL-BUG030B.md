# APPROVAL: TASK-BUG030B — Fix chatHistoryAdapter tests

**Date:** 2026-03-18
**From:** Q33NR (Regent)
**To:** Q33N (Queen Coordinator)
**Task:** `2026-03-18-TASK-BUG030B-fix-chat-history-tests.md`

---

## Review Result: ✅ APPROVED

All mechanical checklist items pass:

- ✅ Deliverables match spec
- ✅ File paths are absolute
- ✅ Test requirements present (2 commands, expected counts)
- ✅ No CSS changes (test-only task)
- ✅ File size constraint explicit (275 lines current, under 500 limit)
- ✅ No stubs allowed (explicit)
- ✅ 8-section response template included

---

## Task Summary

**Objective:** Fix chatHistoryAdapter.test.ts mock expectations to match API contract

**What bee will do:**
1. Change hardcoded 'conv-1' to dynamic regex pattern
2. Fix volume defaults to 'home://' and 'both'
3. Fix badge expectations for offline status ('🔴')
4. NO changes to adapter source code

**Expected outcome:**
- All 9 chatHistoryAdapter tests pass
- No regressions (163+ tests still passing)
- $0.15-0.25 cost estimate (sonnet, ~15-20 min)

---

## Dispatch Approved

Q33N: **You may now dispatch the bee.**

Command:
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG030B-fix-chat-history-tests.md --model sonnet --role bee --inject-boot
```

After bee completes, report results to Q33NR for final review.
