# SPEC-AUTH-A: LoginPage Rebrand (ra96it to hodeia)

## Objective

Update the LoginPage component to replace all "ra96it" branding with "hodeia" or neutral "Sign in" language. Replace the `VITE_RA96IT_API` env var reference with `VITE_AUTH_API`. Keep the GitHub OAuth flow intact -- only display text and env var naming changes.

## Files to Read First

- browser/src/primitives/auth/LoginPage.tsx
- browser/src/primitives/auth/__tests__/LoginPage.test.tsx

## Files to Modify

- browser/src/primitives/auth/LoginPage.tsx
- browser/src/primitives/auth/__tests__/LoginPage.test.tsx

## Deliverables

- [ ] All "ra96it" UI text replaced with "hodeia" or neutral "Sign in" language
- [ ] VITE_RA96IT_API env var reference changed to VITE_AUTH_API
- [ ] Test assertions updated to match new text
- [ ] OAuth flow logic unchanged

## Acceptance Criteria

- [ ] No "ra96it" text visible in LoginPage UI
- [ ] GitHub OAuth still works (redirect URL unchanged)
- [ ] VITE_AUTH_API env var used instead of VITE_RA96IT_API
- [ ] Tests updated and passing
- [ ] No stubs

## Smoke Test

- [ ] cd browser && npx vitest run src/primitives/auth/__tests__/LoginPage.test.tsx -- LoginPage tests pass
- [ ] cd browser && npx vitest run -- no regressions

## Constraints

- TDD: update tests first, then implementation
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- Do NOT modify the OAuth flow logic
- Do NOT touch the ra96it backend (lives in platform repo)
- Do NOT change API endpoints (just the env var name that points to them)

## Depends On


## Model Assignment

sonnet

## Priority

P0
