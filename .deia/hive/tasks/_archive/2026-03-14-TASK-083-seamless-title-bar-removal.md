# TASK-083: Hide title bars in seamless mode

## Objective
When a split node has `seamless: true`, hide the title bar in PaneChrome for child panes while keeping borders removed and showing a 1px hairline divider.

## Context
The `seamless` property already exists in SplitNode (types.ts:76) and is parsed from EGG layouts. The eggToShell.ts converter already annotates child AppNodes with `seamlessEdges` metadata, and PaneChrome already removes borders on those edges. SplitDivider already renders a 1px hairline in seamless mode.

**Current behavior:** Seamless splits have borders removed but title bars still show.
**Required behavior:** Title bars should be hidden when pane has seamless edges.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\eggToShell.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitDivider.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx`

## Deliverables
- [ ] PaneChrome checks if `node.meta.seamlessEdges` has any edges set
- [ ] If seamless edges exist, title bar div is not rendered (height: 0, display: none, or conditional render)
- [ ] Content area remains functional (focus, drag-drop via invisible overlay if needed)
- [ ] Border logic already works (no changes needed)
- [ ] Border-radius on outer corners matches parent container (4px on exposed corners, 0px on seamless edges)
- [ ] No regression for non-seamless panes (chrome: true with no seamlessEdges)
- [ ] No regression for chrome: false panes (already skip all chrome rendering)

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - [ ] Seamless pane has no title bar
  - [ ] Seamless pane still accepts focus when clicked
  - [ ] Seamless pane with `chrome: false` still skips all chrome
  - [ ] Non-seamless pane shows title bar (regression test)
  - [ ] Outer corners have border-radius 4px, inner corners 0px
  - [ ] All existing PaneChrome tests still pass

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT change the behavior of the existing `chrome: false` logic
- Do NOT remove PaneChrome entirely — only hide the title bar div

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260314-TASK-083-RESPONSE.md`

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
