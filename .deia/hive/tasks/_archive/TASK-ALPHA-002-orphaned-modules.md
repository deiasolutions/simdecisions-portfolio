# TASK-ALPHA-002: Identify Orphaned Modules

## Objective
Identify all modules in the ShiftCenter codebase that are never imported by any other module.

## Context
Using the import graph from TASK-ALPHA-001, identify modules that have zero incoming imports. These are either entry points (intentionally standalone) or dead code (unintentionally orphaned).

**Dependencies:**
- TASK-ALPHA-001 must complete first
- Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`

**Known entry points to exclude from orphan list:**
- `browser/src/main.tsx` (Vite entry)
- `browser/app.html` (HTML entry)
- `hivenode/main.py` (FastAPI app entry)
- `hodeia_auth/main.py` (Auth service entry)
- Test files (separate analysis)
- CLI scripts in `_tools/`, `.deia/hive/scripts/`

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\ORPHANED-MODULES.md` with structure:

```markdown
# Orphaned Modules

## Summary
- Total modules analyzed: X
- Orphaned modules found: Y
- Entry points (excluded): Z

## Frontend Orphans (browser/src/)

### [File Path]
**Last modified:** [date from git or filesystem]
**Exports:** [list what it exports]
**Likely reason:** [dead code | config file | utility never imported | unknown]

[Repeat for each orphan]

## Backend Orphans (hivenode/)

[Same format]

## Auth Service Orphans (hodeia_auth/)

[Same format]

## Recommendations
- [ ] Files safe to delete (clearly dead)
- [ ] Files to investigate (unclear purpose)
- [ ] Files to preserve (config, docs, etc.)
```

## Test Requirements
- [ ] No tests required (read-only analysis)
- [ ] Verify orphan count > 0 (there's always some dead code)
- [ ] Verify known entry points are NOT in orphan list
- [ ] Spot-check 3 random orphans to confirm they have no incoming imports

## Constraints
- Read-only operation, no source code modifications
- Output file must not exceed 500 lines
- Depend on IMPORT-GRAPH.md, do not re-scan codebase
- Use git timestamps if available: `git log -1 --format=%ai -- <file>`

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-TASK-ALPHA-002-orphaned-modules-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts (or "No tests required" with reason)
5. **Build Verification** — test/build output summary (or "N/A - read-only analysis")
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
