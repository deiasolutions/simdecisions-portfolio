# SPEC: Fix failures from REQUEUE-BL208-app-directory-sort

## Priority
P0

## Objective
Fix the errors reported after processing REQUEUE-BL208-app-directory-sort. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-18-SPEC-REQUEUE-BL208-app-directory-sort.md
Fix cycle: 1 of 2

### Error Details
Pool exception: [Errno 2] No such file or directory: 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\tasks\\QUEUE-TEMP-2026-03-18-SPEC-REQUEUE-BL208-app-directory-sort.md'

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
