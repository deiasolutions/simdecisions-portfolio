# TASK-AUTH-B: authStore rebrand — ra96it localStorage keys → sd_auth_*

## Objective
Rebrand authStore.ts localStorage keys from `ra96it_token`/`ra96it_user` to `sd_auth_token`/`sd_auth_user`, implement backwards-compatible migration logic, and update all references across the codebase.

## Context
The authStore currently uses `ra96it_token` and `ra96it_user` as localStorage keys. These need to be renamed to `sd_auth_token` and `sd_auth_user` to match the existing `sd_user_settings` convention (generic, not brand-specific).

**Migration strategy (CRITICAL):**
- On first load, if old keys exist and new keys don't, copy values from old keys to new keys and delete old keys
- If new keys already exist, do nothing (already migrated)
- If neither exist, do nothing (new user)
- Migration must be transparent to users — no visible disruption, existing sessions continue seamlessly

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`

## Deliverables
- [ ] Rename `TOKEN_KEY` from `'ra96it_token'` to `'sd_auth_token'`
- [ ] Rename `USER_KEY` from `'ra96it_user'` to `'sd_auth_user'`
- [ ] Implement migration function: `_migrateOldKeys()` called on module load
- [ ] Migration logic: copy old → new, delete old (only if old exists and new doesn't)
- [ ] Update all imports/references across the codebase (check grep results)
- [ ] Update tests: verify migration path, new key names, backwards compat

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test case: old keys exist, new keys don't → migration happens (copy + delete)
- [ ] Test case: new keys already exist → no migration (old keys ignored)
- [ ] Test case: neither old nor new keys exist → no error (new user)
- [ ] Test case: both old and new keys exist → new keys win, old keys deleted
- [ ] Test case: getToken/setToken/clearToken/getUser/setUser work with new keys
- [ ] Test case: isAuthenticated() works with new keys
- [ ] All existing authStore tests pass with new key names

## Constraints
- No file over 500 lines (authStore.ts is 119 lines, will stay well under)
- CSS: `var(--sd-*)` only (not applicable, no UI in this file)
- No stubs
- Migration must be idempotent — safe to run multiple times
- Do NOT break existing sessions — migration is seamless

## Acceptance Criteria
1. [ ] `TOKEN_KEY` and `USER_KEY` constants updated to `'sd_auth_token'` and `'sd_auth_user'`
2. [ ] Migration function implemented and called on module load
3. [ ] Migration tests pass: old → new copy, old key deletion, no-op when new keys exist
4. [ ] All references to `ra96it_token`/`ra96it_user` updated in tests and other files
5. [ ] No localStorage key collisions or race conditions
6. [ ] All authStore tests pass (existing + new migration tests)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-B-RESPONSE.md`

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
