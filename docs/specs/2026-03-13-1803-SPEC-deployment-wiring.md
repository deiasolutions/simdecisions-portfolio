# SPEC: Deployment Wiring — Repoint Vercel + Railway to ShiftCenter Repo

## Priority
P0

## Objective
Repoint the existing Vercel and Railway projects from the old `deiasolutions/platform` repo to the new `deiasolutions/shiftcenter` repo. Set up dev.shiftcenter.com as the dev branch preview. After this, pushing to `dev` auto-deploys to staging, pushing to `main` auto-deploys to production.

## Context
Deployment config notes are at `docs/DEPLOYMENT-WIRING-NOTES.md` and `.deia/config/deployment-env.md` in the repo. The old repo currently deploys:
- Vercel: `simdecisions-2/` → code.shiftcenter.com
- Railway: `simdecisions-2/api/` → api.simdecisions.com

The new repo needs:
- Vercel: `browser/` → code.shiftcenter.com (prod, main branch) + dev.shiftcenter.com (dev branch)
- Railway: `hivenode/` → api.shiftcenter.com (prod) + staging URL (dev)

Files to read first:
- `docs/DEPLOYMENT-WIRING-NOTES.md` — full migration plan
- `.deia/config/deployment-env.md` — env vars inventory
- `browser/vite.config.ts` — Vite build config
- `browser/package.json` — build scripts
- `hivenode/main.py` — FastAPI app entry point
- `pyproject.toml` — Python project config

## Acceptance Criteria

### Vercel
- [ ] Vercel project linked to `deiasolutions/shiftcenter` repo (not `platform`)
- [ ] Root directory set to `browser/`
- [ ] Production branch: `main`
- [ ] Preview branch: `dev` (and all PR branches)
- [ ] `dev.shiftcenter.com` CNAME added in Cloudflare pointing to Vercel
- [ ] Vercel custom domain `dev.shiftcenter.com` assigned to dev branch
- [ ] Env vars set: `VITE_API_URL` = `https://api.shiftcenter.com` (prod), staging URL (preview)
- [ ] `vercel.json` created in `browser/` with SPA fallback rewrites
- [ ] Test: push to dev → Vercel builds → dev.shiftcenter.com loads the chat app

### Railway
- [ ] Railway service linked to `deiasolutions/shiftcenter` repo
- [ ] Root directory set to `hivenode/`
- [ ] Start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
- [ ] Production branch: `main`
- [ ] Staging environment linked to `dev` branch (separate Railway environment if possible, or same service with branch deploy)
- [ ] Env vars carried over from old service: `DATABASE_URL` (auto), `SD_JWT_SECRET`, `SD_KEY_ENCRYPTION_SECRET`
- [ ] New env vars: `HIVENODE_MODE=cloud`, `ANTHROPIC_API_KEY` (server Haiku fallback)
- [ ] Health check: `GET /health` returns 200
- [ ] Test: push to dev → Railway builds → api endpoint responds to /health

### DNS (Cloudflare)
- [ ] `dev.shiftcenter.com` → Vercel CNAME (new)
- [ ] `api.shiftcenter.com` → Railway CNAME (verify existing or update)
- [ ] Existing production domains unchanged until cutover is verified

### Subdomain-to-EGG Routing
- [ ] Add hostname → EGG mapping in `browser/src/App.tsx` or `browser/src/shell/useEggInit.ts`:
  - `chat.efemera.live` → chat.egg.md
  - `code.shiftcenter.com` → code.egg.md (when it exists)
  - `pm.shiftcenter.com` → pm.egg.md (when it exists)
  - `dev.shiftcenter.com` → default to chat.egg.md, override with `?egg=name` query param
  - `localhost:5173` → chat.egg.md (dev default)
- [ ] Test: `dev.shiftcenter.com` loads chat app, `dev.shiftcenter.com?egg=chat` same result

### Do NOT Do
- Do NOT delete old Vercel/Railway projects — they stay live until cutover is verified
- Do NOT change production DNS for code.shiftcenter.com or api.simdecisions.com yet — those point at old deploys until we're confident
- Do NOT hardcode URLs — use environment variables for API URLs

## Smoke Test
- [ ] Push a commit to dev → Vercel preview builds successfully
- [ ] dev.shiftcenter.com loads in browser, shows the chat app
- [ ] Railway staging builds successfully
- [ ] API health endpoint responds at staging URL
- [ ] `?egg=chat` query param loads the chat EGG

## Model Assignment
sonnet

## Constraints
- This task requires access to Vercel CLI (`vercel`), Railway CLI (`railway`), and Cloudflare. The bee should use the CLIs already authenticated on this machine.
- GitHub auth: the repo is under `deiasolutions` org. Use `gh auth switch --user deiasolutions` if needed for Railway/Vercel linking.
- If Railway doesn't support branch-based staging easily, use a separate Railway service for staging with the dev branch.
