# SPEC: AUTH-F — eggResolver mark ra96it entries as deprecated

## Priority
P1

## Objective
Update eggResolver.ts to add deprecation comments on ra96it.com hostname entries while keeping them for backwards compatibility. Add tests verifying both hodeia.me and ra96it.com resolve to login.

## Context
eggResolver.ts already has hodeia.me to login mapping (lines 127-128) and legacy ra96it.com to login mappings (lines 140-142). This task adds deprecation comments and test coverage. Minimal code changes.

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\__tests__\eggResolver.test.ts

## Deliverables
- [ ] Add comment above ra96it.com entries: Legacy DEPRECATED use hodeia.me
- [ ] Add inline comment after each ra96it entry marking deprecated
- [ ] Update tests: verify hodeia.me and ra96it.com both resolve to login
- [ ] Add tests for www.hodeia.me and www.ra96it.com

## Acceptance Criteria
- [ ] Both hodeia.me and ra96it.com to login mappings present
- [ ] Comments added marking ra96it.com entries as deprecated
- [ ] Tests verify both hostnames resolve to login correctly
- [ ] No functional changes — routing behavior unchanged
- [ ] All eggResolver tests pass (existing + new hostname tests)

## Model Assignment
haiku

## Constraints
- No file over 500 lines
- No stubs
- TDD
- Do NOT remove ra96it.com entries — backwards compat required
