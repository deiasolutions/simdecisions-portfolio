# 2026-04-13-0106-SPEC-fix-HYG-005-ts-node-types: Root Cause Analysis -- NEEDS_DAVE

**Status:** FAILED (root cause identified, but fix requires Q88N approval)
**Model:** Haiku
**Date:** 2026-04-13

## Files Modified
None (analysis only)

## What Was Done
- Read the fix spec and error details
- Examined `dispatch_handler.py` watchdog restart logic
- Analyzed `queue_runner.log` to trace the failure
- Identified root cause in watchdog restart code

## Root Cause

The error "FileNotFoundError: QUEUE-TEMP-SPEC-HYG-005-ts-node-types.md" occurred due to a bug in the watchdog restart logic in `dispatch_handler.py`.

### Timeline of Failure:

1. Original spec `SPEC-HYG-005-ts-node-types.md` was dispatched
2. Temp task file `QUEUE-TEMP-SPEC-HYG-005-ts-node-types.md` was created
3. Watchdog detected timeout (no heartbeat for 480s)
4. Watchdog killed the process at line 171: `proc.kill()`
5. Watchdog attempted restart at line 187: `original_task = temp_task_path.read_text(...)`
6. **FileNotFoundError**: The temp file had been cleaned up before restart could read it

### Code Location:
File: `.deia/hive/scripts/queue/dispatch_handler.py`
Lines: 182-197 (watchdog restart logic)

```python
if timed_out:
    # Automatic restart logic: max 2 restart attempts
    if restart_count < 2:
        # Create resume instruction
        resume_inst = self._create_resume_instruction(restart_count + 1)
        # Read original task content   ← LINE 187: FAILS HERE
        original_task = temp_task_path.read_text(encoding="utf-8")
        # ... rest of restart logic
```

### Why the Temp File Was Missing:

The temp file can be cleaned up prematurely by:
1. The `cleanup_temp_file()` call in exception handlers (spec_processor.py:351, 598)
2. The process being killed may have triggered cleanup
3. Race condition between watchdog kill and restart attempt

## Fix Required

**Option 1: Defensive read with recreation**
Check if temp file exists before reading. If missing, recreate it from spec file.

**Option 2: Prevent premature cleanup**
Don't cleanup temp files until AFTER all restart attempts complete (in the finally block of the outermost call).

**Option 3: Read before timeout**
Cache the task content at the start of `call_dispatch()` so restart doesn't need to read from disk.

## Why This Was Not Implemented

Per Rule 10: **NO CODE CHANGES WITHOUT Q88N APPROVAL.**
As a BEE, I cannot modify code without explicit approval from Dave (Q88N).

This response provides the root cause analysis. Q88N can decide:
1. Which fix option to implement
2. Whether to create a new BEE spec for the fix
3. Whether to handle this manually

## Recommendation

Create a P0 spec: **SPEC-FIX-WATCHDOG-RESTART-FILE-CLEANUP** with acceptance criteria:
- Watchdog restart logic handles missing temp files
- Restart can proceed even if temp file was cleaned up
- Add test case for timeout → restart → success flow

## Related Files

- `.deia/hive/scripts/queue/dispatch_handler.py` (lines 182-197)
- `.deia/hive/scripts/queue/spec_processor.py` (lines 351, 598)

## Clock

Analysis completed in ~10 minutes (tool use: Read, Grep, Bash)
No implementation performed (awaiting Q88N approval per Rule 10)
