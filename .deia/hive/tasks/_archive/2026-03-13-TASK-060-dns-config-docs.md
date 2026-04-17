# TASK-060: Document DNS Configuration (Cloudflare)

## Objective

Document the Cloudflare DNS configuration steps for `dev.shiftcenter.com` and verify existing DNS for `api.shiftcenter.com`. This task does NOT execute DNS changes — it only prepares the documentation.

## Context

We are adding `dev.shiftcenter.com` as a new CNAME pointing to Vercel for the `dev` branch preview. We also need to verify that `api.shiftcenter.com` points to Railway (may already exist or need update after Railway repoint).

DNS is managed in Cloudflare for the `shiftcenter.com` zone.

## Deliverables

- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\DEPLOYMENT-WIRING-NOTES.md` — Add DNS section (append to existing file from TASK-058 and TASK-059)

## DNS Section Requirements

Append the following section to `docs/DEPLOYMENT-WIRING-NOTES.md` (after the Railway section):

```markdown
---

## DNS Configuration (Cloudflare)

### Overview

DNS for `shiftcenter.com` is managed in Cloudflare. After Vercel and Railway repoint, we need to:
1. Add `dev.shiftcenter.com` → Vercel (new)
2. Verify `api.shiftcenter.com` → Railway (existing or update)
3. Leave production domains unchanged until cutover is verified

### Prerequisites

- Cloudflare account access (DNS admin for shiftcenter.com zone)
- CNAME target from Vercel for `dev.shiftcenter.com` (provided after custom domain is added in Vercel dashboard)
- CNAME target from Railway for `api.shiftcenter.com` (provided in Railway dashboard under custom domains)

### DNS Records Checklist

| Record | Type | Name | Target | Proxy | Status |
|--------|------|------|--------|-------|--------|
| Dev frontend | CNAME | `dev` | `cname.vercel-dns.com` (or Vercel's target) | Proxied (orange) | **New** — add after Vercel repoint |
| API (new) | CNAME | `api` | Railway custom domain target | Proxied (orange) | **Verify/Update** — check after Railway repoint |
| Production frontend | CNAME | `code` | (existing Vercel target) | Proxied (orange) | **No change** — stays pointed at old deploy until cutover |

### Step-by-Step: Add dev.shiftcenter.com

**Prerequisites:**
1. Vercel custom domain configured (see Vercel section, step 7)
2. Vercel provides CNAME target (e.g., `cname.vercel-dns.com` or `76.76.21.xxx`)

**Steps:**

1. **Log in to Cloudflare:**
   - URL: https://dash.cloudflare.com
   - Select zone: `shiftcenter.com`

2. **Add DNS record:**
   - Click "DNS" in left sidebar
   - Click "Add record"
   - Type: `CNAME`
   - Name: `dev`
   - Target: `<CNAME target from Vercel>` (e.g., `cname.vercel-dns.com`)
   - Proxy status: **Proxied** (orange cloud icon)
   - TTL: Auto
   - Click "Save"

3. **Verify DNS propagation:**
   ```bash
   # Wait 1-2 minutes, then check:
   nslookup dev.shiftcenter.com
   # Should return Cloudflare proxy IP (not Vercel's IP directly)

   # Test in browser:
   curl -I https://dev.shiftcenter.com
   # Should return 200 or redirect to Vercel
   ```

### Step-by-Step: Verify api.shiftcenter.com

**Prerequisites:**
1. Railway custom domain configured (Railway dashboard → Service → Settings → Domains → Add custom domain: `api.shiftcenter.com`)
2. Railway provides CNAME target (e.g., `<service-name>.up.railway.app` or custom target)

**Steps:**

1. **Check existing DNS record:**
   - Cloudflare → shiftcenter.com zone → DNS
   - Look for existing `CNAME` record: `api` → `<old target>`

2. **Update target (if needed):**
   - If target is old Railway service, update it:
   - Click record → Edit
   - Target: `<new CNAME target from Railway>` (e.g., `merry-learning.up.railway.app` or custom domain)
   - Proxy status: **Proxied** (orange cloud icon)
   - Click "Save"

3. **Verify DNS propagation:**
   ```bash
   nslookup api.shiftcenter.com
   # Should return Cloudflare proxy IP

   # Test health endpoint:
   curl https://api.shiftcenter.com/health
   # Should return: {"status":"ok","mode":"cloud",...}
   ```

### Production DNS (No Changes Yet)

**Do NOT change these records until cutover is verified:**

| Record | Current Target | Notes |
|--------|----------------|-------|
| `code.shiftcenter.com` | Old Vercel deployment | Leave unchanged — points at old `deiasolutions/platform` deploy |
| `simdecisions.com` | Old Vercel deployment | Leave unchanged — same as above |
| `api.simdecisions.com` | Old Railway deployment | Leave unchanged — points at old `deiasolutions/platform` deploy |

After successful staging verification (smoke tests pass), these will be updated to point at the new deploys.

### Rollback Plan

If DNS changes cause issues:

1. **Revert dev.shiftcenter.com:**
   - Cloudflare → DNS → Delete `dev` CNAME record
   - TTL is "Auto" (5 minutes) — propagation takes 5-10 minutes

2. **Revert api.shiftcenter.com:**
   - Cloudflare → DNS → Edit `api` CNAME record
   - Target: `<old Railway target>` (from old service)
   - Save → propagation takes 5-10 minutes

---

[Smoke test section will be added by TASK-062]
```

End of DNS section.

## Test Requirements

**No automated tests required** — this is a documentation task.

Manual verification:
- [ ] DNS section is valid markdown (no broken links)
- [ ] DNS table is properly formatted
- [ ] All CNAME targets reference the correct services (Vercel, Railway)

## Constraints

- **DO NOT execute DNS changes** — this task only creates documentation
- **DO NOT delete production DNS records** — they stay pointed at old deploys until cutover is verified
- **DO NOT change production domains** — old deploys stay live
- Use Windows-style absolute paths in documentation where relevant (e.g., `C:\Users\davee\...`)

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260313-TASK-060-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full absolute paths
3. **What Was Done** -- bullet list of concrete changes (DNS section added)
4. **Test Results** -- manual verification steps performed (markdown format check, table formatting)
5. **Build Verification** -- N/A (no build required)
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- dependencies on TASK-058, 059, 062

DO NOT skip any section. A response without all 8 sections is incomplete.

## Model Assignment

sonnet
