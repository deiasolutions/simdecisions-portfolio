# SPEC-fix-DECOMP-01-design-to-specs: Fixed -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-06

## Files Modified

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\claude_cli_subprocess.py` (line 757-773)
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\adapters\cli\test_success_detection.py` (new file, 103 lines)

## What Was Done

### Root Cause Analysis

The original SPEC-DECOMP-01 task was dispatched to a bee configured with the `regent` role (Q88NR-bot). The bee correctly identified a protocol conflict:
- The spec asked Q88NR to directly write specs
- But Q88NR's protocol says "always go through Q33N, never code directly"

The bee stopped and asked for clarification: "This requires your decision. I am waiting for explicit direction before proceeding."

However, the completion detection heuristic in `claude_cli_subprocess.py` marked this as `success=True` because:
1. The output didn't contain explicit failure keywords ("error:", "failed", "exception")
2. The default behavior is to return True when unsure
3. The words "waiting" and "requires your decision" were not recognized as blocker signals

This caused a **false completion** — the dispatcher thought the task succeeded when it actually blocked waiting for human input.

### The Fix

Modified `_check_success()` method in `claude_cli_subprocess.py` (lines 757-773):

**Added blocker detection (checked FIRST, before success indicators):**
```python
# Check for blocked/waiting states first (these are NOT success)
blocker_indicators = ["waiting for", "requires your decision",
                    "waiting for explicit direction", "requires dave",
                    "needs_dave", "blocked by", "cannot proceed"]
if any(indicator in output_lower for indicator in blocker_indicators):
    return False
```

**Order of checks is now:**
1. **Blocker indicators** → return False (NEW)
2. Success indicators → return True
3. Failure indicators → return False
4. Default → return True (unchanged)

This ensures that when a bee explicitly signals it's waiting or blocked, the task is marked as failed (not success), triggering proper error handling.

### Tests Added

Created `test_success_detection.py` with 7 comprehensive test cases:
1. ✓ Success indicators are detected
2. ✓ Failure indicators are detected
3. ✓ **Blocker indicators return False** (NEW - this is the fix)
4. ✓ Ambiguous output defaults to True
5. ✓ Bare questions without blocker words default to True (documented limitation)
6. ✓ Mixed signals: blockers take precedence over success indicators
7. ✓ Failures in stderr are detected

All 7 tests pass.

## Tests Run

**New tests created:**
```bash
pytest hivenode/adapters/cli/test_success_detection.py -v
# Result: 7 passed in 7.64s

pytest hivenode/adapters/cli/test_decomp01_regression.py -v
# Result: 3 passed in 5.58s
```

**Regression testing (existing tests):**
```bash
pytest tests/hivenode/adapters/cli/test_claude_cli_token_tracking.py -v
# Result: 23 passed in 3.06s
```

**Total:** 33/33 tests passed ✓

## Acceptance Criteria Status

- [x] All original acceptance criteria still pass (no regression)
- [x] Reported errors are resolved (false completion fixed)
- [x] No new test regressions (7/7 tests pass)
- [x] Fix is minimal and surgical (6 new lines of blocker detection)
- [x] Existing tests unaffected (no breaking changes to heuristic defaults)

## Impact

### Before Fix
- Bees waiting for human input were marked as successful
- Dispatcher would move task to `_done/` without human review
- Silent failures (work not done, but marked complete)

### After Fix
- Bees explicitly signaling "waiting" or "blocked" are marked as failed
- Dispatcher will **not** move task to `_done/`
- Task remains in `_active/` with `success=False` in response file
- Human operator (Q88N) can see the blocker and respond appropriately

## Next Steps (for Q88N/Dave)

1. **Re-dispatch SPEC-DECOMP-01** with clarified protocol:
   - Either tell Q88NR to directly write the specs (override protocol for this task)
   - Or tell Q88NR to follow protocol and dispatch Q33N as usual

2. **Review other active tasks** in `_active/` for similar false completions

3. **Consider additional blocker phrases** to add to the heuristic if other patterns emerge

## Cost / Duration

- **Fix time:** ~15 minutes
- **Test time:** ~5 minutes
- **Total:** ~20 minutes
- **Cost:** ~$0.20 (Sonnet, fix + test development)

## Notes

This is a **heuristic fix**, not a perfect solution. The completion detection still relies on keyword matching. If a bee blocks without using explicit blocker language, it may still be misclassified as successful. However, this fix covers the most common patterns and significantly reduces false completions.

**Better long-term solution:** Have bees explicitly emit structured status markers (e.g., `## STATUS: BLOCKED` or `## STATUS: COMPLETE`) that the parser can reliably detect.
