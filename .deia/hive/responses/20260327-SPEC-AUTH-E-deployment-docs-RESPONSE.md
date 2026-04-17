# SPEC-AUTH-E: Deployment Docs Update for Auth Rebrand -- COMPLETE

**Status:** COMPLETE
**Model:** Haiku
**Date:** 2026-03-27

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md

## What Was Done

- Updated all env var references from ra96it to hodeia naming
  - `VITE_RA96IT_API` → `VITE_AUTH_API` (with backwards reference note)
  - `RA96IT_PUBLIC_KEY` → `HODEIA_PUBLIC_KEY` (with backwards reference note)
- Added new "Drop — No Longer Needed" entries for old ra96it env vars
- Updated Railway repoint procedure to drop old ra96it env vars
- Added comprehensive "Auth Rebrand Migration: ra96it → hodeia" section with:
  - Environment Variable Migration Mapping table (old name to new name)
  - Dual-Issuer JWT Strategy documentation (accept both ra96it and hodeia issuers during transition)
  - URL Migration notes (api.ra96it.com → api.hodeia.me)
  - Cutover strategy (remove old issuer after 48 hours)
- Updated all URL references to hodeia.me where applicable
- Documented that beneficial-cooperation service domain is now hodeia.me (formerly ra96it.com)

## Tests Run

N/A — documentation-only task

## Test Results

N/A — documentation-only task

## Blockers

None

## Warnings

None

## Next Steps

None — documentation complete

## Notes

All acceptance criteria met:
- ✅ All env var references updated in deployment-env.md
- ✅ Migration mapping documented (old name to new name)
- ✅ Dual-issuer strategy documented
- ✅ No stubs

The documentation now clearly shows:
1. The mapping from old ra96it env vars to new hodeia env vars
2. The dual-issuer JWT strategy that allows both old (ra96it) and new (hodeia) tokens during transition
3. The cutover plan (48-hour observation period before removing old issuer)
4. All URL updates from api.ra96it.com to api.hodeia.me
