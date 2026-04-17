# Deployment Architecture

**Platform:** Railway + Vercel
**Services:** 2 Railway services, 1 Vercel deployment
**Uptime Evidence:** 5.2 days verified (hivenode service)
**Date:** April 2026

---

## Service Topology

```
GitHub (main branch)
    ↓ push
    ├─→ Vercel (browser SPA)
    │   ├─→ shiftcenter.com
    │   ├─→ efemera.live
    │   ├─→ simdecisions.com
    │   └─→ hodeia.me
    │       ↓ proxy rules
    └─→ Railway
        ├─→ hivenode service (FastAPI)
        │   ├─→ /api/* routes
        │   ├─→ /relay/* (message bus)
        │   ├─→ /llm/* (LLM routing)
        │   ├─→ /rag/* (RAG pipeline)
        │   ├─→ /storage/* (file storage)
        │   └─→ /build/* (build monitor)
        └─→ beneficial-cooperation service (hodeia_auth)
            ├─→ /auth/* (SSO)
            ├─→ /token/* (JWT refresh)
            └─→ /dev-login/* (dev mode)

PostgreSQL (Railway)
    ↑ shared by both services
```

---

## Vercel Configuration

**Build Command:** `cd browser && npm run build`
**Output Directory:** `browser/dist`
**Framework:** React (Vite)
**Routing:** SPA with client-side routing (rewrites to `index.html`)

**Proxy Rules (vercel.json):**

```json
{
  "rewrites": [
    { "source": "/api/:path*", "destination": "https://hivenode-production.up.railway.app/api/:path*" },
    { "source": "/relay/:path*", "destination": "https://hivenode-production.up.railway.app/relay/:path*" },
    { "source": "/llm/:path*", "destination": "https://hivenode-production.up.railway.app/llm/:path*" },
    { "source": "/rag/:path*", "destination": "https://hivenode-production.up.railway.app/rag/:path*" },
    { "source": "/storage/:path*", "destination": "https://hivenode-production.up.railway.app/storage/:path*" },
    { "source": "/build/:path*", "destination": "https://hivenode-production.up.railway.app/build/:path*" },
    { "source": "/auth/:path*", "destination": "https://beneficial-cooperation-production.up.railway.app/auth/:path*" },
    { "source": "/token/:path*", "destination": "https://beneficial-cooperation-production.up.railway.app/token/:path*" },
    { "source": "/dev-login/:path*", "destination": "https://beneficial-cooperation-production.up.railway.app/dev-login/:path*" }
  ]
}
```

**Domains:**

- `shiftcenter.com` → primary product
- `efemera.live` → ephemeral workspace
- `simdecisions.com` → simulation engine
- `hodeia.me` → auth service

All domains point to same Vercel deployment, API routes proxy to Railway backends.

---

## Railway Configuration (hivenode service)

**Dockerfile:** Root `Dockerfile`
**Build:** Multi-stage Docker build
**Health Check:** `/health` endpoint (120s timeout)
**Restart Policy:** `ON_FAILURE` (max 3 retries)
**Port:** Dynamic (`$PORT` env var)

**Dockerfile (simplified):**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -e .
COPY hivenode/ hivenode/
COPY simdecisions/ simdecisions/
COPY _tools/ _tools/
CMD ["uvicorn", "hivenode.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--log-level", "info"]
```

**Environment Variables:**

- `HIVENODE_MODE=cloud` (triggers Railway-specific config)
- `PORT` (Railway injects this)
- `DATABASE_URL` (PostgreSQL connection string)
- `ANTHROPIC_API_KEY` (LLM access)
- `GOOGLE_GENERATIVE_AI_API_KEY` (Gemini access)

**Health Endpoint:**

```bash
GET https://hivenode-production.up.railway.app/health
{
  "status": "ok",
  "uptime": 447869,  // seconds (5.2 days)
  "mode": "cloud",
  "services": {
    "database": "connected",
    "ledger": "initialized",
    "storage": "ready",
    "scheduler": "running"
  }
}
```

**Verified Uptime:** 447,869 seconds (~5.2 days) as of snapshot date.

---

## Railway Configuration (beneficial-cooperation service)

**Dockerfile:** `hodeia_auth/Dockerfile`
**Build:** Separate Dockerfile for auth service
**Health Check:** `/health` endpoint
**Port:** Dynamic (`$PORT` env var)

**Purpose:** Centralized authentication service for all products. JWT issuance, refresh, cross-app SSO.

**Dockerfile (simplified):**

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY hodeia_auth/pyproject.toml .
RUN pip install -e .
COPY hodeia_auth/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

**Environment Variables:**

- `DATABASE_URL` (same PostgreSQL as hivenode)
- `JWT_SECRET_KEY` (shared secret for JWT validation)

---

## PostgreSQL (Railway)

**Provider:** Railway managed PostgreSQL
**Endpoint:** `gondola.proxy.rlwy.net:11875` (example endpoint)
**Shared by:** hivenode service + beneficial-cooperation service
**Schema:** Separate schemas per service (`public` for hivenode, `auth` for hodeia_auth)

**Tables (hivenode schema):**

- `inv_features` (feature inventory)
- `inv_backlog` (backlog items)
- `inv_bugs` (bug tracking)
- `inv_estimates` (estimation calibration)
- `inv_calibration` (per-type calibration factors)
- `event_ledger` (append-only event log)
- `stage_log` (stage transitions)

**Tables (auth schema):**

- `users` (user accounts)
- `sessions` (JWT sessions)
- `tokens` (refresh tokens)

---

## CI/CD Flow

**Trigger:** `git push origin main`

**Vercel:**

1. Detect push to `main` branch
2. Clone repo
3. `cd browser && npm run build`
4. Deploy to CDN (global edge)
5. Update DNS for all 4 domains
6. Deploy preview: `deploy-xyz123.vercel.app`
7. Promote to production

**Railway (hivenode):**

1. Detect push to `main` branch
2. Clone repo
3. Build Dockerfile (multi-stage)
4. Push image to Railway registry
5. Start new container with `$PORT` env var
6. Wait for `/health` endpoint to return HTTP 200 (120s timeout)
7. If healthy: swap traffic to new container
8. If unhealthy: rollback to previous container

**Railway (beneficial-cooperation):**

1. Same flow as hivenode
2. Separate Dockerfile (`hodeia_auth/Dockerfile`)
3. Separate health check

**Deployment Time:** ~2-3 minutes (Vercel), ~3-5 minutes (Railway)

---

## Environment Parity

**Dev/Prod Parity Principle:** Same code runs everywhere.

| Aspect | Local Dev | Railway Production |
|--------|-----------|-------------------|
| **Dockerfile** | Same | Same |
| **Python Version** | 3.12 | 3.12 |
| **Database** | SQLite (edge) | PostgreSQL (cloud) |
| **Port** | 8420 (hardcoded) | `$PORT` (dynamic) |
| **Config** | `HIVENODE_MODE=local` | `HIVENODE_MODE=cloud` |
| **Health Check** | `localhost:8420/health` | `*.railway.app/health` |

**Mode-aware Config (hivenode/config.py):**

```python
import os

MODE = os.getenv("HIVENODE_MODE", "local")

if MODE == "cloud":
    PORT = int(os.getenv("PORT", 8000))
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    PORT = 8420
    DATABASE_URL = "sqlite:///[REDACTED].db"
```

---

## Observability

**Logs:** Railway dashboard (live tail), Vercel dashboard (build logs + function logs)
**Metrics:** Railway built-in (CPU, memory, network), Vercel analytics (requests, bandwidth)
**Alerts:** Railway restart alerts (email), Vercel deployment failure alerts (email)
**Uptime Monitoring:** Manual health check polling (TODO: add UptimeRobot)

---

## Disaster Recovery

**Backup:** PostgreSQL daily snapshots (Railway managed)
**Rollback:** Railway "Revert to previous deployment" button (1-click)
**Failover:** Not implemented (single-region deployment)
**Data Loss:** Max 24 hours (daily backup cadence)

**Incident Response:**

1. Railway dashboard → "Deployments" → find last known-good deployment
2. Click "Redeploy" → promotes previous image to production
3. Rollback time: ~2 minutes
4. Data loss: 0 (PostgreSQL not affected by code rollback)

---

## Cost Structure

**Vercel:** Free tier (hobby account), $0/month
**Railway:** ~$20/month (2 services + PostgreSQL)
**Total:** ~$20/month for production infrastructure

**Scaling Strategy:** Vertical scaling (Railway auto-scales RAM/CPU within service limits). If traffic exceeds single-service capacity, horizontal scaling requires multi-instance deployment (not yet implemented).

---

## Security

**TLS:** Enforced everywhere (Vercel + Railway terminate TLS)
**Secrets:** Railway environment variables (encrypted at rest)
**Database:** Railway private network (not exposed to internet)
**Auth:** JWT (hodeia_auth service), HTTPS-only cookies
**CORS:** Configured in `hivenode/main.py` to allow Vercel domains only

---

## 12-Factor Compliance Checklist

| Factor | Evidence |
|--------|----------|
| **I. Codebase** | Single repo → Railway (2 services) + Vercel (4 domains) |
| **II. Dependencies** | `pyproject.toml`, `package.json`, pinned in Dockerfile |
| **III. Config** | `railway.toml` env vars, `HIVENODE_MODE`, `DATABASE_URL`, `PORT` |
| **IV. Backing Services** | PostgreSQL as attached resource (connection string via env) |
| **V. Build, Release, Run** | GitHub → Railway/Vercel CI/CD (build → release → run separation) |
| **VI. Processes** | Stateless hivenode (state in PostgreSQL, not in-process) |
| **VII. Port Binding** | FastAPI binds `$PORT` from Railway env |
| **VIII. Concurrency** | Separate scheduler/dispatcher/triage processes (horizontal scaling ready) |
| **IX. Disposability** | Fast startup (<30s), graceful shutdown, restart policy (ON_FAILURE) |
| **X. Dev/Prod Parity** | Same Dockerfile, same code paths, mode-aware config |
| **XI. Logs** | Stdout/stderr → Railway logs dashboard, Event Ledger as structured stream |
| **XII. Admin Processes** | `_tools/` scripts, one-off bee tasks (run same codebase) |

---

## Future Enhancements

1. **Blue-Green Deployment:** Railway supports this, not yet configured
2. **Auto-scaling:** Horizontal pod autoscaling based on CPU/memory
3. **Multi-region:** Deploy to US-East + EU-West for latency reduction
4. **CDN:** Vercel already provides global CDN for static assets
5. **Monitoring:** Add Datadog/Sentry for error tracking
6. **Load Testing:** Benchmark max throughput (current bottleneck: PostgreSQL connection pool)

---

**END OF DEPLOYMENT ARCHITECTURE DOCUMENTATION**
