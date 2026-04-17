# SPEC: Fix Hamburger Menu Overflow Direction in Pane Status Bars

**ID:** BL-204
**Priority:** P0
**Category:** Bug
**Source:** Q88N-direct 2026-03-16

## Problem

All pane title bar hamburger menus (`PaneMenu.tsx`) currently open to the left via a hardcoded `transform: 'translateX(-100%)'` on line 111. When a title bar sits on the left edge of the viewport or pane frame, the menu opens offscreen or clips outside the pane boundary. The menu must be position-aware — opening in whichever direction keeps it visible.

## Context

`PaneMenu.tsx` is the single shared hamburger menu component. Every pane's `PaneChrome` title bar renders `<PaneMenu>`. The fix must be in this one component — not patched per-pane.

### Files to Read First

- `browser/src/shell/components/PaneMenu.tsx` — the shared hamburger menu (THE file to fix)
- `browser/src/shell/components/PaneChrome.tsx` — renders `<PaneMenu>`, wraps every pane
- `browser/src/shell/components/__tests__/PaneMenu.test.tsx` — existing tests
- `browser/src/shell/components/ChromeBtn.tsx` — the trigger button

### Current Behavior

In `PaneMenu.tsx` toggle handler (line 46):
```ts
const r = btnRef.current.getBoundingClientRect();
setPos({ x: r.right, y: r.bottom + 4 });
```

Then the portal div (line 111) applies:
```ts
transform: 'translateX(-100%)'
```

This always anchors the menu's right edge to the button's right edge, opening leftward. No awareness of available space.

## Requirements

### 1.0 Self-Measuring Position Detection

1.1 On every menu open event, use `getBoundingClientRect()` on both the trigger element (`btnRef`) and the nearest pane container (identifiable by `[data-testid="pane-chrome"]` on the PaneChrome wrapper).

1.2 Compute the trigger's proportional position within the pane bounding rect.

1.3 Do NOT cache — recalculate on every open. Panes can be resized or repositioned.

1.4 No hardcoded pixel offsets — derive direction from proportional position within the pane.

### 2.0 Menu Open Direction Logic

2.1 If trigger is in the **left half** of the pane → menu opens to the **right** (no translateX, left-aligned to trigger).

2.2 If trigger is in the **right half** → menu opens to the **left** (current behavior, translateX(-100%)).

2.3 If trigger is in the **bottom half** of the pane → menu opens **upward** (bottom-anchored to trigger top).

2.4 If trigger is in the **top half** → menu opens **downward** (current behavior, top-anchored to trigger bottom).

2.5 Combine horizontal and vertical: a trigger in the bottom-left opens up-and-right, etc.

### 3.0 Overflow / Float Fallback

3.1 After computing the preferred direction, check whether the menu rect would still overflow the **viewport** boundary (since menu is portaled to `.hhp-root`).

3.2 If it would overflow even in the "correct" direction, allow the menu to float — but always toward the direction with more available screen space.

3.3 The menu must never clip against the side it's opening toward when the opposite direction has room.

### 4.0 Implementation Constraints

4.1 Changes apply to `PaneMenu.tsx` only (and its test file).

4.2 If the pane frame needs a data attribute or class to be identifiable as the bounding container, note that as a one-line change in `PaneChrome.tsx`. Currently `data-testid="pane-chrome"` already exists and can be used.

4.3 The `toggle` handler must be updated to compute direction, not just position.

4.4 The portal div's inline style must use the computed direction instead of hardcoded `transform: 'translateX(-100%)'`.

4.5 CSS: `var(--sd-*)` only. No hex, no rgb(), no named colors.

4.6 No file over 500 lines.

## Deliverables

- [ ] Updated `PaneMenu.tsx` with self-measuring position logic
- [ ] Updated toggle handler: compute trigger position relative to pane container
- [ ] Portal div uses dynamic positioning instead of hardcoded `translateX(-100%)`
- [ ] Viewport overflow fallback logic
- [ ] Tests covering: left-half trigger opens right, right-half opens left, top-half opens down, bottom-half opens up, viewport overflow fallback
- [ ] No regressions in existing PaneMenu tests

## Technical Notes

The menu is rendered via `createPortal` to `.hhp-root` for z-index safety. Position is set via `position: fixed` with `left`/`top` coordinates. The current `translateX(-100%)` trick must be replaced with computed coordinates that account for direction.

Suggested approach in the `toggle` handler:
1. Get trigger rect via `btnRef.current.getBoundingClientRect()`
2. Walk up to find the `[data-testid="pane-chrome"]` ancestor, get its rect
3. Compute trigger center relative to pane rect
4. Set `pos` to include both coordinates and direction flags
5. In the portal div style, use direction flags to choose anchor point
