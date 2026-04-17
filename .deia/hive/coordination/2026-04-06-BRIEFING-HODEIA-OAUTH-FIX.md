# Briefing: Fix GitHub OAuth ProgrammingError on Railway

## Objective

GitHub OAuth login at shiftcenter.com/?egg=workdesk returns `?error=github_error&detail=ProgrammingError`. The Railway Postgres `users` table is missing columns that `hodeia_auth/models.py` expects. Fix it.

## Context

- hodeia-auth runs on Railway service `beneficial-cooperation`
- `hodeia_auth/db.py` has `_migrate_schema()` that auto-adds missing columns on startup
- A deploy was triggered last session (`MSYS_NO_PATHCONV=1 railway up`) but we don't know if it completed
- The fix is: ensure hodeia-auth is deployed with the latest code so `_migrate_schema()` runs on startup

## What Q33N Must Do

1. Check Railway logs to see if the last deploy completed: `MSYS_NO_PATHCONV=1 railway logs -n 50`
2. Look for "Migration:" log lines confirming schema updates ran
3. If deploy didn't land or migration didn't run, redeploy:
   - Verify all imports in `hodeia_auth/main.py` reference modules that exist on disk
   - `MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production`
   - `MSYS_NO_PATHCONV=1 railway up`
   - Watch logs for migration confirmation
4. After deploy confirms, test the OAuth endpoint by checking Railway logs for any ProgrammingError on the next login attempt

## Files to Read

- `hodeia_auth/db.py` — `_migrate_schema()` function
- `hodeia_auth/models.py` — User model with expected columns
- `hodeia_auth/main.py` — startup lifespan that calls `create_tables()`

## Constraints

- ALWAYS prefix Railway CLI commands with `MSYS_NO_PATHCONV=1` (Windows/Git Bash)
- Do NOT drop or recreate tables. The migration is additive (ALTER TABLE ADD COLUMN).
- Do NOT modify `_migrate_schema()` unless it's actually broken. It works — the issue is just that the service needs redeploying.
- Railway project: `peaceful-integrity`, environment: `production`

## Model Assignment

sonnet
