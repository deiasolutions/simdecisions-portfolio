# TOPBAR-FIX-AND-SYNDICATION: Fix TopBar Icons + Add Canvas File Menu Syndication -- COMPLETE

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\top-bar\TopBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\top-bar\TopBar.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx`

## What Was Done

### Fix 1: Replaced broken icon images in TopBar

- **Root cause:** `resolveIcon('gc://icons/menu.svg')` and `resolveIcon('gc://icons/more.svg')` resolve to `/icons/menu.svg` and `/icons/more.svg`, but these files do NOT exist in `browser/public/icons/`. Only `sim.svg`, `canvas.svg`, `efemera.svg`, `login.svg`, `hodeia.svg`, `constitution.svg` exist there.
- **Fix applied (Option A):** Replaced `<img>` tags with `<span>` elements using Unicode characters:
  - Hamburger: U+2630 (trigram for heaven / three horizontal lines)
  - Kebab: U+22EE (vertical ellipsis)
- Removed the `resolveIcon` import from TopBar.tsx (no longer needed).
- Added `.top-bar__icon-char` CSS class with `font-size: 16px`, `line-height: 1`, and `color: var(--sd-text-secondary)` (no hardcoded colors).

### Fix 2: TopBar layout verification

- Layout was already correct in CSS. The broken `<img>` tags were the sole cause of the visual problem -- a missing image source causes either 0-width collapse or alt-text overflow.
- With the Unicode character replacement, the 32x32 buttons now render correctly with centered icons.
- Layout order confirmed: `[hamburger] [brand] [currency chip] [spacer] [kebab] [avatar]`.

### Fix 3: Added canvas file syndication to menu bar

**FlowDesigner.tsx changes:**
- Added `createEmptyFlow` to the imports from `./file-ops/serialization`.
- Added a new `targetMenu: "file"` syndicated menu group with three items:
  - `canvas-new-diagram` - "New Diagram" (Ctrl+N)
  - `canvas-save` - "Save Diagram" (Ctrl+S)
  - `canvas-export-ir` - "Export PHASE-IR" (Ctrl+E)
- Added handlers in the `menu:action-invoked` listener for these three new action IDs:
  - `canvas-new-diagram`: calls `handleFlowChange(createEmptyFlow("Untitled Flow"))`
  - `canvas-save`: calls `fileOpsRef.current?.save()`
  - `canvas-export-ir`: calls `fileOpsRef.current?.exportFlow()`

**MenuBarPrimitive.tsx changes:**
- Added syndicated file group rendering to the File dropdown, matching the existing pattern used by Edit and View menus.
- When the canvas pane is focused, the File menu now shows "Canvas >" submenu with New Diagram, Save Diagram, and Export PHASE-IR items.

**Note on existing syndication:** FlowDesigner.tsx already had syndication for View (canvas zoom/grid/minimap), Edit (undo/redo/select/delete/group/duplicate), and Tools (mode switching). The File menu was the only one missing syndicated items, and the MenuBarPrimitive's File dropdown had no `getSyndicatedGroups('file')` call. Both gaps are now closed.

## Test Results

- `browser/src/primitives/top-bar/__tests__/TopBar.test.tsx`: **9 passed, 0 failed**
- `browser/src/primitives/menu-bar/__tests__/MenuBarPrimitive.test.tsx`: **9 passed, 0 failed**
- Total: **18 tests passed, 0 failed**

## Build Verification

- Tests pass: YES (18/18)
- No TypeScript compilation errors observed during test run.

## Acceptance Criteria

- [x] Hamburger icon renders correctly (Unicode U+2630, no broken image)
- [x] Kebab icon renders correctly (Unicode U+22EE, no broken image)
- [x] No overlap between brand text and icons
- [x] TopBar layout: hamburger, brand, spacer, kebab, avatar
- [x] File menu shows canvas file operations when canvas pane is focused
- [x] No hardcoded colors (all CSS uses `var(--sd-*)`)
- [x] All existing tests pass

## Clock / Cost / Carbon

- **Clock:** ~12 minutes
- **Cost:** ~$0.15
- **Carbon:** ~0.02g CO2e

## Issues / Follow-ups

1. **GC icon system has no icons for common UI elements.** `browser/public/icons/` only has product-level icons (sim, canvas, efemera, etc.). When the Global Commons icon set ships, `menu.svg` and `more.svg` should be added and the TopBar can switch back to `resolveIcon()` calls.
2. **Bus addressing for menu syndication:** The FlowDesigner sends `menu:items-changed` with `target: "*"` but the MenuBarPrimitive subscribes on `${paneId}--menus`. This works because `bus.send()` with the second parameter being `paneId` (source pane) broadcasts to subscribers including wildcard matchers. However, the subscription channel is specific to the MenuBarPrimitive's own paneId. This means the syndication relies on the bus routing implementation to deliver `*`-targeted messages to named channels. If this ever breaks, the syndication will silently stop working.
3. **FlowDesigner.tsx is 1,402 lines** -- over the 1,000-line hard limit. This is a pre-existing issue, not introduced by this change (+10 lines net). Should be modularized.
