# Fix REQUEUE2-BL207: FALSE POSITIVE — No Fix Needed

**Status:** SPEC INVALID (work already complete)
**Model:** Sonnet (Q33NR)
**Date:** 2026-03-18

## Summary

This fix spec was auto-generated based on a "failed" status in monitor-state.json. However, investigation reveals **the work was completed successfully**. No fix is needed.

## Evidence of Completion

### 1. Source Code Verified
**File:** `browser/src/shell/eggToShell.ts`
- **Line 33:** ✅ Changed to `chrome: eggNode.chrome !== false,`
- **Line 115:** ✅ Changed to `chrome: eggNode.chrome !== false,`

Both hardcoded `chrome: true` instances are gone.

### 2. Tests Pass
```
✓ 18/18 tests passing in eggToShell.test.ts
✓ 3/3 chrome-specific tests passing:
  - maps chrome: false from EGG pane to AppNode with chrome: false
  - defaults chrome to true when not specified in EGG pane
  - maps chrome: true from EGG pane to AppNode with chrome: true
```

### 3. Git Commit Exists
```
d3b6ca1 [BEE-SONNET] 2026-03-18-SPEC-REQUEUE2-BL207-chrome-opt-out: task completed (NEEDS_DAVE)
```

The commit message includes "(NEEDS_DAVE)" which is a queue runner tag requesting review, NOT a failure indicator.

### 4. Response File Complete
**File:** `.deia/hive/responses/20260318-TASK-BL207-RESPONSE.md`
- ✅ All 8 required sections present
- ✅ Status: COMPLETE
- ✅ All acceptance criteria marked [x]
- ✅ Test results documented
- ✅ No issues or follow-ups

## Why Monitor State Shows "Failed"

The monitor-state.json shows:
```json
{
  "task_id": "QUEUE-TEMP-2026-03-18-SPEC-REQUEUE2-BL207-chrome-opt-out",
  "status": "failed",
  "message": "duration=636.9s turns=23"
}
```

**Root cause:** The regent bee was dispatched with `role=regent` instead of `role=bee`. The task completed successfully, but the role mismatch may have triggered a "failed" status in the monitor.

**Actual outcome:** Work is complete. Source changed. Tests pass. Response file written.

## Acceptance Criteria (Original Spec)

From `2026-03-18-SPEC-REQUEUE2-BL207-chrome-opt-out.md`:

- [x] `chrome: true` is NO LONGER hardcoded on lines 33 and 115 ✅
- [x] EGG pane with `"chrome": false` hides title bar ✅
- [x] EGG pane without chrome field shows title bar (default ON) ✅
- [x] All eggToShell tests pass (18/18) ✅

## Recommendation

**CLOSE THIS SPEC AS FALSE POSITIVE.**

The original REQUEUE2-BL207 spec is complete. No fix is needed. The queue runner should:
1. Move `2026-03-18-SPEC-REQUEUE2-BL207-chrome-opt-out.md` to `_done/`
2. Move this fix spec to `_dead/` (false alarm)
3. Continue to next spec in queue

## Files Modified

None. No changes were needed.

## What Was Done

- Read original spec
- Read bee response files
- Verified source code changes in eggToShell.ts
- Re-ran tests to confirm 18/18 passing
- Verified git commit exists
- Analyzed monitor-state.json
- Determined this is a false positive

## Test Results

Re-ran eggToShell tests:
```
✓ 18/18 tests passing
Duration: 8.64s
```

No failures. No regressions.

## Build Verification

**Tests:** ✅ 18/18 passing
**Source:** ✅ Both lines fixed
**Commit:** ✅ d3b6ca1 exists on dev branch

## Clock / Cost / Carbon

**Clock:** 5 minutes (investigation only)
**Cost:** $0.08 (analysis, file reads, test run)
**Carbon:** ~0.3g CO2e

## Issues / Follow-ups

**Queue runner improvement:** The monitor should distinguish between:
- **failed** = bee couldn't complete the work
- **needs_review** = bee completed but flagged for human review

The "(NEEDS_DAVE)" tag in the commit message indicates the latter, not the former.

**Process note:** This is Fix Cycle 1 of 2. Since the original work is complete, no Fix Cycle 2 is needed. Mark as CLOSED.
