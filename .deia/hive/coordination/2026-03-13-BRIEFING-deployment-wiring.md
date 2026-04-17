# Q33N Briefing: Deployment Wiring — Repoint Vercel + Railway

**Date:** 2026-03-13
**From:** Q88NR-bot (regent)
**To:** Q33N (coordinator)
**Spec:** `.deia/hive/queue/2026-03-13-1803-SPEC-deployment-wiring.md`

---

## Mission

Repoint Vercel and Railway deployments from `deiasolutions/platform` repo to `deiasolutions/shiftcenter` repo. Set up `dev.shiftcenter.com` as the dev branch preview. After this task:
- Pushing to `dev` auto-deploys to staging (both Vercel and Railway)
- Pushing to `main` auto-deploys to production (both Vercel and Railway)

---

## Context Files

Q33N, you MUST read these files first:
- `.deia/config/deployment-env.md` — env var inventory, repoint checklist, domain strategy
- `browser/vite.config.ts` — Vite build config
- `browser/package.json` — build scripts
- `hivenode/main.py` — FastAPI app entry, lifespan, CORS
- `pyproject.toml` — Python project config
- `browser/src/App.tsx` — root component
- `browser/src/shell/useEggInit.ts` — EGG initialization hook
- `browser/src/eggs/eggResolver.ts` — hostname → EGG mapping logic
- `hivenode/routes/health.py` — health check endpoint (already exists)

---

## Current State

### Browser
- Vite app in `browser/`
- Build: `npm run build` → `browser/dist/`
- Dev: `npm run dev` (port 5173)
- Public files: `../eggs` (symlink from `publicDir` in vite.config.ts)
- Current hostname → EGG resolution: `resolveCurrentEgg()` in `eggResolver.ts`
  - Priority: `?egg=` URL param > pathname > hostname mapping > fallback
  - Fallback: `chat` (hardcoded, should match routing.config.egg once loaded)

### Hivenode
- FastAPI app in `hivenode/`
- Entry: `hivenode.main:app`
- Health check: `GET /health` (already exists at `hivenode/routes/health.py`)
- CORS origins: localhost:5173, localhost:3000, `*.shiftcenter.app` (line 233-237 in main.py)
- Start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`

### Deployment Docs
- Full env var inventory: `.deia/config/deployment-env.md`
- No deployment notes file yet (spec mentioned `docs/DEPLOYMENT-WIRING-NOTES.md` but it doesn't exist)

---

## Acceptance Criteria Breakdown

### 1. Vercel Configuration
- [ ] Create `browser/vercel.json` with:
  - SPA fallback (rewrites all routes to `/index.html` for client-side routing)
  - Optional: build settings, output directory override (if needed)
- [ ] Document Vercel CLI steps in a new file: `docs/DEPLOYMENT-WIRING-NOTES.md`
  - Link repo: `vercel link --repo deiasolutions/shiftcenter`
  - Set root directory: `browser/`
  - Set production branch: `main`
  - Add preview branch: `dev`
  - Set env vars: `VITE_API_URL` (production: `https://api.shiftcenter.com`, preview: staging URL or same prod URL initially)
  - Add custom domains: `code.shiftcenter.com` (prod), `dev.shiftcenter.com` (dev branch)
- [ ] **DO NOT** execute the actual Vercel repoint yet — this task is about wiring, not cutting over

### 2. Railway Configuration
- [ ] Document Railway CLI steps in `docs/DEPLOYMENT-WIRING-NOTES.md`
  - Link repo: `railway link --repo deiasolutions/shiftcenter`
  - Set root directory: (empty — defaults to repo root)
  - Set start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
  - Set production branch: `main`
  - Create staging environment (or link `dev` branch to same service if Railway doesn't support separate envs easily)
  - Carry over env vars from old service (documented in `.deia/config/deployment-env.md`):
    - `HIVENODE_MODE=cloud`
    - `ANTHROPIC_API_KEY` (from Infisical)
    - `VOYAGE_API_KEY` (from Infisical)
    - `RA96IT_PUBLIC_KEY` (from old service)
    - `FRONTEND_URL` (initially `https://simdecisions.com`, later `https://shiftcenter.com`)
    - `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET` (renamed from `SD_GITHUB_CLIENT_ID`, `SD_GITHUB_CLIENT_SECRET`)
    - `DATABASE_URL` (auto-injected by Railway from shared Postgres)
  - Drop old env vars: `SD_JWT_SECRET`, `SD_FRONTEND_URL`
- [ ] Verify health check endpoint: `GET /health` returns 200 (already exists, no code changes needed)
- [ ] **DO NOT** execute the actual Railway repoint yet — this task is about wiring, not cutting over

### 3. DNS Configuration (Cloudflare)
- [ ] Document DNS steps in `docs/DEPLOYMENT-WIRING-NOTES.md`
  - Add CNAME: `dev.shiftcenter.com` → Vercel (after Vercel custom domain is configured)
  - Verify existing CNAME: `api.shiftcenter.com` → Railway (should already exist or update after Railway repoint)
- [ ] **DO NOT** change production DNS yet — old deploys stay live until cutover is verified

### 4. Subdomain-to-EGG Routing
- [ ] Update `browser/src/eggs/eggResolver.ts`:
  - Add hostname → EGG mapping:
    - `chat.efemera.live` → `chat`
    - `code.shiftcenter.com` → `code` (when code.egg.md exists)
    - `pm.shiftcenter.com` → `pm` (when pm.egg.md exists)
    - `dev.shiftcenter.com` → fallback to `chat`, override with `?egg=name` query param
    - `localhost:5173` → `chat` (dev default)
  - Ensure query param override (`?egg=`) still works (already implemented, just verify)
- [ ] **Test coverage:**
  - Add test cases to `browser/src/eggs/__tests__/eggResolver.test.ts` (or create if doesn't exist)
    - Test hostname mappings
    - Test query param override
    - Test pathname fallback

### 5. Smoke Test
- [ ] Document smoke test procedure in `docs/DEPLOYMENT-WIRING-NOTES.md`:
  - Push commit to `dev` branch
  - Verify Vercel preview builds successfully
  - Open `dev.shiftcenter.com` in browser → should load chat app
  - Verify Railway staging builds successfully
  - Verify `GET https://<staging-url>/health` returns 200
  - Verify `dev.shiftcenter.com?egg=chat` loads chat EGG (same as default)
- [ ] **DO NOT** execute smoke test yet — this task creates the wiring, not the cutover

---

## Constraints

- **CLI Access:** The bee will have access to `vercel` CLI, `railway` CLI, and `gh` CLI (GitHub).
- **GitHub Auth:** Repo is under `deiasolutions` org. Use `gh auth switch --user deiasolutions` if needed.
- **Railway Staging:** If Railway doesn't support branch-based staging easily, document how to create a separate Railway service for staging with the `dev` branch.
- **Do NOT delete old projects:** Old Vercel/Railway projects stay live until cutover is verified.
- **Do NOT change production DNS:** `code.shiftcenter.com` and `api.simdecisions.com` point at old deploys until we're confident.
- **No hardcoded URLs:** Use environment variables for API URLs.

---

## Deliverables

Q33N, you will create task files for the following:

1. **TASK-058: Create Vercel Configuration + Documentation**
   - Create `browser/vercel.json` (SPA fallback rewrites)
   - Create `docs/DEPLOYMENT-WIRING-NOTES.md` (Vercel CLI steps, env vars, custom domains)
   - **Tests:** None required (config file, manual steps)
   - **Files modified:**
     - `browser/vercel.json` (new)
     - `docs/DEPLOYMENT-WIRING-NOTES.md` (new, Vercel section)

2. **TASK-059: Document Railway Configuration + Env Vars**
   - Add Railway section to `docs/DEPLOYMENT-WIRING-NOTES.md` (CLI steps, start command, env vars, staging setup)
   - Verify health check endpoint exists (already at `hivenode/routes/health.py`, no changes needed)
   - **Tests:** None required (documentation, no code changes)
   - **Files modified:**
     - `docs/DEPLOYMENT-WIRING-NOTES.md` (Railway section)

3. **TASK-060: Document DNS Configuration (Cloudflare)**
   - Add DNS section to `docs/DEPLOYMENT-WIRING-NOTES.md` (CNAME steps for `dev.shiftcenter.com`, verify `api.shiftcenter.com`)
   - **Tests:** None required (documentation, manual steps)
   - **Files modified:**
     - `docs/DEPLOYMENT-WIRING-NOTES.md` (DNS section)

4. **TASK-061: Update Subdomain-to-EGG Routing**
   - Update `browser/src/eggs/eggResolver.ts`:
     - Add hostname mappings: `chat.efemera.live`, `code.shiftcenter.com`, `pm.shiftcenter.com`, `dev.shiftcenter.com`, `localhost:5173`
     - Verify query param override still works
   - Add test coverage: `browser/src/eggs/__tests__/eggResolver.test.ts`
     - Test hostname mappings (5 hostnames)
     - Test query param override (1 test)
     - Test pathname fallback (1 test)
   - **Tests:** 7 new tests in `eggResolver.test.ts`
   - **Files modified:**
     - `browser/src/eggs/eggResolver.ts` (hostname mappings)
     - `browser/src/eggs/__tests__/eggResolver.test.ts` (7 new tests)

5. **TASK-062: Document Smoke Test Procedure**
   - Add smoke test section to `docs/DEPLOYMENT-WIRING-NOTES.md`
   - List all verification steps (Vercel build, Railway build, health endpoint, EGG loading)
   - **Tests:** None required (documentation, manual steps)
   - **Files modified:**
     - `docs/DEPLOYMENT-WIRING-NOTES.md` (smoke test section)

---

## Task File Requirements

Each task file MUST include:
- **Absolute file paths** (e.g., `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vercel.json`)
- **Test requirements** (count, scenarios, files)
- **Model assignment:** Sonnet (per spec)
- **Response file template** (8-section format)

---

## Notes for Q33N

- This is a **documentation + configuration task**, not a code implementation task.
- Only TASK-061 involves code changes (eggResolver.ts + tests).
- TASK-058, 059, 060, 062 are pure documentation (no TDD required).
- TASK-061 requires TDD: write 7 tests first, then update eggResolver.ts.
- The bee will have access to Vercel CLI, Railway CLI, and gh CLI — document the commands, but DO NOT execute them yet.
- The spec says "DO NOT delete old projects, DO NOT change production DNS" — enforce this in the task files.
- Smoke test is documented, not executed (this task is wiring, not cutover).

---

## Approval Checklist

Before dispatching tasks, verify:
- [ ] All file paths are absolute (Windows format: `C:\Users\davee\...`)
- [ ] Test requirements specified for TASK-061 (7 tests)
- [ ] No TDD requirement for TASK-058, 059, 060, 062 (docs/config only)
- [ ] Response file template included in all task files
- [ ] Model assignment: Sonnet
- [ ] No file over 500 lines (eggResolver.ts is ~118 lines, safe to edit)
- [ ] No stubs or TODOs (if bee can't finish, must say so)

---

**Q33N, write the 5 task files and submit for Q88NR approval.**
