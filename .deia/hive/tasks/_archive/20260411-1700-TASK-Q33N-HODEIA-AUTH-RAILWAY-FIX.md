# TASK — Q33N HODEIA-AUTH RAILWAY FIX

**ID:** 20260411-1700-TASK-Q33N-HODEIA-AUTH-RAILWAY-FIX
**Assignee:** Q33N (Sonnet 4.5, role=queen)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions`
**Briefing:** `.deia/hive/coordination/20260411-1700-BRIEFING-Q33N-HODEIA-AUTH-RAILWAY-FIX.md`
**Response target:** `.deia/hive/responses/20260411-RESPONSE-HODEIA-AUTH-RAILWAY-FIX.md`

---

## Read First

1. `.deia/BOOT.md` — hard rules + response template
2. `.deia/HIVE.md` — your chain of command
3. `.deia/hive/coordination/20260411-1700-BRIEFING-Q33N-HODEIA-AUTH-RAILWAY-FIX.md` — full context

---

## What to Do

### Step 1 — Investigate current state

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/simdecisions
cat packages/hodeia-auth/Dockerfile
cat packages/hodeia-auth/pyproject.toml
cat railway.toml
# Check if there's a separate railway.toml for hodeia-auth
find . -maxdepth 3 -name "railway*.toml"
# Check what Railway service settings say
MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production
MSYS_NO_PATHCONV=1 railway variables 2>&1 | head -40
```

Also read these for context:
- `packages/hodeia-auth/src/hodeia_auth/main.py` (first 30 lines — understand imports)
- `/Dockerfile` (root — the hivenode fix pattern you're mirroring)
- `.deia/hive/responses/20260328-HODEIA-AUTH-REVIEW.md` (prior review, for awareness only — NOT for rework)

### Step 2 — Fix the Dockerfile

You have two viable approaches. Pick whichever is cleanest:

**Option A: Dedicated Dockerfile at `packages/hodeia-auth/Dockerfile`**
- COPY from repo root: `pyproject.toml`, `packages/hodeia-auth/`, `packages/core/` (at minimum)
- Use `uv sync --all-packages` from the workspace root
- Set `PYTHONPATH` + venv `PATH`
- Shell-form CMD: `CMD uvicorn hodeia_auth.main:app --host 0.0.0.0 --port ${PORT:-8430}`
- Update Railway service's build context / Dockerfile path if needed (`railway.toml` in this package dir, or service settings in UI).

**Option B: Separate `Dockerfile.hodeia-auth` at repo root**
- Mirrors the hivenode Dockerfile exactly, but with the hodeia-auth entry point.
- Requires the Railway service to point at this file via `dockerfilePath` in a dedicated `railway.toml` or service setting.

Either way, the resulting image MUST:
1. Contain `packages/core/` source (so the `from hivenode.relay.routes import router` works)
2. Have uvicorn on `PATH`
3. Use shell-form CMD with `${PORT:-8430}` so Railway's dynamic port is honored

### Step 3 — Commit

```bash
git add packages/hodeia-auth/Dockerfile [railway.toml or other config files you changed]
git commit -m "fix(hodeia-auth): repair Railway deploy (core deps, PORT, workspace sync)"
```

One commit only. No debug commits. No chained "fix the fix" commits — iterate locally until you're confident, then push once.

### Step 4 — Deploy

```bash
cd /c/Users/davee/OneDrive/Documents/GitHub/simdecisions
MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production
MSYS_NO_PATHCONV=1 railway up --detach
# Note the build URL and deployment ID from output
```

### Step 5 — Verify

Wait ~90s for build + healthcheck, then:

```bash
MSYS_NO_PATHCONV=1 railway deployment list 2>&1 | head -5
curl -s -o /dev/null -w "health: %{http_code}\n" https://beneficial-cooperation-production.up.railway.app/health
curl -s https://beneficial-cooperation-production.up.railway.app/health
# Grab logs to confirm startup complete
MSYS_NO_PATHCONV=1 railway logs --deployment <new-deploy-id> 2>&1 | head -30
```

Success: deployment SUCCESS, /health 200, logs show `Application startup complete.` and port matches Railway's `$PORT`.

If it fails: pull runtime logs, diagnose, iterate. Do NOT redeploy blindly — read the error first. Follow the same pattern that diagnosed the hivenode failures (the four root causes are documented in the briefing).

### Step 6 — End-to-end proxy check

```bash
curl -s -o /dev/null -w "vercel /auth: %{http_code}\n" https://shiftcenter.com/auth/
curl -s -o /dev/null -w "vercel /token: %{http_code}\n" https://shiftcenter.com/token/
```

These should not be 502 anymore. They may return 404 or 405 (depending on the actual routes) — that's fine. 502 is the only bad outcome here.

## Done Criteria

- [ ] `packages/hodeia-auth/Dockerfile` (or new equivalent) uses shell-form CMD with `${PORT:-8430}` and includes `packages/core/` in the image
- [ ] One commit on `main` with the fix
- [ ] Railway `beneficial-cooperation` deployment SUCCESS
- [ ] `https://beneficial-cooperation-production.up.railway.app/health` → 200
- [ ] Vercel proxies `/auth/*` and `/token/*` → no 502
- [ ] Response file written to `.deia/hive/responses/20260411-RESPONSE-HODEIA-AUTH-RAILWAY-FIX.md` with: commit hash(es), deploy ID, health status codes, any snags encountered

## Out of Scope

- No security feature additions
- No schema migrations (the existing `_migrate_schema()` runs on startup)
- No touching hivenode or any other service
- No debug prints added to main.py — if you need to diagnose, use Railway logs
