# SPEC-BL-956-FAB-EGG-DISCOVERY

## Backlog
BL-956

## Priority
P1

## Model
sonnet

## Summary
EmptyPane FAB uses a hardcoded APP_REGISTRY (6 apps in constants.ts). It should discover available EGGs dynamically from the eggs/ directory. When the user selects an app (full EGG layout), prompt with 3 choices: load into this pane, fill the entire screen, or add to a new tab. Applets and primitives spawn directly without prompting.

## Key Files
- `browser/src/shell/components/EmptyPane.tsx` — FAB component, context menu, app selection logic
- `browser/src/shell/constants.ts` — static `APP_REGISTRY` array (lines 65-91)
- `browser/src/shell/components/appRegistry.ts` — runtime renderer registry (`registerApp`, `listRegisteredApps`)
- `browser/src/eggs/useEggManifest.ts` — existing EGG manifest hook (currently unused by FAB)
- `browser/src/eggs/parseEggManifest.ts` — EGG markdown parser
- `browser/src/eggs/index.ts` — EGG registry, `getEggRegistry()`
- `browser/src/shell/reducer.ts` — handles SPAWN_APP action

## Required Changes

### 1. Dynamic EGG discovery for FAB
Replace the static `APP_REGISTRY` filter in EmptyPane with a dynamic query of available EGGs. Use `getEggRegistry()` or a new hook that returns all discovered EGGs with their metadata (displayName, description, category). The Vite plugin `serveEggs()` already serves `*.egg.md` files from the `eggs/` directory — leverage the existing EGG loader/registry.

### 2. App load prompt dialog
When a user selects an app (category='app') from the FAB menu, show a prompt dialog:

> "[DisplayName] is a full screen app. Do you want to load it into this pane, fill the entire screen, or add it to a new tab?"

Three buttons:
- **This pane** — dispatch `SPAWN_APP` with the app's primary appType into the current pane
- **Full screen** — navigate to the EGG URL (`?egg=eggId`)
- **New tab** — dispatch `ADD_TAB` then `SPAWN_APP` into the new tab's pane

### 3. Keep applets and primitives as-is
Applets and primitives should continue to spawn directly via `SPAWN_APP` without prompting — they're designed for single-pane use.

## Constraints
- Do not remove APP_REGISTRY entirely — it can still hold category/label metadata as a fallback
- Use `var(--sd-*)` CSS variables only, no hardcoded colors
- Dialog should use portal to `.hhp-root` (same as other modals)
- TDD: write tests first
- File size limit: 500 lines

## Tests Required
1. FAB menu shows all EGGs from registry, not just hardcoded 6
2. Clicking an app shows 3-choice prompt dialog
3. "This pane" dispatches SPAWN_APP with correct appType
4. "Full screen" navigates to correct EGG URL
5. "New tab" dispatches ADD_TAB then SPAWN_APP
6. Clicking an applet spawns directly without prompt
7. Clicking a primitive spawns directly without prompt
8. Dialog closes on Escape key
9. Dialog renders via portal to .hhp-root

## Depends On
Nothing

## Acceptance Criteria
- [ ] FAB discovers available EGGs dynamically from the EGG registry
- [ ] App selection shows a 3-choice prompt: this pane, full screen, new tab
- [ ] Prompt dialog text includes the app's display name
- [ ] "This pane" option dispatches SPAWN_APP into current pane
- [ ] "Full screen" option navigates to EGG URL
- [ ] "New tab" option creates a tab and spawns the app there
- [ ] Applets and primitives still spawn directly without prompt
- [ ] All 9 tests passing
- [ ] No hardcoded colors — CSS variables only
