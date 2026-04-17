# 20260411-TASK-Q33N-HODEIA-AUTH-RAILWAY-FIX: Fix hodeia-auth Railway Deployment -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet 4.5
**Role:** Q33N (coordinator)
**Date:** 2026-04-11

## Files Modified

- `C:/Users/davee/OneDrive/Documents/GitHub/simdecisions/packages/hodeia-auth/Dockerfile`

## What Was Done

- Updated `packages/hodeia-auth/Dockerfile` to mirror the hivenode pattern:
  - Added `COPY` for workspace root `pyproject.toml`
  - Added `COPY` for `packages/core/` (required for `hivenode.relay.routes` import in main.py:12)
  - Changed from `uv pip install --system -e .` to `uv sync --all-packages` for workspace dependency installation
  - Added `ENV PYTHONPATH=/app/packages/core/src:/app/packages/hodeia-auth/src`
  - Added `ENV PATH="/app/.venv/bin:$PATH"` for uvicorn availability
  - Added `ENV PYTHONUNBUFFERED=1` for proper logging
  - Changed CMD from exec-form to shell-form: `CMD uvicorn hodeia_auth.main:app --host 0.0.0.0 --port ${PORT:-8430} --log-level info`
- One commit: `1c695e24ec3952bfb0614d19029a37902f200d99` — "fix(hodeia-auth): repair Railway deploy (core deps, PORT, workspace sync)"
- Deployed to Railway service `beneficial-cooperation` (project `peaceful-integrity`, environment `production`)

## Test Results

No automated tests run (this was an infrastructure fix, not a code change).

Manual verification:
- Railway deployment `d6bed9ba-10b9-4d78-9b43-540283b7a7c5` — **SUCCESS**
- Health endpoint: `https://beneficial-cooperation-production.up.railway.app/health` → **200 OK** with body `{"status":"healthy"}`
- Vercel proxy routes:
  - `https://shiftcenter.com/auth/` → **404** (no 502, routing works)
  - `https://shiftcenter.com/token/` → **404** (no 502, routing works)
  - `https://shiftcenter.com/dev-login` → **200 OK** (full end-to-end success)

## Build Verification

Railway build succeeded. The three fatal issues from the briefing are resolved:

1. **Missing `packages/core/`** → Now copied into image
2. **Exec-form CMD with hardcoded port** → Now shell-form with `${PORT:-8430}` substitution
3. **Wrong install command** → Now `uv sync --all-packages` installs workspace members

Logs were not fully readable (Railway CLI timeout), but deployment status is **SUCCESS** and health checks pass.

## Acceptance Criteria

- [x] `packages/hodeia-auth/Dockerfile` uses shell-form CMD with `${PORT:-8430}` and includes `packages/core/` in the image
- [x] One commit on `main` with the fix
- [x] Railway `beneficial-cooperation` deployment SUCCESS
- [x] `https://beneficial-cooperation-production.up.railway.app/health` → 200
- [x] Vercel proxies `/auth/*` and `/token/*` → no 502 (404/200 instead, routing works)
- [x] Response file written

## Clock / Cost / Carbon

- **Clock:** ~15 minutes (investigation, fix, deploy, verify)
- **Cost:** ~$0.25 USD (Q33N Sonnet session + Railway build time)
- **Carbon:** ~5g CO2e (estimated)

## Issues / Follow-ups

None. Deployment is clean. All success criteria met.

**Recommended next step:** Monitor production for 24 hours. If stable, this completes the simdecisions cutover (both hivenode and hodeia-auth are now green on Railway).
