# SPEC: Fix hardcoded colors in 6 animation components

## Priority
P0.70

## Model Assignment
haiku

## Objective
Replace hardcoded color values in 6 animation components with CSS variables (`var(--sd-*)`).

## Task File
`.deia/hive/tasks/2026-03-15-TASK-148-animation-colors-fix.md`

## Acceptance Criteria
- [ ] All 6 animation components use CSS variables only
- [ ] No hardcoded hex, rgb(), or named colors remain
- [ ] All animation tests pass
- [ ] All browser tests pass
