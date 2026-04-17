# TASK-BUG-035: Fix isTextIcon undefined in TreeNodeRow

## Objective
Fix the runtime error "isTextIcon is not defined" in TreeNodeRow.tsx that breaks both Palette and Properties tree-browser panes.

## Context
BUG-022 bee added a call to `isTextIcon(node.icon)` at line 85 of TreeNodeRow.tsx but did NOT include the function definition. This causes a runtime crash in every tree-browser instance (Palette, Properties, filesystem, channels).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeNodeRow.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-TASK-BUG-022-A-RESPONSE.md`

## Root Cause
Line 85 of TreeNodeRow.tsx calls `isTextIcon(node.icon)` but the function is not defined anywhere in the file or imported.

## Deliverables
- [ ] Add `isTextIcon()` helper function to TreeNodeRow.tsx (before the component, after imports)
- [ ] The function should detect whether an icon string is a Unicode/emoji character vs a CSS class name
- [ ] Heuristic: if the string is 1-2 characters long OR contains non-ASCII characters, it's a text icon. Otherwise it's a CSS class.
- [ ] Verify no other tree-browser files reference isTextIcon without having it
- [ ] Run tree-browser tests to confirm no regressions

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test isTextIcon with emoji icons (e.g. "📁", "⚙️") → returns true
- [ ] Test isTextIcon with CSS class icons (e.g. "icon-folder", "fa-gear") → returns false
- [ ] Test isTextIcon with single Unicode chars (e.g. "▸") → returns true
- [ ] Test isTextIcon with empty string → returns false
- [ ] All existing tree-browser tests still pass

## Test Command
```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/tree-browser
```

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-BUG-035-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks
