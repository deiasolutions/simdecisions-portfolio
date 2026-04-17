# TASK-062: Document Smoke Test Procedure

## Objective

Document the smoke test procedure for verifying the Vercel and Railway deployment wiring after repoint. This task does NOT execute the smoke tests — it only prepares the documentation.

## Context

After the Vercel and Railway repoint is executed (using the procedures documented in TASK-058, 059, 060), we need a smoke test checklist to verify that both services are working correctly. The smoke test will:
- Verify Vercel builds successfully from `dev` branch
- Verify `dev.shiftcenter.com` loads the chat app
- Verify Railway builds successfully from `dev` branch
- Verify API health endpoint responds at staging URL
- Verify EGG loading works with `?egg=` query param

This documentation will be used by the human (Q88N) or regent (Q33NR) when executing the cutover.

## Deliverables

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Add smoke test section (append to existing file from TASK-058, 059, 060)

## Smoke Test Section Requirements

Append the following section to `docs/DEPLOYMENT-WIRING-NOTES.md` (after the DNS section):

```markdown
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
```

End of smoke test section.

## Test Requirements

**No automated tests required** — this is a documentation task.

Manual verification:
- [ ] Smoke test section is valid markdown (no broken links)
- [ ] All 7 tests are clearly documented
- [ ] Checklist format is correct (markdown checkboxes)
- [ ] Rollback plan is included

## Constraints

- **DO NOT execute smoke tests** — this task only creates documentation
- **DO NOT change production DNS** — old deploys stay live
- **DO NOT delete old Vercel/Railway projects** — they stay live until cutover is verified
- Use Windows-style absolute paths in documentation where relevant (e.g., `C:\Users\davee\...`)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-062-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full absolute paths
3. **What Was Done** -- bullet list of concrete changes (smoke test section added with 7 tests)
4. **Test Results** -- manual verification steps performed (markdown format check, checklist format)
5. **Build Verification** -- N/A (no build required)
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- note that CORS update may be needed (separate task), dependencies on TASK-058, 059, 060, 061

DO NOT skip any section. A response without all 8 sections is incomplete.

## Model Assignment

sonnet
