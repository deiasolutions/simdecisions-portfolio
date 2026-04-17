# Q33N REPORT: BL-121 Task Files Ready for Review

**Date:** 2026-03-19
**From:** Q33N (Bot ID: QUEEN-2026-03-19-APPROVAL-BL121-WRIT)
**To:** Q33NR
**Status:** ✅ TASK FILES WRITTEN — AWAITING REVIEW

---

## Summary

I have written the 3 task files for BL-121 (Properties Panel Canvas Selection Wiring) as approved. All task files are ready for your review.

---

## Task Files Created

### TASK-BL121-A: Fix Canvas Selection Event Payload
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-19-TASK-BL121-A-fix-canvas-selection-payload.md`

**Objective:** Fix the data payload sent by CanvasApp when a node is selected.

**Key Deliverables:**
- Add TypeScript type for `CanvasNodeSelectedData` to busTypes.ts
- Update CanvasApp.tsx to send correct payload structure (nodeId + full node object)
- Add deselection handlers (background click + ESC key)
- Add TypeScript type for `canvas:node-deselected`
- Write 8+ tests for selection and deselection flows

**Files Modified:**
- `browser/src/primitives/canvas/CanvasApp.tsx`
- `browser/src/infrastructure/relay_bus/busTypes.ts`
- `browser/src/primitives/canvas/__tests__/CanvasApp.test.tsx`

**Test Requirements:** 8+ new tests, all existing tests pass

---

### TASK-BL121-B: Fix Properties Adapter Data Handling
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-19-TASK-BL121-B-fix-properties-adapter-data.md`

**Objective:** Update propertiesAdapter to correctly process canvas node data.

**Key Deliverables:**
- Update propertiesAdapter.ts to handle new CanvasNodeSelectedData payload
- Add mapping function: Canvas NodeData → property tree (General, Timing, Operator sections)
- Subscribe to `canvas:node-deselected` and clear properties pane
- Handle missing/null data gracefully
- Update existing tests + add 5+ new tests

**Files Modified:**
- `browser/src/primitives/tree-browser/adapters/propertiesAdapter.ts`
- `browser/src/primitives/tree-browser/adapters/__tests__/propertiesAdapter.test.ts`

**Test Requirements:** 5+ new tests, all existing tests pass

---

### TASK-BL121-C: Integration Tests
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-19-TASK-BL121-C-integration-tests.md`

**Objective:** Write end-to-end integration tests for the complete flow.

**Key Deliverables:**
- Create integration test file: `canvas-properties-integration.test.tsx`
- Test: select node → properties display
- Test: deselect node → properties clear
- Test: switch selection → properties update
- Test: re-select → properties restore
- Test: missing data → graceful fallback
- Test: bus event payload structure
- Test: full regression smoke test

**Files Created:**
- `browser/src/primitives/canvas/__tests__/canvas-properties-integration.test.tsx`

**Test Requirements:** 7+ integration tests

**Dependencies:** Depends on TASK-BL121-A and TASK-BL121-B completing first

---

## Review Checklist

Please verify the following for each task file:

### ✅ TASK-BL121-A
- [x] Objective is clear and specific
- [x] Context explains the problem (data shape mismatch)
- [x] Files to read are listed with absolute paths
- [x] Deliverables are concrete and testable
- [x] Test requirements are explicit (8+ tests)
- [x] Constraints stated (500 lines, CSS vars, no stubs, TDD)
- [x] Response file requirements (all 8 sections)
- [x] Acceptance criteria from spec
- [x] Smoke test commands provided
- [x] Dependencies noted (independent, can run in parallel)

### ✅ TASK-BL121-B
- [x] Objective is clear and specific
- [x] Context explains the adapter's role
- [x] Files to read are listed with absolute paths
- [x] Deliverables are concrete (mapping function, deselect handler)
- [x] Test requirements are explicit (5+ new tests)
- [x] Constraints stated (500 lines, CSS vars, no stubs, TDD)
- [x] Response file requirements (all 8 sections)
- [x] Acceptance criteria from spec
- [x] Smoke test commands provided
- [x] Dependencies noted (independent, can run in parallel)

### ✅ TASK-BL121-C
- [x] Objective is clear and specific
- [x] Context explains integration test purpose
- [x] Files to read are listed with absolute paths
- [x] Deliverables are concrete (7 specific test scenarios)
- [x] Test requirements are explicit (7+ integration tests)
- [x] Constraints stated (500 lines, no stubs)
- [x] Response file requirements (all 8 sections)
- [x] Acceptance criteria from spec
- [x] Smoke test commands provided
- [x] Dependencies noted (depends on A and B, NOT parallel)

---

## Task Breakdown Summary

| Task | Model | Parallel? | Est. Lines | Test Count | Files Modified |
|------|-------|-----------|------------|------------|----------------|
| **BL121-A** | Sonnet | ✅ Yes | ~80 | 8+ | 3 (CanvasApp, busTypes, tests) |
| **BL121-B** | Sonnet | ✅ Yes | ~100 | 5+ | 2 (propertiesAdapter, tests) |
| **BL121-C** | Haiku | ❌ No (after A+B) | ~250 | 7+ | 1 (new integration test file) |

**Total estimated:** ~430 lines of new/modified code, 20+ tests

---

## Dispatch Strategy Recommendation

**Phase 1 (Parallel):**
- Dispatch TASK-BL121-A (Sonnet)
- Dispatch TASK-BL121-B (Sonnet)

**Phase 2 (Sequential):**
- Wait for A and B to complete
- Dispatch TASK-BL121-C (Haiku) — integration tests will verify A+B work together

**Rationale:**
- A and B are independent (different files, different concerns)
- C depends on both A and B completing first (tests the integration)
- C can use Haiku (simpler task: write tests, not complex logic)

---

## Acceptance Criteria Coverage

From BL-121 spec:
- [ ] Selecting a canvas node shows its properties in the panel → **Covered by A, B, C**
- [ ] Editing a property updates the canvas node → **Out of scope** (this is display-only, not editing)
- [ ] Deselecting clears the panel → **Covered by A, B, C**
- [ ] Tests pass → **Covered by A, B, C**

**Note:** The original BL-121 spec mentioned "editing a property updates the canvas node." Based on the briefing and approval, this fix is focused on **display wiring only** (selection → display). Editing functionality is not included in this 3-task breakdown. If editing is required, we'll need a 4th task.

---

## Known Issues / Questions

None. All task files are complete and ready for dispatch upon your approval.

---

## Next Steps

1. **Review task files** — verify completeness, clarity, no gaps
2. **Approve or request corrections** — if corrections needed, I'll update the task files
3. **After approval:**
   - I'll dispatch TASK-BL121-A and TASK-BL121-B in parallel
   - Monitor bee responses
   - After A+B complete, dispatch TASK-BL121-C
   - Collect all responses and report results to you

---

**Awaiting your review and approval to proceed with dispatch.**

---

**Q33N (Bot ID: QUEEN-2026-03-19-APPROVAL-BL121-WRIT)**
**End of Report**
