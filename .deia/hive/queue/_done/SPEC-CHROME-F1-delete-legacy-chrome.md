# CHROME-F1: Delete Legacy Chrome Components

## Objective
Delete ShellTabBar.tsx and MasterTitleBar.tsx. Migrate any syndication subscribers from MasterTitleBar to top-bar and toolbar primitives. Remove all imports and references.

## Build Type
**Cleanup/delete** — Delete ShellTabBar.tsx and MasterTitleBar.tsx. Remove all imports and references. No new code — only deletion and cleanup.

## Problem Analysis
ShellTabBar is a broken legacy port (no flex CSS, z-index issues) replaced by appType: tab-bar. MasterTitleBar is misnamed and redundant, replaced by top-bar + per-pane toolbar syndication. Both are dead weight once Wave B primitives are in place. All imports, references, and conditional rendering in Shell.tsx must be removed.

## Files to Read First
- browser/src/shell/components/ShellTabBar.tsx
- browser/src/shell/components/MasterTitleBar.tsx
- browser/src/shell/components/Shell.tsx
- browser/src/shell/components/__tests__/ShellTabBar.test.tsx
- browser/src/shell/components/__tests__/MasterTitleBar.test.tsx

## Files to Modify
- browser/src/shell/components/ShellTabBar.tsx — DELETE
- browser/src/shell/components/MasterTitleBar.tsx — DELETE
- browser/src/shell/components/__tests__/ShellTabBar.test.tsx — DELETE
- browser/src/shell/components/__tests__/MasterTitleBar.test.tsx — DELETE
- browser/src/shell/components/Shell.tsx — remove imports, rendering, ctx.masterTitleBar
- browser/src/shell/types.ts — remove masterTitleBar from ShellCtx if applicable

## Deliverables
- [ ] ShellTabBar.tsx deleted
- [ ] MasterTitleBar.tsx deleted
- [ ] All test files for deleted components deleted
- [ ] Shell.tsx no longer imports or renders either component
- [ ] No dangling references in any file
- [ ] Syndication subscribers migrated to new primitives

## Acceptance Criteria
- [ ] ShellTabBar.tsx does not exist
- [ ] MasterTitleBar.tsx does not exist
- [ ] Shell.tsx compiles without errors
- [ ] No import of ShellTabBar or MasterTitleBar anywhere in codebase
- [ ] All remaining tests pass

## Test Requirements
- [ ] Tests written FIRST (TDD) — before implementation
- [ ] Test file: browser/src/shell/components/__tests__/Shell.legacy-cleanup.test.tsx
- [ ] Test: Shell renders without ShellTabBar component
- [ ] Test: Shell renders without MasterTitleBar component
- [ ] Test: Shell.tsx has no reference to masterTitleBar in context
- [ ] All tests pass
- [ ] Minimum 3 tests

## Smoke Test
- [ ] cd browser && npx vitest run src/shell — no regressions
- [ ] cd browser && npx vitest run — full suite passes

## Constraints
- No stubs
- Verify no other component imports the deleted files before deleting

## Depends On
- SPEC-CHROME-B1 (top-bar replaces WorkspaceBar/MasterTitleBar)
- SPEC-CHROME-B4 (tab-bar replaces ShellTabBar)

## Model Assignment
haiku

## Priority
P2
