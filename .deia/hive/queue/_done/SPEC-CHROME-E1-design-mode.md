# CHROME-E1: Design Mode Toggle

## Objective
Implement design mode runtime toggle. When active: all seamless panes get minimal chrome (drag handle + pane ops + close), pane boundaries become visible with dashed borders, user can rearrange/resize/add/remove panes. Scoped add menu (original EGG primitives + GC library). Exit design mode restores seamless state.

## Build Type
**New build** — No design mode exists. devOverride was the closest concept but it is being killed. Design mode toggle, minimal chrome on seamless panes, scoped add menu — all new.

## Problem Analysis
Design mode replaces the dead devOverride concept. It's a runtime toggle available in local development or when the user has edit permissions. Activated via kebab menu or keyboard shortcut. The key challenge: seamless panes must temporarily gain chrome controls without losing their identity as seamless panes. On exit, seamless state is fully restored.

## Files to Read First
- browser/src/shell/components/PaneChrome.tsx
- browser/src/shell/reducer.ts
- browser/src/shell/types.ts
- docs/specs/ADR-SC-CHROME-001-v3.md

## Files to Modify
- browser/src/shell/types.ts — add designMode: boolean to ShellState
- browser/src/shell/reducer.ts — add TOGGLE_DESIGN_MODE action
- browser/src/shell/components/PaneChrome.tsx — minimal chrome when designMode + seamless
- browser/src/shell/components/DesignModeAddMenu.tsx — NEW: scoped add menu
- browser/src/shell/components/__tests__/DesignMode.test.tsx — NEW tests

## Deliverables
- [ ] ShellState gains designMode: boolean
- [ ] TOGGLE_DESIGN_MODE reducer action
- [ ] In design mode: seamless panes show drag handle + split/flip/resize/close
- [ ] In design mode: all pane boundaries show dashed borders
- [ ] Add menu (+) scoped to: original EGG primitives + GC library primitives
- [ ] Proprietary primitives from other EGGs NOT available in add menu
- [ ] Exit design mode: seamless restored, dashed borders removed

## Acceptance Criteria
- [ ] Design mode toggles on/off
- [ ] Seamless panes gain minimal chrome in design mode
- [ ] Seamless panes lose chrome on design mode exit
- [ ] Add menu only shows EGG-appropriate primitives
- [ ] Dashed borders visible in design mode, hidden on exit

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/shell/components/__tests__/DesignMode.test.tsx
- [ ] Test: TOGGLE_DESIGN_MODE sets designMode true
- [ ] Test: seamless pane gets drag handle in design mode
- [ ] Test: seamless pane loses chrome on design mode exit
- [ ] Test: dashed borders applied to pane wrappers in design mode
- [ ] Test: add menu shows original EGG primitives
- [ ] Test: add menu does not show primitives from other EGGs
- [ ] All tests pass
- [ ] Minimum 6 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/shell/components/__tests__/DesignMode — tests pass
- [ ] cd browser && npx vitest run src/shell — no regressions

## Constraints
- No file over 500 lines
- No stubs
- CSS: var(--sd-*) only
- Design mode is visual only — does not persist until explicit save (E2)

## Depends On
- SPEC-CHROME-A6 (dirty flags needed to determine if save prompt is required on exit)

## Model Assignment
sonnet

## Priority
P2
