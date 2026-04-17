# SPEC: Fix GitHub OAuth scope — remove repo access, request only user:email

## Priority
P0.5

## Model Assignment
haiku

## Objective
The GitHub OAuth authorization URL requests `scope=user:email,repo` which grants full read/write access to all the user's repositories. The login page explicitly tells users "We never access your repos, code, or private data." Fix the scope to only request what's needed: `read:user` (public profile) and `user:email` (email address). This is a one-line backend fix.

## Context for Q33NR

**File:** `ra96it/routes/oauth.py` line 171
```python
"scope": "user:email,repo",
```

Should be:
```python
"scope": "read:user,user:email",
```

`read:user` gives access to the public profile (name, avatar, login). `user:email` gives access to email addresses. That's all ra96it needs — the `get_user_profile()` call in `services/github.py` only hits `GET /user` and `GET /user/emails`.

**NOTE:** After changing this, existing users who already authorized with `repo` scope won't be affected — their existing GitHub OAuth grants persist. New authorizations will only request the reduced scope. Users who want to connect repos later can re-authorize with broader scope when that feature exists.

**Recommended task breakdown:**
- Single TASK (haiku): Change the scope string in oauth.py, update the test if there's a scope assertion, verify existing OAuth tests pass.

**Files involved:**
- `ra96it/routes/oauth.py` (line 171)
- `tests/ra96it/` (any test asserting scope value)

## Acceptance Criteria
- [ ] OAuth scope changed from `user:email,repo` to `read:user,user:email`
- [ ] No regressions in ra96it tests
- [ ] Privacy notice text in LoginPage still accurate (it already says "read-only access to public profile")

## Constraints
- Max 500 lines per file
- No stubs
- Do not change any other OAuth behavior

## Smoke Test
- [ ] cd hivenode && python -m pytest tests/ra96it/ -v
- [ ] No new test failures
