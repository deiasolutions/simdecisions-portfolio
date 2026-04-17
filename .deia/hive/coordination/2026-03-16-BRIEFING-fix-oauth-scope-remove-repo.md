# BRIEFING: Fix GitHub OAuth scope — remove repo access

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Priority:** P0.5
**Model Assignment:** Haiku

---

## Objective

Fix the GitHub OAuth authorization URL to request only the necessary scopes. Currently it requests `user:email,repo` which grants full read/write access to all user repositories. The login page explicitly tells users "We never access your repos, code, or private data." Change the scope to `read:user,user:email`.

---

## Context

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\oauth.py` line 171

Current code:
```python
"scope": "user:email,repo",
```

Should be:
```python
"scope": "read:user,user:email",
```

**Why this is safe:**
- `read:user` gives access to public profile (name, avatar, login)
- `user:email` gives access to email addresses
- That's all ra96it needs — the `get_user_profile()` call in `services/github.py` only hits `GET /user` and `GET /user/emails`

**Impact on existing users:**
- Existing users who already authorized with `repo` scope won't be affected — their existing GitHub OAuth grants persist
- New authorizations will only request the reduced scope
- Users who want to connect repos later can re-authorize with broader scope when that feature exists

---

## Task Breakdown

**Single TASK (haiku):**
1. Change the scope string in oauth.py line 171
2. Check if any tests assert the scope value — update if needed
3. Run all ra96it tests to verify no regressions

---

## Files Involved

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\oauth.py` (line 171)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\` (check for any scope assertions)

---

## Acceptance Criteria

- [ ] OAuth scope changed from `user:email,repo` to `read:user,user:email`
- [ ] No regressions in ra96it tests
- [ ] Privacy notice text in LoginPage still accurate (it already says "read-only access to public profile")

---

## Constraints

- Max 500 lines per file
- No stubs
- Do not change any other OAuth behavior
- TDD applies if tests need updating

---

## Smoke Test

```bash
cd hivenode && python -m pytest tests/ra96it/ -v
```

Expected: No new test failures.

---

## Notes for Q33N

This is a one-line fix. The only complexity is checking if any tests hardcode the scope value. If they do, update them. Otherwise, this is truly a one-line change.

The bee should verify that the LoginPage privacy text is still accurate after this change. From the context, it already says "read-only access to public profile," which is accurate for `read:user,user:email`.
