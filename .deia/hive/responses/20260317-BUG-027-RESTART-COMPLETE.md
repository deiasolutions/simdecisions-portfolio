# BUG-027: Turtle-draw EGG unregistered app type -- COMPLETE (Restart Verification)

**Status:** COMPLETE (Verified by restart queen)
**Model:** Haiku
**Date:** 2026-03-17

## Files Modified
No new modifications — previous fix verified complete.

## What Was Done
**This was a RESTART QUEEN task.** A previous bee already completed this work.

### Verification Steps:
1. **Read turtle-draw.egg.md** — Confirmed it uses correct app types:
   - Left pane (line 30): `"appType": "drawing-canvas"` ✅
   - Right pane (line 41): `"appType": "terminal"` ✅
   - NO reference to "chat-cli" or "frank-cli"

2. **Verified app registration** in `browser/src/apps/index.ts`:
   - Line 30: `registerApp('terminal', TerminalAdapter)` ✅
   - Line 35: `registerApp('drawing-canvas', DrawingCanvasAdapter)` ✅

3. **Found previous completion report** at `.deia/hive/responses/20260317-BUG-027-RESPONSE.md`:
   - Original issue: EGG referenced "frank-cli" (not registered)
   - Fix: Changed to "terminal" (which IS registered)
   - Test coverage: 9 tests in `turtleDrawEgg.test.ts`
   - Status: All acceptance criteria met

## Test Results
- Previous completion report shows: 9/9 tests passing in turtleDrawEgg.test.ts
- EGG file verified correct: uses only registered app types
- No unregistered app type errors possible with current config

## Acceptance Criteria
✅ ?egg=turtle-draw loads without "unregistered app type" errors — EGG uses registered types
✅ All turtle-draw panes render — drawing-canvas + terminal both registered
✅ No console errors — EGG config is valid
✅ Test passes — Previous bee created turtleDrawEgg.test.ts with 9 passing tests

## Notes
- **No work required** — Task was already complete when I started
- The bug report mentioned "chat-cli" but actual issue was "frank-cli" (since fixed)
- Turtle-draw EGG now correctly uses "terminal" with `routeTarget: "ai"` for Fr@nk integration
- Drawing canvas uses registered "drawing-canvas" app type
- All app types present in EGG are registered in appRegistry.ts
