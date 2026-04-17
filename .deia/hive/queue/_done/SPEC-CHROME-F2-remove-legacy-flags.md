# CHROME-F2: Remove devOverride and hide* Flags

## Objective
Remove the devOverride flag from EGG schema and all code paths. Remove hideMenuBar, hideStatusBar, hideTabBar, hideActivityBar flags from EGG schema. Update the inflater to reject old-style flags with a clear error message directing the author to the migration guide. Remove SAVE_WORKSPACE / LOAD_WORKSPACE reducer actions.

## Build Type
**Cleanup/delete** — Remove devOverride, hide* flags, and workspace concept from types, inflater, and reducer. Add inflater validation that rejects old flags with migration error messages.

## Problem Analysis
The ADR kills: devOverride (replaced by design mode), hide* flags (replaced by layout composition — chrome presence determined by whether the EGG includes the primitive), and the workspace concept (replaced by derived user EGGs). The inflater must reject old flags with actionable error messages so EGG authors know how to migrate.

## Files to Read First
- browser/src/eggs/types.ts
- browser/src/eggs/eggInflater.ts
- browser/src/shell/reducer.ts
- browser/src/shell/actions/lifecycle.ts
- browser/src/shell/types.ts

## Files to Modify
- browser/src/eggs/types.ts — remove devOverride, hide* from EggUiConfig
- browser/src/eggs/eggInflater.ts — add validation rejecting old flags with error messages
- browser/src/shell/reducer.ts — remove SAVE_WORKSPACE, LOAD_WORKSPACE
- browser/src/shell/actions/lifecycle.ts — remove workspace handlers
- browser/src/shell/types.ts — remove workspaces from ShellState
- browser/src/eggs/__tests__/eggInflater.legacy-reject.test.ts — NEW tests

## Deliverables
- [ ] devOverride removed from EGG types and all code paths
- [ ] hideMenuBar, hideStatusBar, hideTabBar, hideActivityBar removed
- [ ] Inflater rejects EGGs with old flags: clear error message
- [ ] SAVE_WORKSPACE / LOAD_WORKSPACE removed from reducer
- [ ] workspaces removed from ShellState

## Acceptance Criteria
- [ ] EGG with devOverride: true fails inflater with migration error
- [ ] EGG with hideMenuBar: true fails inflater with migration error
- [ ] Error message includes instruction: "Use layout composition instead"
- [ ] SAVE_WORKSPACE dispatch throws or is no-op
- [ ] No references to devOverride, hide* flags, or workspace concept remain

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/eggs/__tests__/eggInflater.legacy-reject.test.ts
- [ ] Test: EGG with devOverride rejected with error
- [ ] Test: EGG with hideMenuBar rejected with error
- [ ] Test: EGG with hideStatusBar rejected with error
- [ ] Test: EGG with hideTabBar rejected with error
- [ ] Test: Error message includes migration guidance
- [ ] Test: EGG without old flags inflates normally
- [ ] All tests pass
- [ ] Minimum 6 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/eggs/__tests__/eggInflater.legacy-reject — tests pass
- [ ] cd browser && npx vitest run src/shell — no regressions
- [ ] cd browser && npx vitest run — full suite passes

## Constraints
- No stubs
- Error messages must be actionable (tell the author what to do instead)

## Depends On
- SPEC-CHROME-F5 (all EGGs retrofitted first, otherwise inflater rejects them)

## Model Assignment
haiku

## Priority
P2
