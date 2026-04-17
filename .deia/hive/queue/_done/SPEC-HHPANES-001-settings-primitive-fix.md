# SPEC-HHPANES-001: Settings Primitive Fix

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Fix the Settings primitive so it renders without errors, displays current state on load, and emits correct bus events on change. Currently the settings pane does not function correctly when instantiated in composites.

## Files to Read First

- browser/src/primitives/settings/SettingsPanel.tsx
- browser/src/primitives/settings/SettingsModal.tsx
- browser/src/primitives/settings/settingsStore.ts
- browser/src/primitives/settings/types.ts
- browser/src/primitives/settings/index.tsx
- browser/src/apps/authAdapter.tsx

## Acceptance Criteria

- [ ] Settings pane renders without errors
- [ ] Settings values display current state on load
- [ ] Settings changes emit correct bus events
- [ ] Settings pane works in isolation (test harness)
- [ ] Settings pane works when composed in at least one composite (AI Chat set)
- [ ] All existing settings tests still pass
- [ ] New tests added for any fixed behavior

## Smoke Test

- [ ] Load settings pane in test harness — no console errors
- [ ] Change a setting value — confirm bus event emitted with correct payload
- [ ] Reload pane — confirm value persisted in-memory

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations
- Use var(--sd-*) CSS variables only
- If scope expands beyond one session, split into TASK-HHPANES-SETTINGS-001a/b/c
