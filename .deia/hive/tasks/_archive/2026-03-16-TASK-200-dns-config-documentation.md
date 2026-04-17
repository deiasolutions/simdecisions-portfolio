# TASK-200: Document Cloudflare + Vercel DNS Configuration Steps

## Objective
Create step-by-step documentation for Q88N to manually configure dev.shiftcenter.com DNS via Cloudflare dashboard and assign custom domain in Vercel dashboard.

## Context
This task is infrastructure configuration for the dev branch preview environment. We do not have Cloudflare CLI tools or API tokens available, so DNS configuration must be done manually via dashboard. The bee will create clear, actionable documentation that Q88N can follow.

From spec `.deia/hive/queue/2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`:
- dev.shiftcenter.com should CNAME to Vercel's DNS target
- Vercel custom domain must be assigned to dev branch
- SSL must work (Cloudflare Flexible or Full mode)
- api.shiftcenter.com CNAME must be verified for Railway

From `.deia/config/deployment-env.md`:
- Dev branch uses `dev.shiftcenter.com` with `?egg=name` query params
- Railway hivenode already configured (from w3-01 dependency)
- Vercel already repointed to shiftcenter/browser/ (from w3-01 dependency)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-16-3001-SPEC-w3-02-dev-shiftcenter-dns.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\_done\2026-03-16-3000-SPEC-w3-01-vercel-railway-repoint.md`

## Deliverables

### Primary Deliverable
- [ ] `.deia/hive/coordination/2026-03-16-DNS-CONFIG-STEPS.md` — comprehensive manual configuration guide

### Documentation Must Include

#### Section 1: Cloudflare DNS Configuration
- [ ] Login URL and account navigation steps
- [ ] How to add CNAME record for `dev.shiftcenter.com`
- [ ] Exact DNS target (research Vercel's current CNAME target — typically `cname.vercel-dns.com`)
- [ ] Proxy status recommendation (Orange cloud ON or OFF)
- [ ] TTL recommendation

#### Section 2: Vercel Custom Domain Assignment
- [ ] Login URL and project navigation
- [ ] How to add custom domain `dev.shiftcenter.com` to the project
- [ ] How to assign domain to `dev` branch specifically (not main)
- [ ] Domain verification steps (TXT record if needed)
- [ ] How to verify SSL certificate is issued

#### Section 3: SSL Configuration
- [ ] Cloudflare SSL/TLS mode recommendation (Flexible vs Full)
- [ ] Why this mode is needed for Cloudflare + Vercel
- [ ] How to verify SSL is working (browser test)

#### Section 4: Railway API Domain Verification
- [ ] How to verify api.shiftcenter.com CNAME in Cloudflare
- [ ] Expected Railway CNAME target
- [ ] How to verify it's pointing to correct Railway service

#### Section 5: Verification Checklist
- [ ] DNS propagation check command: `nslookup dev.shiftcenter.com`
- [ ] Browser test: `https://dev.shiftcenter.com` should load
- [ ] API test: `https://api.shiftcenter.com/health` should return 200
- [ ] SSL test: Certificate should be valid, not browser warning

## Test Requirements

This is a documentation task — no automated tests required. However:

- [ ] Documentation must be written in clear, numbered steps
- [ ] Each step must be actionable (no vague instructions)
- [ ] Include screenshots paths if helpful (not required to create actual screenshots)
- [ ] Include expected outcomes for each step ("You should see...")

## Constraints

- **No file over 500 lines:** Documentation should be concise, under 200 lines
- **Absolute paths:** All file references must use absolute paths
- **No stubs:** Every step must be complete, not "configure SSL (details TBD)"
- **No assumptions:** Do NOT assume Q88N knows Cloudflare or Vercel UI — explain everything

## Research Requirements

The bee MUST research:
1. **Current Vercel CNAME target:** Check Vercel documentation for what DNS target to use (e.g., `cname.vercel-dns.com` or project-specific)
2. **Railway CNAME format:** Verify expected Railway CNAME target format
3. **Cloudflare + Vercel SSL mode:** Confirm whether Flexible or Full(strict) is recommended

Do NOT guess or use outdated information. Check current Vercel docs (2026).

## Model Assignment
Haiku

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260316-TASK-200-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — N/A for documentation task (state this explicitly)
5. **Build Verification** — N/A for documentation task (state this explicitly)
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Acceptance Criteria

From spec:
- [ ] dev.shiftcenter.com CNAME documentation complete
- [ ] Vercel custom domain assignment steps documented
- [ ] SSL configuration steps documented
- [ ] api.shiftcenter.com verification steps documented
- [ ] Verification checklist provided

Task-specific:
- [ ] All 5 sections of documentation present
- [ ] Steps are numbered and actionable
- [ ] Research completed (Vercel CNAME target identified)
- [ ] File written to `.deia/hive/coordination/2026-03-16-DNS-CONFIG-STEPS.md`
