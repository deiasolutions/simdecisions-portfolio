# BRIEFING-BUG022B: Canvas Palette Click-to-Place — Q33N RESPONSE

**Status:** Task file ready for Q33NR review
**Model:** Sonnet
**Date:** 2026-03-18

---

## Task File Created

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-18-TASK-BUG022B-canvas-click-to-place.md`

**Task ID:** TASK-BUG022B
**Model Assignment:** Sonnet
**Priority:** P0

---

## Analysis Summary

After reading the briefing and examining the codebase, I identified the exact issue:

### Root Cause
Previous bees wrote comprehensive tests (`paletteClickToPlace.test.tsx`, 10 tests, 334 lines) but **never modified the source code** to implement the feature. The tests define the contract perfectly, but there's no implementation.

### Architecture Review
The bus infrastructure is sound:
- MessageBus works (verified by BUG-024 tests)
- CanvasApp has bus subscription pattern (line 181-214)
- TreeBrowser has onSelect callback (line 111, 171)
- EGG config defines pane IDs: `canvas-palette` and `canvas-editor`

### What's Missing
1. **TreeBrowser** does not detect palette nodes (nodes with `meta.nodeType`) and publish `palette:node-click` events
2. **CanvasApp** does not subscribe to `palette:node-click` events
3. Bus prop may not be wired through to TreeBrowser (needs verification)

---

## Task File Structure

The task file breaks the work into three clear deliverables:

### Part 1: TreeBrowser publishes palette:node-click
- Add `bus` prop to TreeBrowserProps
- Detect palette nodes via `meta.nodeType`
- Publish bus event with correct structure
- Don't break existing onSelect behavior

### Part 2: CanvasApp subscribes to palette:node-click
- Add subscription in existing useEffect
- Extract nodeType from message
- Create node with unique ID at viewport center
- Add to canvas via setNodes

### Part 3: Wire bus prop
- Find where TreeBrowser is instantiated for palette
- Pass bus prop when adapter is 'palette'
- Document if bus is unavailable at that level

---

## Test Coverage

All required tests already exist:
- **10 tests** in `paletteClickToPlace.test.tsx` (must pass)
- **15 tests** in `TreeNodeRow.icon.test.tsx` (no regressions)
- **Integration tests** in `TreeNodeRow.palette-icons.integration.test.tsx` (no regressions)

Tests define the exact contract:
- Message type: `'palette:node-click'`
- Message structure: `{ type, sourcePane, target, nonce, timestamp, data: { nodeType } }`
- Node creation: unique ID, lowercase type, viewport center position
- Edge cases: null bus, missing nodeType, null data

---

## Key Files and Line Numbers

Provided specific line references for the bee:
- **TreeBrowser.tsx:111** — onSelect on Enter key
- **TreeBrowser.tsx:171** — onSelect passed to TreeNodeRow
- **TreeNodeRow.tsx:86** — onSelect on click
- **CanvasApp.tsx:181-214** — Bus subscription block

---

## Constraints Verified

- ✅ No file over 500 lines (TreeBrowser: 184 lines, CanvasApp: ~500 lines)
- ✅ TDD approach (tests exist, implement code to pass them)
- ✅ No stubs required (clear implementation path)
- ✅ No messageBus.ts modifications (only publishers/subscribers)
- ✅ Type safety (TypeScript interfaces defined)

---

## Recommended Approach

1. Start with TreeBrowser (simpler, isolated change)
2. Then CanvasApp (add subscription)
3. Find palette TreeBrowser instantiation and wire bus
4. Run tests incrementally

---

## Smoke Test Commands

Provided 5 test commands:
1. Palette click-to-place tests (10 tests)
2. Icon regression tests (15 tests)
3. Palette integration tests
4. Full tree-browser suite
5. Full canvas suite

---

## Edge Cases Documented

From test file analysis:
- Null/undefined bus handling
- Missing nodeType in message
- Null data in message
- Exact message type matching
- Unique ID generation
- Support all node types

---

## Re-Queue Emphasis

Added strong warning at bottom of task file:
> **REMEMBER:** This is a re-queue because previous bees only wrote tests. You must modify BOTH TreeBrowser/TreeNodeRow AND CanvasApp source files. No more tests. Actual implementation code only.

---

## Ready for Review

**Q33NR:** This task file is ready for your review. It provides:
- ✅ Clear objective (click palette item → node appears on canvas)
- ✅ Specific deliverables (3 parts with checkboxes)
- ✅ All required file paths (absolute paths)
- ✅ Test requirements (10 tests must pass, no regressions)
- ✅ Exact acceptance criteria (copy from spec)
- ✅ Smoke test commands (5 commands)
- ✅ Implementation notes (line numbers, approach, edge cases)
- ✅ Response file requirements (8 sections)
- ✅ Model assignment (Sonnet)
- ✅ Priority (P0)

**Awaiting your approval to dispatch.**
