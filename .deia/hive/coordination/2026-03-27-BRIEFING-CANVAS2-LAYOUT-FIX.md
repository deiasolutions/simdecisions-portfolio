# BRIEFING: Canvas2 EGG Layout Rendering is Broken

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-27
**Priority:** P0 — Visible in production at www.shiftcenter.com/app.html?egg=canvas2

## Situation

The canvas2 EGG loads but the layout proportions are wrong. Reported by Q88N at 7:35 AM today (localhost) and still broken at 7:31 PM (production). Screenshots in `C:\Users\davee\Downloads\`:
- `Screenshot 2026-03-27 073600.png` (morning, localhost)
- `Screenshot 2026-03-27 193151.png` (evening, production)

Both show the same problems — 8 hours, no fix.

## What's Wrong

The EGG spec (`eggs/canvas2.egg.md`) defines this layout:

```
Outer: horizontal split ["30px", "1fr", "24px"] → menu-bar | main | status-bar
Main: vertical split [0.22, 0.53, 0.25] → sidebar | canvas | right-column
Right-column: horizontal split 0.80 → chat | IR terminal
```

What's RENDERING:
1. **Right column is way too wide** — should be 25% of main, looks like 40%+
2. **Canvas pane is squeezed** — should be 53%, much smaller
3. **Chat pane is crammed into bottom-right corner** — tiny, truncated text
4. **Minimap floating awkwardly** in dead space

## Root Cause Investigation

A fix for N-child splits landed today (`42fafd1` — `eggToShell.ts`). It uses right-recursive binary nesting to convert 3+ children into nested binary splits. The math for ratio distribution at each nesting level may be wrong, OR the shell renderer isn't applying the computed ratios correctly.

### Key files to investigate:

1. **`browser/src/shell/eggToShell.ts`** — `nestSplits()` and `normalizeRatios()` functions. Check that a 3-child split [0.22, 0.53, 0.25] produces correct nested binary ratios.
2. **`browser/src/shell/eggToShell.multiChild.test.ts`** — 16 tests exist. Check if they actually verify the rendered pixel proportions or just structural correctness.
3. **`browser/src/shell/reducer.ts`** — Does the shell reducer correctly apply ratios from eggToShell output?
4. **`browser/src/shell/ShellRenderer.tsx`** (or equivalent) — Is the CSS flex/grid actually using the ratio values?
5. **`eggs/canvas2.egg.md`** — The source of truth for the layout spec.

### Specific math to verify:

For [0.22, 0.53, 0.25] right-recursive nesting:
- Outer: first child ratio = 0.22 / (0.22 + 0.53 + 0.25) = 0.22, rest = 0.78
- Inner: second child ratio = 0.53 / (0.53 + 0.25) = 0.6795, third = 0.3205

If the renderer sees 0.22 | (0.78 containing 0.68 | 0.32), the final proportions should be:
- sidebar: 22%
- canvas: 78% × 68% = 53%
- right: 78% × 32% = 25%

Verify that THIS is what's actually happening, both in the data structures AND in the rendered DOM.

## Deliverables

1. **Root cause identified** — explain exactly why the proportions are wrong
2. **Fix implemented** — ratios render correctly matching the egg spec
3. **Tests added/updated** — verify the canvas2 egg layout renders at correct proportions
4. **Visual verification** — load canvas2 in browser, confirm layout matches spec

## Constraints

- TDD — write failing test first
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs

## Model Assignment

Sonnet — this is debugging + targeted fix work.
