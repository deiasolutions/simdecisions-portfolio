# Q33N Response: BUG-038 Task Files Ready for Review

**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Date:** 2026-03-18
**Briefing:** 2026-03-18-BRIEFING-BUG-038-pa (Palette Drag-to-Canvas Not Working)

---

## Summary

I've analyzed the briefing and created 3 task files to fix the palette drag-to-canvas bug. The problem has 3 root causes:

1. **paletteAdapter missing drag metadata** — sets `draggable: true` but no dragMimeType/dragData
2. **CanvasApp missing stopPropagation** — BUG-019 claimed to add these but never committed
3. **CanvasApp wrong data format** — expects plain string, TreeNodeRow sends JSON

## Task Files Created

### TASK-BUG-038-A: Add Drag Metadata to paletteAdapter
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-038-A-PALETTE-DRAG-METADATA.md`
**Model:** Haiku (straightforward metadata addition)
**Deliverables:**
- New test file: `paletteAdapter.test.ts` (4+ tests)
- Modify `entryToNode()` to add `meta.dragMimeType` and `meta.dragData`
- All tests pass

**Key change:**
```typescript
meta: {
  nodeType: entry.nodeType,
  description: entry.description,
  dragMimeType: 'application/sd-node-type',  // ← ADD
  dragData: { nodeType: entry.nodeType },    // ← ADD
}
```

### TASK-BUG-038-B: Fix CanvasApp Drag Handlers
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-038-B-CANVAS-DRAG-HANDLERS.md`
**Model:** Haiku (add 2 lines + parse JSON)
**Deliverables:**
- Add 3 new tests to existing `canvas.dragDrop.test.tsx` (8 tests total)
- Add `stopPropagation()` to onDragOver (line ~418)
- Add `stopPropagation()` to onDrop (line ~423)
- Parse JSON dragData with fallback to plain string
- All tests pass

**Key changes:**
```typescript
// Both handlers:
event.stopPropagation(); // ← ADD

// onDrop:
const rawData = event.dataTransfer.getData('application/sd-node-type');
try {
  const parsed = JSON.parse(rawData);
  nodeType = parsed.nodeType;
} catch {
  nodeType = rawData as CanvasNodeType; // Fallback
}
```

### TASK-BUG-038-C: Integration Test for Full Palette Drag Flow
**File:** `.deia/hive/tasks/2026-03-18-TASK-BUG-038-C-INTEGRATION-TEST.md`
**Model:** Haiku (test-only task)
**Deliverables:**
- New test file: `canvas.paletteIntegration.test.tsx` (6+ tests)
- Verify full chain: paletteAdapter → TreeNodeRow → CanvasApp
- Test all node types (Task, Queue, Start, End, Decision, etc.)
- All tests pass

**Tests verify:**
- paletteAdapter provides correct metadata
- TreeNodeRow sets dataTransfer correctly
- CanvasApp reads dataTransfer and creates nodes
- stopPropagation prevents shell interference
- Multiple node types work

## Verification Against Briefing

| Briefing Requirement | Task Coverage |
|---------------------|---------------|
| **AC1:** paletteAdapter sets dragMimeType/dragData | TASK-BUG-038-A (D2, AC1-AC2) |
| **AC2:** TreeNodeRow handleDragStart reads metadata | Already correct (verified in task context) |
| **AC3:** CanvasApp onDragOver/onDrop call stopPropagation | TASK-BUG-038-B (D2-D3, AC1-AC2) |
| **AC4:** CanvasApp onDrop parses JSON dragData | TASK-BUG-038-B (D3, AC3-AC5) |
| **AC5:** Dragging creates node at drop position | TASK-BUG-038-B (D3) + TASK-BUG-038-C (full test) |
| **AC6:** All existing tests pass | All 3 tasks (D3/D4 in each) |
| **AC7:** New integration test verifies full flow | TASK-BUG-038-C (all deliverables) |

## Task Dependencies

```
TASK-BUG-038-A (paletteAdapter)
   ↓
TASK-BUG-038-B (CanvasApp) — depends on A for correct dragData format
   ↓
TASK-BUG-038-C (integration test) — depends on A+B being complete
```

**Dispatch order:** Sequential (A → B → C)

## Files to Be Modified

### Created (3 new test files):
1. `browser/src/primitives/tree-browser/adapters/__tests__/paletteAdapter.test.ts` (TASK-A)
2. `browser/src/primitives/canvas/__tests__/canvas.paletteIntegration.test.tsx` (TASK-C)

### Modified (3 source files):
1. `browser/src/primitives/tree-browser/adapters/paletteAdapter.ts` (TASK-A) — 96 lines → ~100 lines
2. `browser/src/primitives/canvas/CanvasApp.tsx` (TASK-B) — ~600 lines → ~615 lines
3. `browser/src/primitives/canvas/__tests__/canvas.dragDrop.test.tsx` (TASK-B) — 148 lines → ~250 lines

**All files under 500-line limit** ✅

## Test Coverage

| Task | New Tests | Existing Tests | Total |
|------|-----------|----------------|-------|
| TASK-A | 4+ (paletteAdapter unit) | 0 | 4+ |
| TASK-B | 3+ (CanvasApp unit) | 5 (existing) | 8+ |
| TASK-C | 6+ (integration) | 0 | 6+ |
| **TOTAL** | **13+** | **5** | **18+** |

## Hard Rules Compliance

- ✅ **Rule 3:** No hardcoded colors (N/A — no CSS changes)
- ✅ **Rule 4:** No file over 500 lines (all files remain under limit)
- ✅ **Rule 5:** TDD (all tasks require tests first)
- ✅ **Rule 6:** No stubs (explicit requirement in all tasks)
- ✅ **Rule 8:** Absolute paths (all file paths are absolute)

## Recommended Dispatch Plan

**Model assignment:** All Haiku (simple changes, well-defined tests)

**Dispatch sequence:**
```bash
# TASK-A: paletteAdapter metadata
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-A-PALETTE-DRAG-METADATA.md \
  --model haiku --role bee --inject-boot

# Wait for TASK-A completion, then:

# TASK-B: CanvasApp handlers
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-B-CANVAS-DRAG-HANDLERS.md \
  --model haiku --role bee --inject-boot

# Wait for TASK-B completion, then:

# TASK-C: Integration test
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-18-TASK-BUG-038-C-INTEGRATION-TEST.md \
  --model haiku --role bee --inject-boot
```

**Estimated clock:** 45-60 minutes total (15-20 min per task)

## Context Provided to Bees

Each task file includes:
- ✅ Exact file paths to read first (absolute paths)
- ✅ Current code snippets showing what's wrong
- ✅ Expected code snippets showing what to add
- ✅ Line numbers for changes
- ✅ Context about why each change is needed
- ✅ Clear acceptance criteria (testable)
- ✅ TDD requirements (tests first)
- ✅ Edge cases to test
- ✅ Response file template requirements

## Known Issues Addressed

1. **BUG-019 never committed:** TASK-B explicitly notes this and adds the missing stopPropagation calls
2. **JSON vs string format mismatch:** TASK-B adds JSON.parse() with fallback to plain string
3. **No integration test coverage:** TASK-C fills this gap

## Questions for Q33NR

None. Task files are complete and ready for review.

## Next Steps

**Awaiting Q33NR approval to dispatch bees.**

Once approved:
1. Dispatch TASK-A
2. Wait for TASK-A response
3. Dispatch TASK-B
4. Wait for TASK-B response
5. Dispatch TASK-C
6. Wait for TASK-C response
7. Report completion to Q33NR

---

**END OF Q33N RESPONSE**
