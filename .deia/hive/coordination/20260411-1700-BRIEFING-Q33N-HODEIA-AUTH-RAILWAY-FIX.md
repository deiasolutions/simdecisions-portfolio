# BRIEFING — Q33N HODEIA-AUTH RAILWAY FIX

**Date:** 2026-04-11 17:00
**From:** Q33NR (Opus 4.6)
**To:** Q33N (Sonnet 4.5)
**Repo:** `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions` (canonical)
**Task file:** `.deia/hive/tasks/20260411-1700-TASK-Q33N-HODEIA-AUTH-RAILWAY-FIX.md`
**Response target:** `.deia/hive/responses/20260411-RESPONSE-HODEIA-AUTH-RAILWAY-FIX.md`

---

## Context

Production cutover from shiftcenter → simdecisions completed earlier today on both Railway `hivenode` and Vercel (`shiftcenter` project). `hivenode` is green. But the `beneficial-cooperation` Railway service (hodeia-auth) was skipped because its Dockerfile is broken. OAuth / JWT / dev-login / token refresh are currently down in production.

**What's down:**
- `https://beneficial-cooperation-production.up.railway.app/health` — 502 / no-response
- Vercel routes that proxy to it: `/auth/*`, `/token/*`, `/dev-login/*`

**Why it's broken (diagnosed earlier, DO NOT re-diagnose):**
1. `packages/hodeia-auth/Dockerfile` only `COPY`s `packages/hodeia-auth/` — it does NOT copy `packages/core/`.
2. But `packages/hodeia-auth/src/hodeia_auth/main.py:12` has `from hivenode.relay.routes import router as relay_router` — a hard import. This will fail at import time inside the container.
3. Same `$PORT` bug we just hit on hivenode: Dockerfile uses exec-form `CMD ["uvicorn", ..., "8430"]` which cannot substitute Railway's injected `$PORT`. Even if imports were fixed, Railway's proxy would route to `$PORT` (usually 8080) while uvicorn listens on 8430 → 502.
4. `uv pip install --system -e .` only installs hodeia-auth's own deps, not the core workspace package.

## What Worked for hivenode (reference pattern)

See `/Dockerfile` at simdecisions repo root (hivenode). Key moves:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml .
COPY packages/ packages/
COPY tests/ tests/
RUN uv sync --all-packages
ENV PYTHONPATH=/app/packages/core/src:/app/packages/engine/src:/app/packages/tools/src
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
EXPOSE 8420
# Shell-form CMD so ${PORT} gets substituted at runtime from Railway's injected env var.
CMD uvicorn hivenode.main:app --host 0.0.0.0 --port ${PORT:-8420} --log-level info
```

Three gotchas that matter:
1. **`uv sync --all-packages`** (not bare `uv sync`) because workspace root has no `[project.dependencies]`.
2. **`ENV PATH="/app/.venv/bin:$PATH"`** so `uvicorn` is findable.
3. **Shell-form CMD with `${PORT:-NNNN}`** — exec-form does NOT substitute, Railway sets `$PORT` dynamically.

## Railway Service Info

- **Project:** `peaceful-integrity`
- **Service name:** `beneficial-cooperation`
- **Public URL:** `https://beneficial-cooperation-production.up.railway.app`
- **CLI prefix on Windows/Git Bash:** `MSYS_NO_PATHCONV=1` is MANDATORY.
- **Link command:** `MSYS_NO_PATHCONV=1 railway link -s beneficial-cooperation -p peaceful-integrity -e production`
- **Deploy command:** `MSYS_NO_PATHCONV=1 railway up --detach`
- **List deploys:** `MSYS_NO_PATHCONV=1 railway deployment list`
- **Runtime logs:** `MSYS_NO_PATHCONV=1 railway logs --deployment <ID>`

## Environment Variables Already Set

Don't touch these. They're fine as-is:
- `DATABASE_URL` (Railway Postgres reference)
- `HIVENODE_MODE=cloud` (if applicable to hodeia-auth — it may not read it)
- Any JWT keys / OAuth provider creds already provisioned

## Constraints

- **DO NOT touch hivenode.** It's healthy. Stay in `packages/hodeia-auth/` and the Dockerfile you're fixing.
- **DO NOT rewrite audit.py.** Its `try/except ImportError` is already correct — it degrades gracefully.
- **DO NOT change `main.py:12` to a try/except.** The fix is to make the import actually work by including `packages/core/` in the image, not to hide the breakage.
- **DO NOT deploy until you've sanity-checked the Dockerfile builds locally** (or at least has obvious consistency with the hivenode pattern).
- **You may need a dedicated Dockerfile per service.** Hodeia-auth's Dockerfile can live at `packages/hodeia-auth/Dockerfile`, but must be referenced correctly by Railway. Check `railway.toml` or the service settings — if Railway uses the root Dockerfile for this service, we need a different strategy (likely: a new `Dockerfile.hodeia-auth` at repo root, or a service-specific `dockerfilePath` override).

## Success Criteria

1. `curl -s https://beneficial-cooperation-production.up.railway.app/health` returns 200 with a non-error JSON body.
2. Railway deployment shows SUCCESS status.
3. Runtime logs show `Application startup complete.` and `Uvicorn running on http://0.0.0.0:NNNN` where `NNNN` matches Railway's `$PORT`.
4. Vercel proxy still routes: `curl -s https://shiftcenter.com/auth/ping` (or similar) gives a hodeia-auth response, not a 502.
5. Response file written with full summary + commit hashes + deploy ID.

## Out of Scope

- Don't fix security issues noted in the earlier audit (rate limiting, password reset flow, TOTP, etc.).
- Don't touch the database migration logic — `_migrate_schema()` already handles PostgreSQL column additions on startup.
- Don't add new features. Just get it booted.
