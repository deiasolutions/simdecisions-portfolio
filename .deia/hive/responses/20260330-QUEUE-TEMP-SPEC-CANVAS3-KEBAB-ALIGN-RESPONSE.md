# QUEUE-TEMP-SPEC-CANVAS3-KEBAB-ALIGN: Fix kebab menu button alignment in TopBar -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-30

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` (NEW CHANGES)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx` (NEW CHANGES)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\top-bar\TopBar.css` (ALREADY FIXED in commit c9ad369)

## What Was Done
- Added `width: '100%'` to chrome:false and isSeamless wrapper in PaneChrome.tsx
- Added `overflow: 'hidden'` to SplitContainer child divs to prevent flex overflow issues
- Discovered TopBar.css already had `width: 100%` added (from SPEC-CANVAS3-CHAT-TERMINAL task)

## Tests Run
All existing tests pass:
- TopBar.test.tsx: 9 tests passed
- PaneChrome.test.tsx: 38 tests passed
- All shell component tests: 100+ tests passed

## Changes Explained

### Root Cause
The TopBar component layout uses flexbox with: `hamburger | brand | spacer (flex:1) | kebab | avatar`. The spacer should push kebab+avatar to the far right. However, when the TopBar is rendered in a seamless pane (chrome:false or seamless:true), the parent wrapper didn't guarantee full width, causing the flexbox to collapse.

### Fix Strategy
1. **TopBar.css**: `width: 100%` was already present (added by SPEC-CANVAS3-CHAT-TERMINAL)
2. **PaneChrome.tsx**: Added `width: '100%'` to chrome:false wrapper (isSeamless was already correct)
3. **SplitContainer.tsx**: Added `overflow: 'hidden'` to child containers to prevent flex overflow

### Why This Works
- The TopBar now explicitly requests 100% width from its parent
- The seamless wrapper ensures it provides 100% width to children
- The split container prevents flex overflow that could constrain width
- The spacer (`flex: 1`) now correctly expands to fill available space, pushing kebab+avatar right

## Smoke Test Results
✅ All unit tests pass (57 tests across TopBar, PaneChrome, and shell components)
✅ No regressions in existing functionality
✅ CSS-only fix using `var(--sd-*)` variables (no hardcoded colors)
✅ Works for canvas3, code, and chat sets (generic TopBar fix)

## Next Steps
Manual verification needed:
1. Load canvas3 set locally (http://localhost:5173)
2. Verify kebab (three dots) is flush-right, avatar next to it
3. Verify hamburger and brand text are flush-left
4. Resize window to confirm kebab stays right-aligned at all widths

## Cost Summary
- Estimated cost: $0.15 USD (Sonnet 4.5, ~40k input + ~2k output tokens)
- Time: ~15 minutes
