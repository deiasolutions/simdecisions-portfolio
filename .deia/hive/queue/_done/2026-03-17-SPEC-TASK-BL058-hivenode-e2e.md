# BL-058: Hivenode E2E - volumes, sync, shell

## Objective
Complete end-to-end testing for hivenode covering volume operations, file sync, and shell execution.

## Context
Hivenode has volume routes, sync capabilities, and shell execution. E2E tests need to verify the full stack works: create volume, write files, sync, execute shell commands, verify results.

## Files to Read First
- `tests/hivenode/test_e2e.py`
- `hivenode/routes/`
- `hivenode/shell/`
- `hivenode/volumes/`

## Deliverables
- [ ] E2E test: volume create, write, read, delete
- [ ] E2E test: file sync between volumes
- [ ] E2E test: shell command execution with allowlist
- [ ] E2E test: combined workflow (create volume, write file, execute command on file)
- [ ] All tests use real server subprocess

## Acceptance Criteria
- [ ] Volume CRUD operations tested E2E
- [ ] Sync operations tested E2E
- [ ] Shell execution tested E2E with allowlist
- [ ] All E2E tests pass
- [ ] Tests use tmp dirs for isolation

## Smoke Test
- [ ] `cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter" && python -m pytest tests/hivenode/test_e2e.py -v`

## Constraints
- No file over 500 lines
- No stubs
- Use tmp dirs for test isolation

## Model Assignment
sonnet

## Priority
P0
