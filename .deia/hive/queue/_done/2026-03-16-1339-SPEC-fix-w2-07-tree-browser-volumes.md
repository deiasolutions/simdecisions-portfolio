# SPEC: Fix failures from w2-07-tree-browser-volumes

## Priority
P0

## Objective
Fix the errors reported after processing w2-07-tree-browser-volumes. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-16-1032-SPEC-w2-07-tree-browser-volumes.md
Fix cycle: 1 of 2

### Error Details
Pool exception: Command '['python', 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\scripts\\dispatch\\dispatch.py', 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\tasks\\QUEUE-TEMP-2026-03-16-1032-SPEC-w2-07-tree-browser-volumes.md', '--model', 'sonnet', '--role', 'regent', '--inject-boot']' timed out after 10 seconds

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
