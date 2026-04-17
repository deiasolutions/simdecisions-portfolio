# BUG-037: Palette Click-to-Add Task Files Ready

**Status:** TASK FILES READY FOR Q33NR REVIEW
**Model:** Sonnet
**Date:** 2026-03-18
**Coordinator:** Q33N

---

## Summary

Task file created for BUG-037 (Palette Click-to-Add Broken). This is a single-bee task requiring Sonnet.

## Root Cause Analysis

After reading the codebase and recent BUG-022 response files, I identified the issue:

**The architecture is partially wired:**
1. ✅ `treeBrowserAdapter.tsx` (line 209-218) broadcasts `palette:node-drag-start` when palette node selected
2. ✅ Palette nodes have `meta.nodeType` with correct type (Task, Queue, Start, etc.)
3. ❌ **CanvasApp.tsx does NOT subscribe to this message**
4. ✅ CanvasApp has drag-and-drop handlers but these require physical dragging
5. ❌ **Click-to-place functionality is missing**

**Naming confusion:**
- Implementation sends: `palette:node-drag-start`
- Test file expects: `palette:node-click` (line 37, 311, 322)
- **Solution:** Standardize to `palette:node-click` (clearer semantics)

**What broke it:**
BUG-022 response file (line 35) claimed "Click handling already wired" but this was incorrect. TreeBrowserAdapter broadcasts the message, but CanvasApp never listens.

## Task Files Created

### TASK-BUG-037-palette-click-to-add.md
**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG-037-palette-click-to-add.md`

**Deliverables:**
1. Update `treeBrowserAdapter.tsx` to send `palette:node-click` (not `palette:node-drag-start`)
2. Add `PaletteNodeClickData` interface to `messages.ts`
3. Add click-to-place handler to `CanvasApp.tsx` bus subscription (lines 181-215)
4. Verify all 13 existing tests pass

**Test Coverage:**
- Tests already exist: `paletteClickToPlace.test.tsx` (13 tests, 334 lines)
- Covers: message broadcast, node creation, unique IDs, all node types, edge cases
- Implementation must pass existing tests (TDD reverse)

**Model:** Sonnet (careful bus integration + ReactFlow position calculation)

**Complexity:** Low-Medium
- Clear implementation pattern from `onDrop` handler
- Existing test file provides exact specification
- Single file modification (CanvasApp.tsx) + type definitions

**Dependencies:** None

## Files Referenced in Task

Read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx` (lines 179-215, 421-439, 147-149)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (lines 208-218)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\paletteClickToPlace.test.tsx` (full file)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

## Constraints Verified

- [x] CanvasApp.tsx is 525 lines (grandfathered, don't make larger)
- [x] All deliverables specified
- [x] TDD requirement met (tests already exist)
- [x] No stubs allowed (all functions fully implemented)
- [x] No hardcoded colors
- [x] Absolute file paths in task doc
- [x] 8-section response template included

## Dispatch Plan

**Single bee, Sonnet:**
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-18-TASK-BUG-037-palette-click-to-add.md --model sonnet --role bee --inject-boot
```

**Estimated effort:** 30-45 minutes
- Read files: 5 min
- Add message type: 5 min
- Update treeBrowserAdapter: 5 min
- Add CanvasApp subscription: 15 min
- Run tests: 5 min
- Write response: 10 min

## Next Steps

Awaiting Q33NR review of task file. Ready to dispatch on approval.

---

## Q33N Notes

This bug is a reversion from BUG-022. The fix is straightforward:
1. Rename message type for clarity (`palette:node-click` is clearer than `palette:node-drag-start`)
2. Add bus subscription in CanvasApp (pattern already exists in lines 181-215)
3. Use existing node creation pattern from `onDrop` handler
4. Tests already exist and are comprehensive

No architectural changes needed. This is a simple wiring fix.
