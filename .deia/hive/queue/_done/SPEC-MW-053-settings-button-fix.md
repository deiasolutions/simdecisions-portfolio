# SPEC-MW-053-settings-button-fix: Fix duplicate settings buttons and settings action

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

On the workdesk set, the hamburger menu (sandwich icon on top-bar) shows TWO "Settings" buttons — neither works correctly. Clicking Settings should: 1) close the hamburger menu, 2) open the settings slideover panel (defined in workdesk.set.md as a slideover with trigger "settings"). Additionally, the kebab menu (three dots) on the top-bar also has a Settings option. Investigate why there are duplicates, remove the extra, and wire the remaining Settings button to dispatch the correct action to open the slideover panel. The settings slideover in workdesk.set.md uses `"trigger": "settings"` — the dispatch action should be `TOGGLE_SLIDEOVER_VISIBILITY` with trigger `settings`.

## Files to Read First

- browser/src/primitives/top-bar/TopBar.tsx
- browser/src/primitives/menu-bar/MenuBarPrimitive.tsx
- browser/src/shell/components/DrawerMenu.tsx
- browser/src/shell/components/Shell.tsx
- browser/sets/workdesk.set.md
- browser/src/shell/components/SlideoverPanel.tsx

## Acceptance Criteria

- [ ] The hamburger menu shows exactly ONE "Settings" button, not two
- [ ] Clicking Settings in the hamburger menu closes the menu and opens the settings slideover panel
- [ ] The kebab menu settings option also opens the settings slideover panel
- [ ] Settings slideover opens from the left edge as defined in workdesk.set.md (`"edge": "left"`, `"width": "400px"`)
- [ ] Clicking Settings again (or clicking outside) closes the slideover
- [ ] No TypeScript compilation errors (`npx tsc --noEmit` passes)

## Smoke Test

- [ ] Open `http://localhost:5173/?set=workdesk`, click hamburger — verify one Settings button, click it — settings panel slides in from left
- [ ] Click kebab (three dots) — verify Settings option opens the same settings panel

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- The settings slideover trigger is "settings" — match the workdesk.set.md definition exactly
