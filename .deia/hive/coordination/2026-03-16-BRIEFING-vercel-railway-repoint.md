# BRIEFING: Vercel + Railway Repoint to ShiftCenter Repo

**Date:** 2026-03-16
**From:** Q33NR
**To:** Q33N
**Spec:** `2026-03-16-3000-SPEC-w3-01-vercel-railway-repoint.md`
**Priority:** P1

---

## Objective

Repoint existing Vercel project and Railway service from `deiasolutions/platform` to `deiasolutions/shiftcenter`. Set up dev branch preview at `dev.shiftcenter.com`. Do NOT change production DNS or delete old projects.

---

## Context Files Read

- `docs/DEPLOYMENT-WIRING-NOTES.md` — comprehensive repoint procedure, DNS config, smoke tests
- `.deia/config/deployment-env.md` — environment variables checklist
- `browser/vite.config.ts` — current Vite config (basic, needs `vercel.json`)
- `hivenode/main.py` — CORS already includes `dev.shiftcenter.com`
- `pyproject.toml` — dependencies and project metadata

---

## Key Requirements

### 1. Vercel Repoint
- Link to `deiasolutions/shiftcenter`, root dir `browser/`
- Production branch: `main` → code.shiftcenter.com
- Preview branch: `dev` → dev.shiftcenter.com (new custom domain)
- Create `browser/vercel.json` with SPA fallback rewrites
- Set env vars: `VITE_API_URL`, `VITE_GITHUB_CLIENT_ID`, `VITE_RA96IT_URL`

### 2. Railway Repoint
- Link to `deiasolutions/shiftcenter`, root dir (empty)
- Start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
- Health check: `GET /health` (already exists)
- Add env vars: `HIVENODE_MODE=cloud`, `RA96IT_PUBLIC_KEY`, `FRONTEND_URL`
- Rename: `SD_GITHUB_CLIENT_ID` → `GITHUB_CLIENT_ID`, `SD_GITHUB_CLIENT_SECRET` → `GITHUB_CLIENT_SECRET`
- Drop: `SD_JWT_SECRET`, `SD_FRONTEND_URL`

### 3. DNS (Cloudflare)
- Add CNAME: `dev.shiftcenter.com` → Vercel target (proxied)
- Do NOT touch production DNS (`code.shiftcenter.com`, `api.shiftcenter.com`)

### 4. Smoke Tests
- Push to dev → Vercel builds
- Push to dev → Railway builds
- `dev.shiftcenter.com` loads chat app
- Railway `/health` returns 200

---

## Task Breakdown

This is a **configuration and deployment wiring task** — no code changes except adding `vercel.json`. The tasks will be documentation-focused with verification steps.

### Proposed Tasks

1. **TASK-191: Create vercel.json for SPA Fallback**
   - Deliverable: `browser/vercel.json` with SPA rewrites
   - Test: Build locally, verify config is valid

2. **TASK-192: Document Vercel Repoint Procedure**
   - Deliverable: Step-by-step instructions to repoint Vercel (based on DEPLOYMENT-WIRING-NOTES.md)
   - Test: None (documentation only)

3. **TASK-193: Document Railway Repoint Procedure**
   - Deliverable: Step-by-step instructions to repoint Railway (based on DEPLOYMENT-WIRING-NOTES.md)
   - Test: None (documentation only)

4. **TASK-194: Document DNS Configuration**
   - Deliverable: Step-by-step instructions to add `dev.shiftcenter.com` CNAME (based on DEPLOYMENT-WIRING-NOTES.md)
   - Test: None (documentation only)

5. **TASK-195: Document Smoke Test Procedure**
   - Deliverable: Smoke test checklist and verification steps (based on DEPLOYMENT-WIRING-NOTES.md)
   - Test: None (documentation only)

**Note:** The actual execution of Vercel/Railway/DNS configuration is manual (via dashboards/CLI). The bees will create the necessary files and documentation to guide Q88N through the repoint.

---

## Files to Create/Modify

- `browser/vercel.json` (new)
- `.deia/hive/tasks/2026-03-16-TASK-191-vercel-json.md` (Q33N creates)
- `.deia/hive/tasks/2026-03-16-TASK-192-doc-vercel-repoint.md` (Q33N creates)
- `.deia/hive/tasks/2026-03-16-TASK-193-doc-railway-repoint.md` (Q33N creates)
- `.deia/hive/tasks/2026-03-16-TASK-194-doc-dns-config.md` (Q33N creates)
- `.deia/hive/tasks/2026-03-16-TASK-195-doc-smoke-tests.md` (Q33N creates)

---

## Constraints

- **Rule 10:** No git operations without Q88N approval (bees create files, Q88N commits)
- **No production impact:** Old Vercel/Railway projects stay live until cutover verified
- **No deletion:** Do NOT delete old projects
- **Manual steps:** Vercel CLI, Railway dashboard, Cloudflare DNS — all executed by Q88N, not bees

---

## Model Assignment

- **TASK-191 (vercel.json):** haiku (simple JSON file)
- **TASK-192-195 (documentation):** haiku (copy/extract from existing docs)

---

## Success Criteria

- [ ] `browser/vercel.json` created with SPA fallback rewrites
- [ ] Task files provide clear step-by-step instructions for Q88N
- [ ] All 5 tasks reference `docs/DEPLOYMENT-WIRING-NOTES.md` as source
- [ ] No code changes to backend or frontend logic
- [ ] No git commits without Q88N approval

---

## Q33N Next Steps

1. Read this briefing
2. Read `docs/DEPLOYMENT-WIRING-NOTES.md` sections:
   - Vercel: Browser App (lines 11-130)
   - Railway: Hivenode API (lines 132-310)
   - DNS Configuration (lines 312-423)
   - Smoke Test Procedure (lines 425-740)
3. Write task files for TASK-191 through TASK-195
4. Return task files to Q33NR for review
5. Wait for Q33NR approval before dispatching bees

---

**End of Briefing**
