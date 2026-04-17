# Q33N Task Approval Request — Deployment Wiring

**Date:** 2026-03-13
**Bot ID:** QUEEN-2026-03-13-BRIEFING-deployment
**Briefing:** `.deia/hive/coordination/2026-03-13-BRIEFING-deployment-wiring.md`
**Spec:** `.deia/hive/queue/2026-03-13-1803-SPEC-deployment-wiring.md`

---

## Summary

Q33N has created **5 task files** to wire Vercel and Railway deployments from `deiasolutions/platform` to `deiasolutions/shiftcenter`. All tasks are documentation and configuration only — no code execution, no cutover, no production impact.

**Task breakdown:**
1. **TASK-058:** Vercel config + docs (vercel.json, Vercel section)
2. **TASK-059:** Railway docs + health check verification (Railway section)
3. **TASK-060:** DNS docs (Cloudflare section)
4. **TASK-061:** Subdomain → EGG routing (eggResolver.ts + 7 tests)
5. **TASK-062:** Smoke test docs (7-test procedure)

**Only TASK-061 involves code changes** (eggResolver.ts + tests). All other tasks are pure documentation.

---

## Task Files Created

All task files written to: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\`

1. `2026-03-13-TASK-058-vercel-config-docs.md` (Vercel config + docs)
2. `2026-03-13-TASK-059-railway-config-docs.md` (Railway docs + health check)
3. `2026-03-13-TASK-060-dns-config-docs.md` (DNS docs)
4. `2026-03-13-TASK-061-subdomain-egg-routing.md` (eggResolver.ts + 7 tests)
5. `2026-03-13-TASK-062-smoke-test-docs.md` (smoke test procedure)

---

## Task Details

### TASK-058: Vercel Config + Docs
**Files modified:**
- `browser/vercel.json` (new) — SPA fallback rewrites
- `docs/DEPLOYMENT-WIRING-NOTES.md` (new) — Vercel section

**Deliverables:**
- Create `vercel.json` with SPA fallback (`"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]`)
- Document Vercel CLI repoint procedure:
  - `vercel link` to repoint repo
  - Set root directory: `browser/`
  - Set production branch: `main`
  - Add preview branch: `dev`
  - Set env vars: `VITE_API_URL`, `VITE_GITHUB_CLIENT_ID`, `VITE_RA96IT_URL`
  - Add custom domain: `dev.shiftcenter.com` → `dev` branch
- Document DNS steps (Cloudflare CNAME for dev.shiftcenter.com)

**Tests:** None (config + docs only)

**Model:** sonnet

**Constraints:**
- DO NOT execute Vercel repoint
- DO NOT delete old Vercel project
- DO NOT change production DNS

---

### TASK-059: Railway Docs + Health Check
**Files modified:**
- `docs/DEPLOYMENT-WIRING-NOTES.md` (append Railway section)

**Deliverables:**
- Document Railway CLI repoint procedure:
  - `railway link` to repoint repo
  - Set root directory: (empty)
  - Set start command: `uvicorn hivenode.main:app --host 0.0.0.0 --port $PORT`
  - Set production branch: `main`
  - Create staging environment for `dev` branch
  - Set env vars: `HIVENODE_MODE`, `RA96IT_PUBLIC_KEY`, `FRONTEND_URL`, carry over `DATABASE_URL`, `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, rename `GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`
  - Drop old env vars: `SD_JWT_SECRET`, `SD_FRONTEND_URL`
- Verify health check exists at `hivenode/routes/health.py` (already implemented, no code changes needed)
- Document CORS update needed (separate task, out of scope)

**Tests:** None (docs only)

**Model:** sonnet

**Constraints:**
- DO NOT execute Railway repoint
- DO NOT delete old Railway service
- DO NOT modify CORS config (note it in docs as "action required")

---

### TASK-060: DNS Docs
**Files modified:**
- `docs/DEPLOYMENT-WIRING-NOTES.md` (append DNS section)

**Deliverables:**
- Document Cloudflare DNS steps:
  - Add CNAME: `dev.shiftcenter.com` → Vercel (after Vercel custom domain is configured)
  - Verify existing CNAME: `api.shiftcenter.com` → Railway (update if needed)
  - Leave production DNS unchanged (code.shiftcenter.com, simdecisions.com, api.simdecisions.com point at old deploys)
- Document rollback plan (revert CNAME targets)

**Tests:** None (docs only)

**Model:** sonnet

**Constraints:**
- DO NOT execute DNS changes
- DO NOT delete production DNS records
- DO NOT change production domains

---

### TASK-061: Subdomain → EGG Routing (TDD)
**Files modified:**
- `browser/src/eggs/eggResolver.ts` (add hostname mappings)
- `browser/src/eggs/__tests__/eggResolver.test.ts` (add 7 new tests, 8 total)

**Deliverables:**
- Update `resolveEggFromHostname()` to add hardcoded hostname → EGG mappings:
  - `chat.efemera.live` → `chat`
  - `code.shiftcenter.com` → `code`
  - `pm.shiftcenter.com` → `pm`
  - `dev.shiftcenter.com` → `chat`
  - `localhost:5173` → `chat`
  - `localhost:3000` → `chat`
- Add 7 new tests:
  1. Test `chat.efemera.live` → `chat`
  2. Test `code.shiftcenter.com` → `code`
  3. Test `pm.shiftcenter.com` → `pm`
  4. Test `dev.shiftcenter.com` → `chat`
  5. Test `localhost:5173` → `chat`
  6. Test `localhost:3000` → `chat`
  7. Test query param override: `?egg=code` → `code`

**Tests:** 8 tests total (1 existing + 7 new)

**TDD required:** Write tests FIRST, then update eggResolver.ts

**Model:** sonnet

**Constraints:**
- No file over 500 lines (eggResolver.ts is 118 lines, safe)
- No breaking changes (query param override and pathname fallback still work)
- Do NOT modify routing.config.egg

---

### TASK-062: Smoke Test Docs
**Files modified:**
- `docs/DEPLOYMENT-WIRING-NOTES.md` (append smoke test section)

**Deliverables:**
- Document 7-step smoke test procedure:
  1. Vercel build verification (push to dev, verify build succeeds)
  2. Frontend loading (dev.shiftcenter.com loads chat app)
  3. Railway build verification (push to dev, verify build succeeds)
  4. API health endpoint (curl /health returns 200)
  5. CORS verification (fetch from dev.shiftcenter.com succeeds)
  6. EGG loading (`?egg=chat` loads chat EGG)
  7. Rollback verification (old production deploys still work)
- Document smoke test checklist (markdown checkboxes)
- Document next steps (CORS update, production cutover, archive old projects)

**Tests:** None (docs only)

**Model:** sonnet

**Constraints:**
- DO NOT execute smoke tests
- DO NOT change production DNS
- DO NOT delete old projects

---

## Approval Checklist

Q33NR, please verify:

- [x] All file paths are absolute (Windows format: `C:\Users\davee\...`)
- [x] Test requirements specified for TASK-061 (7 new tests, TDD required)
- [x] No TDD requirement for TASK-058, 059, 060, 062 (docs/config only)
- [x] Response file template included in all task files (8 sections)
- [x] Model assignment: sonnet (all tasks)
- [x] No file over 500 lines (eggResolver.ts: 118 lines → ~128 lines after changes)
- [x] No stubs or TODOs (bee must complete or fail, no partial work)
- [x] All tasks enforce constraints:
  - DO NOT execute repoint
  - DO NOT delete old projects
  - DO NOT change production DNS
- [x] TASK-061 preserves existing behavior (query param override, pathname fallback)
- [x] TASK-059 notes CORS update needed (separate task, out of scope)

---

## Known Dependencies

- **TASK-058** creates `DEPLOYMENT-WIRING-NOTES.md`
- **TASK-059** appends Railway section (depends on TASK-058)
- **TASK-060** appends DNS section (depends on TASK-058, 059)
- **TASK-062** appends smoke test section (depends on TASK-058, 059, 060)
- **TASK-061** is independent (no dependencies)

**Dispatch order:**
1. TASK-058 (creates base doc)
2. TASK-059, TASK-061 (parallel — no dependencies)
3. TASK-060 (depends on TASK-058, 059)
4. TASK-062 (depends on TASK-058, 059, 060)

---

## Follow-Up Tasks (Out of Scope)

After these 5 tasks complete, the following are needed (separate specs):

1. **CORS update** — Update `hivenode/main.py` line 233-237 to add `dev.shiftcenter.com`, `code.shiftcenter.com` to `allow_origins`
2. **Execute repoint** — Run the documented Vercel/Railway CLI commands (manual, not bee work)
3. **Execute smoke tests** — Follow TASK-062 procedure (manual, not bee work)
4. **Production cutover** — Update DNS for code.shiftcenter.com, api.shiftcenter.com (manual)
5. **Archive old projects** — Delete old Vercel/Railway projects after 7 days of stable production (manual)

---

## Q33NR — Ready to Dispatch?

Q33NR, if task files look good, approve dispatch. Q33N will run dispatch.py for each task file.

**Dispatch command (for Q33NR to run after approval):**
```bash
# TASK-058
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-13-TASK-058-vercel-config-docs.md --model sonnet --role bee --inject-boot

# TASK-059 (after TASK-058 completes)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-13-TASK-059-railway-config-docs.md --model sonnet --role bee --inject-boot

# TASK-061 (parallel with TASK-059)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-13-TASK-061-subdomain-egg-routing.md --model sonnet --role bee --inject-boot

# TASK-060 (after TASK-058, 059 complete)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-13-TASK-060-dns-config-docs.md --model sonnet --role bee --inject-boot

# TASK-062 (after all above complete)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-13-TASK-062-smoke-test-docs.md --model sonnet --role bee --inject-boot
```

Or approve me (Q33N) to dispatch all tasks.

---

**Q33N complete. Awaiting Q33NR approval.**
