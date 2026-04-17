# SPEC: Fix failures from HYG-004-python-dead-code

## Priority
P0

## Objective
Fix the errors reported after processing HYG-004-python-dead-code. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\_active\SPEC-HYG-004-python-dead-code.md
Fix cycle: 1 of 2

### Error Details
Dispatch subprocess exception (FileNotFoundError): [Errno 2] No such file or directory: 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\hive\\tasks\\QUEUE-TEMP-SPEC-HYG-004-python-dead-code.md'

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
haiku

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
