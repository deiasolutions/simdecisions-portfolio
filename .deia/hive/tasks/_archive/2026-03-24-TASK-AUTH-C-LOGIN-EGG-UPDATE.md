# TASK-AUTH-C: login.egg.md update — ra96it → hodeia

## Objective
Update login.egg.md description text from "ra96it service" to "hodeia authentication" and update any localStorage key references to match new `sd_auth_*` keys. No layout changes needed.

## Context
The login.egg.md file currently references "ra96it service" in its description and may reference the old `ra96it_token`/`ra96it_user` localStorage keys in documentation. This task updates the branding to hodeia and ensures localStorage key references are consistent with TASK-AUTH-B.

This is a documentation/config update only — no code changes, no layout modifications.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\login.egg.md`

## Deliverables
- [ ] Update description: "ra96it service" → "hodeia authentication"
- [ ] Update any localStorage key references: `ra96it_token` → `sd_auth_token`, `ra96it_user` → `sd_auth_user`
- [ ] Keep layout unchanged (no changes to pane structure or config)
- [ ] Keep all other metadata unchanged (version, schema_version, author, etc.)

## Test Requirements
- [ ] No automated tests required (pure documentation/config file)
- [ ] Manual verification: file is valid markdown, YAML frontmatter is valid
- [ ] Manual verification: no references to "ra96it" remain in the file (except possibly in historical context)

## Constraints
- No file over 500 lines (login.egg.md is 39 lines, stays small)
- No stubs
- Do NOT change the layout structure or pane config
- Do NOT change version numbers or schema_version

## Acceptance Criteria
1. [ ] Description updated from "ra96it service" to "hodeia authentication"
2. [ ] All localStorage key references updated to `sd_auth_*` format
3. [ ] No references to "ra96it" remain except in deprecated/legacy context (if any)
4. [ ] File structure and YAML frontmatter remain valid
5. [ ] No layout or config changes (only description/docs)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-AUTH-C-RESPONSE.md`

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
