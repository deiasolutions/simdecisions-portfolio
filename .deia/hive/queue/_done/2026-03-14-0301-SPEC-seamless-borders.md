# SPEC: BL-002 Seamless Pane Borders

## Priority
P2

## Objective
When `seamless: true` is set on a split node in an EGG layout, remove internal chrome between panes and show a 1px hairline divider instead. Outer panes share the parent's border-radius.

## Context
The shell split container renders PaneChrome around each child pane. When seamless mode is active, the chrome (title bar, borders) should be removed and replaced with a minimal hairline divider.

Files to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\SplitContainer.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\types.ts` — SplitNode type

## Acceptance Criteria
- [ ] SplitNode type supports `seamless?: boolean` property
- [ ] When `seamless: true`, child panes render without PaneChrome title bars
- [ ] 1px hairline divider between seamless panes using `var(--sd-border)`
- [ ] Outer corners of the split group share the parent's border-radius
- [ ] Inner corners between seamless panes have no border-radius (sharp)
- [ ] Resizer handle still works in seamless mode
- [ ] Non-seamless splits unchanged (no regression)
- [ ] 6+ tests
- [ ] CSS: var(--sd-*) only

## Model Assignment
haiku

## Constraints
- Do NOT change behavior of non-seamless splits
- Seamless is opt-in per split node, not global
