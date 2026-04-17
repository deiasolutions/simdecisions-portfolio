# CHROME-POLISH: Polish Chrome Primitives (TopBar + MenuBar) -- COMPLETE

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-03-28

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\top-bar\TopBar.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\top-bar\TopBar.css`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\menu-bar\MenuBarPrimitive.css`

## What Was Done

### Fix 1: TopBar not stretching full width
- Removed inline `style={{ height }}` from the root div in TopBar.tsx
- Added `width: 100%`, `height: 36px`, `box-sizing: border-box` to `.top-bar` in TopBar.css
- Added `.top-bar--compact` modifier class with `height: 28px` for compact/immersive modes
- Changed root div className to use conditional `top-bar--compact` class instead of inline style
- Replaced `height` variable with `isCompact` boolean for cleaner logic

### Fix 2: TopBar reads wrong config key
- Changed brand logic from `cfg.brand === 'egg' ? 'SHIFTCENTER' : (cfg.brand || 'SHIFTCENTER')` to `cfg.appName || cfg.brand || 'SHIFTCENTER'`
- Added `appName?: string` to the `TopBarConfig` interface

### Fix 3: MenuBar font too large
- Changed `.menu-bar-primitive` font-size from `0.9rem` to `var(--sd-font-sm, 12px)`
- Changed `.menu-button` font-size from `0.9rem` to `var(--sd-font-sm, 12px)`, padding from `6px 12px` to `4px 10px`
- Changed `.menu-dropdown-item` font-size from `0.9rem` to `var(--sd-font-sm, 12px)`, padding from `8px 16px` to `6px 14px`

### Fix 4: Remove unicode/emoji from MenuBarPrimitive
- Replaced all 3 instances of `▶` (submenu indicator) with `›` (standard right single angle quotation mark)
- Changed toolbar action button rendering: if `action.icon` contains non-ASCII characters (emoji), renders `action.label` text instead
- Left `✓` for checked items (standard character, not emoji, as briefing noted is OK)

## Test Results

### menu-bar tests
- File: `src/primitives/menu-bar/__tests__/MenuBarPrimitive.test.tsx`
- Result: **9 passed, 0 failed**

### top-bar tests
- File: `src/primitives/top-bar/__tests__/TopBar.test.tsx`
- Result: **9 passed, 0 failed**

## Build Verification
- menu-bar: 1 test file, 9 tests passed (772ms)
- top-bar: 1 test file, 9 tests passed (257ms)
- No failures, no warnings.

## Acceptance Criteria

- [x] Fix 1: TopBar stretches full width via CSS (no inline height style)
- [x] Fix 2: TopBar reads `appName` config key with proper fallback chain
- [x] Fix 3: MenuBar uses `var(--sd-font-sm)` for all text elements
- [x] Fix 4: Unicode `▶` replaced with `›`; emoji icons in toolbar fall back to label text
- [x] Fix 5: All tests pass (18/18)

## Clock / Cost / Carbon
- **Clock:** ~4 minutes
- **Cost:** ~$0.15
- **Carbon:** ~0.02g CO2e

## Issues / Follow-ups
- The CurrencyChip sub-component in TopBar.tsx still uses emoji for currency icons (line 75-83). These were NOT in scope per the briefing (Fix 4 targeted MenuBarPrimitive only). If these also need removal, that would be a separate fix.
- The `.menu-dropdown-item.submenu::after` CSS rule has empty `content: ''` -- the `::after` pseudo-element is effectively invisible. The `›` character in the JSX handles the visual indicator. The CSS rule could be cleaned up in a future pass.
