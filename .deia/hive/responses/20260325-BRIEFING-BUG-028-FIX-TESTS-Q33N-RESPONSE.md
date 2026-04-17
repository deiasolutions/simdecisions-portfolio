# Q33N Response: BUG-028 Regression Test Fix

**From:** Q33N (QUEEN-2026-03-25-BRIEFING-BUG-028-FI)
**To:** Q33NR
**Date:** 2026-03-25
**Status:** TASK FILE READY FOR REVIEW

---

## Summary

I have analyzed the failing BUG-028 regression tests and created a task file for a bee to fix them.

**Current situation:**
- Implementation code is CORRECT (treeBrowserAdapter.tsx lines 275-289)
- Tests are FAILING due to test infrastructure issues
- Status changed from bee's report: was 4/5 passing, now 2/5 failing (tests degraded)

**Root cause identified:**
1. **Mock fetch broken:** The mock `fetch` doesn't properly implement the Response interface. `json()` method needs to return a real Promise.
2. **Grouped structure:** channelsAdapter groups channels into Pinned/Channels/DMs sections. Tests need to account for nested structure.
3. **DOM selectors:** Tests search for `.tree-node-label` but may need to search within expanded groups.

---

## Task File Created

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-25-TASK-BUG-028-FIX-TESTS.md`

**Assigned to:** Sonnet

**Deliverables:**
- Fix mock fetch implementation to match Response interface
- Fix 3 failing tests (channels click, non-channel adapter, nonce/timestamp)
- All 5 tests pass
- No changes to implementation code

**Investigation checklist provided:**
- Mock fetch structure fix: `json: () => Promise.resolve(channels)`
- Account for grouped channel structure (Pinned/Channels/DMs)
- Verify DOM selectors match rendered tree
- Check timing/waitFor conditions

---

## Files Analyzed

1. `browser\src\primitives\tree-browser\__tests__\BUG-028-regression.test.tsx` (285 lines)
2. `browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (132 lines)
3. `browser\src\apps\treeBrowserAdapter.tsx` (lines 275-289)
4. `.deia\hive\responses\20260324-TASK-BUG-028-RESPONSE.md` (previous bee response)

---

## Test Failure Details

**Current test results:** 2 failed, 3 passed

### Failing:
1. ❌ "clicking a channel fires channel:selected bus event"
   - Error: `expect(generalNode).toBeTruthy()` — can't find node
   - Root cause: Mock fetch or grouped structure

2. ❌ "non-channel tree-browser adapters do NOT send channel:selected"
   - Error: Tree shows "No items" instead of loading
   - Root cause: Mock fetch for explorer adapter is wrong structure

3. ❌ "channel:selected event includes nonce and timestamp" (implied)
   - Same as test 1 — can't find node to click

### Passing:
1. ✅ "clicking a DM fires channel:selected with type=dm"
2. ✅ "clicking different channels sends separate events"

---

## Next Steps

**Awaiting Q33NR review of task file.**

Once approved, I will dispatch a Sonnet bee to:
```bash
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-25-TASK-BUG-028-FIX-TESTS.md \
  --model sonnet \
  --role bee \
  --inject-boot
```

---

## Task File Location

`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-25-TASK-BUG-028-FIX-TESTS.md`
