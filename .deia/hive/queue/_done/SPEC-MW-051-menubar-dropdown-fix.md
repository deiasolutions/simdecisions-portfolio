# SPEC-MW-051-menubar-dropdown-fix: Fix menu bar dropdown positioning on workdesk

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set (`?set=workdesk`), the menu bar dropdown menus render in the wrong position — up and to the left instead of down and to the right of the menu button.

ROOT CAUSE (already identified): On Mar 30 (commit 8f6058e) the dropdown was fixed by portaling to `document.body` with `position: fixed` to escape `overflow: hidden` on parent containers. This worked. Then on the SAME DAY (commit b7d48e8) the portal target was changed from `document.body` to `.hhp-root` because CSS variables (`--sd-surface`, etc.) are scoped to `.hhp-root` and the dropdown lost its theme styling when portaled to body. But `.hhp-root` IS the `shell-frame` div which has `overflow: hidden` in shell.css — so the portal fix was defeated.

THE FIX: Portal to `document.body` (to escape overflow) but COPY the relevant CSS custom properties from `.hhp-root` onto the portaled dropdown wrapper. This can be done by:
1. Reading `getComputedStyle(hhpRoot)` for the `--sd-*` variables on mount
2. OR adding a small wrapper div in the portal with `className="hhp-root"` and the same `data-theme`/`data-mode` attributes so the CSS selectors match
3. OR importing the theme CSS at `:root` level instead of `.hhp-root` (not recommended — breaks multi-theme)

Option 2 is cleanest: wrap the portaled content in a `<div className="hhp-root" data-theme={theme} data-mode={mode}>` so theme CSS selectors apply.

## Files to Read First

- browser/src/primitives/menu-bar/MenuBarPrimitive.tsx
- browser/src/primitives/menu-bar/MenuBarPrimitive.css
- browser/src/shell/components/MenuBar.tsx
- browser/src/shell/components/Shell.tsx
- browser/src/shell/components/shell.css
- browser/sets/workdesk.set.md
- browser/src/shell/useEggInit.ts

## Acceptance Criteria

- [ ] Loading `?set=workdesk` and clicking File/Edit/View/Help shows dropdowns directly BELOW the clicked menu button, left-aligned
- [ ] Dropdown menus do not render above or to the left of the menu button
- [ ] Submenus (e.g. View > Theme) render to the RIGHT of the parent menu item
- [ ] If the dropdown would overflow the right edge of the viewport, it adjusts left (existing overflow logic preserved)
- [ ] Only ONE menu bar component renders on workdesk (not both MenuBar and MenuBarPrimitive)
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)
- [ ] The fix works on both desktop and mobile viewports

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk`, click "File" — dropdown appears below the button
- [ ] Click "View" > hover "Theme" — submenu appears to the right
- [ ] Resize window to < 768px — menu bar adapts to mobile layout without errors

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- If changing the portal target from `.hhp-root` to `document.body`, ensure CSS variables still apply (theme vars are scoped to `.hhp-root`)
- Do not remove the old MenuBar.tsx — other sets may depend on it. Only ensure workdesk uses the correct one.
