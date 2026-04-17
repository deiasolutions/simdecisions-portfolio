# CANVAS3-CHROME-FIX: Fix canvas3 Chrome Primitives -- COMPLETE

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas3.egg.md` — added `showCurrencyChip: false` to top-bar config
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.css` — changed dropdown to `position: fixed` with `z-index: 3000`, added `z-index: 3001` to submenu
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx` — added fixed-position dropdown computation via `getBoundingClientRect()` on menu-item elements; updated all menu click/hover handlers to pass event and compute dropdown position

## What Was Done

### Part 1: canvas3.egg.md
- Added `"showCurrencyChip": false` to the `chrome-top` (top-bar) config section
- `appName: "SimDecisions Canvas"` and `showBreadcrumb: true` were already present

### Part 2: MenuBarPrimitive Investigation
- **Git history:** Only one commit ever touched `browser/src/primitives/menu-bar/` — commit `b939667` ("fix: commit missing bee source files") which added all three files (TSX, CSS, test). The component was created as a port of the legacy MenuBar.tsx (594 lines) during the Chrome ADR Wave B implementation.
- **Git stash:** Checked all 13 stashes (stash@{0} through stash@{12}). None contain changes to `browser/src/primitives/menu-bar/`. Stashes 5, 6, and 8 (which relate to Chrome ADR work) do not include menu-bar modifications.
- **Platform repo:** Access to the platform repo was denied by permissions. Could not search for a newer MenuBar version there.
- **Branches:** Four branches exist: `browser-recovery`, `dev` (current), `main`, `temp-clean-main`. The `browser-recovery` branch has no menu-bar commits. No chrome-specific branches exist.
- **Old MenuBar.tsx in shell/components:** Git history shows 7 commits touching `browser/src/shell/components/MenuBar*`, confirming the old MenuBar.tsx existed in the shell directory before being ported to a primitive.
- **Conclusion:** No newer version of MenuBarPrimitive exists anywhere in the shiftcenter repo. The current version is the only one ever created. A search of the platform repo was blocked by permissions.

### Part 3: MenuBar z-index Fix
- **Root cause identified:** The `.menu-dropdown` used `position: absolute` (relative to `.menu-item` parent). However, the PaneChrome wrapper for seamless panes applies `overflow: hidden` (PaneChrome.tsx lines 47-55), which clips any absolutely-positioned elements that extend beyond the pane boundary. The dropdown was invisible because it was clipped by the ancestor's overflow.
- **Fix applied:**
  - Changed `.menu-dropdown` from `position: absolute` to `position: fixed` in CSS
  - Set z-index to `3000` (matches shell context menu level, above all layout content including `Z_LAYERS.SPOTLIGHT = 1000`)
  - Added z-index `3001` to `.menu-submenu` to layer above the parent dropdown
  - In TSX: added `dropdownPos` state that tracks computed `{ top, left }` for each menu's dropdown, derived from the `.menu-item` element's `getBoundingClientRect()` at click/hover time
  - Updated all 5 menu click handlers and 5 hover handlers to pass the MouseEvent and compute the dropdown position
  - Applied inline `style={dropdownPos[menuId]}` to each dropdown div

### Part 4: TopBar CSS
- **No changes needed.** The TopBar CSS is correct:
  - `.top-bar` uses `display: flex; align-items: center; gap: var(--sd-gap-md, 8px)`
  - `.top-bar__spacer` uses `flex: 1; min-width: var(--sd-gap-md, 8px)` which correctly pushes kebab+avatar to the right
  - With `showCurrencyChip: false`, the render order is: hamburger | brand | spacer(flex:1) | kebab | avatar
  - The bar stretches full width via default cross-axis stretching in the parent flex column container (PaneChrome seamless wrapper)
  - `flex-shrink: 0` prevents the bar from being compressed

### Part 5: Test Results

### Part 6: ADR on Menu-Bar Design
- ADR-SC-CHROME-001-v3, Section 3.2 specifies:
  - menu-bar renders: **File/Edit/View/Help menus** plus **syndicated toolbar action buttons on the right side**
  - Subscribes to `menu:items-changed` for syndication from focused pane
  - Emits `menu:action-invoked` on click
  - On mobile: hidden, syndicated items route to command palette via kebab
  - **No mention of unicode emoji buttons** — the ADR Section 2.3 explicitly states: "All icons in the schema are SVG references: `gc://icons/{name}.svg`. No unicode, no emoji, no font icons."
  - The current implementation uses text labels for menus (File, Edit, View, Help) which is correct. The toolbar action icons are syndicated from focused panes and currently use emoji (from the pane that sends them). This is acceptable short-term since Global Commons icon resolver is not yet live.

## Test Results

- **menu-bar tests:** 9 passed, 0 failed (MenuBarPrimitive.test.tsx)
- **top-bar tests:** 9 passed, 0 failed (TopBar.test.tsx)
- **eggToShell tests:** 43 passed, 0 failed (4 test files: eggToShell.test.ts, eggToShell.multiChild.test.ts, eggToShell.showChrome.test.ts, eggToShell.slideover.test.ts)
- **Total:** 61 tests passed, 0 failed

## Build Verification

All 61 tests pass. No build command was run separately (tests include compilation via esbuild/vitest transform).

## Acceptance Criteria

- [x] canvas3.egg.md has `showCurrencyChip: false` in top-bar config
- [x] canvas3.egg.md has `appName: "SimDecisions Canvas"` in top-bar config
- [x] canvas3.egg.md has `showBreadcrumb: true` in top-bar config
- [x] MenuBar investigation complete — no newer version found in git history, stashes, or branches
- [x] MenuBar dropdown z-index fixed — uses `position: fixed` with `z-index: 3000` to escape `overflow: hidden`
- [x] TopBar CSS verified — layout is correct with flexbox, no changes needed
- [x] All tests pass (menu-bar: 9, top-bar: 9, eggToShell: 43)

## Clock / Cost / Carbon

- **Clock:** ~15 minutes
- **Cost:** estimated $0.30
- **Carbon:** estimated 0.1g CO2e

## Issues / Follow-ups

1. **Platform repo investigation blocked:** Could not search the platform repo for a newer MenuBar version due to file permission restrictions. Q88N may want to check `C:\Users\davee\OneDrive\Documents\GitHub\platform\` manually for any menu-bar components.
2. **Unicode emoji in toolbar actions:** The ADR mandates SVG icons via `gc://icons/` but the toolbar actions syndicated from panes still use emoji. This is a known pre-existing issue that will resolve when Global Commons ships.
3. **TopBar `appName` config not consumed:** The TopBar component's `TopBarConfig` interface defines `brand` not `appName`. The `appName` value set in canvas3.egg.md is currently ignored by the TopBar component. A follow-up task should either rename the config key to `brand` in the EGG or update TopBar to read `appName`.
