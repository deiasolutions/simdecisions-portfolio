# BL-066: Deployment wiring - repoint Vercel + Railway to shiftcenter repo

## Objective
Document and verify the deployment wiring so Vercel serves the frontend from shiftcenter repo and Railway serves the hivenode backend from shiftcenter repo.

## Context
Deployment needs to be wired: Vercel for frontend (browser/ build output), Railway for backend (hivenode). This may involve vercel.json config, Railway service config, build commands, and environment variable setup.

## Files to Read First
- `vercel.json` (if exists)
- `browser/vite.config.ts`
- `browser/package.json`
- `hivenode/`
- `railway.toml` or `railway.json` (if exists)
- `Procfile` (if exists)

## Deliverables
- [ ] Verify or create vercel.json with correct build settings for browser/
- [ ] Verify or create Railway config for hivenode
- [ ] Document required environment variables for both services
- [ ] Smoke test: Vercel preview build succeeds
- [ ] Smoke test: Railway deploy serves /health endpoint

## Acceptance Criteria
- [ ] Vercel config points to browser/ with correct build command
- [ ] Railway config points to hivenode with correct start command
- [ ] Environment variables documented
- [ ] Build verification passes

## Smoke Test
- [ ] Verify vercel.json or vercel project settings are correct
- [ ] Verify railway config is correct
- [ ] `cd browser && npm run build` succeeds

## Constraints
- No file over 500 lines
- No stubs
- Do not expose secrets in config files

## Model Assignment
sonnet

## Priority
P0
