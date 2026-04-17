# ShiftCenter Deployment Guide

## Overview

ShiftCenter is deployed as a two-service architecture:
- **Frontend (Vercel):** Browser-based SPA built with React + Vite, served from `browser/` directory
- **Backend (Railway):** Python FastAPI server (hivenode), connected to PostgreSQL database

This guide provides a quick reference for required environment variables and deployment verification steps. For detailed deployment wiring procedures, see [DEPLOYMENT-WIRING-NOTES.md](./DEPLOYMENT-WIRING-NOTES.md).

---

## Vercel Environment Variables

Configure these environment variables in Vercel dashboard → Project Settings → Environment Variables.

### Production Environment

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `VITE_API_URL` | Yes | `https://api.shiftcenter.com` | Backend API base URL |
| `VITE_AUTH_API` | Yes | `https://api.hodeia.me` | hodeia.me identity service URL |
| `VITE_GITHUB_CLIENT_ID` | No | `<from GitHub OAuth>` | GitHub OAuth Client ID (if OAuth is enabled) |

### Preview/Dev Environment

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `VITE_API_URL` | Yes | `https://<staging-url>.up.railway.app` | Railway staging URL or `https://api.simdecisions.com` |
| `VITE_AUTH_API` | Yes | `https://api.hodeia.me` | hodeia.me identity service URL |
| `VITE_GITHUB_CLIENT_ID` | No | `<from GitHub OAuth>` | GitHub OAuth Client ID (same as production) |

**Note:** All `VITE_*` variables are baked into the build at compile time. Changes require a new build/deployment.

---

## Railway Environment Variables

Configure these environment variables in Railway dashboard → Service → Variables.

### Required Variables

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `HIVENODE_MODE` | Yes | `cloud` | Deployment mode (must be `cloud` for Railway) |
| `PORT` | Auto-injected | `8080` | Railway auto-injects this — do NOT set manually |
| `DATABASE_URL` | Auto-injected | `postgresql://...` | Railway auto-injects from linked PostgreSQL service |
| `HIVENODE_RA96IT_PUBLIC_KEY` | Yes | `-----BEGIN PUBLIC KEY-----\n...` | RS256 PEM public key for JWT verification (from ra96it service) |
| `ANTHROPIC_API_KEY` | Yes | `sk-ant-...` | Anthropic API key (sync from Infisical) |
| `VOYAGE_API_KEY` | Yes | `<voyage key>` | Voyage AI API key (sync from Infisical) |

### Optional Variables

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `HIVENODE_INVENTORY_DATABASE_URL` | No | `postgresql://...` | Inventory database URL — defaults to Railway PostgreSQL if not set |
| `GITHUB_CLIENT_ID` | No | `<from GitHub OAuth>` | GitHub OAuth Client ID (if GitHub auth is enabled) |
| `GITHUB_CLIENT_SECRET` | No | `<from GitHub OAuth>` | GitHub OAuth Client Secret (if GitHub auth is enabled) |
| `HIVENODE_DISPLAY_NAME` | No | `ShiftCenter Cloud` | Optional display name (shown in identity endpoint) |

### MCP Queue Notifications (Added 2026-04-06)

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `MCP_ENABLED` | No (default: true) | `true` | Enable MCP queue event system |
| `SCHEDULER_MCP_PORT` | No (default: 8422) | `8422` | Scheduler MCP event receiver port |
| `DISPATCHER_MCP_PORT` | No (default: 8423) | `8423` | Dispatcher MCP event receiver port |
| `SCHEDULER_FALLBACK_INTERVAL` | No (default: 60) | `60` | Fallback polling interval (seconds) when MCP unavailable |
| `DISPATCHER_FALLBACK_INTERVAL` | No (default: 60) | `60` | Fallback refresh interval (seconds) when MCP unavailable |

**Note:** MCP queue notifications improve scheduler/dispatcher latency from 30s to <2s. System gracefully falls back to polling if MCP unavailable.

**Railway automatically injects `PORT` and `DATABASE_URL` when a PostgreSQL service is linked. Do NOT set these manually.**

---

## Build Verification Steps

Follow these steps to verify deployments before production cutover.

### 1. Verify Vercel Build Locally

Test the Vercel build process locally before deploying:

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npm run build
```

**Expected result:**
- Build succeeds (exit code 0)
- `browser/dist/` directory created
- `browser/dist/index.html` exists
- EGG files copied to `browser/dist/` (14+ `*.egg.md` files)

**Check build output:**
```bash
# Count files in dist/
ls browser/dist/ | wc -l
# Should be 15+ files (index.html + assets/ + EGG files)

# Verify EGG files exist
ls browser/dist/*.egg.md
# Should list: apps.egg.md, canvas.egg.md, chat.egg.md, code.egg.md, etc.
```

### 2. Verify Vercel Configuration

Ensure `vercel.json` at repo root is correct:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "buildCommand": "cd browser && npm run build",
  "outputDirectory": "browser/dist",
  "installCommand": "cd browser && npm install",
  "framework": null
}
```

**Key settings:**
- Build command: `cd browser && npm run build` (includes `npm run copy-eggs`)
- Output directory: `browser/dist`
- SPA rewrites: All routes fall back to `index.html`

### 3. Verify Railway Configuration

Ensure Railway service settings are correct:

**Start Command:**
```
python -m hivenode
```

Or equivalently:
```
hive
```

Both commands are equivalent — `hive` is a console script defined in `pyproject.toml` → `[project.scripts]`.

**Health Check:**
- Path: `/health`
- Timeout: 30 seconds
- Interval: 60 seconds

**Root Directory:**
- Leave empty (run from repo root)

### 4. Test Railway Start Command Locally

Verify the start command works locally:

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter

# Test with python -m
python -m hivenode

# Or test with console script (requires package install)
hive
```

**Expected result:**
- Server starts on port 8420 (local mode) or `$PORT` (cloud mode)
- No errors on startup
- Logs: `INFO: Uvicorn running on http://0.0.0.0:8420`

**Stop server:** `Ctrl+C`

---

## Health Check Verification

The hivenode API includes health endpoints for monitoring and liveness checks.

### Test Health Endpoints (Local)

```bash
# Start hivenode locally
python -m hivenode

# In another terminal, test main health endpoint:
curl http://localhost:8420/health

# Test scheduler MCP health (if running):
curl http://localhost:8422/health

# Test dispatcher MCP health (if running):
curl http://localhost:8423/health
```

**Expected response (hivenode):**
```json
{
  "status": "ok",
  "mode": "local",
  "version": "0.1.0",
  "uptime_s": 12.34
}
```

**Expected response (scheduler/dispatcher MCP):**
```json
{
  "status": "ok"
}
```

### Test Health Endpoint (Railway Staging)

```bash
# Replace <staging-url> with Railway staging URL from dashboard
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

**Note:** `mode` should be `"cloud"` for Railway deployments (set via `HIVENODE_MODE=cloud` env var).

### Test Health Endpoint (Railway Production)

```bash
curl https://api.shiftcenter.com/health
```

**Expected response:**
```json
{
  "status": "ok",
  "mode": "cloud",
  "version": "0.1.0",
  "uptime_s": 456.78
}
```

---

## Port Configuration

Railway auto-injects the `PORT` environment variable. Hivenode config automatically detects and uses this port when `HIVENODE_MODE=cloud`.

### Port Detection Logic

Source: `hivenode/config.py` lines 84-86

```python
# Port for cloud mode reads from $PORT (Railway convention)
if self.mode == "cloud" and "PORT" in os.environ:
    self.port = int(os.environ["PORT"])
```

### Port Defaults

| Environment | Port | Source |
|-------------|------|--------|
| Local mode | 8420 | Default in `hivenode/config.py` |
| Remote mode | 8420 | Default in `hivenode/config.py` |
| Cloud mode (Railway) | `$PORT` | Railway-injected environment variable |

**Note:** Railway auto-injects `PORT` (usually 8080 or similar). Do NOT set this manually in Railway dashboard.

---

## EGG File Handling

EGG files (`*.egg.md`) define the pane layout and app configuration for each ShiftCenter workspace.

### Development Mode

In development, EGG files are served via Vite plugin from `eggs/` directory:
- **Source:** `eggs/*.egg.md` (repo root)
- **Served at:** `http://localhost:5173/*.egg.md`
- **Plugin:** `serveEggs()` in `browser/vite.config.ts`

**No copies in `browser/public/` directory** — single source of truth in `eggs/`.

### Production Build (Vercel)

For production builds, EGG files are copied from `eggs/` to `browser/dist/`:
- **Build command:** `npm run build` (which runs `npm run copy-eggs && vite build`)
- **Copy script:** `browser/package.json` → `scripts.copy-eggs`
- **Target:** `browser/dist/*.egg.md`

After build:
```bash
ls browser/dist/*.egg.md
# Should list: apps.egg.md, canvas.egg.md, chat.egg.md, code.egg.md, efemera.egg.md, etc.
```

**Verification:** After deploying to Vercel, test EGG loading:
```bash
curl https://dev.shiftcenter.com/chat.egg.md
# Should return markdown content of chat.egg.md
```

---

## Railway Start Command

Railway should use one of these start commands (both are equivalent):

### Option 1: Direct Module Execution (Recommended)

```
python -m hivenode
```

### Option 2: Console Script (Requires Package Install)

```
hive
```

**Note:** The `hive` console script is defined in `pyproject.toml` → `[project.scripts]`:
```toml
[project.scripts]
hive = "hivenode.__main__:main"
```

Both commands invoke the same entry point: `hivenode.__main__:main()`.

**Configure in Railway:**
- Railway dashboard → Service Settings → Deploy → Start Command
- Enter: `python -m hivenode`

---

## Pre-Deployment Checklist

Use this checklist before deploying to production:

### Vercel (Frontend)

- [ ] `vercel.json` exists at repo root
- [ ] Build command includes `npm run copy-eggs` (via `npm run build`)
- [ ] Output directory is `browser/dist`
- [ ] Install command is `cd browser && npm install`
- [ ] SPA rewrites configured: `/(.*) → /index.html`
- [ ] Environment variables set (production and preview)
- [ ] Local build succeeds: `npm run build` in `browser/` directory
- [ ] EGG files copied to `browser/dist/` (14+ files)

### Railway (Backend)

- [ ] Start command: `python -m hivenode`
- [ ] Health check path: `/health`
- [ ] Root directory: (empty — run from repo root)
- [ ] Environment variables set (all required variables)
- [ ] `HIVENODE_MODE=cloud` is set
- [ ] `PORT` is NOT manually set (Railway auto-injects)
- [ ] `DATABASE_URL` is NOT manually set (Railway auto-injects from linked DB)
- [ ] Health endpoint returns 200: `curl <railway-url>/health`

### DNS (Cloudflare)

- [ ] `dev.shiftcenter.com` CNAME added (points to Vercel)
- [ ] `api.shiftcenter.com` CNAME updated (points to Railway)
- [ ] DNS propagation verified: `nslookup dev.shiftcenter.com`
- [ ] Production DNS unchanged until cutover approved

---

## Rollback Plan

If deployment issues occur, follow this rollback procedure:

### Vercel Rollback

1. **Revert to previous deployment:**
   - Vercel dashboard → Deployments → Select previous working deployment
   - Click "Promote to Production"
   - Vercel will redeploy the old version

2. **Or revert git commit:**
   ```bash
   git revert <commit-sha>
   git push origin main
   # Vercel auto-deploys from git push
   ```

### Railway Rollback

1. **Revert to previous deployment:**
   - Railway dashboard → Deployments → Select previous working deployment
   - Click "Redeploy"
   - Railway will redeploy the old version

2. **Or revert git commit:**
   ```bash
   git revert <commit-sha>
   git push origin main
   # Railway auto-deploys from git push
   ```

### DNS Rollback

1. **Revert DNS changes:**
   - Cloudflare → DNS → Edit CNAME record
   - Change target back to old deployment
   - TTL is Auto (5 minutes) — propagation takes 5-10 minutes

2. **Verify rollback:**
   ```bash
   nslookup dev.shiftcenter.com
   curl https://dev.shiftcenter.com/health
   ```

---

## Additional Resources

- **Full deployment wiring procedures:** [DEPLOYMENT-WIRING-NOTES.md](./DEPLOYMENT-WIRING-NOTES.md)
- **Smoke test procedures:** [DEPLOYMENT-WIRING-NOTES.md](./DEPLOYMENT-WIRING-NOTES.md) → Smoke Test Procedure section
- **Vercel docs:** https://vercel.com/docs
- **Railway docs:** https://docs.railway.app
- **Hivenode config:** `hivenode/config.py`
- **Vercel config:** `vercel.json` (repo root)
- **Package scripts:** `browser/package.json` → `scripts`

---

---

## MCP Queue Notifications (Added 2026-04-06)

The MCP (Message Control Protocol) queue notification system enables real-time event delivery from hivenode to scheduler and dispatcher daemons. This replaces polling-based detection, reducing latency from 30s to <2s.

### Architecture Overview

```
[Hivenode Watcher] → [MCP Event Broadcaster]
                            ↓
                      ┌─────┴─────┐
                      ↓           ↓
              [Scheduler]   [Dispatcher]
               (port 8422)  (port 8423)
```

### Configuration (Railway)

MCP is enabled by default. No additional configuration required.

**Optional tuning:**
```bash
# Disable MCP (fallback to polling)
MCP_ENABLED=false

# Change MCP ports (if conflicts)
SCHEDULER_MCP_PORT=9422
DISPATCHER_MCP_PORT=9423
```

### Health Checks (Railway)

Add these health check endpoints to Railway service settings:

| Service | Port | Health Check Path | Expected Response |
|---------|------|-------------------|-------------------|
| Hivenode | `$PORT` | `/health` | `{"status":"ok"}` |
| Scheduler MCP | 8422 | `/health` | `{"status":"ok"}` |
| Dispatcher MCP | 8423 | `/health` | `{"status":"ok"}` |

**Note:** Scheduler and dispatcher MCP servers run as background threads within hivenode process. No separate Railway services needed.

### Monitoring

Set up alerts for:
- MCP server downtime (health check 500 or timeout)
- High fallback poll rate (>10/hour indicates MCP issues)
- Event delivery failures (check hivenode logs)

**Event log:**
- File: `.deia/hive/queue_events.jsonl`
- Contains: All queue state change events (queued, active, done, dead)
- Rotation: Keep last 7 days (manual cleanup)

### Troubleshooting

**Scheduler not waking on completions:**
```bash
# Check MCP server health
curl http://localhost:8422/health

# Check event log
tail -n 20 .deia/hive/queue_events.jsonl

# Check scheduler logs
grep "MCP" .deia/hive/schedule_log.jsonl
```

**Dispatcher counters out of sync:**
```bash
# Check dispatcher status
curl http://localhost:8423/status

# Compare with actual file counts
ls .deia/hive/queue/_active/SPEC-*.md | wc -l
```

**Reference:** See `.deia/processes/P-SCHEDULER.md` and `.deia/processes/P-DISPATCHER.md` for detailed troubleshooting guides.

---

**Last updated:** 2026-04-06
**Deployment target:** `deiasolutions/shiftcenter` (main branch → production, dev branch → staging)
