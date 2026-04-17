# Q33N Report: TASK-BUG-036 Ready for Review

**From:** Q33N
**To:** Q33NR
**Date:** 2026-03-18
**Status:** TASK FILE READY FOR REVIEW

---

## Summary

I have created a task file for BUG-036 (Build Monitor Tree Layout Fix) based on the briefing from Q33NR.

## Task File Created

**Path:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-036-build-monitor-tree-layout.md`

## What the Task Requires

The bee will fix two functions in `buildStatusMapper.ts`:

1. **`mapActiveBees()` (lines 148-159):**
   - Move detail (model, elapsed time, cost) from child node into main label
   - Keep lastMsg as a child node (if present)
   - Result: `B: SPEC-001 haiku 5m $0.023` (one line)

2. **`mapCompletedTasks()` (lines 260-274):**
   - Move detail (time, duration, cost) from child node into main label
   - Remove children array entirely
   - Result: `SPEC-001 14:32 12m $0.045` (one line)

## Approach

- **TDD:** Update tests first to expect new structure
- **Model:** haiku (simple refactor)
- **File count:** 2 files modified (implementation + tests)
- **No breaking changes:** Internal structure only

## Validation

- File paths: All absolute ✓
- No stubs: Pure function refactor ✓
- No hardcoded colors: No CSS changes ✓
- Under 500 lines: 279 lines currently ✓
- TDD required: Yes ✓
- All 8 response sections required: Yes ✓

## Ready for Q33NR Review

Please review the task file. If approved, I will dispatch the bee with:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG-036-build-monitor-tree-layout.md --model haiku --role bee --inject-boot
```

---

**Awaiting Q33NR approval to dispatch.**
