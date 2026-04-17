# SPEC: Fix Hamburger Menu Overflow Direction in Pane Status Bars

## Priority
P0

## Objective
Fix PaneMenu.tsx so the hamburger menu opens in the direction with available space rather than always opening to the left. The menu must self-measure its trigger position relative to the pane container on every open event and choose the correct direction.

## Context
Files to read first:
- `browser/src/shell/components/PaneMenu.tsx` (THE file to fix — line 111 has hardcoded `transform: 'translateX(-100%)'`)
- `browser/src/shell/components/PaneChrome.tsx` (renders `<PaneMenu>`, has `data-testid="pane-chrome"` on the container)
- `browser/src/shell/components/__tests__/PaneMenu.test.tsx` (existing tests)
- `browser/src/shell/components/ChromeBtn.tsx` (trigger button)
- Full spec: `docs/specs/SPEC-HAMBURGER-MENU-OVERFLOW.md`

## Current Bug
The `toggle` handler sets `pos` to `{ x: r.right, y: r.bottom + 4 }` and the portal div applies `transform: 'translateX(-100%)'`. This always opens the menu to the left of the trigger. When the trigger is on the left side of a pane, the menu overflows offscreen.

## Acceptance Criteria
- [ ] On menu open, `getBoundingClientRect()` is called on both the trigger and the nearest `[data-testid="pane-chrome"]` ancestor
- [ ] If trigger is in the left half of the pane → menu opens to the right
- [ ] If trigger is in the right half → menu opens to the left
- [ ] If trigger is in the top half → menu opens downward
- [ ] If trigger is in the bottom half → menu opens upward
- [ ] Horizontal + vertical directions combine (bottom-left → up-and-right)
- [ ] If the computed position would overflow the viewport, the menu shifts to stay visible
- [ ] Direction is recalculated on every open (not cached)
- [ ] No hardcoded pixel offsets — proportional position only
- [ ] Hardcoded `transform: 'translateX(-100%)'` removed, replaced with computed positioning
- [ ] CSS uses var(--sd-*) only
- [ ] 5+ tests covering each quadrant direction + viewport overflow fallback
- [ ] No regressions in existing PaneMenu tests
- [ ] No file over 500 lines

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- Changes to PaneMenu.tsx only (+ test file). PaneChrome.tsx already has `data-testid="pane-chrome"` — no change needed there.

## Smoke Test
```bash
cd browser && npx vitest run src/shell/components/__tests__/PaneMenu
```
