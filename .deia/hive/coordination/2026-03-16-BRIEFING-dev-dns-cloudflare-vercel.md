# BRIEFING: dev.shiftcenter.com DNS Configuration

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`
**Priority:** P1
**Assigned Model:** Haiku

---

## Objective

Configure dev.shiftcenter.com custom domain for Vercel preview deployment and verify api.shiftcenter.com points to Railway staging.

## Context from Q88N

This spec requires DNS configuration in Cloudflare and custom domain assignment in Vercel. The dev branch needs its own subdomain separate from production. The spec explicitly notes this may require manual dashboard work if CLI access is unavailable.

## What Q33N Must Do

1. **Research the current state:**
   - Check if Cloudflare CLI tools are available (e.g., `wrangler`, `flarectl`)
   - Check if Vercel CLI can assign custom domains (`vercel domains add`, `vercel domains inspect`)
   - Determine if we have API keys/tokens in env for programmatic access

2. **Write task file(s) that either:**
   - **Option A (automated):** If CLI tools are available and authenticated:
     - Task to add CNAME via Cloudflare API
     - Task to assign custom domain in Vercel
     - Task to verify SSL configuration
     - Task to verify api.shiftcenter.com CNAME
   - **Option B (manual documentation):** If CLI access is not available:
     - Task to document exact Cloudflare steps for Q88N to execute
     - Task to document exact Vercel steps for Q88N to execute
     - Task to write smoke test script that Q88N can run after manual config

3. **Ensure deliverables include:**
   - CNAME record: `dev.shiftcenter.com` → Vercel's DNS target (likely `cname.vercel-dns.com`)
   - Vercel custom domain assigned to dev branch
   - SSL working (Cloudflare Flexible or Full mode)
   - Verification that `api.shiftcenter.com` CNAME is correct for Railway
   - Smoke test confirming both URLs resolve and load

## Constraints

- This is infrastructure work, not code. If the bee cannot automate it, document it.
- Do NOT make assumptions about which Vercel DNS target to use. The bee must inspect Vercel's actual assignment.
- SSL must work. Cloudflare + Vercel typically requires Flexible SSL mode.
- Smoke test MUST verify both `https://dev.shiftcenter.com` (app loads) and `https://api.shiftcenter.com/health` (or staging equivalent).

## Dependencies

- Spec says "Depends On: w3-01-vercel-railway-repoint" — check if that spec has already run and if Railway/Vercel are already configured.

## Acceptance Criteria (from spec)

- [ ] dev.shiftcenter.com CNAME -> Vercel (cname.vercel-dns.com or similar)
- [ ] Vercel custom domain dev.shiftcenter.com assigned to dev branch
- [ ] SSL works (Cloudflare flex or full)
- [ ] api.shiftcenter.com CNAME verified or updated for Railway
- [ ] Both resolve and load correctly

## Smoke Test (from spec)

- [ ] https://dev.shiftcenter.com loads the chat app
- [ ] https://api.shiftcenter.com/health returns 200 (or staging equivalent)

## Model Assignment

Haiku (as specified in spec)

---

## Q33N Instructions

1. Read the spec: `.deia/hive/queue/2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`
2. Check for dependency completion: `.deia/hive/queue/_done/2026-03-16-3000-SPEC-w3-01-vercel-railway-repoint.md` (if it exists)
3. Inspect available CLI tools: `vercel --version`, `wrangler --version` or similar
4. Write task file(s) to `.deia/hive/tasks/`
5. Return to Q33NR for review
6. After approval, dispatch bee(s)
7. When complete, verify smoke tests pass and report results to Q33NR

---

**Q33NR will review your task files before you dispatch. Do NOT dispatch bees until approved.**
