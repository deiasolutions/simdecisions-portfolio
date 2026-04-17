# TASK-BL066: Deployment Wiring Verification

## Objective
Verify and document deployment wiring for Vercel (frontend) and Railway (backend) pointing to shiftcenter repo. Ensure configuration files are correct, build commands work, and all required environment variables are documented.

## Context
The `docs/DEPLOYMENT-WIRING-NOTES.md` file already exists with comprehensive documentation. This task verifies that the actual configuration files match the documented deployment plan, tests build processes locally, and fills any documentation gaps.

### Current State
- **Vercel config:** `vercel.json` exists at repo root with SPA rewrites configured
- **Railway config:** NO `railway.toml` or `Procfile` — Railway uses dashboard settings
- **Hivenode entry point:** `hivenode/__main__.py` with port auto-detection
- **Health endpoint:** `GET /health` exists at `hivenode/routes/health.py`
- **EGG files:** 14 EGG files in `eggs/` directory, served via Vite plugin in dev, copied via `npm run copy-eggs` for build
- **Deployment docs:** `docs/DEPLOYMENT-WIRING-NOTES.md` (765 lines, comprehensive)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\vercel.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vite.config.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\__main__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\health.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\pyproject.toml`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md`

## Deliverables

### 1. Create railway.toml (Optional)
Railway can be configured via dashboard OR via `railway.toml` file. Review Railway best practices and decide:
- **If railway.toml is recommended:** Create it with start command, health check path, port config
- **If dashboard-only is preferred:** Document in `docs/DEPLOYMENT.md` why no config file is needed

File location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\railway.toml` (if created)

**Expected content (if created):**
```toml
[build]

[deploy]
startCommand = "python -m hivenode"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### 2. Verify Vercel Configuration
Read `vercel.json` and verify:
- Build command includes `npm run copy-eggs` OR document that it's included in `npm run build`
- Output directory is `browser/dist`
- Install command is `cd browser && npm install`
- SPA rewrites are configured: `{ "source": "/(.*)", "destination": "/index.html" }`

If any issues found, document them in the response file.

### 3. Create docs/DEPLOYMENT.md
Create a concise deployment checklist document that supplements `docs/DEPLOYMENT-WIRING-NOTES.md`. This file should be a quick reference for required environment variables and verification steps.

File location: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT.md`

**Required sections:**
- Overview (1 paragraph)
- Vercel Environment Variables (table format)
- Railway Environment Variables (table format)
- Build Verification Steps (numbered list)
- Health Check Verification (curl command examples)
- Link to `DEPLOYMENT-WIRING-NOTES.md` for full procedures

**Environment Variables Tables:**

**Vercel (Frontend):**
| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `VITE_API_URL` | Yes | `https://api.shiftcenter.com` | Backend API base URL |
| `VITE_GITHUB_CLIENT_ID` | No | `<from GitHub OAuth>` | GitHub OAuth (if enabled) |
| `VITE_RA96IT_URL` | Yes | `https://api.ra96it.com` | ra96it identity service |

**Railway (Backend):**
| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `HIVENODE_MODE` | Yes | `cloud` | Deployment mode |
| `PORT` | Auto-injected | `8080` | Railway auto-injects this |
| `DATABASE_URL` | Auto-injected | `postgresql://...` | Railway auto-injects from linked DB |
| `HIVENODE_RA96IT_PUBLIC_KEY` | Yes | `<RS256 PEM public key>` | JWT verification key |
| `HIVENODE_INVENTORY_DATABASE_URL` | No | `<Railway PG URL>` | Defaults to Railway PG if not set |
| `ANTHROPIC_API_KEY` | Yes | `sk-ant-...` | Anthropic API key (from Infisical) |
| `VOYAGE_API_KEY` | Yes | `<voyage key>` | Voyage AI API key (from Infisical) |
| `GITHUB_CLIENT_ID` | No | `<from GitHub OAuth>` | GitHub OAuth (if enabled) |
| `GITHUB_CLIENT_SECRET` | No | `<from GitHub OAuth>` | GitHub OAuth (if enabled) |

### 4. Test: Vercel Build Locally
Run the Vercel build command locally and verify it succeeds. This confirms the build process works before deploying to Vercel.

**Command:**
```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npm run build
```

**Expected result:**
- Build succeeds (exit code 0)
- `browser/dist/` directory created
- `browser/dist/index.html` exists
- EGG files copied to `browser/dist/` OR accessible via Vite plugin (verify approach)

**Capture:**
- Last 10 lines of build output
- File count in `browser/dist/`
- Presence of EGG files (check if `*.egg.md` files exist in dist)

### 5. Test: Verify Health Endpoint Exists
Read `hivenode/routes/health.py` and confirm:
- Endpoint: `GET /health` exists
- Response includes: `status`, `mode`, `version`, `uptime_s`
- No code changes needed

If endpoint exists, document it. If not, flag as NEEDS_DAVE.

### 6. Document Railway Start Command
Verify the start command in `hivenode/__main__.py` and document the correct Railway start command.

**Expected start command:**
- `python -m hivenode` OR
- `hive` (console script from pyproject.toml)

**Verify:**
- Read `pyproject.toml` → `[project.scripts]` → confirm `hive = "hivenode.__main__:main"`
- Both commands should work

**Document in `docs/DEPLOYMENT.md`:**
```markdown
## Railway Start Command

Railway should use one of these start commands (both are equivalent):

1. `python -m hivenode` (direct module execution)
2. `hive` (console script, requires package install)

The start command is configured in Railway dashboard → Service Settings → Deploy → Start Command.
```

### 7. Document Port Configuration
Verify that `hivenode/config.py` respects Railway's `$PORT` environment variable.

**Read:**
- `hivenode/config.py` line 84-86 (cloud mode port detection)

**Expected behavior:**
```python
# Port for cloud mode reads from $PORT (Railway convention)
if self.mode == "cloud" and "PORT" in os.environ:
    self.port = int(os.environ["PORT"])
```

**Document in `docs/DEPLOYMENT.md`:**
```markdown
## Port Configuration

Railway auto-injects the `PORT` environment variable. Hivenode config automatically detects and uses this port when `HIVENODE_MODE=cloud`.

Default port (local/remote): 8420
Cloud port: `$PORT` (Railway-injected)
```

## Test Requirements

### Manual Tests (No Automated Tests Required)

**Test 1: Vercel build succeeds**
```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npm run build
```
- Verify: exit code 0, `browser/dist/` created

**Test 2: EGG files accessible**
- Check if EGG files are in `browser/dist/` OR
- Check if Vite plugin serves them from `eggs/` directory in dev mode
- Document approach in response file

**Test 3: Health endpoint exists**
- Read `hivenode/routes/health.py`
- Verify endpoint returns JSON with `status`, `mode`, `version`, `uptime_s`

**Test 4: Console script works**
- Verify `pyproject.toml` defines `hive` console script
- Document that `hive` and `python -m hivenode` are equivalent

## Constraints
- No file over 500 lines (DEPLOYMENT.md should be under 300 lines)
- No stubs
- No secrets in committed files (use placeholders like `<from Infisical>`)
- Do NOT run `git commit` (Queen will handle archival)
- Do NOT modify existing code files (only create/update documentation)

## Acceptance Criteria
- [ ] `railway.toml` created OR documented why it's not needed (in DEPLOYMENT.md)
- [ ] `docs/DEPLOYMENT.md` created with all required sections
- [ ] Vercel build test passes locally (last 10 lines of output captured)
- [ ] EGG file handling documented (copied to dist OR served via Vite plugin)
- [ ] Health endpoint verified (exists, correct response format)
- [ ] Railway start command documented (both `python -m hivenode` and `hive`)
- [ ] Port configuration documented (Railway $PORT auto-detection)
- [ ] All environment variables documented in tables

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260317-BL066-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — manual tests run, outcomes
5. **Build Verification** — Vercel build output (last 10 lines), dist file count, EGG file check
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any issues, recommended next tasks

DO NOT skip any section.

## Model Assignment
sonnet

## Priority
P0
