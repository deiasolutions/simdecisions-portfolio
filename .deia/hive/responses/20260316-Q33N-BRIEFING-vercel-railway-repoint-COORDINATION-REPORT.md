# Q33N Coordination Report: Vercel + Railway Repoint to ShiftCenter Repo

**Date:** 2026-03-16
**From:** Q33N (coordinator)
**To:** Q33NR
**Briefing:** `2026-03-16-3000-SPEC-w3-01-vercel-railway-repoint.md`
**Status:** ANALYSIS COMPLETE — NO TASK FILES NEEDED

---

## Summary

The briefing requested breaking down the Vercel/Railway repoint procedure into 5 tasks (TASK-191 through TASK-195). However, **all required files already exist** and the only remaining work is **manual execution** of the repoint via dashboards/CLI.

---

## Files Already Complete

### 1. `browser/vercel.json` — ✅ EXISTS

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vercel.json`

**Content:**
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": null
}
```

**Status:** Complete. This file provides SPA fallback routing as required.

**Originally proposed as:** TASK-191 (create vercel.json)

---

### 2. `hivenode/main.py` CORS Configuration — ✅ ALREADY CONFIGURED

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 253-262)

**CORS origins include:**
- ✅ `http://localhost:5173` (Vite dev)
- ✅ `http://localhost:3000` (alternative dev port)
- ✅ `https://simdecisions.com` (current production)
- ✅ `https://code.shiftcenter.com` (ShiftCenter production)
- ✅ `https://dev.shiftcenter.com` (ShiftCenter dev)
- ✅ `https://ra96it.com` (ra96it login)
- ✅ `https://dev.ra96it.com` (ra96it dev login)
- ✅ `https://efemera.live` (Efemera)

**Status:** Complete. All required CORS origins are already configured.

---

### 3. Deployment Documentation — ✅ COMPREHENSIVE

**Primary doc:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` (765 lines)

**Sections:**
- **Vercel: Browser App** (lines 11-130)
  - Current state, target state, repoint procedure (8 steps)
  - DNS configuration (Cloudflare)
  - Verification steps
- **Railway: Hivenode API** (lines 132-310)
  - Current state, target state, repoint procedure (6 steps)
  - Environment variables checklist (table format)
  - CORS verification, health check verification
- **DNS Configuration** (lines 312-423)
  - Step-by-step: Add `dev.shiftcenter.com` (3 steps)
  - Step-by-step: Verify `api.shiftcenter.com` (3 steps)
  - Production DNS (no changes), rollback plan
- **Smoke Test Procedure** (lines 425-740)
  - 7 smoke tests with detailed steps and expected results
  - Smoke test checklist
  - Next steps after tests pass

**Status:** Complete. This document provides everything Q88N needs to execute the repoint.

**Originally proposed as:** TASK-192 (Vercel docs), TASK-193 (Railway docs), TASK-194 (DNS docs), TASK-195 (smoke test docs)

---

### 4. Environment Variables Checklist — ✅ DOCUMENTED

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md` (161 lines)

**Sections:**
- Vercel env vars (3 vars: `VITE_API_URL`, `VITE_GITHUB_CLIENT_ID`, `VITE_RA96IT_URL`)
- Railway env vars (3 categories):
  - Required — New (3 vars: `HIVENODE_MODE`, `RA96IT_PUBLIC_KEY`, `FRONTEND_URL`)
  - Required — Carried Over (3 vars: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`)
  - Required — Renamed (2 vars: `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`)
  - Drop — No Longer Needed (4 vars: `SD_JWT_SECRET`, `SD_FRONTEND_URL`, etc.)
- Domain strategy (dev vs production)
- Repoint procedure (when ready)

**Status:** Complete. All environment variables are documented with clear instructions.

---

## What Remains: Manual Execution Only

The repoint procedure is **manual** and requires:

1. **Vercel CLI** or Vercel dashboard
   - Link repo `deiasolutions/shiftcenter` to existing project `simdecisions-2`
   - Set root directory: `browser/`
   - Set production branch: `main`
   - Add preview branch: `dev`
   - Set env vars (3 vars)
   - Add custom domain: `dev.shiftcenter.com`

2. **Railway CLI** or Railway dashboard
   - Link repo `deiasolutions/shiftcenter` to existing service `merry-learning`
   - Set root directory: (empty)
   - Set start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
   - Set production branch: `main`
   - Add env vars (8 new/renamed vars)
   - Remove old env vars (4 vars)
   - Optional: create staging service for `dev` branch

3. **Cloudflare DNS**
   - Add CNAME: `dev.shiftcenter.com` → Vercel target (proxied)
   - Verify CNAME: `api.shiftcenter.com` → Railway target (proxied)

4. **Smoke Tests**
   - Run 7 smoke tests from `DEPLOYMENT-WIRING-NOTES.md` (lines 425-740)

---

## Recommendation: No Task Files Needed

Since all code artifacts exist and the remaining work is **manual dashboard/CLI operations**, I recommend:

### Option A: Q88N Executes Directly
Q88N follows the existing documentation (`DEPLOYMENT-WIRING-NOTES.md`) to execute the repoint manually. No task files or bee dispatch needed.

### Option B: Q33NR Creates Summary Checklist
If Q33NR wants a condensed checklist, I can create a single file:
- `.deia/hive/coordination/2026-03-16-REPOINT-CHECKLIST.md`
- Summary of all manual steps with checkboxes
- References to full documentation

**I do NOT recommend creating 5 separate task files (TASK-191 through TASK-195) because:**
1. TASK-191 (`vercel.json`) already exists — no work needed
2. TASK-192-195 (documentation) already exist — no work needed
3. Bees cannot execute Vercel/Railway/DNS operations (requires human access)
4. Creating task files for documentation extraction is redundant

---

## Q33NR Decision Required

Please advise:

1. **Option A:** Q88N executes repoint using existing documentation (no task files)
2. **Option B:** Q33N creates a single summary checklist file (no bee dispatch)
3. **Option C:** Q33N creates task files TASK-191-195 as originally proposed (redundant, but follows briefing exactly)

I recommend **Option A** or **Option B**.

---

## Files Referenced

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vercel.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 253-262)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md`

---

**End of Coordination Report**
