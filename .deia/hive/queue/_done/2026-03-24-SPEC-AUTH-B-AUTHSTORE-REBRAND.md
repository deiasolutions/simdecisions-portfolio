# SPEC: AUTH-B — authStore rebrand localStorage keys ra96it to sd_auth

## Priority
P1

## Objective
Rebrand authStore.ts localStorage keys from ra96it_token/ra96it_user to sd_auth_token/sd_auth_user, implement backwards-compatible migration logic, update all references across the codebase.

## Context
authStore currently uses ra96it_token and ra96it_user as localStorage keys. Rename to sd_auth_token and sd_auth_user to match existing sd_user_settings convention. Migration must be transparent — existing sessions continue seamlessly.

Migration strategy:
- On first load, if old keys exist and new keys don't, copy values from old to new and delete old
- If new keys already exist, do nothing (already migrated)
- If neither exist, do nothing (new user)
- Migration must be idempotent

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts

## Deliverables
- [ ] Rename TOKEN_KEY from ra96it_token to sd_auth_token
- [ ] Rename USER_KEY from ra96it_user to sd_auth_user
- [ ] Implement _migrateOldKeys() called on module load
- [ ] Migration: copy old to new, delete old (only if old exists and new doesn't)
- [ ] Update all imports/references across the codebase
- [ ] Update tests: verify migration path, new key names, backwards compat

## Acceptance Criteria
- [ ] TOKEN_KEY and USER_KEY constants updated to sd_auth_token and sd_auth_user
- [ ] Migration function implemented and called on module load
- [ ] Migration tests pass: old to new copy, old key deletion, no-op when new keys exist
- [ ] All references to ra96it_token/ra96it_user updated in tests and other files
- [ ] No localStorage key collisions or race conditions
- [ ] All authStore tests pass (existing + new migration tests)

## Model Assignment
haiku

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only
- No stubs
- TDD
- Migration must be idempotent — safe to run multiple times
- Do NOT break existing sessions
