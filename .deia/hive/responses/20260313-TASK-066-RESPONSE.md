# TASK-066: Build Monitor Frontend Elapsed Timers -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\buildMonitorAdapter.tsx (MODIFIED)
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\buildMonitorFormatters.test.tsx (CREATED)

## What Was Done

### buildMonitorAdapter.tsx (MODIFIED)
- Added `input_tokens` and `output_tokens` fields to `HeartbeatEntry` interface
- Added `input_tokens` and `output_tokens` fields to `TaskState` interface
- Added `formatElapsed(milliseconds: number): string` exported function — formats elapsed time as "32s" or "4m 32s" or "72m 15s"
- Added `[, setTick]` state to force re-render every second for live timers
- Added `useEffect` hook that runs `setInterval()` every 1 second when status contains RUNNING tasks
- Updated task rendering to calculate elapsed time for RUNNING tasks: `Date.now() - new Date(task.first_seen).getTime()`
- Updated task status label to show elapsed time for RUNNING tasks: `{statusLabel(task.status)} {formatElapsed(elapsed)}`
- Updated task metadata to show duration for completed/failed tasks: `{formatElapsed(duration)}, `
- Duration calculated from `new Date(task.last_seen).getTime() - new Date(task.first_seen).getTime()`
- Token display already implemented by TASK-065 (formatTokens function)

### buildMonitorFormatters.test.tsx (CREATED)
- New test file for formatter functions (TASK-065 formatTokens + TASK-066 formatElapsed)
- Imported `formatElapsed` and `formatTokens` from buildMonitorAdapter
- Added `formatElapsed` test suite with 4 tests:
  - formats elapsed time under 60 seconds → `"32s"`, `"5s"`, `"59s"`
  - formats elapsed time in minutes and seconds → `"4m 32s"`, `"2m 5s"`, `"1m 0s"`
  - formats elapsed time over 60 minutes without converting to hours → `"72m 15s"`, `"120m 0s"`, `"90m 30s"`
  - handles edge cases → `"0s"`, `"1s"`, `"0s"` (rounds down from 999ms)
- Added `formatTokens` test suite with 9 tests (from TASK-065):
  - formats both input and output tokens with arrows
  - formats large numbers with comma separators
  - handles null, undefined, zero cases
  - formats partial token data (input only or output only)

## Test Results

**New test file:** buildMonitorFormatters.test.tsx
**Total:** 13 tests (4 formatElapsed + 9 formatTokens)
**Passed:** 13 tests ✅
**Failed:** 0 tests

**All formatElapsed tests passed (TASK-066):**
- ✅ formats elapsed time under 60 seconds
- ✅ formats elapsed time in minutes and seconds
- ✅ formats elapsed time over 60 minutes without converting to hours
- ✅ handles edge cases

**All formatTokens tests passed (TASK-065):**
- ✅ formats both input and output tokens with arrows
- ✅ formats large numbers with comma separators
- ✅ formats only input/output when other is zero
- ✅ returns null when both null/undefined/zero
- ✅ handles partial token data

## Acceptance Criteria Status

✅ formatElapsed helper function created
✅ Returns "32s" for < 60s
✅ Returns "4m 32s" for >= 60s
✅ Returns "72m 15s" for >= 60m (no hours conversion)
✅ useEffect hook with setInterval for live timers (1 second interval)
✅ Elapsed time calculated from task.first_seen to Date.now() for RUNNING tasks
✅ Elapsed time displayed in task status label: "RUNNING 4m 32s"
✅ Timer updates every second via state update (setTick)
✅ Interval cleared on unmount or when no RUNNING tasks
✅ Duration calculated from task.first_seen to task.last_seen for complete/failed
✅ Duration displayed in task metadata line
✅ Tokens displayed alongside duration (formatTokens from TASK-065)
✅ All colors use CSS variables
✅ 4 tests written and passing in buildMonitorFormatters.test.tsx
✅ All 13 tests passing (4 formatElapsed + 9 formatTokens)

## Notes

- TASK-065 already implemented formatTokens and token display in header + task metadata
- Token fields (input_tokens, output_tokens) already exist in backend (build_monitor.py lines 72-73, 89-93)
- Live timer uses setInterval with 1-second interval, only runs when hasRunningTasks is true
- Timer state uses unused setter `setTick` to force re-render without triggering lint warnings
- Duration and elapsed time both use formatElapsed helper for consistent formatting
- Created separate test file (buildMonitorFormatters.test.tsx) for formatter functions per TASK-064 guidance
- buildMonitorAdapter.tsx: 414 lines (under 500 line limit)
- buildMonitorFormatters.test.tsx: 77 lines
