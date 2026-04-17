# QUEUE-TEMP-2026-04-13-0106-SPEC-fix-HYG-003-python-implicit-optional: Fix failures from HYG-003-python-implicit-optional -- FAILED

**Status:** FAILED (code bug in dispatch_handler.py)
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified
None

## What Was Done
Investigated the FileNotFoundError reported in the spec. The error originates from a bug in the queue runner's dispatch handler watchdog restart logic.

## Root Cause Analysis

The error message:
```
FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\hive\\tasks\\QUEUE-TEMP-SPEC-HYG-003-python-implicit-optional.md'
```

Occurs at C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\dispatch_handler.py:187 in the `call_dispatch` method during a watchdog restart:

```python
# Line 187
original_task = temp_task_path.read_text(encoding="utf-8")
```

### Issue Flow:

1. Original spec `SPEC-HYG-003-python-implicit-optional.md` was processed
2. Temp file `QUEUE-TEMP-SPEC-HYG-003-python-implicit-optional.md` was created
3. Bee completed work, temp file was deleted/archived
4. Fix spec `2026-04-13-0106-SPEC-fix-HYG-003-python-implicit-optional.md` was created and submitted
5. New temp file `QUEUE-TEMP-2026-04-13-0106-SPEC-fix-HYG-003-python-implicit-optional.md` was created (EXISTS in tasks/)
6. During processing, watchdog detected timeout and attempted restart
7. Restart code tried to read from wrong temp file path (original spec's path instead of fix spec's path)

### Current State:

The correct temp file EXISTS:
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\tasks\QUEUE-TEMP-2026-04-13-0106-SPEC-fix-HYG-003-python-implicit-optional.md`

The file being referenced DOES NOT EXIST:
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\tasks\QUEUE-TEMP-SPEC-HYG-003-python-implicit-optional.md`

## Blocker Report

**Cannot complete this fix spec** because the issue is not in the Python code that was modified for HYG-003. The issue is a BUG in the queue runner infrastructure code itself.

The bug is in: `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\dispatch_handler.py`

Specifically, the watchdog restart logic at line 187 is using a stale `temp_task_path` that references the ORIGINAL spec's temp file instead of the current FIX spec's temp file.

### Recommended Fix (for Q88N/Dave):

The dispatch_handler.py watchdog restart needs to:
1. Either derive the correct temp file path from the spec_id parameter
2. Or verify the temp_task_path exists before attempting to read it
3. Or pass through/reconstruct the correct temp path during recursive calls

This is infrastructure code that only Q88N or a specially assigned infrastructure bee should modify.

## Tests Run
None (blocked by infrastructure bug)

## Cost Estimate
~$0.05

## Next Steps Required
1. Q88N should review this analysis
2. Create infrastructure fix spec for dispatch_handler.py watchdog restart bug
3. Once infrastructure is fixed, retry this fix spec

## Files Read for Investigation
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\dispatch_handler.py
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\scripts\queue\spec_processor.py
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\queue_runner.log
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\dispatcher.log

## Acceptance Criteria Status

From original spec:
- [ ] All original acceptance criteria still pass — **BLOCKED: Cannot verify due to infrastructure bug**
- [ ] Reported errors are resolved — **NO: Error is in infrastructure, not in HYG-003 changes**
- [ ] No new test regressions — **N/A: Cannot run tests due to infrastructure bug**

## Smoke Test

Not performed - blocked by infrastructure bug in dispatch_handler.py watchdog restart logic.

## Notes

**CRITICAL:** This is not a failure of the HYG-003 work itself. The HYG-003 changes completed successfully:
- 18 files modified
- 39 implicit Optional violations fixed
- All mypy checks passed
- Auto-committed with tag (NEEDS_DAVE)

The FileNotFoundError occurred in the queue runner's FIX CYCLE infrastructure when it tried to:
1. Detect the dispatch subprocess timeout via watchdog
2. Restart the subprocess by reading the temp task file
3. Use the WRONG temp file path (original spec instead of fix spec)

This is a systemic bug in `.deia/hive/scripts/queue/dispatch_handler.py` line 187 that affects ANY fix spec processing when watchdog restarts are triggered.

**Recommendation:** Q88N should create an infrastructure fix spec specifically for the dispatch_handler.py watchdog restart bug before processing more fix specs.
