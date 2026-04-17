# TASK-231: Seamless Pane Borders

## Objective
Remove double borders between adjacent shell panes. When two panes sit side-by-side in a split, their borders should collapse into a single 1px line, not double up to 2px.

## Context
Shell panes are rendered by `PaneChrome.tsx`. Each pane has a border. When two panes are adjacent in a split, both borders render = 2px gap between panes. The fix is CSS-only: use border-collapse logic.

**Current behavior:**
```
┌─────────┐ ┌─────────┐
│ Pane A  │ │ Pane B  │   ← 2px gap (1px from A's border-right + 1px from B's border-left)
└─────────┘ └─────────┘
```

**Desired behavior:**
```
┌─────────┬─────────┐
│ Pane A  │ Pane B  │   ← 1px shared border
└─────────┴─────────┘
```

**Solution approaches:**
1. **Border-collapse via selective borders:** Only apply border-right/border-bottom to panes, not border-left/border-top (let parent container handle outer borders)
2. **Negative margins:** Apply negative margin to collapse adjacent borders (risky, can break layout)
3. **Parent gap:** Use `gap` on the parent flexbox container to control spacing (cleanest)

**Recommended:** Use parent `gap` + selective borders.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx` (parent layout)
- Any related CSS modules (e.g., `PaneChrome.module.css` if exists)

## Strategy
1. Read `PaneChrome.tsx` to understand current border styling (line 76-88: `borderStyle` object)
2. Read `SplitContainer.tsx` to understand split layout (flexbox with two children)
3. Identify the cleanest approach:
   - Option A: Add `gap` to SplitContainer flexbox + adjust PaneChrome border logic
   - Option B: Use selective borders (border-right/bottom only) + outer container borders
   - Option C: Use CSS combinators (`:not(:last-child)`) to remove redundant borders
4. Implement the fix in MAX 3 files
5. Write tests to verify:
   - Single pane still has border
   - Split panes have single shared border (not double)
   - Triple-split works correctly
   - Seamless edges (`node.meta.seamlessEdges`) still work

## Files You May Modify
**Maximum files:** 3

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\TripleSplitContainer.tsx` (if exists and needs updating)
- Any related CSS module file (e.g., `PaneChrome.module.css`)

## Files You Must NOT Modify
- Any primitive files (anything in `browser/src/primitives/`)
- Any adapter files (anything in `browser/src/primitives/*/adapters/`)
- Any backend files (`hivenode/`, `engine/`)
- Any shell action/reducer files (only modify components, not logic)

## Deliverables
- [ ] Double borders removed between adjacent panes
- [ ] Single panes still have complete border
- [ ] Seamless edge logic (`node.meta.seamlessEdges`) still works correctly
- [ ] Tests verify border behavior

## Test Requirements
**Minimum tests:** 3

- [ ] Tests written FIRST (TDD)
- [ ] Test: single pane has border on all 4 sides
- [ ] Test: two panes in a split have single shared border (not double)
- [ ] Test: seamless edges still remove borders correctly

**Test file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneChrome.seamless-borders.test.tsx`

## Build Verification
```bash
# Run PaneChrome tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/shell/components/__tests__/PaneChrome

# Run all shell tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/shell/

# Build
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npm run build
```

Include test summary and last 5 lines of build output in response file.

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only (no hardcoded colors)
- NO stubs — every function fully implemented
- CSS-only fix — no logic changes to shell reducer/actions

## Response Requirements — MANDATORY
When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260319-TASK-231-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes (not intent)
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria
- [ ] Double borders removed between adjacent panes in splits
- [ ] Single panes still have complete border
- [ ] Seamless edge logic still works
- [ ] 3+ tests pass (single pane, split, seamless)
- [ ] All existing tests still pass
- [ ] Build succeeds
- [ ] No hardcoded colors introduced
- [ ] No files exceed 500 lines

## Model Assignment
haiku

## Risk
LOW — CSS-only change, no logic modifications
