# BRIEFING: Remove Layout Submenu from View Menu (BUG-074)

**Date:** 2026-03-25
**From:** Q33NR
**To:** Q33N
**Spec:** SPEC-BUG-074-remove-layout-menu
**Model Assignment:** Sonnet
**Priority:** P1

---

## Objective

Remove the Layout submenu from the View menu in MenuBar.tsx. Layout is determined by EGG config, not user menu selection. This is vestigial UI from the old simdecisions-2 port that no longer applies to the current architecture.

## Context

The MenuBar.tsx component currently has a "Layout" submenu under the View menu with preset options:
- Single
- Horizontal Split
- Vertical Split
- Left & Two Right
- Two Left & Right
- Two Top & Bottom
- Top & Two Bottom
- Four Pane

These presets were used in the old system where users could manually switch layouts. In ShiftCenter, layouts are determined by EGG files (e.g., `canvas.egg.md`, `efemera.egg.md`), not by user menu selection.

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\MenuBar.tsx` (the component to modify)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\MenuBar.test.tsx` (tests to update)

## What Q33N Must Deliver

Write ONE task file for a bee to:

1. **Remove the Layout submenu** from the View menu rendering (lines ~400-441)
2. **Remove the `handleLayoutChange` function** (line ~223)
3. **Update tests** to remove Layout-related test cases or assertions
4. **Verify no regressions** — all other MenuBar functionality still works

## Technical Details

### Current Implementation (to be removed)

The `handleLayoutChange` function at line 223 calls `dispatch({ type: 'APPLY_PRESET', preset })`. This entire function and all its references in the View menu JSX should be deleted.

### What Stays

- File menu (New Window, Close Window)
- Edit menu (if any items exist)
- View menu (but WITHOUT Layout submenu)
- Tools menu (syndicated items)
- Help menu (Documentation, Commands, About)
- Theme menu (Light/Dark/Auto)
- Mode menu (Local/Cloud)
- Toolbar syndication
- Menu syndication

## Acceptance Criteria

- [ ] View menu no longer shows "Layout" submenu
- [ ] No layout preset buttons anywhere in the menu
- [ ] `handleLayoutChange` function removed from MenuBar.tsx
- [ ] Tests updated and all passing
- [ ] Build passes with no regressions

## Test Requirements

The bee MUST:
- Run `cd browser && npx vitest run src/shell/components/__tests__/MenuBar.test.tsx` — all MenuBar tests pass
- Run `cd browser && npx vitest run` — no regressions

## Constraints

- TDD: update tests first, then implementation
- No file over 500 lines (MenuBar.tsx is currently under 500, must stay under)
- CSS: var(--sd-*) only (not applicable here, but reminder)
- No stubs

## Model Assignment

**Sonnet** — this is straightforward deletion work but requires test updates

---

## Q33N Instructions

1. Read the two files listed above
2. Write ONE task file to `.deia/hive/tasks/2026-03-25-TASK-BUG-074-REMOVE-LAYOUT-MENU.md`
3. Return the task file to me for review
4. DO NOT dispatch the bee yet — wait for my approval
