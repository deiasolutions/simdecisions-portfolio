# TASK — Q33N HODEIA-AUTH RAILWAY RETRY (v2)

**ID:** 20260411-1830-TASK-Q33N-HODEIA-AUTH-RETRY
**Assignee:** Q33N (Sonnet 4.5, role=queen)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions`
**Briefing:** `.deia/hive/coordination/20260411-1830-BRIEFING-Q33N-HODEIA-AUTH-RETRY.md`
**Response target:** `.deia/hive/responses/20260411-1830-RESPONSE-HODEIA-AUTH-RETRY.md`
**Supersedes:** previous attempt which failed silently — read briefing first

---

## Read First (MANDATORY)

1. `.deia/BOOT.md` — hard rules + response template
2. `.deia/HIVE.md` — your chain of command
3. `.deia/hive/coordination/20260411-1830-BRIEFING-Q33N-HODEIA-AUTH-RETRY.md` — **ENTIRE briefing, especially "What Went Wrong Last Time" and "Mandatory Safety Rules"**
4. `.deia/hive/responses/20260411-RESPONSE-HODEIA-AUTH-RAILWAY-FIX.md` — prior Q33N's self-reported "success" (was actually a no-op on the target service)

---

## Step 1 — Establish Ground Truth

Before changing anything, capture the current state:

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/simdecisions

# Explicit link
MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production

# Verify link is correct
MSYS_NO_PATHCONV=1 railway status 2>&1 | head -10
# MUST show "Service: beneficial-cooperation"  — if not, abort and re-link

# Capture current deploys on this service
MSYS_NO_PATHCONV=1 railway deployment list 2>&1 | head -10 > /tmp/bc-before.txt
cat /tmp/bc-before.txt

# Capture current env vars
MSYS_NO_PATHCONV=1 railway variables 2>&1 > /tmp/bc-vars-before.txt
grep -iE "app_module|nixpacks|start_command|dockerfile|port" /tmp/bc-vars-before.txt
```

Write these findings into a scratch file or your mental model:
- Latest deploy ID + date on `beneficial-cooperation`
- Which builder type (Nixpacks vs Dockerfile) the env vars imply
- Any other unexpected env vars

## Step 2 — Read Relevant Files

```bash
cat railway.toml
cat packages/hodeia-auth/Dockerfile
cat packages/hodeia-auth/pyproject.toml
head -30 packages/hodeia-auth/src/hodeia_auth/main.py
# Check if there's a packages/hodeia-auth/railway.toml
find packages/hodeia-auth -maxdepth 2 -name "railway.toml" -o -name "nixpacks.toml"
```

Confirm Q33N-1's existing `packages/hodeia-auth/Dockerfile` (from commit `1c695e2`) is correct or needs fixing.

## Step 3 — Decide Path A or Path B

See briefing for details.

- **Path A (Dockerfile):** Preferred. Matches hivenode.
- **Path B (Nixpacks):** Fallback if Path A's config override is too awkward.

Document your choice and rationale in the response file.

## Step 4 — Execute the Fix

### If Path A — Dockerfile build

```bash
# 1. Clear stale Nixpacks env vars (use --remove if CLI supports it)
MSYS_NO_PATHCONV=1 railway variables --help 2>&1 | head -20   # check flags
# Try:
MSYS_NO_PATHCONV=1 railway variables --remove APP_MODULE
MSYS_NO_PATHCONV=1 railway variables --remove NIXPACKS_CONFIG_FILE
MSYS_NO_PATHCONV=1 railway variables --remove NIXPACKS_START_CMD
MSYS_NO_PATHCONV=1 railway variables --remove RAILWAY_START_COMMAND
# If --remove doesn't exist, try setting to empty:
# MSYS_NO_PATHCONV=1 railway variables --set APP_MODULE=""
# etc.

# 2. Update railway.toml with per-service override
# Edit root railway.toml to add a [environments.production.services."beneficial-cooperation".build] section
# pointing at packages/hodeia-auth/Dockerfile. Syntax reference:
# https://docs.railway.com/reference/config-as-code

# 3. Verify Dockerfile correctness (read it; check: COPY packages/core, uv sync --all-packages,
#    PATH includes venv, shell-form CMD with ${PORT:-8430})
cat packages/hodeia-auth/Dockerfile

# 4. Commit any changes
git add railway.toml packages/hodeia-auth/Dockerfile
git commit -m "fix(hodeia-auth): switch beneficial-cooperation to Dockerfile build"
```

### If Path B — Nixpacks with simdecisions paths

```bash
# 1. Create packages/hodeia-auth/nixpacks.toml with correct install/start
# 2. Update env vars to point at new paths
MSYS_NO_PATHCONV=1 railway variables --set NIXPACKS_CONFIG_FILE=packages/hodeia-auth/nixpacks.toml
# etc.
# 3. Commit
git add packages/hodeia-auth/nixpacks.toml
git commit -m "fix(hodeia-auth): add simdecisions-layout nixpacks config"
```

## Step 5 — Deploy With Verification

```bash
# Re-verify link
MSYS_NO_PATHCONV=1 railway status 2>&1 | grep -i "Service:"
# If it doesn't say "beneficial-cooperation", STOP and re-link.

# Deploy
MSYS_NO_PATHCONV=1 railway up --detach 2>&1 | tee /tmp/bc-up.log

# Extract the deploy ID from the build URL in the output
# Example: https://railway.com/...service/xxx?id=<DEPLOY_ID>&
# Write it down. Call it $NEW_DEPLOY_ID.
```

## Step 6 — Verify Landing (CRITICAL)

```bash
# Wait for build + healthcheck window (about 2-3 min)
sleep 180

# Confirm $NEW_DEPLOY_ID is at top of beneficial-cooperation deploy list
MSYS_NO_PATHCONV=1 railway deployment list 2>&1 | head -5
# The top row MUST match $NEW_DEPLOY_ID. If it doesn't, you deployed to the wrong service.

# Confirm status SUCCESS
# Get runtime logs
MSYS_NO_PATHCONV=1 railway logs --deployment $NEW_DEPLOY_ID 2>&1 > /tmp/bc-runtime.log
head -40 /tmp/bc-runtime.log
grep -E "Uvicorn running|Application startup complete|ERROR|Traceback" /tmp/bc-runtime.log

# Health check
curl -s -o /dev/null -w "bc /health: %{http_code}\n" https://beneficial-cooperation-production.up.railway.app/health
curl -s https://beneficial-cooperation-production.up.railway.app/health

# Vercel proxy check
curl -s -o /dev/null -w "vercel /auth: %{http_code}\n" https://shiftcenter.com/auth/
```

**Only declare success if ALL of these are true:**
- `$NEW_DEPLOY_ID` is at the top of the `beneficial-cooperation` deploy list
- That deploy has status SUCCESS
- Runtime logs show uvicorn running without errors
- /health returns 200 (non-stale — by deploy ID check)
- Vercel proxies are not 502

## Step 7 — Write Response File

Write `.deia/hive/responses/20260411-1830-RESPONSE-HODEIA-AUTH-RETRY.md` with:

- Status: COMPLETE or BLOCKED
- Path chosen (A or B) with rationale
- All commit hashes
- `$NEW_DEPLOY_ID` (verified on beneficial-cooperation)
- Before/after state of the service (deploy list, env vars)
- Log excerpts proving uvicorn is actually running on simdecisions code
- Vercel proxy results
- Any snags you hit and how you worked around them

## Done Criteria

- [ ] Ground truth captured before any mutation
- [ ] Decision documented (Path A or B)
- [ ] Stale env vars cleared or updated
- [ ] Build config corrected
- [ ] `railway status` verified `beneficial-cooperation` before every `railway up`
- [ ] `railway up` landed a new deploy ID on `beneficial-cooperation` (verified against deploy list)
- [ ] Deploy status SUCCESS
- [ ] `/health` returns 200 from the NEW deploy
- [ ] Vercel proxy `/auth/*` not 502
- [ ] Response file complete with verified evidence

## Out of Scope

- Hivenode (don't touch)
- Security hardening of hodeia-auth
- Database schema changes
- Dispatching bees
- Rewriting history

## Escalation

If you hit max 3 deploy attempts without success, or if Railway CLI lacks a capability you need (e.g., can't remove env vars, can't override builder type), stop and write a BLOCKED response file with:
- What you tried
- What failed
- What you think the next step should be (e.g., "user must click X in Railway dashboard")
