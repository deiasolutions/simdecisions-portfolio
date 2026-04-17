# TASK-059: Document Railway Configuration + Env Vars

## Objective

Document the Railway CLI repoint procedure and environment variable configuration. Verify the health check endpoint exists (already implemented). This task does NOT execute the repoint — it only prepares the documentation.

## Context

We are repointing the Railway service from `deiasolutions/platform` to `deiasolutions/shiftcenter`. The new repo has the hivenode FastAPI app at `hivenode/`. The Railway service is currently called `merry-learning` and serves `api.simdecisions.com` in production. After repoint:
- Production branch: `main` → api.shiftcenter.com
- Staging environment: `dev` branch → separate Railway service or environment

Environment variables documented in: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md`

FastAPI app entry: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py`

Health check endpoint (already exists): `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py`

## Deliverables

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Add Railway section (append to existing file from TASK-058)
- [ ] Verify health check endpoint exists at `hivenode/routes/health.py` (no code changes needed)

## Railway Section Requirements

Append the following section to `docs/DEPLOYMENT-WIRING-NOTES.md` (after the Vercel section):

```markdown
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

[DNS section will be added by TASK-060]
[Smoke test section will be added by TASK-062]
```

End of Railway section.

## Health Check Verification

Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py` and verify:
- [ ] Endpoint exists at `GET /health`
- [ ] Returns `HealthResponse` with `status`, `mode`, `version`, `uptime_s` fields
- [ ] No code changes needed

If the health endpoint does NOT exist or is incomplete, note this in the response file (Issues / Follow-ups section). This should NOT happen based on the briefing, but verify anyway.

## Test Requirements

**No automated tests required** — this is a documentation task.

Manual verification:
- [ ] Railway section is valid markdown (no broken links)
- [ ] All env vars match `.deia/config/deployment-env.md`
- [ ] Health check endpoint exists at `hivenode/routes/health.py` (verified by reading the file)

## Constraints

- **DO NOT execute the Railway repoint** — this task only creates documentation
- **DO NOT delete old Railway service** — it stays live until cutover is verified
- **DO NOT change production DNS** — old deploys stay live
- **DO NOT modify CORS config in main.py** — that's a separate task (note it in the docs as "action required")
- Use Windows-style absolute paths in documentation where relevant (e.g., `C:\Users\davee\...`)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-059-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full absolute paths
3. **What Was Done** -- bullet list of concrete changes (Railway section added, health endpoint verified)
4. **Test Results** -- manual verification steps performed (markdown format check, health endpoint read)
5. **Build Verification** -- N/A (no build required)
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- note CORS update needed (separate task), dependencies on TASK-058, 060, 062

DO NOT skip any section. A response without all 8 sections is incomplete.

## Model Assignment

sonnet
