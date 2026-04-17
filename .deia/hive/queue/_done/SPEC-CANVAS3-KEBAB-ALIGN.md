# SPEC-CANVAS3-KEBAB-ALIGN

Fix kebab menu button alignment in TopBar — should be flush right.

## Priority
P2

## Depends On
None

## Model Assignment
haiku

## Description

The kebab (three-dot) menu button in the TopBar primitive is not aligned to the right side of the page in the canvas3 set. The TopBar layout is: hamburger | brand | spacer (flex:1) | kebab | avatar. The spacer should push kebab+avatar to the far right.

### Root Cause Investigation

Check these potential causes:
1. The `.top-bar` container may not have `width: 100%` or its parent (the pane frame from the split container) may constrain it
2. The AppFrame or PaneChrome wrapper may not give the top-bar pane full width
3. The seamless pane wrapper in PaneChrome (chrome:false path) needs `width: 100%`
4. The split container child div may need explicit `min-width: 0` and `overflow: hidden`

### Files

| File | Change |
|------|--------|
| `browser/src/primitives/top-bar/TopBar.css` | Ensure `.top-bar` has `width: 100%` |
| `browser/src/shell/components/PaneChrome.tsx` | Check seamless wrapper gives full width to children |
| `browser/src/shell/components/SplitContainer.tsx` | Check child containers allow full-width flex |

## Acceptance Criteria
- [ ] Kebab button and user avatar are flush-right in the top bar
- [ ] Hamburger and brand text are flush-left
- [ ] Spacer fills remaining space between left and right groups
- [ ] Works in canvas3, code, and chat sets

## Smoke Test
1. Load canvas3 set locally
2. Verify kebab (three dots) is on the far right, avatar next to it
3. Resize window — kebab stays right-aligned at all widths

## Constraints
- CSS only — use `var(--sd-*)` variables
- Do not change TopBar component logic
- Must not break other sets that use top-bar
