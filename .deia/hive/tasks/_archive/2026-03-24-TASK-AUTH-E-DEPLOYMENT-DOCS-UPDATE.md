# TASK-AUTH-E: deployment docs update — ra96it → hodeia migration

## Objective
Update `.deia/config/deployment-env.md` with new auth env var names (VITE_AUTH_API, HIVENODE_AUTH_PUBLIC_KEY, HIVENODE_AUTH_JWKS_URL), document the ra96it → hodeia migration, and document the dual-issuer strategy.

## Context
The deployment-env.md file currently references `VITE_RA96IT_URL`, `RA96IT_PUBLIC_KEY`, and `HIVENODE_RA96IT_JWKS_URL` (note: some inconsistency in naming). This task:
1. Updates env var names to match new generic naming
2. Documents the migration path: old var → new var mapping
3. Documents the dual-issuer strategy (JWT issuer can be "ra96it" or "hodeia" during transition)
4. Clarifies that the ra96it backend service stays at api.ra96it.com (no change to that service)

This is a documentation-only task. No code changes.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\deployment-env.md`

## Deliverables
- [ ] Update Vercel env vars section:
  - `VITE_RA96IT_URL` → `VITE_AUTH_API` (rename, document old→new)
  - Note: URL value stays `https://api.ra96it.com` for now (backend service unchanged)
- [ ] Update Railway env vars section:
  - `RA96IT_PUBLIC_KEY` → `HIVENODE_AUTH_PUBLIC_KEY` (rename, document old→new)
  - Add `HIVENODE_AUTH_JWKS_URL` if not present (default: `https://ra96it.com/.well-known/jwks.json`)
- [ ] Add migration section:
  - Table: old env var → new env var mapping
  - Note: values unchanged, names only
  - Dual-issuer strategy: JWT issuer can be "ra96it" or "hodeia" during transition
- [ ] Clarify: ra96it service stays on platform repo at api.ra96it.com (no changes needed)
- [ ] Update any other references to "ra96it" env vars in the document

## Test Requirements
- [ ] No automated tests required (docs only)
- [ ] Manual verification: markdown is valid, tables are formatted correctly
- [ ] Manual verification: env var names match what was implemented in TASK-AUTH-A, TASK-AUTH-D

## Constraints
- No file over 500 lines (deployment-env.md is 161 lines, will stay under 200)
- No stubs
- Do NOT change Railway/Vercel service names or domains (those stay as-is)
- Keep existing structure — add migration section, update env var names

## Acceptance Criteria
1. [ ] `VITE_RA96IT_URL` → `VITE_AUTH_API` documented in Vercel section
2. [ ] `RA96IT_PUBLIC_KEY` → `HIVENODE_AUTH_PUBLIC_KEY` documented in Railway section
3. [ ] Migration table added: old var → new var mapping
4. [ ] Dual-issuer strategy documented: JWTs with issuer="ra96it" OR "hodeia" accepted
5. [ ] Clarification added: ra96it service stays on platform repo, no backend changes
6. [ ] All env var references updated throughout the document

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-E-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts (or "N/A — docs only")
5. **Build Verification** — test/build output summary (or "N/A — no build impact")
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
