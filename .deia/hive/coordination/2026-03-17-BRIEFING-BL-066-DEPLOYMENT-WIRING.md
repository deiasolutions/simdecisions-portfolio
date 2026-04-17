# BRIEFING: BL-066 Deployment Wiring Verification

**To:** Q33N
**From:** Q88NR-bot
**Date:** 2026-03-17
**Spec:** `2026-03-17-SPEC-TASK-BL066-deployment-wiring.md`

---

## Objective

Verify and document deployment wiring for Vercel (frontend) and Railway (backend) pointing to shiftcenter repo.

---

## Current State Analysis

**Vercel (Frontend):**
- `vercel.json` EXISTS at repo root
- Build command: `cd browser && npm run build`
- Output directory: `browser/dist`
- Install command: `cd browser && npm install`
- Rewrites: all routes to `/index.html` (SPA routing)
- ✅ Configuration looks complete

**Railway (Backend):**
- NO `railway.toml`, `railway.json`, or `Procfile` found in repo
- Backend entry point: `hivenode/__main__.py` with `main()` function
- Start command should be: `python -m hivenode` OR `hive` (console script defined in pyproject.toml)
- Port: Auto-detected from settings, default 8080, with retry logic for sequential ports
- ❌ NO RAILWAY CONFIG FILE — needs to be created OR documented as Railway project settings

**Environment Variables Needed:**
- Backend (hivenode):
  - `MODE` (local/cloud/remote)
  - Database URLs (SQLite by default, PostgreSQL for production)
  - JWT secrets for ra96it integration
  - JWKS URLs
  - Rate limit settings
  - Storage volume paths
- Frontend (browser):
  - `VITE_API_BASE_URL` (points to Railway backend)
  - Other runtime API endpoints

---

## Tasks for Q33N

Create **ONE** task file:

**2026-03-17-TASK-BL066-deployment-wiring.md**

### Deliverables

1. **Create `railway.toml`** at repo root with:
   - `[build]` section with build command if needed (likely none for Python)
   - `[deploy]` section with start command: `python -m hivenode`
   - Health check endpoint: `/health` (verify exists in routes)
   - Port configuration (Railway auto-injects `$PORT`, verify hivenode config respects it)

2. **Verify Vercel config is production-ready:**
   - Check that `copy-eggs` script in `browser/package.json` copies EGG files before build
   - Verify build command includes `npm run copy-eggs`
   - Test: `cd browser && npm run build` succeeds

3. **Document required environment variables:**
   - Create or update `docs/DEPLOYMENT.md` with:
     - Vercel env vars (frontend)
     - Railway env vars (backend)
     - Links to where to set them in each platform
   - Absolute path: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT.md`

4. **Verify health endpoint exists:**
   - Read routes to confirm `/health` endpoint exists
   - If not, flag as NEEDS_DAVE (separate BUG/BL item)

5. **Test build locally:**
   - Run `cd browser && npm run build` and verify success
   - Verify `browser/dist/` contains built files
   - Verify EGG files are copied to dist

### Acceptance Criteria

- [ ] `railway.toml` created with correct start command
- [ ] `docs/DEPLOYMENT.md` exists with all env vars documented
- [ ] Vercel build test passes locally
- [ ] Health endpoint verified (exists or flagged as missing)
- [ ] EGG files confirmed copied to build output

### Test Requirements

- **Manual test:** Run `cd browser && npm run build` → verify no errors
- **Manual test:** Check `browser/dist/` for built files and EGG files
- **Manual test:** Read routes to confirm `/health` endpoint exists

### Constraints

- NO actual deployment to Vercel/Railway (just config verification)
- NO environment secrets in committed files
- Use Railway environment variable injection for secrets
- File size limits: keep `railway.toml` under 100 lines, `DEPLOYMENT.md` under 500 lines

---

## Model Assignment

**sonnet** — requires understanding of deployment platforms, config formats, and documentation

---

## Priority

**P0** — needed before prod deploy

---

## Notes

- Railway likely configured via web UI rather than config file — if no `railway.toml` needed, document why in DEPLOYMENT.md
- Vercel config looks good, just needs verification
- Focus on documentation and smoke tests, not actual deployment
