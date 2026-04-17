# TASK-058: Create Vercel Configuration + Documentation

## Objective

Create Vercel configuration file with SPA fallback rewrites and document the Vercel CLI repoint procedure. This task does NOT execute the repoint — it only prepares the configuration and documentation.

## Context

We are repointing the Vercel project from `deiasolutions/platform` to `deiasolutions/shiftcenter`. The new repo has the browser app at `browser/` (Vite SPA). The Vercel project is currently called `simdecisions-2` and serves `code.shiftcenter.com` in production. After repoint:
- Production branch: `main` → code.shiftcenter.com
- Preview branch: `dev` → dev.shiftcenter.com
- All routes must fall back to `/index.html` for client-side routing (SPA behavior)

Environment variables documented in: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md`

Vite config: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vite.config.ts`

## Deliverables

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vercel.json` — Vercel config with SPA fallback rewrites
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — New documentation file (Vercel section only)

## vercel.json Requirements

Create `browser/vercel.json` with the following structure:

```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": null
}
```

This ensures all routes (`/chat`, `/code`, `/pm`) fall back to `/index.html` for client-side routing.

## DEPLOYMENT-WIRING-NOTES.md Requirements

Create `docs/DEPLOYMENT-WIRING-NOTES.md` with the following structure:

```markdown
# Deployment Wiring — ShiftCenter Repoint

## Overview

This document describes the procedure to repoint Vercel and Railway deployments from `deiasolutions/platform` to `deiasolutions/shiftcenter`. This wiring is in place as of 2026-03-13. The actual repoint cutover will be executed when approved.

**DO NOT execute these commands yet** — this is the wiring documentation. The cutover will be coordinated separately.

---

## Vercel: Browser App

### Current State
- **Repo:** `deiasolutions/platform`
- **Project:** `simdecisions-2`
- **Root directory:** `simdecisions-2/`
- **Domain:** code.shiftcenter.com (production)

### Target State
- **Repo:** `deiasolutions/shiftcenter`
- **Root directory:** `browser/`
- **Production branch:** `main` → code.shiftcenter.com
- **Preview branch:** `dev` → dev.shiftcenter.com
- **Config file:** `browser/vercel.json` (SPA fallback)

### Repoint Procedure

**Prerequisites:**
- Vercel CLI installed: `npm install -g vercel`
- Authenticated: `vercel login`
- GitHub user: `deiasolutions` org member

**Steps:**

1. **Link repo to Vercel project:**
   ```bash
   cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
   vercel link --yes
   # Select project: simdecisions-2
   # This repoints the existing project to the new repo
   ```

2. **Set root directory:**
   ```bash
   vercel --cwd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser env add ROOT_DIRECTORY
   # Enter: browser
   ```

3. **Set production branch:**
   Vercel dashboard → Project Settings → Git → Production Branch: `main`

4. **Add preview branch:**
   Vercel dashboard → Project Settings → Git → Preview Branches: Include `dev`

5. **Set environment variables (production):**
   ```bash
   vercel env add VITE_API_URL production
   # Enter: https://api.shiftcenter.com

   vercel env add VITE_GITHUB_CLIENT_ID production
   # Enter: <GitHub OAuth Client ID from 1Password>

   vercel env add VITE_RA96IT_URL production
   # Enter: https://api.ra96it.com
   ```

6. **Set environment variables (preview/dev):**
   ```bash
   vercel env add VITE_API_URL preview
   # Enter: https://api.simdecisions.com (or staging URL when available)

   vercel env add VITE_GITHUB_CLIENT_ID preview
   # Enter: <same as production>

   vercel env add VITE_RA96IT_URL preview
   # Enter: https://api.ra96it.com
   ```

7. **Add custom domain for dev branch:**
   Vercel dashboard → Project Settings → Domains → Add Domain: `dev.shiftcenter.com`
   - Assign to branch: `dev`
   - Vercel will provide CNAME target (e.g., `cname.vercel-dns.com`)

8. **Verify build settings:**
   Vercel dashboard → Project Settings → Build & Development Settings:
   - Framework Preset: Other (or Vite if available)
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
   - Root Directory: `browser`

### DNS Configuration (Cloudflare)

After Vercel provides the CNAME target for `dev.shiftcenter.com`:

1. Log in to Cloudflare → shiftcenter.com zone
2. Add DNS record:
   - Type: CNAME
   - Name: `dev`
   - Target: `cname.vercel-dns.com` (or Vercel's provided target)
   - Proxy status: Proxied (orange cloud)
   - TTL: Auto

### Verification

After repoint (when executed):

1. **Test production build:**
   ```bash
   git checkout main
   git push origin main
   # Wait for Vercel build to complete
   # Visit: https://code.shiftcenter.com
   # Should load chat app (or code app if code.egg.md exists)
   ```

2. **Test dev branch build:**
   ```bash
   git checkout dev
   git push origin dev
   # Wait for Vercel build to complete
   # Visit: https://dev.shiftcenter.com
   # Should load chat app by default
   # Visit: https://dev.shiftcenter.com?egg=chat
   # Should load same chat app
   ```

---

[Railway section will be added by TASK-059]
[DNS section will be added by TASK-060]
[Smoke test section will be added by TASK-062]
```

End of Vercel section.

## Test Requirements

**No automated tests required** — this is a configuration file and documentation task.

Manual verification:
- [ ] `vercel.json` is valid JSON (use `npx jsonlint browser/vercel.json`)
- [ ] `DEPLOYMENT-WIRING-NOTES.md` follows markdown format (no broken links)
- [ ] File paths in documentation use absolute Windows paths where relevant

## Constraints

- **DO NOT execute the Vercel repoint** — this task only creates the config and docs
- **DO NOT delete old Vercel project** — it stays live until cutover is verified
- **DO NOT change production DNS** — old deploys stay live
- Use Windows-style absolute paths in documentation where relevant (e.g., `C:\Users\davee\...`)
- JSON file must be valid (use `npx jsonlint` to verify)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-058-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full absolute paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- manual verification steps performed (JSON lint, markdown format check)
5. **Build Verification** -- N/A (no build required)
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- dependencies on TASK-059, 060, 062

DO NOT skip any section. A response without all 8 sections is incomplete.

## Model Assignment

sonnet
