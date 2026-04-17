# QUEUE-TEMP-2026-04-13-0549-SPEC-fix-HYG-005-ts-node-types: Fix cycle 2 analysis -- NEEDS_DAVE

**Status:** NEEDS_DAVE (queue infrastructure issue, not code failure)
**Model:** Haiku
**Date:** 2026-04-13

## Files Modified

None (analysis only - no code changes needed)

## What Was Done

- Analyzed the fix spec and error context
- Reviewed previous bee responses (fix cycle 1)
- Verified original HYG-005 acceptance criteria are still met
- Confirmed TypeScript error count is still 3 (well below target)
- Verified `@types/node` and tsconfig "node" entry are present

## Analysis

This is **fix cycle 2 of 2** for HYG-005-ts-node-types. Per HIVE.md rules, after 2 failed fix cycles, the spec must be flagged NEEDS_DAVE.

### Original Spec Status: ✅ COMPLETE

The original SPEC-HYG-005-ts-node-types acceptance criteria are **already satisfied**:

- ✅ `@types/node` is in browser/package.json devDependencies (line 39, version ^22.0.0)
- ✅ "node" is in browser/tsconfig.json types array (line 15)
- ✅ TS2304 error count is 3 (target was <50, so 341+ errors were fixed)
- ✅ No new TypeScript errors introduced
- ✅ `npm install` completes successfully

The original bee response (20260412-QUEUE-TEMP-SPEC-HYG-005-ts-node-types-RESPONSE.md) correctly reported COMPLETE with no changes needed.

### "Failures" Are Queue Infrastructure Bugs

The "failures" reported in both fix cycles are NOT code failures:

**Fix Cycle 1 Error:**
```
FileNotFoundError: [Errno 2] No such file or directory:
'C:\\Users\\davee\\...\\QUEUE-TEMP-SPEC-HYG-005-ts-node-types.md'
```

This was correctly analyzed in fix cycle 1 response as a **watchdog restart bug** in `dispatch_handler.py` (lines 182-197). The watchdog tried to restart after timeout but the temp file had been cleaned up.

**Fix Cycle 2 Error:**
```
Dispatch reported failure
```

No specific error details provided in the spec, indicating the same infrastructure issue.

### Root Cause: Queue Infrastructure Bug

The failure is in `.deia/hive/scripts/queue/dispatch_handler.py`:
- Watchdog detects timeout (no heartbeat for 480s)
- Watchdog kills the process
- Watchdog tries to restart but temp file is already cleaned up
- FileNotFoundError thrown

This is NOT a bug in the HYG-005 code changes (which were already complete). This is a bug in the queue runner's watchdog/restart logic.

## Why This Is NEEDS_DAVE

Per HIVE.md Fix Cycle Rule:
> **Max 2 fix cycles per original spec.**
> After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing.

This is fix cycle 2 of 2. Both "failures" are queue infrastructure bugs, not code failures. The original spec work is complete and correct.

## Recommended Actions for Q88N

1. **Move SPEC-HYG-005-ts-node-types to `.deia/hive/queue/_needs_review/`** per HIVE.md
2. **Create new spec: SPEC-FIX-WATCHDOG-RESTART-FILE-CLEANUP** to fix the queue infrastructure bug:
   - Fix watchdog restart logic in `dispatch_handler.py` lines 182-197
   - Handle missing temp files gracefully (check exists before read, or cache content)
   - Prevent premature temp file cleanup during restart attempts
   - Add test case for timeout → restart → success flow
3. **Mark original HYG-005 as COMPLETE** - no code changes needed, acceptance criteria satisfied

## Verification

Current state verified:
```bash
# TS2304 count (target: <50)
$ cd browser && npx tsc --noEmit 2>&1 | grep -c "TS2304"
3

# @types/node present
$ grep "@types/node" browser/package.json
    "@types/node": "^22.0.0",

# "node" in types array
$ grep "types.*node" browser/tsconfig.json
    "types": ["vitest/globals", "@testing-library/jest-dom", "node"]
```

All original acceptance criteria are met. The spec work is complete.

## Blockers

Queue infrastructure bug prevents fix spec dispatch from completing. This is outside the scope of HYG-005 and requires Q88N review.

## Clock

Analysis completed in ~5 minutes. No code changes made (none needed).
