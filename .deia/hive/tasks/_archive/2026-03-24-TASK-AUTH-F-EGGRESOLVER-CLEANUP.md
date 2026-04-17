# TASK-AUTH-F: eggResolver routing cleanup — mark ra96it entries deprecated

## Objective
Update eggResolver.ts to keep both `hodeia.me` and `ra96it.com` → `login` mappings for backwards compatibility, but add comments marking ra96it.com entries as deprecated. Update tests to verify both old and new hostnames resolve to login.

## Context
The eggResolver.ts hardcoded hostname map already includes `hodeia.me` → `login` mapping (lines 127-128) and legacy `ra96it.com` → `login` mappings (lines 140-142). This task:
1. Keeps both mappings (backwards compat — existing ra96it.com URLs must still work)
2. Adds comments marking ra96it.com entries as deprecated
3. Updates tests to verify both hostnames resolve correctly

This is a small cleanup task with minimal code changes.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\eggs\eggResolver.ts`

## Deliverables
- [ ] Keep `hodeia.me` and `www.hodeia.me` → `login` mappings (lines 127-128)
- [ ] Keep `ra96it.com` and `www.ra96it.com` → `login` mappings (lines 140-142)
- [ ] Add comment above `ra96it.com` entries: `// ── Legacy (DEPRECATED — use hodeia.me) ──`
- [ ] Add inline comment after each ra96it entry: `// DEPRECATED: use hodeia.me`
- [ ] Update tests: verify both `hodeia.me` and `ra96it.com` resolve to `login`
- [ ] Add test: verify `www.hodeia.me` and `www.ra96it.com` resolve to `login`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] Test case: `hodeia.me` → resolves to `login`
- [ ] Test case: `www.hodeia.me` → resolves to `login`
- [ ] Test case: `ra96it.com` → resolves to `login` (backwards compat)
- [ ] Test case: `www.ra96it.com` → resolves to `login` (backwards compat)
- [ ] Test case: `dev.ra96it.com` → resolves to `login` (if present in map)
- [ ] All existing eggResolver tests pass

## Constraints
- No file over 500 lines (eggResolver.ts is 181 lines, stays well under)
- CSS: `var(--sd-*)` only (not applicable, TS module)
- No stubs
- Do NOT remove ra96it.com entries — backwards compat required
- Keep comments clear and concise

## Acceptance Criteria
1. [ ] Both `hodeia.me` and `ra96it.com` → `login` mappings present in hostnameMap
2. [ ] Comments added marking ra96it.com entries as deprecated
3. [ ] Tests verify both hostnames resolve to `login` correctly
4. [ ] No functional changes — routing behavior unchanged
5. [ ] All eggResolver tests pass (existing + new hostname tests)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-F-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
