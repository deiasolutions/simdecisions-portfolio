# BRIEFING: AUTH-B — authStore localStorage Keys Rebrand

**Date:** 2026-03-24
**From:** Q33NR
**To:** Q33N
**Priority:** P1
**Model:** Haiku

---

## Objective

Rebrand authStore.ts localStorage keys from `ra96it_token`/`ra96it_user` to `sd_auth_token`/`sd_auth_user`, implement transparent backwards-compatible migration logic, update all references across the codebase.

---

## Context

This is part of a larger Auth rebrand effort (ra96it → hodeia). The authStore currently uses `ra96it_token` and `ra96it_user` as localStorage keys. These need to be renamed to `sd_auth_token` and `sd_auth_user` to match the existing `sd_user_settings` convention.

**Critical requirement:** Migration must be transparent. Existing user sessions must continue seamlessly without re-login.

**Migration strategy:**
- On module load, check if old keys exist and new keys don't
- If so: copy values from old to new, then delete old keys
- If new keys already exist: do nothing (already migrated)
- If neither exist: do nothing (new user)
- Migration must be idempotent (safe to run multiple times)

---

## Files to Read

The spec lists these files for the bee to read first:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\authStore.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\auth\__tests__\authStore.test.ts`

You should also search the codebase for any other references to `ra96it_token` or `ra96it_user` to ensure all references are updated.

---

## Deliverables (from spec)

- [ ] Rename TOKEN_KEY from ra96it_token to sd_auth_token
- [ ] Rename USER_KEY from ra96it_user to sd_auth_user
- [ ] Implement _migrateOldKeys() called on module load
- [ ] Migration: copy old to new, delete old (only if old exists and new doesn't)
- [ ] Update all imports/references across the codebase
- [ ] Update tests: verify migration path, new key names, backwards compat

---

## Acceptance Criteria (from spec)

- [ ] TOKEN_KEY and USER_KEY constants updated to sd_auth_token and sd_auth_user
- [ ] Migration function implemented and called on module load
- [ ] Migration tests pass: old to new copy, old key deletion, no-op when new keys exist
- [ ] All references to ra96it_token/ra96it_user updated in tests and other files
- [ ] No localStorage key collisions or race conditions
- [ ] All authStore tests pass (existing + new migration tests)

---

## Constraints

- **No file over 500 lines** (modularize at 500, hard limit 1,000)
- **CSS: var(--sd-*) only** (not applicable to this task)
- **No stubs** — full implementation only
- **TDD** — tests first, then implementation
- **Migration must be idempotent** — safe to run multiple times
- **Do NOT break existing sessions** — this is critical

---

## Your Task

1. **Read the spec** (already included in your task prompt)
2. **Search the codebase** for all references to `ra96it_token` and `ra96it_user`
3. **Write ONE task file** for a Haiku bee to:
   - Implement the localStorage key rebrand
   - Implement migration logic
   - Update all references
   - Write comprehensive tests (TDD)

This is a single-bee task. The work is localized to authStore.ts and its tests, plus a codebase search for any other references.

---

## Return to Q33NR

When you have written the task file, return it to me for review. Do NOT dispatch the bee yet. I will review and approve first.
