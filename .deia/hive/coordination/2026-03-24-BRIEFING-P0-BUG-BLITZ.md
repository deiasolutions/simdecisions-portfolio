# BRIEFING: P0 Bug Blitz

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0 — Alpha blockers

---

## Objective

Fix or verify-and-close all 7 open P0 bugs. Three may already be fixed by the Canvas Full Port (commit 0336f49). Verify those first, then dispatch bees for the remaining.

## Bug List

### Verify First (may already be fixed by canvas port bees)

1. **BUG-018** — Canvas IR generation shows error, response appears in Code egg instead
   - Component: `browser/canvas`
   - The canvas port added IR pipeline (`irConverter.ts`), pane adapters, and terminal IR routing. Check if this is now wired correctly.

2. **BUG-019** — Canvas component drag captured by Stage instead of dropping on canvas
   - Component: `browser/canvas`
   - The canvas port added smart edge handles, lasso overlay, and NodePalette with 16 draggable items. Check if drag isolation is now handled.

3. **BUG-028** — Efemera channels not wired: clicking channels does nothing
   - Component: `browser/efemera`
   - channelsAdapter.ts, membersAdapter.ts, relayPoller.ts were all implemented. Check if the wiring is complete.

### Fix Required

4. **BUG-017** — OAuth redirect to ra96it.com shows LandingPage instead of logged-in state
   - Component: `ra96it`
   - OAuth flow issue. After redirect back from provider, the app shows LandingPage instead of recognizing the auth token.

5. **BUG-023** — Canvas components panel does not collapse to icon-only mode per spec
   - Component: `browser/canvas`
   - NodePalette should support a collapsed state showing only icons. Currently always shows full labels.

6. **BUG-058** — Canvas to_ir handler not wired: IR deposits from terminal do not render on canvas
   - Component: `browser/canvas`
   - Terminal can generate IR but the canvas pane doesn't have a bus listener to receive and render it.

7. **BUG-068** — Explorer tree items not rendering with correct file type icons or directory indicators
   - Component: `browser/tree-browser`
   - Items in the code app explorer don't show file type differentiation or directory markers.

## Dispatch Strategy

1. **Wave 0 (verify):** Dispatch 1 bee to investigate BUG-018, BUG-019, BUG-028. If fixed, close them. If not, write fix specs.
2. **Wave 1 (fix):** Dispatch bees for each remaining bug (BUG-017, BUG-023, BUG-058, BUG-068) plus any from Wave 0 that weren't actually fixed.

## Additional Task: Bus API Sweep

One more task to write and dispatch — a sweep for incorrect MessageBus API calls:
- `bus.emit()` — DOES NOT EXIST, must be `bus.send()`
- `bus.on()` — DOES NOT EXIST, must be `bus.subscribe()`
- `bus.off()` — DOES NOT EXIST, `subscribe()` returns unsubscribe function

Search all `.ts` and `.tsx` under `browser/src/` and fix every violation. The MessageBus only has `send()` and `subscribe()`. See `browser/src/infrastructure/relay_bus/messageBus.ts` for the interface.

## Instructions

- Read `.deia/BOOT.md` first — 10 hard rules apply.
- Write task files for each bug, then **dispatch bees yourself**.
- TDD: tests first for every fix.
- No files over 500 lines.
- CSS: `var(--sd-*)` only — no hardcoded colors.
- Each bee gets ONE bug. Do not combine bugs into a single task.
- Mark bugs FIXED in inventory after verification: `python _tools/inventory.py bug update --id BUG-NNN --status FIXED`
- The Q33N already wrote task files in `.deia/hive/tasks/` from a previous run. Review those, and if they look good, dispatch the bees directly. No need to rewrite them.

## Also Note

- **171 hardcoded color violations** exist across the codebase. Do NOT address these in bug fix tasks — that's a separate sweep.
- **FlowDesigner.tsx is 1,272 lines** — over 1,000-line limit. Do NOT refactor in bug fix tasks — separate task.
