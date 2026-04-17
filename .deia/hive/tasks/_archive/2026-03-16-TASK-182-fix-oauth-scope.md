# TASK-182: Fix GitHub OAuth scope — remove repo access

## Objective

Change the GitHub OAuth authorization scope from `user:email,repo` to `read:user,user:email` to match privacy commitments ("read-only access to public profile").

## Context

The LoginPage says "We never access your repos, code, or private data." Currently, the OAuth implementation requests `user:email,repo` scope which grants full read/write access to all user repositories. This is a privacy/security mismatch.

The application only needs:
- `read:user` — access to public profile (name, avatar, login)
- `user:email` — access to email addresses

Both are used in `get_user_profile()` which calls:
- `GET /user` — gets profile (name, login, etc.)
- `GET /user/emails` — gets email

Neither endpoint requires repo scope.

**Impact:**
- Existing users who already authorized with `repo` scope won't be affected — their GitHub OAuth grant persists
- New users will only be asked for the reduced scope
- This makes the authorization dialog match the privacy promise

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\routes\oauth.py` (lines 171, 279)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\ra96it\services\github.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\ra96it\test_oauth.py`

## Deliverables

- [ ] Change scope at line 171 from `"user:email,repo"` to `"read:user,user:email"`
- [ ] Change scope at line 279 from `"user:email,repo"` to `"read:user,user:email"`
- [ ] All ra96it tests pass with no regressions
- [ ] No tests assert hardcoded scope values (check test_oauth.py)

## Test Requirements

- [ ] Run: `cd hivenode && python -m pytest tests/ra96it/test_oauth.py -v`
- [ ] Run: `cd hivenode && python -m pytest tests/ra96it/ -v` (full suite)
- [ ] All existing tests continue to pass
- [ ] No new test failures introduced

## Constraints

- Change only the two scope strings
- Do not modify any other OAuth behavior
- No file will exceed 500 lines (both files stay well under)
- No stubs or placeholders

## Smoke Test Command

```bash
cd hivenode && python -m pytest tests/ra96it/ -v
```

Expected result: All tests pass (same count as before, no new failures).

## Notes

The test file `test_oauth.py` does NOT assert on scope values, so no test updates are needed. The only changes are the two scope strings in oauth.py. This is truly a one-line-times-two fix.

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-182-RESPONSE.md`

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
