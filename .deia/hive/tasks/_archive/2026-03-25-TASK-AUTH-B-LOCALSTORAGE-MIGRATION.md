# TASK-AUTH-B: localStorage Key Migration (hodeia to sd_auth)

## Objective

Rename localStorage keys from `hodeia_token`/`hodeia_user` to `sd_auth_token`/`sd_auth_user` to match the existing `sd_user_settings` convention. Add a backwards-compatible migration function that runs on authStore init. Existing authenticated sessions must survive the rename (no forced logout).

## Context

The current auth localStorage keys use the `hodeia_` prefix, which is inconsistent with the existing `sd_user_settings` key convention used elsewhere in the app. We need to:

1. Rename the key constants in authStore.ts
2. Add a migration function that runs on init
3. Ensure existing sessions survive the rename (no forced logout)
4. Make the migration idempotent (safe to run multiple times)

The migration must handle 4 scenarios:
- **Old keys exist, new keys do not** → copy old to new, delete old
- **New keys exist, old keys do not** → do nothing (already migrated)
- **Both exist** → new keys take precedence, delete old (cleanup)
- **Neither exist** → do nothing (fresh user)

### Current Implementation

**authStore.ts:**
- Constants: `TOKEN_KEY = 'hodeia_token'`, `USER_KEY = 'hodeia_user'`
- Functions: `getToken()`, `setToken()`, `clearToken()`, `getUser()`, `setUser()`, `getAuthHeaders()`, `isAuthenticated()`, `claimDeviceData()`

**Referenced in 3 files:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx`

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\__tests__\App.shouldShowLanding.test.tsx`

## Deliverables

- [ ] Rename constants from `hodeia_token`/`hodeia_user` to `sd_auth_token`/`sd_auth_user` in authStore.ts
- [ ] Add `migrateAuthKeys()` function to authStore.ts that:
  - Checks if old keys exist (`hodeia_token`, `hodeia_user`)
  - If old keys exist AND new keys do NOT exist → copy old to new, delete old
  - If both exist → delete old (new takes precedence)
  - If old keys do not exist → do nothing (already migrated or fresh user)
  - Returns void (fire-and-forget)
- [ ] Call `migrateAuthKeys()` at the top level of authStore.ts (runs on module init)
- [ ] Export `migrateAuthKeys()` for testability
- [ ] Update all hardcoded key strings in test files:
  - `authStore.test.ts`: Update `TOKEN_KEY` and `USER_KEY` constants
  - `App.shouldShowLanding.test.tsx`: Update `mockAuthToken()` helper
- [ ] Add migration tests in `authStore.test.ts` covering all 4 scenarios:
  - Old only → copy and delete
  - New only → no action
  - Both exist → delete old, keep new
  - Neither exist → no action
- [ ] Add test that verifies migration preserves an existing session (token + user data)
- [ ] Add test that verifies migration is idempotent (safe to run multiple times)

## Test Requirements

- [ ] **TDD: Write tests first**, then implementation
- [ ] All existing tests pass (no regressions)
- [ ] Add 6 new migration tests:
  1. `test_migrateAuthKeys_copies_old_to_new_when_only_old_exists`
  2. `test_migrateAuthKeys_preserves_both_token_and_user_data`
  3. `test_migrateAuthKeys_does_nothing_when_only_new_exists`
  4. `test_migrateAuthKeys_deletes_old_when_both_exist`
  5. `test_migrateAuthKeys_does_nothing_when_neither_exist`
  6. `test_migrateAuthKeys_is_idempotent`
- [ ] Edge cases tested:
  - Migration with token but no user data
  - Migration with user data but no token
  - Migration with malformed JSON in user data (should still migrate token)
- [ ] Smoke test passes: `cd browser && npx vitest run src/primitives/auth/__tests__/authStore.test.ts`
- [ ] Full test suite passes: `cd browser && npx vitest run`

## Constraints

- **TDD:** Write tests first, then implementation
- **No file over 500 lines:** authStore.ts is currently 137 lines, will remain under 200
- **No stubs:** Migration function must be fully implemented
- **No hardcoded colors:** N/A (no UI changes)
- **Migration logic:** If old keys exist AND new keys do NOT exist → copy old to new, delete old. If both exist → delete old (cleanup).
- **Idempotency:** Migration must be safe to run multiple times (no data loss)

## Acceptance Criteria

- [ ] Constants renamed to `sd_auth_token` and `sd_auth_user` in authStore.ts
- [ ] `migrateAuthKeys()` function implemented and exported
- [ ] Migration runs on authStore module init (top-level call)
- [ ] Migration handles all 4 scenarios correctly:
  - Old only → copy and delete
  - New only → no action
  - Both exist → delete old, keep new
  - Neither exist → no action
- [ ] Migration is idempotent (safe to run multiple times)
- [ ] Existing sessions survive the rename (no forced logout)
- [ ] All 3 files updated with new key names
- [ ] All tests pass (existing + 6 new migration tests)
- [ ] No stubs shipped

## Smoke Test Commands

```bash
# Run auth tests only
cd browser && npx vitest run src/primitives/auth/__tests__/authStore.test.ts

# Run full frontend test suite (check for regressions)
cd browser && npx vitest run
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-AUTH-B-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Model Assignment

sonnet

## Priority

P0
