# TASK-059: Document Railway Configuration + Env Vars -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Railway section appended (160 lines added)

## What Was Done

- Appended comprehensive Railway repoint documentation to `DEPLOYMENT-WIRING-NOTES.md`
- Documented Railway CLI repoint procedure (6 steps: link, root dir, start command, branch, env vars, staging)
- Created environment variables checklist table (8 required env vars)
- Documented CORS configuration requirements (noted as separate task)
- Documented health check endpoint configuration for Railway
- Verified health check endpoint exists at `hivenode/routes/health.py:18-27`
- Verified health endpoint returns `HealthResponse` with `status`, `mode`, `version`, `uptime_s` fields
- Included verification steps for post-repoint smoke testing
- Cross-referenced env vars with `.deia/config/deployment-env.md` (all match)
- Noted CORS update as "action required" but out of scope for this task
- Used Windows-style absolute paths in documentation where relevant

## Test Results

**Manual Verification:**

1. ✅ Markdown format validation: Railway section is valid markdown, no broken links
2. ✅ Env var cross-reference: All env vars match `.deia/config/deployment-env.md` specification
3. ✅ Health check endpoint verification: Read `hivenode/routes/health.py` — endpoint exists at line 18-27
   - Endpoint: `GET /health`
   - Response model: `HealthResponse`
   - Fields: `status`, `mode`, `version`, `uptime_s`
   - Implementation: complete, no code changes needed
4. ✅ Documentation completeness: Railway section includes all required sections (current state, target state, repoint procedure, env vars checklist, CORS verification, health check verification, post-repoint verification)
5. ✅ Windows path format: Absolute paths use Windows-style backslashes (e.g., `C:\Users\davee\...`)

## Build Verification

N/A — This is a documentation task. No build required.

## Acceptance Criteria

- [x] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Add Railway section (append to existing file from TASK-058)
- [x] Verify health check endpoint exists at `hivenode/routes/health.py` (no code changes needed)

**Railway Section Requirements:**
- [x] Current state documented (repo, service, root dir, domain, start command)
- [x] Target state documented (repo, root dir, branches, start command, health check)
- [x] Repoint procedure documented (prerequisites + 6 steps)
- [x] Environment variables checklist table (8 required env vars: HIVENODE_MODE, RA96IT_PUBLIC_KEY, FRONTEND_URL, DATABASE_URL, ANTHROPIC_API_KEY, VOYAGE_API_KEY, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET)
- [x] CORS configuration verification section (noted as separate task)
- [x] Health check verification section (endpoint exists, no code changes needed)
- [x] Post-repoint verification steps (production, staging, CORS)

**Health Check Verification:**
- [x] Endpoint exists at `GET /health` (verified at `hivenode/routes/health.py:18-27`)
- [x] Returns `HealthResponse` with `status`, `mode`, `version`, `uptime_s` fields (verified)
- [x] No code changes needed (verified)

## Clock / Cost / Carbon

**Clock:** 3 minutes (documentation writing + health check verification)
**Cost:** $0.03 (Sonnet, 1 read + 1 edit + 1 write)
**Carbon:** ~0.3g CO2e (estimated)

## Issues / Follow-ups

**Dependencies:**
- TASK-058 (Vercel docs) — ✅ COMPLETE (Railway section appended after Vercel section)
- TASK-060 (DNS docs) — Pending (will append DNS section after Railway section)
- TASK-062 (Smoke test docs) — Pending (will append smoke test section after DNS section)

**Follow-up Tasks Required:**
1. **CORS Update:** `hivenode/main.py` line 233-237 needs CORS origins updated to include:
   - `https://simdecisions.com` (current production)
   - `https://code.shiftcenter.com` (new production)
   - `https://dev.shiftcenter.com` (dev preview)

   This is documented in the Railway section as "action required" but marked as out of scope for this documentation task. Create a separate task to update CORS config.

2. **RA96IT Public Key Extraction:** The `RA96IT_PUBLIC_KEY` env var requires exporting the RS256 PEM public key from the `beneficial-cooperation` Railway service. Document extraction procedure or create separate task.

**Notes:**
- Health check endpoint already exists and is fully implemented — no code changes needed
- All env vars cross-referenced against `.deia/config/deployment-env.md` — all match
- Railway section follows same format as Vercel section (consistent documentation style)
- Windows-style absolute paths used where relevant (e.g., `cd C:\Users\davee\...`)
- Documentation warns "DO NOT execute these commands yet" — repoint cutover will be coordinated separately
