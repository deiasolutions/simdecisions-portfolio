# ShiftCenter Deployment Wiring

This document describes the deployment configuration for ShiftCenter:

- **Frontend (browser/)**: Deployed to **Vercel**
- **Backend (hivenode)**: Deployed to **Railway**

---

## Vercel — Frontend Deployment

### Configuration File
`vercel.json` at repo root:

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

### Build Process
1. **Install**: `cd browser && npm install`
2. **Build**: `cd browser && npm run build`
   - Runs `copy-eggs` script (copies `eggs/*.egg.md` to `browser/public/`)
   - Runs `vite build` (outputs to `browser/dist/`)
3. **Output**: `browser/dist/` directory

### Environment Variables (Vercel)
| Variable | Value | Purpose |
|----------|-------|---------|
| `NODE_ENV` | `production` | Node environment |
| `VITE_API_URL` | `https://hivenode-production.up.railway.app` | Backend API endpoint |

**Note:** Vite requires environment variables to be prefixed with `VITE_` to be accessible in the browser build.

### Vercel Project Settings
- **Framework Preset**: None (custom via vercel.json)
- **Root Directory**: Leave blank (repo root)
- **Build Command**: `cd browser && npm run build`
- **Output Directory**: `browser/dist`
- **Install Command**: `cd browser && npm install`

---

## Railway — Backend Deployment

### Configuration File
`railway.toml` at repo root:

```toml
[build]
# No build command needed — Railway auto-detects Python and runs pip install

[deploy]
# Start command for hivenode API server
startCommand = "python -m hivenode"

# Health check configuration
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### Build Process
1. **Railway auto-detects Python** via `pyproject.toml`
2. **Install dependencies**: `pip install -e .`
   - Installs all packages from `pyproject.toml` dependencies
3. **Start command**: `python -m hivenode`
   - Runs `hivenode/__main__.py:main()`
   - Starts Uvicorn server on `0.0.0.0:$PORT`

### Environment Variables (Railway)

#### Required
| Variable | Example Value | Purpose |
|----------|---------------|---------|
| `PORT` | `8420` | Port (Railway auto-sets this) |
| `HIVENODE_MODE` | `cloud` | Deployment mode (`local`, `remote`, or `cloud`) |
| `DATABASE_URL` | `postgresql://[REDACTED]@[REDACTED]/db` | PostgreSQL connection (Railway auto-provides) |

#### Optional
| Variable | Default | Purpose |
|----------|---------|---------|
| `HIVENODE_STORAGE_ROOT` | `~/.shiftcenter/storage` | File storage directory |
| `HIVENODE_LEDGER_DB_PATH` | `~/.shiftcenter/ledger.db` | Event ledger database |
| `HIVENODE_NODE_DB_PATH` | `~/.shiftcenter/nodes.db` | Node registry database |
| `HIVENODE_CLOUD_URL` | `https://hivenode-production.up.railway.app` | Cloud hub URL |
| `HIVENODE_DISPLAY_NAME` | `ShiftCenter Cloud` | Display name for node |
| `HIVENODE_RA96IT_PUBLIC_KEY` | `-----BEGIN PUBLIC KEY-----...` | ra96it JWT verification key |
| `HIVENODE_RA96IT_JWKS_URL` | `https://ra96it.com/.well-known/jwks.json` | JWKS endpoint for JWT verification |
| `HIVENODE_INVENTORY_DATABASE_URL` | `postgresql://...` | Inventory database (defaults to Railway PG) |
| `HIVENODE_RATE_LIMIT_AUTH` | `10` | Rate limit for auth endpoints |

### Health Check Endpoint
Railway uses `/health` to verify deployment health:

**Request:**
```
GET https://hivenode-production.up.railway.app/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "mode": "cloud",
  "timestamp": "2026-03-17T12:34:56Z"
}
```

---

## Connecting Frontend to Backend

### CORS Configuration
The backend (`hivenode/main.py`) is pre-configured with CORS origins:

```python
allow_origins=[
    "http://localhost:5173",  # Vite dev
    "http://localhost:3000",  # Alternative dev port
    "https://simdecisions.com",  # Current production
    "https://code.shiftcenter.com",  # ShiftCenter production
    "https://dev.shiftcenter.com",  # ShiftCenter dev
    "https://ra96it.com",  # ra96it login
    "https://dev.ra96it.com",  # ra96it dev login
    "https://efemera.live",  # Efemera
]
```

**Action Required**: Add your Vercel deployment domain to this list (e.g., `https://shiftcenter.vercel.app`).

### API Calls from Frontend
Frontend code should use the `VITE_API_URL` environment variable:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8420'

fetch(`${API_URL}/api/endpoint`)
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Verify `vercel.json` buildCommand and outputDirectory
- [ ] Verify `railway.toml` startCommand and healthcheckPath
- [ ] Set `VITE_API_URL` in Vercel environment variables
- [ ] Set `HIVENODE_MODE=cloud` in Railway environment variables
- [ ] Add Vercel domain to CORS allow_origins in `hivenode/main.py`

### Post-Deployment
- [ ] Test Vercel deployment: visit frontend URL
- [ ] Test Railway health endpoint: `curl https://<railway-url>/health`
- [ ] Test frontend-to-backend connection: check browser console for API errors
- [ ] Test auth flow: verify ra96it login redirects work

---

## Troubleshooting

### Frontend Build Fails
- **Issue**: `npm run build` fails
- **Check**: `cd browser && npm install && npm run build` locally
- **Common Causes**: Missing dependencies, TypeScript errors, Vite config issues

### Backend Health Check Fails
- **Issue**: Railway reports unhealthy after deploy
- **Check**: Railway logs for startup errors
- **Common Causes**: Missing `DATABASE_URL`, Python dependency issues, port binding errors

### Frontend Can't Reach Backend
- **Issue**: Browser console shows CORS or network errors
- **Check 1**: Verify `VITE_API_URL` is set in Vercel environment variables
- **Check 2**: Verify backend CORS includes Vercel domain
- **Check 3**: Verify Railway deployment is running (`/health` returns 200)

### Environment Variable Not Working
- **Issue**: Railway or Vercel env var doesn't take effect
- **Vercel**: Rebuild deployment after setting variables
- **Railway**: Redeploy after setting variables
- **Vite**: Environment variables MUST be prefixed with `VITE_` to be exposed to browser

---

## Local Development vs Production

| Aspect | Local | Production |
|--------|-------|------------|
| Frontend Port | 5173 (Vite dev) | 443 (Vercel HTTPS) |
| Backend Port | 8420 | Railway-assigned port |
| Database | SQLite (~/.shiftcenter/hivenode.db) | PostgreSQL (Railway) |
| CORS | localhost:5173 | Vercel domain |
| Mode | `HIVENODE_MODE=local` | `HIVENODE_MODE=cloud` |

---

## References

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Vite Env Variables**: https://vitejs.dev/guide/env-and-mode.html
- **FastAPI CORS**: https://fastapi.tiangolo.com/tutorial/cors/
