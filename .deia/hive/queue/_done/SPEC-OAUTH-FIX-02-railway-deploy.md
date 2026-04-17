## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-OAUTH-FIX-02: Deploy hodeia-auth to Railway

## Role Override
bee

## Priority
P0

## Model Assignment
haiku

## Depends On
SPEC-OAUTH-FIX-01

## Intent
Deploy hodeia-auth to Railway service `beneficial-cooperation` so _migrate_schema() runs on startup and adds missing Postgres columns. Then verify deploy succeeded via logs.

## Files to Read First
- `hodeia_auth/main.py` — confirm startup calls create_tables()
- `railway.toml` — confirm Dockerfile build config

## Acceptance Criteria
- [ ] Railway linked to correct service: `MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production`
- [ ] Deploy triggered: `MSYS_NO_PATHCONV=1 railway up`
- [ ] Logs checked for "Migration:" lines confirming schema update: `MSYS_NO_PATHCONV=1 railway logs -n 50`
- [ ] Write response file to `.deia/hive/responses/`

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- ALWAYS prefix Railway CLI commands with `MSYS_NO_PATHCONV=1`
- If `railway link` prompts interactively, report failure — do not hang
- Do NOT modify any source code
- Do NOT run git commands
- If deploy upload succeeds, wait 60 seconds then check logs
- Do NOT drop or recreate tables

## Smoke Test
`MSYS_NO_PATHCONV=1 railway logs -n 10` should show startup logs with migration lines.

## Triage History
- 2026-04-09T15:50:45.785480Z — requeued (empty output)
- 2026-04-12T18:52:40.089930Z — requeued (empty output)
