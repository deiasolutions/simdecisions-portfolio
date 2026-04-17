# BRIEFING: AUTH-B localStorage Key Migration

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-25
**Model:** sonnet
**Priority:** P0

---

## Objective

Rename localStorage keys from `ra96it_token`/`ra96it_user` to `sd_auth_token`/`sd_auth_user` to match existing `sd_user_settings` convention. Implement a backwards-compatible migration that runs on authStore init.

---

## Context

The current auth localStorage keys use the `ra96it_` prefix, which is inconsistent with the existing `sd_user_settings` key convention used elsewhere in the app. We need to:

1. Rename the key constants
2. Add a migration function that runs on init
3. Ensure existing sessions survive the rename (no forced logout)
4. Make the migration idempotent (safe to run multiple times)

The migration must handle 4 scenarios:
- Old keys exist, new keys do not → copy old to new, delete old
- New keys exist, old keys do not → do nothing
- Both exist → new keys take precedence, delete old
- Neither exist → do nothing

---

## Spec File

`.deia/hive/queue/_active/SPEC-AUTH-B-LOCALSTORAGE-MIGRATION.md`

---

## Files to Review

Before writing task files, read these files to understand the current implementation:

- `browser/src/primitives/auth/authStore.ts` — current authStore implementation with ra96it keys
- `browser/src/primitives/auth/__tests__/authStore.test.ts` — existing tests

---

## Deliverables Required

1. **Key constants renamed** from `ra96it_token`/`ra96it_user` to `sd_auth_token`/`sd_auth_user`
2. **Migration function** that:
   - Runs on authStore init
   - Copies old keys to new if old exist and new do not
   - Deletes old keys after copying
   - Is idempotent (safe to run multiple times)
3. **All references updated** throughout the codebase
4. **Tests** covering all 4 migration paths:
   - Old only (copy and delete)
   - New only (no action)
   - Both exist (delete old, keep new)
   - Neither exist (no action)

---

## Constraints

- **TDD:** Write tests first, then implementation
- **No file over 500 lines**
- **No stubs**
- **Migration logic:** if old keys exist AND new keys do NOT exist, copy old to new, delete old
- **Model:** sonnet (specified in spec)

---

## Acceptance Criteria (from spec)

- [ ] New key names used everywhere in codebase
- [ ] Migration handles: old only, new only, both exist, neither exist
- [ ] Migration is idempotent (safe to run multiple times)
- [ ] Existing sessions survive the rename (no forced logout)
- [ ] Tests cover all 4 migration paths
- [ ] No stubs

---

## Smoke Test

```bash
cd browser && npx vitest run src/primitives/auth/__tests__/authStore.test.ts
cd browser && npx vitest run
```

---

## Your Task

1. Read the files listed above
2. Write task file(s) to `.deia/hive/tasks/`
3. Return to Q33NR for review
4. **Do NOT dispatch bees yet** — wait for Q33NR approval

---

## Notes

- This is a straightforward migration task
- The main risk is forgetting to update a reference somewhere
- The migration function should be simple and defensive
- Test the migration thoroughly — it only runs once per browser/user
