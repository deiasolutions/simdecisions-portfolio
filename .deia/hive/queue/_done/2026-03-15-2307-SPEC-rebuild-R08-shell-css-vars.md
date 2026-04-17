# SPEC: Fix CSS var violations in ShellTabBar + WorkspaceBar

## Priority
P0.40

## Model Assignment
haiku

## Objective
Replace hardcoded `rgba()` values in `ShellTabBar.tsx` and `WorkspaceBar.tsx` with CSS variables.

## Task File
`.deia/hive/tasks/2026-03-15-TASK-R08-fix-shell-css-variables.md`

## Acceptance Criteria
- [ ] ShellTabBar.tsx boxShadow uses CSS variable
- [ ] WorkspaceBar.tsx hover/active/shadow all use CSS variables
- [ ] All browser tests pass
- [ ] No hardcoded rgba() values remain in either file
