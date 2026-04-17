# SPEC: dev.shiftcenter.com DNS

## Priority
P1

## Objective
Add dev.shiftcenter.com CNAME in Cloudflare pointing to Vercel preview deployment. Verify api staging URL.

## Context
Cloudflare manages DNS for shiftcenter.com. Vercel assigns preview URLs automatically. We need a custom domain for the dev branch.

## Acceptance Criteria
- [ ] dev.shiftcenter.com CNAME -> Vercel (cname.vercel-dns.com or similar)
- [ ] Vercel custom domain dev.shiftcenter.com assigned to dev branch
- [ ] SSL works (Cloudflare flex or full)
- [ ] api.shiftcenter.com CNAME verified or updated for Railway
- [ ] Both resolve and load correctly

## Smoke Test
- [ ] https://dev.shiftcenter.com loads the chat app
- [ ] https://api.shiftcenter.com/health returns 200 (or staging equivalent)

## Depends On
- w3-01-vercel-railway-repoint

## Model Assignment
haiku

## Constraints
This may require manual Cloudflare + Vercel dashboard work. If the bee can't access these services via CLI, document the exact steps for Dave to execute manually.
