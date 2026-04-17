# SPEC: Fix failures from HYG-005-ts-node-types

## Priority
P0

## Objective
Fix the errors reported after processing HYG-005-ts-node-types. See error details below.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\_active\SPEC-HYG-005-ts-node-types.md
Fix cycle: 1 of 2

### Error Details
Dispatch subprocess exception (FileNotFoundError): [Errno 2] No such file or directory: 'C:\\Users\\davee\\OneDrive\\Documents\\GitHub\\simdecisions\\.deia\\hive\\tasks\\QUEUE-TEMP-SPEC-HYG-005-ts-node-types.md'

## Acceptance Criteria
- [ ] All original acceptance criteria still pass
- [ ] Reported errors are resolved
- [ ] No new test regressions

## Model Assignment
haiku

## Constraints
- Do not break existing tests
- Fix the reported errors, do not refactor
