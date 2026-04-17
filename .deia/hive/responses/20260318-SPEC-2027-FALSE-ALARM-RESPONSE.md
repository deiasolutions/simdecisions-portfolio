# SPEC-2027: Fix REQUEUE-BUG031 -- FALSE_ALARM

**Status:** FALSE_ALARM (queue runner logic issue)
**Model:** Sonnet (Q33NR regent)
**Date:** 2026-03-18

## Files Modified
None — spec closed without work.

## What Was Done
- ✅ Read spec 2027 claiming BUG031 fix failed
- ✅ Investigated error: "No such file or directory: QUEUE-TEMP-2026-03-18-1945-SPEC..."
- ✅ Traced to previous cycle: SPEC-1945 was closed as FALSE POSITIVE
- ✅ Verified BUG-031 code changes present: `browser/src/apps/treeBrowserAdapter.tsx`
- ✅ Verified tests passing: 4/4 in `treeBrowserAdapter.fileSelected.test.tsx`
- ✅ Confirmed original bee response: COMPLETE
- ✅ Identified root cause: Queue runner doesn't recognize false positive closures
- ✅ Wrote briefing for Q88N: `.deia/hive/coordination/2026-03-18-BRIEFING-SPEC-2027-FALSE-ALARM.md`
- ✅ Moved spec to `_needs_review/` with NEEDS_DAVE flag

## Test Results
Not applicable — no code changes made.

Original tests remain passing:
```bash
cd browser && npx vitest run src/primitives/tree-browser/adapters/__tests__/treeBrowserAdapter.fileSelected.test.tsx
# Result: 4 passed (Tests: 4 passed, 4 total)
```

## Build Verification
Not applicable — no code changes made.

Existing build verified healthy during investigation.

## Acceptance Criteria
This spec's acceptance criteria cannot be met because the premise is false:

- [ ] All original acceptance criteria still pass → **N/A** (original already passed)
- [ ] Reported errors are resolved → **N/A** (error was false alarm)
- [ ] No new test regressions → **✅** (no changes made, no regressions)

**Why FALSE_ALARM:** The "error" reported was that a task file for SPEC-1945 doesn't exist. This is EXPECTED and CORRECT behavior — SPEC-1945 was closed as a false positive without creating task files because the regent verified the original work succeeded.

## Clock / Cost / Carbon
- **Clock:** 15 minutes (investigation + verification + documentation)
- **Cost:** $0.15 USD (regent analysis + file reads)
- **Carbon:** ~0.02 kg CO2e (estimated)

## Issues / Follow-ups

### Root Cause: Queue Runner Logic Gap

The queue runner generates fix specs when:
1. Bee completes with `Success: False` in RAW file
2. Task file doesn't exist

**Problem:** The runner doesn't check if the spec was already closed as FALSE_POSITIVE by a regent in a previous cycle.

**Result:** False alarm fix specs like SPEC-2027.

### Recommended Fix

Add to queue runner spec processing logic:

```python
def should_generate_fix_spec(spec_id, error):
    # Check if previous cycle closed as false positive
    response_files = glob(f".deia/hive/responses/*{spec_id}*")
    for response in response_files:
        content = read(response)
        if "FALSE_POSITIVE" in content or "FALSE_ALARM" in content:
            return False  # Don't generate fix spec

    # Check if error is "task file not found"
    if "No such file or directory" in error and "QUEUE-TEMP" in error:
        # Regent may have closed without task files — verify
        if regent_closed_without_tasks(spec_id):
            return False

    return True  # Generate fix spec
```

### BUG-031 Final Status

**✅ RESOLVED** — Code EGG file selection works correctly.

**Fix applied:** `browser/src/apps/treeBrowserAdapter.tsx` lines 191-204
**Tests:** 4/4 passing in `treeBrowserAdapter.fileSelected.test.tsx`
**Verified by:** Original bee (REQUEUE) + Q33NR (SPEC-1945) + Q33N (SPEC-1945)

No further action needed on BUG-031.

---

## ⚠️ NEEDS_DAVE

**Issue:** Queue runner logic creates false alarm fix specs when regent closes specs as false positives without task files.

**Flag:** This spec moved to `_needs_review/` — requires Dave's decision on:
1. Should queue runner be updated to detect false positive closures?
2. Should regent workflow change to always create task files (even for false positives)?
3. Accept current behavior as "low-cost noise" and manually close false alarms?

**Cost impact:** ~$0.15-0.30 per false alarm (regent investigation time). Low frequency (1-2 per batch).

---

**Summary:** SPEC-2027 is a false alarm triggered by queue runner logic. BUG-031 is resolved. No code changes needed. Moved to _needs_review for Dave's review of queue runner behavior.
