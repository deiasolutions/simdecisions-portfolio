# Deployment Wiring — ShiftCenter Repoint

## Overview

This document describes the procedure to repoint Vercel and Railway deployments from `deiasolutions/platform` to `deiasolutions/shiftcenter`. This wiring is in place as of 2026-03-13. The actual repoint cutover will be executed when approved.

**DO NOT execute these commands yet** — this is the wiring documentation. The cutover will be coordinated separately.

---

## Vercel: Browser App

### Current State
- **Repo:** `deiasolutions/platform`
- **Project:** `simdecisions-2`
- **Root directory:** `simdecisions-2/`
- **Domain:** code.shiftcenter.com (production)

### Target State
- **Repo:** `deiasolutions/shiftcenter`
- **Root directory:** `browser/`
- **Production branch:** `main` → code.shiftcenter.com
- **Preview branch:** `dev` → dev.shiftcenter.com
- **Config file:** `browser/vercel.json` (SPA fallback)

### Repoint Procedure

**Prerequisites:**
- Vercel CLI installed: `npm install -g vercel`
- Authenticated: `vercel login`
- GitHub user: `deiasolutions` org member

**Steps:**

1. **Link repo to Vercel project:**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
   vercel link --yes
   # Select project: simdecisions-2
   # This repoints the existing project to the new repo
   ```

2. **Set root directory:**
   ```bash
   vercel --cwd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser env add ROOT_DIRECTORY
   # Enter: browser
   ```

3. **Set production branch:**
   Vercel dashboard → Project Settings → Git → Production Branch: `main`

4. **Add preview branch:**
   Vercel dashboard → Project Settings → Git → Preview Branches: Include `dev`

5. **Set environment variables (production):**
   ```bash
   vercel env add VITE_API_URL production
   # Enter: https://api.shiftcenter.com

   vercel env add VITE_GITHUB_CLIENT_ID production
   # Enter: <GitHub OAuth Client ID from 1Password>

   vercel env add VITE_AUTH_API production
   # Enter: https://api.hodeia.me
   ```

6. **Set environment variables (preview/dev):**
   ```bash
   vercel env add VITE_API_URL preview
   # Enter: https://api.simdecisions.com (or staging URL when available)

   vercel env add VITE_GITHUB_CLIENT_ID preview
   # Enter: <same as production>

   vercel env add VITE_AUTH_API preview
   # Enter: https://api.hodeia.me
   ```

7. **Add custom domain for dev branch:**
   Vercel dashboard → Project Settings → Domains → Add Domain: `dev.shiftcenter.com`
   - Assign to branch: `dev`
   - Vercel will provide CNAME target (e.g., `cname.vercel-dns.com`)

8. **Verify build settings:**
   Vercel dashboard → Project Settings → Build & Development Settings:
   - Framework Preset: Other (or Vite if available)
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
   - Root Directory: `browser`

### DNS Configuration (Cloudflare)

After Vercel provides the CNAME target for `dev.shiftcenter.com`:

1. Log in to Cloudflare → shiftcenter.com zone
2. Add DNS record:
   - Type: CNAME
   - Name: `dev`
   - Target: `cname.vercel-dns.com` (or Vercel's provided target)
   - Proxy status: Proxied (orange cloud)
   - TTL: Auto

**See comprehensive DNS section below for full configuration details, including `api.shiftcenter.com` verification and rollback plans.**

### Verification

After repoint (when executed):

1. **Test production build:**
   ```bash
   git checkout main
   git push origin main
   # Wait for Vercel build to complete
   # Visit: https://code.shiftcenter.com
   # Should load chat app (or code app if code.egg.md exists)
   ```

2. **Test dev branch build:**
   ```bash
   git checkout dev
   git push origin dev
   # Wait for Vercel build to complete
   # Visit: https://dev.shiftcenter.com
   # Should load chat app by default
   # Visit: https://dev.shiftcenter.com?egg=chat
   # Should load same chat app
   ```

---

## Railway: Hivenode API

### Current State
- **Repo:** `deiasolutions/platform`
- **Service:** `merry-learning`
- **Root directory:** `simdecisions-2/api/`
- **Domain:** api.simdecisions.com (production)
- **Start command:** (inherited from Procfile or auto-detected)

### Target State
- **Repo:** `deiasolutions/shiftcenter`
- **Root directory:** (empty — run from repo root)
- **Production branch:** `main` → api.shiftcenter.com
- **Staging branch:** `dev` → separate Railway service or environment
- **Start command:** `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
- **Health check:** `GET /health` returns 200

### Repoint Procedure

**Prerequisites:**
- Railway CLI installed: `npm install -g @railway/cli` or `brew install railway`
- Authenticated: `railway login`
- GitHub user: `deiasolutions` org member

**Steps:**

1. **Link repo to Railway service (production):**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
   railway link
   # Select service: merry-learning
   # This repoints the existing service to the new repo
   ```

2. **Set root directory:**
   Railway dashboard → Service Settings → Source → Root Directory: (leave empty)

3. **Set start command:**
   Railway dashboard → Service Settings → Deploy → Start Command:
   ```
   uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set production branch:**
   Railway dashboard → Service Settings → Source → Production Branch: `main`

5. **Configure environment variables (production):**

   **Required — New:**
   ```bash
   railway variables set HIVENODE_MODE=cloud
   railway variables set RA96IT_PUBLIC_KEY="<RS256 PEM public key from beneficial-cooperation service>"
   railway variables set FRONTEND_URL=https://simdecisions.com
   ```

   **Required — Carried Over:**
   These should already exist (verify in Railway dashboard):
   - `DATABASE_URL` — auto-injected by Railway from shared Postgres service
   - `ANTHROPIC_API_KEY` — carry over from old service (sync from Infisical: `sk-ant-...`)
   - `VOYAGE_API_KEY` — carry over from old service (sync from Infisical)

   **Required — Renamed:**
   ```bash
   # Rename GitHub OAuth vars (drop SD_ prefix)
   railway variables set GITHUB_CLIENT_ID="<value from old SD_GITHUB_CLIENT_ID>"
   railway variables set GITHUB_CLIENT_secret="[REDACTED]"
   ```

   **Drop — No Longer Needed:**
   Remove these old env vars from the Railway dashboard:
   - `SD_JWT_SECRET` (replaced by RA96IT_PUBLIC_KEY asymmetric verification)
   - `SD_FRONTEND_URL` (replaced by FRONTEND_URL)
   - `SD_GITHUB_CLIENT_ID` (renamed to GITHUB_CLIENT_ID)
   - `SD_GITHUB_CLIENT_SECRET` (renamed to GITHUB_CLIENT_SECRET)

6. **Create staging environment (for dev branch):**

   **Option A: Separate Railway Service (recommended)**
   ```bash
   # Create new Railway service from dashboard
   # Name: shiftcenter-staging
   # Link to same repo: deiasolutions/shiftcenter
   # Branch: dev
   # Root directory: (empty)
   # Start command: uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT
   # Env vars: same as production, but set FRONTEND_URL to dev.shiftcenter.com
   ```

   **Option B: Railway Environments (if supported)**
   ```bash
   # Railway dashboard → Service → Environments → New Environment
   # Name: staging
   # Branch: dev
   # Env vars: inherit from production, override FRONTEND_URL
   ```

### Environment Variables Checklist

| Env Var | Source | Production Value | Staging Value |
|---------|--------|------------------|---------------|
| `HIVENODE_MODE` | Manual | `cloud` | `cloud` |
| `RA96IT_PUBLIC_KEY` | From `beneficial-cooperation` service | `<RS256 PEM public key>` | `<same>` |
| `FRONTEND_URL` | Manual | `https://simdecisions.com` | `https://dev.shiftcenter.com` |
| `DATABASE_URL` | Railway auto-inject | (auto) | (auto, same DB) |
| `ANTHROPIC_API_KEY` | Infisical | `sk-ant-...` | `<same>` |
| `VOYAGE_API_KEY` | Infisical | `<voyage key>` | `<same>` |
| `GITHUB_CLIENT_ID` | GitHub OAuth App | `<client ID>` | `<same>` |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth App | `<client secret>` | `<same>` |

### CORS Configuration Verification

The `hivenode/main.py` file already includes CORS middleware with these origins:
- `http://localhost:5173` (Vite dev)
- `http://localhost:3000` (alternative dev port)
- `https://*.shiftcenter.app` (production wildcard)

After repoint, verify CORS allows:
- `https://simdecisions.com` (current production domain)
- `https://code.shiftcenter.com` (new production domain)
- `https://dev.shiftcenter.com` (dev branch preview)

**Action required:** Update CORS origins in `hivenode/main.py` line 233-237 to include:
```python
allow_origins=[
    "http://localhost:5173",  # Vite dev
    "http://localhost:3000",  # Alternative dev port
    "https://simdecisions.com",  # Current production
    "https://code.shiftcenter.com",  # New production
    "https://dev.shiftcenter.com",  # Dev preview
    "https://*.shiftcenter.app",  # Wildcard for future subdomains
],
```

Note: This CORS update will be handled by a separate task (out of scope for this documentation task).

### Health Check Verification

The health check endpoint already exists at `hivenode/routes/health.py`:
- **Endpoint:** `GET /health`
- **Response:** `{ "status": "ok", "mode": "cloud", "version": "0.1.0", "uptime_s": 123.45 }`
- **No code changes needed** — Railway will use this for health checks

Railway health check configuration:
- Railway dashboard → Service Settings → Health Check
- Path: `/health`
- Timeout: 30 seconds
- Interval: 60 seconds

### Verification

After repoint (when executed):

1. **Test production deployment:**
   ```bash
   git checkout main
   git push origin main
   # Wait for Railway build to complete
   # Test health endpoint:
   curl https://api.shiftcenter.com/health
   # Should return: {"status":"ok","mode":"cloud","version":"0.1.0","uptime_s":...}
   ```

2. **Test staging deployment:**
   ```bash
   git checkout dev
   git push origin dev
   # Wait for Railway build to complete
   # Test health endpoint (staging URL):
   curl https://<staging-url>.up.railway.app/health
   # Should return: {"status":"ok","mode":"cloud","version":"0.1.0","uptime_s":...}
   ```

3. **Test CORS:**
   ```bash
   # From browser console on dev.shiftcenter.com:
   fetch('https://api.shiftcenter.com/health').then(r => r.json()).then(console.log)
   # Should succeed (no CORS error)
   ```

---

## DNS Configuration (Cloudflare)

### Overview

DNS for `shiftcenter.com` is managed in Cloudflare. After Vercel and Railway repoint, we need to:
1. Add `dev.shiftcenter.com` → Vercel (new)
2. Verify `api.shiftcenter.com` → Railway (existing or update)
3. Leave production domains unchanged until cutover is verified

### Prerequisites

- Cloudflare account access (DNS admin for shiftcenter.com zone)
- CNAME target from Vercel for `dev.shiftcenter.com` (provided after custom domain is added in Vercel dashboard)
- CNAME target from Railway for `api.shiftcenter.com` (provided in Railway dashboard under custom domains)

### DNS Records Checklist

| Record | Type | Name | Target | Proxy | Status |
|--------|------|------|--------|-------|--------|
| Dev frontend | CNAME | `dev` | `cname.vercel-dns.com` (or Vercel's target) | Proxied (orange) | **New** — add after Vercel repoint |
| API (new) | CNAME | `api` | Railway custom domain target | Proxied (orange) | **Verify/Update** — check after Railway repoint |
| Production frontend | CNAME | `code` | (existing Vercel target) | Proxied (orange) | **No change** — stays pointed at old deploy until cutover |

### Step-by-Step: Add dev.shiftcenter.com

**Prerequisites:**
1. Vercel custom domain configured (see Vercel section, step 7)
2. Vercel provides CNAME target (e.g., `cname.vercel-dns.com` or `76.76.21.xxx`)

**Steps:**

1. **Log in to Cloudflare:**
   - URL: https://dash.cloudflare.com
   - Select zone: `shiftcenter.com`

2. **Add DNS record:**
   - Click "DNS" in left sidebar
   - Click "Add record"
   - Type: `CNAME`
   - Name: `dev`
   - Target: `<CNAME target from Vercel>` (e.g., `cname.vercel-dns.com`)
   - Proxy status: **Proxied** (orange cloud icon)
   - TTL: Auto
   - Click "Save"

3. **Verify DNS propagation:**
   ```bash
   # Wait 1-2 minutes, then check:
   nslookup dev.shiftcenter.com
   # Should return Cloudflare proxy IP (not Vercel's IP directly)

   # Test in browser:
   curl -I https://dev.shiftcenter.com
   # Should return 200 or redirect to Vercel
   ```

### Step-by-Step: Verify api.shiftcenter.com

**Prerequisites:**
1. Railway custom domain configured (Railway dashboard → Service → Settings → Domains → Add custom domain: `api.shiftcenter.com`)
2. Railway provides CNAME target (e.g., `<service-name>.up.railway.app` or custom target)

**Steps:**

1. **Check existing DNS record:**
   - Cloudflare → shiftcenter.com zone → DNS
   - Look for existing `CNAME` record: `api` → `<old target>`

2. **Update target (if needed):**
   - If target is old Railway service, update it:
   - Click record → Edit
   - Target: `<new CNAME target from Railway>` (e.g., `merry-learning.up.railway.app` or custom domain)
   - Proxy status: **Proxied** (orange cloud icon)
   - Click "Save"

3. **Verify DNS propagation:**
   ```bash
   nslookup api.shiftcenter.com
   # Should return Cloudflare proxy IP

   # Test health endpoint:
   curl https://api.shiftcenter.com/health
   # Should return: {"status":"ok","mode":"cloud",...}
   ```

### Production DNS (No Changes Yet)

**Do NOT change these records until cutover is verified:**

| Record | Current Target | Notes |
|--------|----------------|-------|
| `code.shiftcenter.com` | Old Vercel deployment | Leave unchanged — points at old `deiasolutions/platform` deploy |
| `simdecisions.com` | Old Vercel deployment | Leave unchanged — same as above |
| `api.simdecisions.com` | Old Railway deployment | Leave unchanged — points at old `deiasolutions/platform` deploy |

After successful staging verification (smoke tests pass), these will be updated to point at the new deploys.

### Rollback Plan

If DNS changes cause issues:

1. **Revert dev.shiftcenter.com:**
   - Cloudflare → DNS → Delete `dev` CNAME record
   - TTL is "Auto" (5 minutes) — propagation takes 5-10 minutes

2. **Revert api.shiftcenter.com:**
   - Cloudflare → DNS → Edit `api` CNAME record
   - Target: `<old Railway target>` (from old service)
   - Save → propagation takes 5-10 minutes

---

## Smoke Test Procedure

### Overview

After Vercel, Railway, and DNS configurations are complete, follow this smoke test procedure to verify deployments before cutting over production traffic.

**Prerequisites:**
- Vercel repoint executed (see Vercel section above)
- Railway repoint executed (see Railway section above)
- DNS for `dev.shiftcenter.com` added (see DNS section above)
- Dev branch is up to date with latest changes

### Test Environment

- **Frontend:** `dev.shiftcenter.com` (Vercel, `dev` branch)
- **Backend:** Railway staging URL (Railway, `dev` branch)
- **Browser:** Chrome or Firefox (latest version)
- **Tools:** `curl`, browser DevTools (Network tab)

---

### Test 1: Vercel Build Verification

**Objective:** Verify Vercel builds successfully from `dev` branch

**Steps:**

1. **Push a test commit to dev branch:**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
   git checkout dev
   git pull origin dev

   # Add a small test change (e.g., update a comment)
   echo "// Smoke test: $(date)" >> browser/src/App.tsx
   git add browser/src/App.tsx
   git commit -m "Smoke test: Vercel build verification"
   git push origin dev
   ```

2. **Monitor Vercel build:**
   - Vercel dashboard → Deployments → Filter by branch: `dev`
   - Wait for build to complete (usually 1-3 minutes)
   - Build status should be: **Ready** (green checkmark)

3. **Verify build logs:**
   - Click deployment → View Build Logs
   - Check for errors or warnings
   - Verify build command ran: `npm run build`
   - Verify output directory: `dist/`

**Expected Result:**
- Build completes successfully
- No errors in build logs
- Deployment status: Ready

**If test fails:**
- Check build logs for errors
- Verify `browser/package.json` scripts are correct
- Verify `browser/vercel.json` config is valid
- Rollback commit and investigate

---

### Test 2: Frontend Loading (dev.shiftcenter.com)

**Objective:** Verify `dev.shiftcenter.com` loads the chat app in browser

**Steps:**

1. **Open browser:**
   - Navigate to: https://dev.shiftcenter.com
   - Wait for page to load (should be fast, < 2 seconds)

2. **Verify page loads:**
   - Page displays without errors
   - No blank white screen
   - Browser console has no red errors (open DevTools → Console)

3. **Verify app content:**
   - ShiftCenter logo or branding visible (if implemented)
   - Chat interface loads (text pane, terminal, tree-browser)
   - No "404 Not Found" or "500 Internal Server Error"

4. **Check Network tab:**
   - Open DevTools → Network
   - Refresh page
   - Verify `/` request returns 200
   - Verify `index.html` loads successfully
   - Verify JS/CSS bundles load (Vite chunks)

**Expected Result:**
- Page loads successfully
- Chat app UI visible
- No console errors
- All network requests return 200

**If test fails:**
- Check browser console for errors
- Verify DNS is propagated: `nslookup dev.shiftcenter.com`
- Verify Vercel deployment is live (Vercel dashboard)
- Check `browser/vercel.json` rewrites (SPA fallback)

---

### Test 3: Railway Build Verification

**Objective:** Verify Railway builds successfully from `dev` branch

**Steps:**

1. **Trigger Railway build:**
   - Railway dashboard → Service (staging or dev environment)
   - Deployments tab → Latest deployment
   - Status should be: **Active** (green)

   Or push a test commit:
   ```bash
   git checkout dev
   echo "# Smoke test: $(date)" >> hivenode/README.md
   git add hivenode/README.md
   git commit -m "Smoke test: Railway build verification"
   git push origin dev
   ```

2. **Monitor Railway build:**
   - Railway dashboard → Deployments
   - Wait for build to complete (usually 2-5 minutes)
   - Build status should be: **Success**

3. **Verify build logs:**
   - Click deployment → View Logs
   - Check for errors or warnings
   - Verify start command ran: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
   - Verify health check passes (Railway auto-checks `/health`)

**Expected Result:**
- Build completes successfully
- No errors in build logs
- Deployment status: Active
- Health check passes

**If test fails:**
- Check build logs for errors
- Verify `pyproject.toml` dependencies are correct
- Verify start command is correct (Railway settings)
- Check Railway env vars (HIVENODE_MODE, DATABASE_URL, etc.)

---

### Test 4: API Health Endpoint

**Objective:** Verify Railway API responds at staging URL

**Steps:**

1. **Get staging URL:**
   - Railway dashboard → Service → Settings → Domains
   - Copy staging URL (e.g., `https://<service-name>.up.railway.app`)

2. **Test health endpoint:**
   ```bash
   curl https://<staging-url>.up.railway.app/health
   ```

   **Expected response:**
   ```json
   {
     "status": "ok",
     "mode": "cloud",
     "version": "0.1.0",
     "uptime_s": 123.45
   }
   ```

3. **Verify response:**
   - Status code: **200 OK**
   - JSON response contains `status`, `mode`, `version`, `uptime_s`
   - `mode` should be `"cloud"`

**Expected Result:**
- Health endpoint returns 200
- JSON response is valid
- `status` field is `"ok"`

**If test fails:**
- Check Railway deployment status (should be Active)
- Verify Railway start command is correct
- Check Railway logs for errors
- Verify `hivenode/routes/health.py` exists and is mounted

---

### Test 5: CORS Verification

**Objective:** Verify API allows CORS from `dev.shiftcenter.com`

**Steps:**

1. **Open browser console:**
   - Navigate to: https://dev.shiftcenter.com
   - Open DevTools → Console

2. **Test CORS:**
   ```javascript
   fetch('https://<staging-url>.up.railway.app/health')
     .then(r => r.json())
     .then(data => console.log('CORS success:', data))
     .catch(err => console.error('CORS error:', err))
   ```

   Replace `<staging-url>` with Railway staging URL.

3. **Verify response:**
   - Console logs: `CORS success: {status: "ok", mode: "cloud", ...}`
   - No CORS error in console (no "blocked by CORS policy" message)

**Expected Result:**
- Fetch succeeds
- No CORS errors
- API response logged to console

**If test fails:**
- Check `hivenode/main.py` CORS origins (line 233-237)
- Verify `dev.shiftcenter.com` is in `allow_origins` list
- Check Railway logs for CORS errors
- Note: CORS update may be needed (see TASK-059 notes)

---

### Test 6: EGG Loading with Query Param

**Objective:** Verify `?egg=` query param loads correct EGG

**Steps:**

1. **Test default EGG:**
   - Navigate to: https://dev.shiftcenter.com
   - Verify chat EGG loads (default)

2. **Test query param override:**
   - Navigate to: https://dev.shiftcenter.com?egg=chat
   - Verify chat EGG loads (same as default)

3. **Test different EGG (if exists):**
   - Navigate to: https://dev.shiftcenter.com?egg=code
   - Verify code EGG attempts to load (may show "EGG not found" if code.egg.md doesn't exist yet — this is OK)

4. **Check browser console:**
   - Open DevTools → Console
   - Verify no errors related to EGG resolution
   - May see warning: "routing.config.egg not loaded — using hardcoded hostname mappings" (this is OK)

**Expected Result:**
- `?egg=chat` loads chat EGG
- `?egg=code` attempts to load code EGG (may fail gracefully if EGG file doesn't exist)
- No JavaScript errors related to EGG resolution

**If test fails:**
- Check `browser/src/eggs/eggResolver.ts` (TASK-061 changes)
- Verify hostname → EGG mappings are correct
- Check browser console for errors
- Verify query param parsing works (`URLSearchParams`)

---

### Test 7: Rollback Verification (Sanity Check)

**Objective:** Verify old production deploys are still live (no impact to production)

**Steps:**

1. **Test old production frontend:**
   - Navigate to: https://code.shiftcenter.com (if old deploy is still pointed here)
   - Or: https://simdecisions.com (if old deploy is still pointed here)
   - Verify old app still loads (no downtime)

2. **Test old production API:**
   ```bash
   curl https://api.simdecisions.com/health
   # Should return 200 from old deploy
   ```

**Expected Result:**
- Old production frontend still loads
- Old production API still responds
- No impact to production traffic

**If test fails:**
- CRITICAL: Production is down — rollback immediately
- Check DNS records (should still point to old deploys)
- Verify Vercel/Railway projects are NOT deleted

---

## Smoke Test Checklist

Use this checklist when executing smoke tests:

- [ ] Test 1: Vercel build succeeds from `dev` branch
- [ ] Test 2: `dev.shiftcenter.com` loads chat app in browser
- [ ] Test 3: Railway build succeeds from `dev` branch
- [ ] Test 4: API health endpoint returns 200 at staging URL
- [ ] Test 5: CORS allows requests from `dev.shiftcenter.com`
- [ ] Test 6: `?egg=chat` query param loads chat EGG
- [ ] Test 7: Old production deploys still work (no downtime)

**All tests pass?**
- Deployment wiring is verified ✅
- Ready to proceed with production cutover (separate task)

**Any tests fail?**
- Rollback DNS changes (see DNS section → Rollback Plan)
- Investigate failures in Railway/Vercel logs
- Do NOT proceed with production cutover until all tests pass

---

## Next Steps (After Smoke Tests Pass)

1. **Update CORS origins in hivenode/main.py** (if CORS test failed)
   - Add `https://dev.shiftcenter.com` to `allow_origins` list
   - Add `https://code.shiftcenter.com` to `allow_origins` list
   - Commit and push to `dev` branch
   - Re-run Test 5 (CORS verification)

2. **Production cutover** (separate task, not documented here)
   - Update DNS for `code.shiftcenter.com` → new Vercel deploy
   - Update DNS for `api.shiftcenter.com` → new Railway deploy
   - Monitor production traffic
   - Keep old deploys live for 24 hours (rollback safety net)

3. **Archive old Vercel/Railway projects** (after 7 days of stable production)
   - Vercel dashboard → old project → Settings → Delete
   - Railway dashboard → old service → Settings → Delete
   - Only after confirming new deploys are stable

---

End of DEPLOYMENT-WIRING-NOTES.md
