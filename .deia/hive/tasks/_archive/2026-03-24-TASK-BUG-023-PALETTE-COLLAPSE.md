# TASK-BUG-023: Canvas Components Panel Icon-Only Collapse Mode — CSS ONLY

## Objective

**IMPORTANT:** The JavaScript wiring and tests for collapse mode are COMPLETE. You ONLY need to implement the CSS. DO NOT modify the JS/TS code.

Implement CSS classes and styles for icon-only collapse mode for the Canvas components panel (NodePalette / tree-browser sidebar). The `collapsed` prop is already wired through `sidebarAdapter → TreeBrowser`. Tests are written and failing because CSS is missing.

## Context — WORK ALREADY DONE

✅ **Already implemented (DO NOT modify):**
- `sidebarAdapter.tsx` — `collapsed` state, localStorage persistence, collapse button rendering
- `TreeBrowser.tsx` — `collapsed` prop accepted and passed to child components
- `types.ts` — Interface updated with `collapsed?: boolean`
- Test files created: 14 tests (all failing due to missing CSS)

❌ **What's MISSING (your job):**
- CSS classes for `.tree-browser--collapsed`
- CSS to hide search box when collapsed
- CSS to hide labels when collapsed
- CSS to hide badges when collapsed
- CSS to center icons when collapsed
- CSS width transition (200-300ms ease)

**Expected behavior:**
- Click a collapse affordance (e.g., chevron icon in panel header) → panel collapses to icon-only mode
- In collapsed mode:
  - Panel width shrinks to match activity bar width (~48px)
  - Tree-browser shows only icons (no labels, no search box)
  - NodePalette shows only component icons (no labels, no descriptions)
- Click expand affordance → panel restores to full width with labels
- State persists per sidebar (stored in localStorage or component state)

**Relevant files:**
- `browser/src/apps/sidebarAdapter.tsx` — manages activity bar + panel routing
- `browser/src/primitives/tree-browser/components/TreeBrowser.tsx` — tree-browser with search box
- `browser/src/primitives/tree-browser/components/TreeNodeRow.tsx` — tree node rendering (icon + label)
- `browser/src/apps/sim/components/flow-designer/NodePalette.tsx` — palette component (may be embedded or tree-browser)
- `eggs/canvas.egg.md` — EGG config with sidebar panels definition (line 46-77)

## Files to Read First

**Read the TEST FILES to understand expected behavior:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\__tests__\sidebarAdapter.collapse.test.tsx` (7 CSS tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\TreeBrowser.collapse.test.tsx` (7 CSS tests)

**Read the implementation to see where CSS hooks exist:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sidebarAdapter.tsx` (collapsed state wiring)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\components\TreeBrowser.tsx` (collapsed prop)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\components\TreeNodeRow.tsx` (labels/badges)

## Deliverables

**CSS ONLY — DO NOT modify JS/TS files:**

- [ ] CSS class `.tree-browser--collapsed` applied correctly
- [ ] CSS to hide search box when `.tree-browser--collapsed` (display: none)
- [ ] CSS to hide `.tree-node-label` when `.tree-browser--collapsed` (display: none)
- [ ] CSS to hide `.tree-node-badge` when `.tree-browser--collapsed` (display: none)
- [ ] CSS to center icons in `.tree-node-row` when collapsed (justify-content: center)
- [ ] CSS width transition on `[data-sidebar-content]` (transition: width 250ms ease)
- [ ] Width behavior:
  - Expanded: width matches `panelWidth` from config (220px default)
  - Collapsed: width matches `activityBarWidth` from config (48px default)
- [ ] All 14 existing tests pass (7 sidebarAdapter + 7 TreeBrowser)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases covered:
  - Collapse when panel is active
  - Collapse when panel is not active (no effect)
  - Expand when collapsed
  - Expand when already expanded (no effect)
  - State persists across remounts (localStorage)
  - Multiple sidebars on same page (independent collapse states)
  - TreeBrowser with no search box (e.g., properties panel)
  - Drag-and-drop from tree-browser when collapsed (icons draggable, no labels)
- [ ] Minimum 14 test cases total (8 sidebar + 6 tree-browser)
- [ ] No existing tests broken

## Constraints

- No file over 500 lines
- CSS: `var(--sd-*)` only — no hardcoded colors
- No stubs — fully implement all functions
- Do NOT modify canvas.egg.md config — work with existing `activityBarWidth` and `panelWidth` values
- Do NOT change tree-browser API — add collapse prop, do not refactor existing behavior
- Width transition: CSS transition, not JavaScript animation

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260324-TASK-BUG-023-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Bug Details (from inventory)

- **ID:** BUG-023
- **Severity:** P0
- **Component:** canvas
- **Title:** Canvas components panel does not collapse to icon-only mode per spec
- **Status:** OPEN
- **Description:** NodePalette sidebar should support collapse to icon-only mode (48px width) but currently always shows full labels at 220px width

## Design Guidance

**Collapsed state (icon-only):**
```
┌─────┐
│  ▶  │ ← Start icon only
│  ⏹  │ ← End icon only
│  ◇  │ ← Decision icon only
│  ◆  │ ← Activity icon only
│  ⚙  │ ← Resource icon only
└─────┘
   48px
```

**Expanded state (icon + label):**
```
┌──────────────────┐
│ ▶  Start         │
│ ⏹  End           │
│ ◇  Decision      │
│ ◆  Activity      │
│ ⚙  Resource      │
└──────────────────┘
       220px
```

**Collapse affordance:**
- Place chevron icon in panel header, right-aligned
- Chevron points left when expanded (`◀`), points right when collapsed (`▶`)
- Click chevron to toggle state
- Tooltip: "Collapse panel" / "Expand panel"
