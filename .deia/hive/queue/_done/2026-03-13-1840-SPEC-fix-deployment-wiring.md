# SPEC: Fix failures from deployment-wiring

## Priority
P0

## Objective
Fix the errors reported after processing deployment-wiring. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-13-1803-SPEC-deployment-wiring.md
Fix cycle: 1 of 2

### Error Details
Dispatch timeout after 1800s: Command '['python', 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\scripts\\dispatch\\dispatch.py', 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\shiftcenter\\.deia\\hive\\tasks\\QUEUE-TEMP-2026-03-13-1803-SPEC-deployment-wiring.md', '--model', 'sonnet', '--role', 'queen', '--inject-boot', '--timeout', '1800']' timed out after 1800 seconds

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
sonnet

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
