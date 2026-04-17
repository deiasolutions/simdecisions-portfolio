# TASK-220: Fix Hamburger Menu Overflow Direction

## Objective

Fix `PaneMenu.tsx` so the hamburger menu opens in the direction with available space rather than always opening to the left, preventing menu overflow when the trigger is near pane edges.

## Context

The current implementation in `PaneMenu.tsx` has a hardcoded `transform: 'translateX(-100%)'` on line 111, which always opens the menu to the left of the trigger button. When the trigger is on the left edge of a pane, the menu overflows offscreen.

The fix must:
1. **Self-measure** on every open: get `getBoundingClientRect()` on both the trigger (`btnRef`) and the nearest `[data-testid="pane-chrome"]` ancestor (the pane container)
2. **Compute direction** based on proportional position within the pane (left half → open right, right half → open left, top half → open down, bottom half → open up)
3. **Combine directions** (e.g., bottom-left quadrant → up-and-right)
4. **Fallback for viewport overflow** — if the menu would still overflow the viewport boundary after correct direction is applied, shift it to stay visible
5. **No caching** — recalculate on every open

**Key architectural details:**
- `PaneChrome.tsx` already has `data-testid="pane-chrome"` on the container (line 98) — no change needed there
- Menu is rendered via `createPortal` to `.hhp-root` for z-index safety
- Position is set via `position: fixed` with `left`/`top` coordinates
- The current `translateX(-100%)` trick must be replaced with computed coordinates that account for direction

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneMenu.tsx` — THE file to fix (line 111 has the hardcoded transform)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\PaneChrome.tsx` — renders `<PaneMenu>`, has `data-testid="pane-chrome"` on the container (line 98) — NO changes needed here
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneMenu.test.tsx` — existing tests (15 tests, all passing)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\ChromeBtn.tsx` — trigger button component
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HAMBURGER-MENU-OVERFLOW.md` — full spec reference

## Deliverables

- [ ] Updated `toggle` handler in `PaneMenu.tsx`:
  - Get trigger rect via `btnRef.current.getBoundingClientRect()`
  - Walk up DOM to find `[data-testid="pane-chrome"]` ancestor, get its rect
  - Compute trigger center relative to pane rect
  - Determine horizontal direction: left half → open right, right half → open left
  - Determine vertical direction: top half → open down, bottom half → open up
  - Store both coordinates AND direction flags in `pos` state
  - Do NOT cache — this runs on every open

- [ ] Updated portal div style (line 111):
  - Remove hardcoded `transform: 'translateX(-100%)'`
  - Use computed direction flags to set anchor point
  - If opening right: `left: pos.x` (left-aligned to trigger)
  - If opening left: `left: pos.x, transform: 'translateX(-100%)'` (right-aligned to trigger)
  - If opening down: `top: pos.y` (top-anchored to trigger bottom)
  - If opening up: `top: pos.y, transform: 'translateY(-100%)'` (bottom-anchored to trigger top)
  - Combine transforms when needed: `translateX(-100%) translateY(-100%)` for up-and-left

- [ ] Viewport overflow fallback:
  - After computing preferred direction, check whether the menu rect would overflow the viewport
  - If yes, shift the menu toward the direction with more available space
  - Menu must never clip against the side it's opening toward when the opposite direction has room

## Test Requirements

Write **5+ new tests** covering:
- [ ] Trigger in left half of pane → menu opens to the right
- [ ] Trigger in right half of pane → menu opens to the left
- [ ] Trigger in top half of pane → menu opens downward
- [ ] Trigger in bottom half of pane → menu opens upward
- [ ] Trigger in bottom-left quadrant → menu opens up-and-right
- [ ] Viewport overflow fallback (menu near viewport edge shifts to stay visible)

All existing tests (15 tests) must still pass.

Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\__tests__\PaneMenu.test.tsx`

**Testing notes:**
- Mock `getBoundingClientRect()` on both `btnRef.current` and a mock `[data-testid="pane-chrome"]` element
- Set up mock DOM hierarchy: pane-chrome → title-bar → button
- Test each quadrant by adjusting the mock rects
- Verify the portal div's style includes correct `left`, `top`, and `transform` values

## Constraints

- **No file over 500 lines** (PaneMenu.tsx is currently 172 lines, test file is 302 lines)
- **CSS: var(--sd-*) only** — no hex, no rgb(), no named colors
- **No stubs** — every function fully implemented
- **TDD** — tests first, then implementation

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

## Technical Guidance

Suggested `pos` state shape:
```ts
const [pos, setPos] = useState<{
  x: number;
  y: number;
  openRight?: boolean;
  openDown?: boolean;
}>({ x: 0, y: 0 });
```

Suggested `toggle` handler logic:
```ts
const toggle = (e: React.MouseEvent) => {
  e.stopPropagation();
  if (!open && btnRef.current) {
    const btnRect = btnRef.current.getBoundingClientRect();

    // Walk up to find pane-chrome ancestor
    let paneChrome = btnRef.current.parentElement;
    while (paneChrome && paneChrome.getAttribute('data-testid') !== 'pane-chrome') {
      paneChrome = paneChrome.parentElement;
    }

    if (paneChrome) {
      const paneRect = paneChrome.getBoundingClientRect();

      // Compute trigger center relative to pane
      const btnCenterX = btnRect.left + btnRect.width / 2;
      const btnCenterY = btnRect.top + btnRect.height / 2;
      const paneCenterX = paneRect.left + paneRect.width / 2;
      const paneCenterY = paneRect.top + paneRect.height / 2;

      // Determine direction
      const openRight = btnCenterX < paneCenterX;
      const openDown = btnCenterY < paneCenterY;

      // Set position (viewport coords for portal)
      setPos({
        x: openRight ? btnRect.left : btnRect.right,
        y: openDown ? btnRect.bottom + 4 : btnRect.top - 4,
        openRight,
        openDown,
      });
    }
  }
  setOpen(o => !o);
};
```

Suggested portal div style:
```ts
transform: `${pos.openRight ? '' : 'translateX(-100%)'} ${pos.openDown ? '' : 'translateY(-100%)'}`.trim()
```

**Viewport overflow fallback** (optional enhancement if time permits):
After setting `pos`, compute the menu's expected rect and check against `window.innerWidth`/`window.innerHeight`. Adjust `x`/`y` if overflow detected.

## Smoke Test Command

```bash
cd browser && npx vitest run src/shell/components/__tests__/PaneMenu
```

Expected output: All 15 existing tests + 5+ new tests pass (20+ total).

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-220-RESPONSE.md`

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
