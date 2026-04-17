# BRIEFING: Fix Hamburger Menu Overflow Direction

**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-16
**Spec ID:** BL-204 / QUEUE-TEMP-2026-03-16-1830-SPEC-fix-hamburger-menu-overflow
**Priority:** P0
**Model Assignment:** Haiku (single-file fix, TDD)

---

## Objective

Fix `PaneMenu.tsx` so the hamburger menu opens in the direction with available space rather than always opening to the left. The menu must self-measure its trigger position relative to the pane container on every open event and choose the correct direction.

---

## Context — What Q88N Said

The current implementation has a hardcoded `transform: 'translateX(-100%)'` on line 111 of `PaneMenu.tsx`. This always opens the menu to the left of the trigger button. When the trigger is on the left edge of a pane, the menu overflows offscreen.

The fix must:
1. **Self-measure** on every open: get `getBoundingClientRect()` on both the trigger (`btnRef`) and the nearest `[data-testid="pane-chrome"]` ancestor (the pane container)
2. **Compute direction** based on proportional position within the pane (left half → open right, right half → open left, top half → open down, bottom half → open up)
3. **Combine directions** (e.g., bottom-left quadrant → up-and-right)
4. **Fallback for viewport overflow** — if the menu would still overflow the viewport boundary after correct direction is applied, shift it to stay visible
5. **No caching** — recalculate on every open

---

## Files to Read Before Writing Task Files

- `browser/src/shell/components/PaneMenu.tsx` — THE file to fix (line 111 has the hardcoded transform)
- `browser/src/shell/components/PaneChrome.tsx` — renders `<PaneMenu>`, has `data-testid="pane-chrome"` on the container (line 98) — NO changes needed here
- `browser/src/shell/components/__tests__/PaneMenu.test.tsx` — existing tests (15 tests, all passing)
- `browser/src/shell/components/ChromeBtn.tsx` — trigger button component

---

## What Must Be Delivered (Task Requirements)

### Code Changes

1. **Updated `toggle` handler in PaneMenu.tsx:**
   - Get trigger rect via `btnRef.current.getBoundingClientRect()`
   - Walk up DOM to find `[data-testid="pane-chrome"]` ancestor, get its rect
   - Compute trigger center relative to pane rect
   - Determine horizontal direction: left half → open right, right half → open left
   - Determine vertical direction: top half → open down, bottom half → open up
   - Store both coordinates AND direction flags in `pos` state
   - Do NOT cache — this runs on every open

2. **Updated portal div style (line 111):**
   - Remove hardcoded `transform: 'translateX(-100%)'`
   - Use computed direction flags to set anchor point
   - If opening right: `left: pos.x` (left-aligned to trigger)
   - If opening left: `left: pos.x, transform: 'translateX(-100%)'` (right-aligned to trigger)
   - If opening down: `top: pos.y` (top-anchored to trigger bottom)
   - If opening up: `top: pos.y, transform: 'translateY(-100%)'` (bottom-anchored to trigger top)
   - Combine transforms when needed: `translateX(-100%) translateY(-100%)` for up-and-left

3. **Viewport overflow fallback:**
   - After computing preferred direction, check whether the menu rect would overflow the viewport
   - If yes, shift the menu toward the direction with more available space
   - Menu must never clip against the side it's opening toward when the opposite direction has room

### Tests

Write **5+ new tests** covering:
- Trigger in left half of pane → menu opens to the right
- Trigger in right half of pane → menu opens to the left
- Trigger in top half of pane → menu opens downward
- Trigger in bottom half of pane → menu opens upward
- Trigger in bottom-left quadrant → menu opens up-and-right
- Viewport overflow fallback (menu near viewport edge shifts to stay visible)

All existing tests (15 tests) must still pass.

---

## Constraints (from 10 Hard Rules)

- **Rule 3:** CSS uses `var(--sd-*)` only. No hex, no rgb(), no named colors.
- **Rule 4:** No file over 500 lines.
- **Rule 5:** TDD — tests first.
- **Rule 6:** NO STUBS. Every function fully implemented.
- **Rule 8:** All file paths absolute in task docs.

---

## Acceptance Criteria (from Spec)

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

---

## Technical Guidance

The spec suggests this approach in the `toggle` handler:
1. Get trigger rect via `btnRef.current.getBoundingClientRect()`
2. Walk up DOM to find `[data-testid="pane-chrome"]` ancestor, get its rect
3. Compute trigger center relative to pane rect
4. Set `pos` to include both coordinates and direction flags
5. In the portal div style, use direction flags to choose anchor point

Example state shape (Q33N may refine):
```ts
const [pos, setPos] = useState<{
  x: number;
  y: number;
  openRight?: boolean;
  openDown?: boolean;
}>({ x: 0, y: 0 });
```

Then in the style:
```ts
transform: `${pos.openRight ? '' : 'translateX(-100%)'} ${pos.openDown ? '' : 'translateY(-100%)'}`.trim()
```

---

## Smoke Test Command

```bash
cd browser && npx vitest run src/shell/components/__tests__/PaneMenu
```

---

## What Q33N Must Do Next

1. **Read the four files listed above** to understand current implementation
2. **Write ONE task file** (this is a single-component fix, single bee)
3. **Include all acceptance criteria** from the spec in the task file
4. **Specify test requirements clearly** (5+ new tests, existing tests must pass)
5. **Return task file to Q88NR for review** (do NOT dispatch the bee yet)

---

## Notes

- `PaneChrome.tsx` already has `data-testid="pane-chrome"` on line 98 — no change needed there
- The fix is entirely in `PaneMenu.tsx` (+ test file)
- Assign **Haiku** — this is a single-file fix with clear requirements
- The spec is in `docs/specs/SPEC-HAMBURGER-MENU-OVERFLOW.md` (Q33N may reference for detail)
