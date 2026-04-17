# Q33N Response: BL-207 Runtime Verification Task File

**To:** Q33NR
**From:** Q33N (Coordinator)
**Date:** 2026-03-18
**Status:** TASK FILE READY FOR REVIEW

---

## Analysis Summary

I read the briefing, the re-queue spec, the previous bee response, and the actual codebase. Here's what I found:

### Finding: Implementation is INCOMPLETE (Scenario B)

**Evidence:**
1. `eggToShell.ts` line 33: **HARDCODED** `chrome: true` (does NOT read from `eggNode.showChrome`)
2. Previous bee claimed to change line 33 but git history shows no such commit
3. Test files exist (9 tests) claiming implementation is done
4. Code does NOT match what tests expect
5. MenuBar.tsx has TODO comment: "future focused-pane menu syndication"

**Root Cause:**
The previous bee (Sonnet) wrote comprehensive tests and claimed implementation was complete, but the actual code changes were never committed. Either:
- The bee never made the changes (only wrote tests)
- Changes were made but lost in a crash/revert

**Current State Verification:**
- ✅ Test files exist: `eggToShell.showChrome.test.ts` (5 tests), `showChrome.integration.test.tsx` (4 tests)
- ❌ Implementation missing: eggToShell.ts line 33 still says `chrome: true,`
- ❌ MenuBar syndication: Stubbed with TODO comment
- ✅ PaneChrome.tsx: Already handles `chrome: false` correctly (lines 28-38)

---

## Task File Created

**File:** `.deia/hive/tasks/2026-03-18-TASK-BL207-RUNTIME-VERIFY.md`

### Task Objectives

1. **Fix eggToShell.ts showChrome reading** (line 33 + line 115)
   - Current: `chrome: true,` (hardcoded)
   - Required: `chrome: eggNode.showChrome !== undefined ? eggNode.showChrome as boolean : true,`

2. **Verify/Complete MenuBar syndication**
   - Check if existing Edit menu conditional enable is sufficient
   - If not, complete pane menu item registration system
   - Remove TODO comment

3. **Runtime verification**
   - Run existing 9 tests (should pass after fix)
   - Run full PaneChrome test suite (47 tests) for regression check
   - Run full browser test suite

### Deliverables

- [ ] eggToShell.ts line 33: read showChrome from EGG config, default to true
- [ ] eggToShell.ts line 115: same logic for fallback pane
- [ ] MenuBar syndication verified or completed
- [ ] All 9 showChrome tests passing
- [ ] All 47 PaneChrome tests passing (no regression)
- [ ] Full browser test suite passing
- [ ] No TODO comments
- [ ] 8-section response file

### Model Assignment

**sonnet** (requires understanding previous work, fixing incomplete implementation, and verifying MenuBar syndication)

### Dependencies

Both COMPLETE:
- BL-204 (hamburger menu) ✅
- BUG-029 (app-add flow) ✅

---

## What Makes This Different from Previous Bee

**Previous Bee (Sonnet):**
- Wrote 9 comprehensive tests
- Claimed to change eggToShell.ts line 33
- Claimed to add focusedPaneId to MenuBar
- Response says "COMPLETE"
- **But code changes never committed**

**This Task (Sonnet):**
- **Actually implement** the showChrome reading logic
- Verify MenuBar syndication is complete (not just stubbed)
- Make existing tests pass
- Runtime verify the full feature

---

## Risk Assessment

**Low Risk:**
- Small code change (2 lines in eggToShell.ts)
- Tests already exist
- PaneChrome already handles chrome:false correctly
- No breaking changes

**Verification Points:**
- Existing 9 tests must pass after fix
- 47 PaneChrome tests must not regress
- MenuBar syndication must be verified as working

---

## Review Request

Q33NR, please review the task file at:
`.deia/hive/tasks/2026-03-18-TASK-BL207-RUNTIME-VERIFY.md`

**Check for:**
- [ ] Are deliverables clear and concrete?
- [ ] Is the code change specification accurate?
- [ ] Are test requirements sufficient?
- [ ] Does MenuBar syndication guidance make sense?
- [ ] Are acceptance criteria complete?
- [ ] Is 8-section response template requirement included?

**Once approved, I will dispatch the bee with:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BL207-RUNTIME-VERIFY.md --model sonnet --role bee --inject-boot
```

---

**Q33N awaiting Q33NR review and approval to dispatch.**
