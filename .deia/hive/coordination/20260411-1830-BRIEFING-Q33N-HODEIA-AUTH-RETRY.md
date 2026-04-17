# BRIEFING — Q33N HODEIA-AUTH RAILWAY RETRY (v2)

**Date:** 2026-04-11 18:30
**From:** Q33NR (Opus 4.6)
**To:** Q33N (Sonnet 4.5)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` (canonical)
**Task file:** `.deia/hive/tasks/20260411-1830-TASK-Q33N-HODEIA-AUTH-RETRY.md`
**Response target:** `.deia/hive/responses/20260411-1830-RESPONSE-HODEIA-AUTH-RETRY.md`
**Supersedes:** `20260411-1700-TASK-Q33N-HODEIA-AUTH-RAILWAY-FIX.md` (failed silently — see below)

---

## What Went Wrong Last Time

An earlier Q33N (commit `1c695e2`) was dispatched to fix hodeia-auth. It edited `packages/hodeia-auth/Dockerfile` correctly, committed, ran `railway up`, and reported SUCCESS. But **none of that deployment ever reached the `beneficial-cooperation` Railway service.** Two Q33Ns were running in parallel in the same CWD and both called `railway link`. The second Q33N's link clobbered the first one's, so both `railway up` commands deployed to `hivenode` instead of `beneficial-cooperation`.

Worse: the earlier Q33N verified `/health` returned 200 and declared victory — but that was the **stale deployment from 2026-04-09** still running old shiftcenter-era code. It never checked the deployment ID to confirm its own `railway up` actually landed on the target service. **Do not repeat this mistake. Verify by deployment ID, not by health status.**

## Actual Current State

| Service | Current deploy | Source |
|---|---|---|
| hivenode | `d6bed9ba` SUCCESS (2026-04-11 17:58) | simdecisions, healthy |
| beneficial-cooperation | `4faefc29` SUCCESS (**2026-04-09 18:11**) | **old shiftcenter code**, still running |

`beneficial-cooperation` has NOT been rebuilt since before the simdecisions cutover. The `/health` 200 it returns is the old shiftcenter `hodeia_auth` code still running from two days ago. That code is functional but it is NOT the simdecisions canonical code and it is running on outdated everything.

## Additional Complication: Service Uses Nixpacks, Not Dockerfile

When I inspected `railway variables` on `beneficial-cooperation`, I found it's configured with the following stale Nixpacks env vars (left over from shiftcenter layout):

```
APP_MODULE              = hodeia_auth.main:app
NIXPACKS_CONFIG_FILE    = hodeia_auth/nixpacks.toml
NIXPACKS_START_CMD      = uvicorn hodeia_auth.main:app --host 0.0.0.0 --port 8420
RAILWAY_START_COMMAND   = uvicorn hodeia_auth.main:app --host 0.0.0.0 --port 8420
```

Meaning:
1. The service builds with **Nixpacks**, not Dockerfile. The previous Q33N's Dockerfile edits were never going to be picked up even if the deploy had landed on the right service.
2. The paths reference `hodeia_auth/` at repo root — that path exists in shiftcenter but **NOT in simdecisions** (the package is at `packages/hodeia-auth/`).
3. Any Nixpacks-based rebuild from simdecisions main will fail because `hodeia_auth/nixpacks.toml` doesn't exist.

So to actually get simdecisions code running on `beneficial-cooperation`, the Railway service config must change. That is your core task.

## The Fix — Two Viable Paths

You must choose ONE. Both are acceptable. Pick the one you can execute most cleanly.

### Path A (preferred): Switch to Dockerfile build

1. **Clear the stale Nixpacks env vars on beneficial-cooperation:**
   - `APP_MODULE`, `NIXPACKS_CONFIG_FILE`, `NIXPACKS_START_CMD`, `RAILWAY_START_COMMAND`
   - Use `railway variables --remove <name>` or `railway variables --set <name>=""` depending on CLI support.
2. **Force Dockerfile build.** Options:
   - (a) A service-scoped `railway.toml` section. The root `railway.toml` currently forces Dockerfile for all services at path `Dockerfile`. That's the hivenode Dockerfile, which would NOT work for hodeia-auth. You need a PER-SERVICE override.
   - Railway supports `[environments.production.services.<service-name>]` sections in `railway.toml`. Test this syntax:
     ```toml
     [environments.production.services."beneficial-cooperation".build]
     builder = "DOCKERFILE"
     dockerfilePath = "packages/hodeia-auth/Dockerfile"
     ```
   - (b) Alternatively, set `RAILWAY_DOCKERFILE_PATH=packages/hodeia-auth/Dockerfile` as an env var on the service (if the CLI supports this) — verify this is a real Railway feature before relying on it.
3. **Verify the existing `packages/hodeia-auth/Dockerfile`** (commit `1c695e2` by the previous Q33N) is correct. Read it. Confirm it:
   - COPYs `packages/core/` so `hivenode.relay.routes` import works
   - Uses `uv sync --all-packages`
   - Sets `PATH="/app/.venv/bin:$PATH"` and `PYTHONPATH` including `packages/core/src` and `packages/hodeia-auth/src`
   - Uses **shell-form** CMD with `${PORT:-8430}`
   - If any of these are missing or wrong, fix them in a new commit.
4. **Deploy with explicit link verification:**
   ```bash
   MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production
   MSYS_NO_PATHCONV=1 railway status 2>&1 | grep -i "Service:"   # MUST show beneficial-cooperation
   MSYS_NO_PATHCONV=1 railway up --detach
   # Capture the build URL. Extract deployment ID from it.
   ```
5. **Verify by deployment ID, NOT by /health.** Run `railway deployment list` and confirm the NEW deploy ID is at the top of the beneficial-cooperation deployment list. Only THEN check `/health`.

### Path B (fallback): Keep Nixpacks, add a nixpacks.toml for simdecisions layout

1. Create `packages/hodeia-auth/nixpacks.toml` with install + start commands that work from simdecisions monorepo root (needs `packages/core/` on PYTHONPATH).
2. Update the service env vars:
   - `NIXPACKS_CONFIG_FILE=packages/hodeia-auth/nixpacks.toml`
   - `NIXPACKS_START_CMD=uvicorn hodeia_auth.main:app --host 0.0.0.0 --port ${PORT:-8430}`
   - `APP_MODULE=hodeia_auth.main:app` (or remove if unused)
   - `RAILWAY_START_COMMAND` — remove if possible, or update to shell-form with `${PORT}`
3. Deploy with explicit link verification (same as Path A step 4-5).

## Mandatory Safety Rules

1. **You are the ONLY Q33N running right now.** Do not dispatch any bees. Do not assume another process is mutating Railway state.
2. **Always verify the current `railway link` state before every `railway up`:**
   ```bash
   MSYS_NO_PATHCONV=1 railway status 2>&1 | grep -i "Service:"
   ```
   It must say `Service: beneficial-cooperation` or you abort.
3. **Never trust /health alone.** After deploy, run:
   ```bash
   MSYS_NO_PATHCONV=1 railway deployment list 2>&1 | head -5
   ```
   and confirm the NEW deploy ID (from your `railway up` output) is at the top with status SUCCESS. Only then check /health.
4. **Don't touch hivenode.** It's healthy and clean. Don't run any `railway up` commands while linked to hivenode. If you accidentally link to hivenode, re-link to beneficial-cooperation before any deploy action.
5. **Don't blindly retry on failure.** If a `railway up` fails, pull the build logs and runtime logs, diagnose root cause, then act. Max 3 deploy attempts — if you can't get it healthy in 3 tries, write up what you tried and escalate via the response file.

## Success Criteria

- [ ] `beneficial-cooperation` has a new SUCCESS deployment from 2026-04-11 with a deploy ID **you personally obtained from `railway up` output**
- [ ] That deploy ID appears in `railway deployment list` output for `beneficial-cooperation` (verified)
- [ ] `curl https://beneficial-cooperation-production.up.railway.app/health` returns 200 (but this is a secondary check)
- [ ] Runtime logs (via `railway logs --deployment <id>`) show uvicorn running on port matching Railway's `$PORT` (probably 8080, not 8420/8430)
- [ ] Vercel proxy routes still work: `curl https://shiftcenter.com/auth/` returns non-502 (any of 200/404/405 is OK)
- [ ] Stale Nixpacks env vars either cleared or updated to point at simdecisions paths (not shiftcenter paths)
- [ ] At most 1-2 new commits on main with clear messages
- [ ] Response file written with: commit hash(es), verified deploy ID, deployment list output, health check result, vercel proxy check, any path decision rationale

## Out of Scope

- Do NOT touch hivenode service or the root Dockerfile.
- Do NOT add new features to hodeia-auth (no rate limiting, password reset, etc.).
- Do NOT rewrite `audit.py` — it already has `try/except ImportError` for LedgerWriter.
- Do NOT "fix" `main.py:12`'s `from hivenode.relay.routes import router` by try/excepting it — the fix is to include `packages/core/` in the image so the import works.
- Do NOT squash commits or rewrite history.
- Do NOT dispatch bees.

## Tactical Notes

- `MSYS_NO_PATHCONV=1` is MANDATORY on Windows/Git Bash for every Railway CLI invocation.
- Railway CLI may take 30-90s per command. Be patient.
- `railway logs --deployment <id>` may hang or return partial logs — if so, capture what you can and continue. Don't block on logs.
- Railway's `$PORT` is dynamically assigned (usually 8080). Your CMD must use `${PORT:-8430}` shell substitution.
- The hodeia-auth port 8430 is ONLY the fallback for local dev. On Railway, `$PORT` wins.
