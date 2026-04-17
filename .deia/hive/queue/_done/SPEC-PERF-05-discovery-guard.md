# SPEC: Skip Localhost Port Scanning in Production for discoverHivenodeUrl

## Priority
P2

## Objective
Prevent discoverHivenodeUrl() from probing 13 localhost ports when running on a production domain (efemera.live, shiftcenter.com, etc.). Currently it probes http://localhost:8420 through http://localhost:8429 plus 8000, 8080, 3001 — each with a 1.5-second timeout — even when running on a non-localhost hostname.

## Context
`hivenodeDiscovery.ts` is used by `claimDeviceData()` during OAuth token extraction. On production domains, `HIVENODE_URL` (from hivenodeUrl.ts) correctly returns `""` for same-origin requests, but `discoverHivenodeUrl()` (from hivenodeDiscovery.ts) doesn't have the same production guard. When called on efemera.live, it sequentially probes 13 localhost ports, each waiting 1.5 seconds to timeout = up to 19.5 seconds of wasted network calls.

The fix: mirror the same production detection from hivenodeUrl.ts. On non-localhost, return `""` immediately (same-origin, Vercel proxies to Railway).

## Files to Read First
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\hivenodeDiscovery.ts
- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\hivenodeUrl.ts

## Acceptance Criteria
- [ ] In `discoverHivenodeUrl()`, before probing, check if hostname is not localhost — if so, return `""` immediately (same-origin)
- [ ] Cache the result so subsequent calls are instant
- [ ] Keep the existing localhost probing logic intact for dev environments
- [ ] Tests written FIRST (TDD)
- [ ] Add test: discoverHivenodeUrl returns "" immediately on non-localhost hostname
- [ ] Add test: discoverHivenodeUrl still probes ports on localhost
- [ ] Add test: result is cached after first call

## Smoke Test
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser && npx vitest run src/services

## Model Assignment
haiku

## Depends On
(none)

## Constraints
- No file over 500 lines
- No stubs
- TDD — tests first
- Do NOT change the port probing logic for localhost — only add the production guard
- Write response to: .deia/hive/responses/20260401-SPEC-PERF-05-RESPONSE.md
