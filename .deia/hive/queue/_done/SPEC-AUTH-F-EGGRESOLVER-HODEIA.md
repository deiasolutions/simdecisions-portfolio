# SPEC-AUTH-F: eggResolver hodeia.me Mapping

## Objective

Add `hodeia.me` hostname-to-EGG mapping in eggResolver so that hodeia.me resolves to the login EGG. Keep `ra96it.com` mapping as deprecated backwards compatibility. Add tests verifying both old and new hostnames resolve to the login EGG.

## Files to Read First

- browser/src/eggs/eggResolver.ts
- browser/src/eggs/__tests__/eggResolver.test.ts

## Files to Modify

- browser/src/eggs/eggResolver.ts
- browser/src/eggs/__tests__/eggResolver.test.ts

## Deliverables

- [ ] hodeia.me hostname mapping added to eggResolver
- [ ] ra96it.com mapping kept with deprecation comment
- [ ] Tests added for both hostnames

## Acceptance Criteria

- [ ] hodeia.me resolves to login EGG
- [ ] ra96it.com still resolves to login EGG (backwards compat)
- [ ] ra96it.com mapping marked as deprecated in comments
- [ ] Tests cover both hostnames
- [ ] No stubs

## Smoke Test

- [ ] cd browser && npx vitest run src/eggs/__tests__/eggResolver.test.ts -- eggResolver tests pass
- [ ] cd browser && npx vitest run -- no regressions

## Constraints

- TDD: write tests first, then implementation
- No file over 500 lines
- No stubs

## Depends On


## Model Assignment

haiku

## Priority

P1
