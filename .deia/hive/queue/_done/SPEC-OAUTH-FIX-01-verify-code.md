## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-OAUTH-FIX-01: Verify hodeia-auth deploy readiness

## Role Override
bee

## Priority
P0

## Model Assignment
haiku

## Depends On
(none)

## Intent
Verify that hodeia_auth code is deploy-ready: all imports resolve, _migrate_schema() covers all User model columns, and main.py startup calls create_tables().

## Files to Read First
- `hodeia_auth/main.py` — check all imports reference modules on disk
- `hodeia_auth/models.py` — list all User model columns
- `hodeia_auth/db.py` — verify _migrate_schema() adds every column from models.py
- `hodeia_auth/routes/oauth.py` — check github OAuth route for column references

## Acceptance Criteria
- [ ] All imports in main.py verified to exist on disk
- [ ] All User model columns listed
- [ ] _migrate_schema() covers every User model column with ALTER TABLE ADD COLUMN
- [ ] Any missing column coverage identified and reported
- [ ] Write response file to `.deia/hive/responses/`

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- Do NOT modify any code unless you find a gap in _migrate_schema() where a model column is missing from the migration
- If you DO find a gap, fix it in db.py
- Do NOT run Railway CLI commands
- Do NOT run git commands

## Smoke Test
Read hodeia_auth/models.py, extract column names. Read hodeia_auth/db.py _migrate_schema(), extract column names handled. Compare. Report any gaps.

## Triage History
- 2026-04-09T15:50:45.782481Z — requeued (empty output)
