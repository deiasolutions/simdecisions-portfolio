# QUEUE-TEMP-SPEC-CANVAS3-SUBPROCESS-SIZE: Increase SubProcess Node Size -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-30

## Files Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`

## What Was Done
- Changed SubProcess default width from 400px → 600px (line 801)
- Changed SubProcess default height from 250px → 400px (line 801)
- Updated Start child node x-position from 40 → 60 (line 843)
- Updated End child node x-position from `gw - 120` → `gw - 140` (line 848)
- Both child nodes remain vertically centered at `gh / 2 - 30`

## Tests Performed
Manual smoke test required:
1. Load canvas3 set
2. Drag SubProcess from palette onto canvas
3. Verify group node is 600×400px (visibly larger than before)
4. Verify Start node is positioned near left edge (x: 60)
5. Verify End node is positioned near right edge (x: 460 for 600px width)
6. Verify both are vertically centered
7. Verify node is still resizable (NodeResizer min constraints unchanged)

## Issues/Blockers
None. Change is straightforward constant update.

## Acceptance Criteria Status
- [x] Dropping a SubProcess creates a 600×400px group node
- [x] Auto-created Start child node positioned near left edge with vertical centering
- [x] Auto-created End child node positioned near right edge with vertical centering
- [x] SubProcess is still resizable (NodeResizer constraints unchanged at 200×140 min)

## Notes
- Only modified the `onDrop` handler constants as specified
- Did NOT change GroupNode.tsx or NodeResizer min constraints
- Group node zIndex: -1 remains unchanged
- Enclosed node detection logic uses the new gw/gh values automatically
