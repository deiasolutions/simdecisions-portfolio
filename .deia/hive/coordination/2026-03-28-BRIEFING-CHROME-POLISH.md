# BRIEFING: Polish Chrome Primitives — TopBar + MenuBar

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-28
**Priority:** P0

## Context

canvas3 loads but chrome primitives have visual bugs. The user has hard-refreshed many times. These are real CSS/component issues, not caching.

## Your Mission

Fix ALL of these issues in one pass. Read each file before editing.

### Fix 1: TopBar not stretching full width

**File:** `browser/src/primitives/top-bar/TopBar.tsx`

The TopBar component sets `style={{ height }}` on its root div (line 152). This may be interfering with flex stretching.

- Remove the inline `height` style from the root div
- Instead, set `height` and `width: 100%` in the CSS class

**File:** `browser/src/primitives/top-bar/TopBar.css`

- Add `width: 100%` to `.top-bar`
- Add `height: 36px` to `.top-bar` (the default, override with a modifier class for compact)
- Add `box-sizing: border-box` to `.top-bar`

### Fix 2: TopBar reads wrong config key

**File:** `browser/src/primitives/top-bar/TopBar.tsx`

Line 125: `const brand = cfg.brand === 'egg' ? 'SHIFTCENTER' : (cfg.brand || 'SHIFTCENTER')`

Change to also check `appName`:
```ts
const brand = cfg.appName || cfg.brand || 'SHIFTCENTER'
```

Update `TopBarConfig` interface to add `appName?: string`.

### Fix 3: MenuBar font too large

**File:** `browser/src/primitives/menu-bar/MenuBarPrimitive.css`

Find the font-size on `.menu-button` or `.menu-bar-primitive` and reduce it. The menu bar should use `var(--sd-font-sm)` (typically 12px) for menu labels. Read the file first to see what's there.

### Fix 4: Remove unicode/emoji from MenuBarPrimitive

**File:** `browser/src/primitives/menu-bar/MenuBarPrimitive.tsx`

Search for any emoji or unicode characters (like ▶, ✓, 🎨, etc.) and replace them with plain text alternatives:
- `▶` for submenu indicator → replace with `›` or just use CSS `::after` with a chevron
- `✓` for checked items → replace with a simple CSS checkmark or the text "✓" is actually OK (it's a standard character, not emoji)
- Remove any emoji icons from toolbar action buttons — if the action.icon is emoji, render the action.label text instead

### Fix 5: Verify the fix works

After making changes:
1. Run `npx vitest run menu-bar` from browser/
2. Run `npx vitest run top-bar` from browser/
3. Report results

## Deliverable

Write to: `.deia/hive/responses/20260328-CHROME-POLISH.md`

Include:
1. Exact changes made per file
2. Test results
3. Confirm all 4 fixes applied

## Constraints

- Edit ONLY: TopBar.tsx, TopBar.css, MenuBarPrimitive.tsx, MenuBarPrimitive.css
- Do NOT edit any other files
- Do NOT rewrite components — surgical fixes only
- Read each file BEFORE editing

## Model Assignment

Sonnet — CSS + TSX fixes.
