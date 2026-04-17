# BL-207 Re-Queue 2 — COMPLETE

**To:** Q88N (Dave — Human Sovereign)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Time:** 20:54

---

## Status: COMPLETE ✅

**BL-207 (Re-Queue 2): EGG chrome opt-out** is now COMPLETE after two failed attempts.

---

## What Was Fixed

**File:** `browser/src/shell/eggToShell.ts`
**Lines changed:** 33 and 115

**Before:**
```typescript
chrome: true,  // hardcoded on both lines
```

**After:**
```typescript
chrome: eggNode.chrome !== false,  // reads from EGG config, defaults to true
```

**Behavior:**
- EGG panes with `"chrome": false` now hide their title bar
- EGG panes without chrome field show title bar (default true)
- EGG panes with `"chrome": true` show title bar

---

## Test Results

**File:** `browser/src/shell/__tests__/eggToShell.test.ts`

**Tests:** 18 passing (15 existing + 3 new)
- ✓ maps chrome: false from EGG pane to AppNode with chrome: false
- ✓ defaults chrome to true when not specified in EGG pane
- ✓ maps chrome: true from EGG pane to AppNode with chrome: true

**All existing tests still pass.** No regressions.

---

## Why This Succeeded (After 2 Failures)

### First Attempt (BL-207 original)
- Bee left `chrome: true` hardcoded
- Did not read EGG config

### Re-Queue 1
- Bee wrote a "runtime verify briefing" instead of changing code
- Zero source changes landed

### Re-Queue 2 (THIS)
- Briefing explicitly stated: "YOU MUST CHANGE SOURCE CODE"
- Task file repeated: "If you only write tests, you have FAILED"
- Bee understood and modified source code correctly

---

## What Unblocked

This fix unblocks **BUG-036** (Build Monitor tree layout test), which depends on the build-data-service pane having `chrome: false`.

---

## Files Modified

1. `browser/src/shell/eggToShell.ts` — lines 33 and 115
2. `browser/src/shell/__tests__/eggToShell.test.ts` — added 3 test cases

---

## Process Notes

**Q33NR workflow:**
1. ✅ Wrote briefing for Q33N (crystal clear instructions)
2. ✅ Dispatched Q33N to write task file
3. ✅ Reviewed Q33N's task file (approved)
4. ✅ Dispatched Q33N to dispatch bee
5. ✅ Bee completed task (source code modified, tests pass)
6. ✅ Verified source code changes in repo
7. ✅ Verified tests pass (ran tests myself)

**Q33N correction:**
Q33N correctly identified that the original briefing was wrong about line 115 needing to be in a "fallback with no eggNode." Actually, line 115 is still inside the function with eggNode access, so changing both lines was correct. Good analysis by Q33N.

---

## Cost / Clock / Carbon

**Bee:** 4 minutes, ~$0.02, ~2g CO2e (per bee response)
**Q33N:** ~2 dispatches (briefing → approval), ~$2.80 total
**Total:** ~$2.82, ~10 minutes wall time

---

## Next Steps

1. **Commit:** The bee's changes are ready to commit
2. **Deploy:** Ready for dev branch merge
3. **Smoke test:** Can manually verify build-monitor.egg chrome behavior

---

## Q88N: Your Options

1. **Approve commit** — I can write commit message and commit to dev
2. **Test manually** — Load build-monitor.egg and verify build-service pane has no chrome
3. **Move to next spec** — This spec is done, queue can continue

---

## Spec Location

- Original: `.deia/hive/queue/_done/2026-03-17-SPEC-TASK-BL207-unified-title-bar.md`
- Re-queue 1: `.deia/hive/queue/_done/2026-03-18-SPEC-REQUEUE-BL207-unified-title-bar.md`
- Re-queue 2: `.deia/hive/tasks/QUEUE-TEMP-2026-03-18-SPEC-REQUEUE2-BL207-chrome-opt-out.md`

This spec can now be moved to `_done/`.

---

**END OF REPORT**
