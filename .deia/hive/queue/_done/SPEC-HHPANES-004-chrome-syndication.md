# SPEC-HHPANES-004: Chrome Hiding and Menu Syndication

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

When launching an app that should hide pane chrome (title bars, per-pane menus), the chrome is not hidden. Additionally, per-pane menu items do not syndicate to the main app menubar when chrome is hidden. Fix both behaviors.

## Files to Read First

- browser/src/shell/components/PaneChrome.tsx
- browser/src/shell/components/MenuBar.tsx
- browser/src/sets/eggConfig.ts
- browser/src/primitives/top-bar/TopBar.tsx

## Acceptance Criteria

- [ ] Set config supports chrome: hidden at pane level and app level
- [ ] When chrome: hidden, pane title bars do not render
- [ ] When chrome: hidden, per-pane menu items syndicate to main menubar
- [ ] Syndicated menu items include source pane identifier for disambiguation
- [ ] Focus changes update which pane's menu items are active in main menubar
- [ ] Chrome visibility can toggle at runtime (not just set load time)
- [ ] All existing PaneChrome and MenuBar tests still pass
- [ ] New tests cover hidden-chrome and syndication behaviors

## Smoke Test

- [ ] Load set with chrome: hidden — no pane title bars visible
- [ ] Confirm main menubar contains syndicated items from focused pane
- [ ] Change focus to different pane — confirm menubar updates
- [ ] Toggle chrome visibility via command — title bars appear/disappear

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
