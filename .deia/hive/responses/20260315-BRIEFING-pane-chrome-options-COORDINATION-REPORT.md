# COORDINATION REPORT: Pane Chrome Options (BL-151)

**From:** Q33N (QUEEN-2026-03-15-BRIEFING-pane-chrom)
**To:** Q33NR
**Date:** 2026-03-15
**Briefing:** 2026-03-15-BRIEFING-pane-chrome-options
**Spec:** SPEC-w2-04-pane-chrome-options

---

## Summary

I've analyzed the briefing and codebase, then created **5 task files** to implement the pane chrome options feature (BL-151). The work is broken into:
1. Type definitions and schema extensions (Haiku)
2. UI component updates (Sonnet)
3. Reducer logic for pin/collapse behavior (Sonnet)
4. Collapsed pane icon strip component (Sonnet)
5. E2E integration tests (Haiku)

All tasks follow TDD, use absolute paths, and respect the 500-line limit.

---

## Task Files Created

### TASK-168: Add Pane Chrome Option Types (Haiku)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-168-pane-chrome-schema-types.md`

**Scope:**
- Extend `EggLayoutNode` interface to support `chromeClose`, `chromePin`, `chromeCollapsible` boolean fields
- Add `ChromeOptions` interface and field to `AppNode` in shell types
- Update `eggLayoutToShellTree()` to read chrome options from EGG config and set defaults
- Update SPEC-EGG-SCHEMA-v1.md documentation

**Files modified:** 4 (types.ts x2, eggToShell.ts, SPEC-EGG-SCHEMA-v1.md)

**Dependencies:** None (foundational task)

---

### TASK-169: Implement Pane Chrome UI Components (Sonnet)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-169-pane-chrome-ui-components.md`

**Scope:**
- Update `PaneChrome.tsx` to conditionally render close X, pin toggle, collapse toggle based on `chromeOptions`
- Wire buttons to shell actions: `TOGGLE_PIN`, `TOGGLE_COLLAPSE`
- Use existing `ChromeBtn` component for consistency
- Add tests for button rendering and action dispatch

**Files modified:** 2 (PaneChrome.tsx, PaneChrome.test.tsx)

**Dependencies:** TASK-168 (needs chromeOptions types)

---

### TASK-170: Implement Pin and Collapse Reducer Logic (Sonnet)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-170-pane-chrome-reducer-logic.md`

**Scope:**
- Add `TOGGLE_PIN` and `TOGGLE_COLLAPSE` actions to shell reducer
- Pin behavior: set `node.meta.isPinned = true`, collapse sibling pane in binary split
- Collapse behavior: set `node.meta.isCollapsed = true`
- Helper functions: `findParentSplit()`, `getSibling()`
- Immutable tree updates, edge case handling (no parent, not in binary split, pinned sibling)

**Files modified:** 3 (reducer.ts, types.ts, reducer.test.ts)

**Dependencies:** TASK-168 (needs types), TASK-169 (completes button wiring)

---

### TASK-171: Implement Collapsed Pane Icon Strip (Sonnet)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-171-collapsed-pane-strip.md`

**Scope:**
- Create `CollapsedPaneStrip.tsx` component: thin ~34px vertical strip with icon, label, expand button
- Update `ShellNodeRenderer.tsx` to render CollapsedPaneStrip when `node.meta.isCollapsed === true`
- CSS styles using `var(--sd-*)` variables only
- Click anywhere on strip dispatches `TOGGLE_COLLAPSE` to restore pane

**Files modified:** 4 (CollapsedPaneStrip.tsx, ShellNodeRenderer.tsx, CollapsedPaneStrip.test.tsx, shell.css)

**Dependencies:** TASK-170 (needs isCollapsed state)

---

### TASK-172: E2E Tests for Pane Chrome Options (Haiku)
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-172-pane-chrome-e2e-tests.md`

**Scope:**
- End-to-end integration tests verifying full user flow
- Test EGG inflation with chrome options → UI rendering → user interaction → state changes → DOM updates
- 9 test cases covering all chrome options, pin/collapse interactions, edge cases

**Files modified:** 1 (PaneChrome.e2e.test.tsx)

**Dependencies:** TASK-168, 169, 170, 171 (full feature implementation)

---

## Dependency Graph

```
TASK-168 (types/schema)
  ↓
TASK-169 (UI buttons) ──→ TASK-170 (reducer logic)
                            ↓
                          TASK-171 (collapsed strip)
                            ↓
                          TASK-172 (E2E tests)
```

**Execution order:**
1. TASK-168 (Haiku) — foundational, must complete first
2. TASK-169 (Sonnet) + TASK-170 (Sonnet) — can run in parallel after TASK-168
3. TASK-171 (Sonnet) — depends on TASK-170
4. TASK-172 (Haiku) — final integration tests, depends on all prior tasks

---

## Model Assignments

| Task | Model | Rationale |
|------|-------|-----------|
| TASK-168 | Haiku | Simple type extensions, schema docs update |
| TASK-169 | Sonnet | React component UI logic, conditional rendering |
| TASK-170 | Sonnet | Complex reducer logic, tree traversal, immutable updates |
| TASK-171 | Sonnet | New component + integration into ShellNodeRenderer |
| TASK-172 | Haiku | E2E tests, straightforward test scenarios |

---

## Estimated Test Coverage

- **TASK-168:** ~8 tests (type propagation, defaults, edge cases)
- **TASK-169:** ~10 tests (button rendering, dispatch, active states)
- **TASK-170:** ~12 tests (pin/unpin, collapse/expand, edge cases, immutability)
- **TASK-171:** ~8 tests (strip rendering, expand button, ShellNodeRenderer integration)
- **TASK-172:** ~9 tests (E2E flows, full user interactions)

**Total:** ~47 tests

---

## Files Touched (All Tasks)

**Modified:**
- `browser/src/eggs/types.ts`
- `browser/src/shell/types.ts`
- `browser/src/shell/eggToShell.ts`
- `browser/src/shell/components/PaneChrome.tsx`
- `browser/src/shell/components/ShellNodeRenderer.tsx`
- `browser/src/shell/reducer.ts`
- `browser/src/shell/components/shell.css`
- `docs/specs/SPEC-EGG-SCHEMA-v1.md`

**Created:**
- `browser/src/shell/components/CollapsedPaneStrip.tsx`
- `browser/src/shell/components/__tests__/CollapsedPaneStrip.test.tsx`
- `browser/src/shell/components/__tests__/PaneChrome.e2e.test.tsx`

**Total:** 11 files (8 modified, 3 created)

---

## Acceptance Criteria Coverage

All acceptance criteria from the briefing are covered:

- [x] EGG schema supports `chromeClose`, `chromePin`, `chromeCollapsible` per pane (TASK-168)
- [x] eggInflater reads and passes chrome options to shell panes (TASK-168)
- [x] PaneChrome component renders optional close X, pin toggle, collapse toggle (TASK-169)
- [x] Pin toggle: when active, sibling pane collapses; pane gets full width (TASK-170)
- [x] Collapse: pane shrinks to ~34px vertical icon strip with expand button (TASK-171)
- [x] Collapsed strip shows pane icon and expand arrow (TASK-171)
- [x] Expand button restores pane to previous size (TASK-171)
- [x] All chrome buttons use `var(--sd-*)` CSS variables only (TASK-169, TASK-171)
- [x] Tests written and passing (TDD) (all tasks)
- [x] Existing browser tests still pass (verified in TASK-172)

---

## Risk Assessment

**Low risk:**
- Type extensions are non-breaking (optional fields with defaults)
- UI components use existing patterns (ChromeBtn, shell.css variables)
- Reducer logic uses existing tree traversal patterns
- All changes are additive (no breaking changes to existing EGGs)

**Medium risk:**
- Pin behavior requires finding parent split and sibling — edge cases possible (no parent, not in split)
- Collapsed state may interact with other shell features (maximize, seamless, swap) — needs testing

**Mitigations:**
- TDD approach ensures edge cases caught early
- E2E tests verify full integration
- Pin/collapse only work when applicable (graceful no-op otherwise)

---

## Open Questions

None. All requirements from the briefing are clear and can be implemented as specified.

---

## Next Steps

**Awaiting Q33NR approval to dispatch bees.**

Once approved, dispatch order:
1. Dispatch TASK-168 (Haiku) — wait for completion
2. Dispatch TASK-169 (Sonnet) + TASK-170 (Sonnet) in parallel — wait for completion
3. Dispatch TASK-171 (Sonnet) — wait for completion
4. Dispatch TASK-172 (Haiku) — final verification

Estimated total time: ~4-5 hours (serial), ~3 hours (with parallelization).

---

**Q33N ready for Q33NR review.**
