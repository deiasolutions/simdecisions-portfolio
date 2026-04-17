# TASK-ALPHA-001: Build Complete Import Graph

## Objective
Generate a comprehensive import/export graph covering all TypeScript/JavaScript and Python source files in the ShiftCenter codebase.

## Context
This is part of a static analysis to identify dependency relationships across the entire codebase. The graph will be used to identify orphaned modules and dead exports.

**Target directories:**
- `browser/src/` (TypeScript/JavaScript frontend)
- `hivenode/` (Python backend)
- `hodeia_auth/` (Python auth service)
- `engine/` (Python engine)

**Exclusions:**
- `node_modules/`, `dist/`, `build/`, `__pycache__/`, `.pytest_cache/`, `venv/`, `.venv/`
- Test files (analyze separately but don't include in main graph)
- Type definition files (`.d.ts`)

## Files to Read First
None required — this is a codebase-wide scan.

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md` with the following structure:

```markdown
# Import Graph

## Summary
- Total files analyzed: X
- Total import statements: Y
- Total export statements: Z

## Frontend (browser/src/)

### [File Path]
**Imports:**
- `symbol` from `./relative/path` (resolved: absolute/path)
- `{ namedSymbol }` from `package-name`

**Exports:**
- `export function foo()`
- `export default Bar`
- `export { baz }`

[Repeat for each file]

## Backend (hivenode/)

[Same format]

## Auth Service (hodeia_auth/)

[Same format]

## Engine (engine/)

[Same format]
```

## Test Requirements
- [ ] No tests required (read-only analysis)
- [ ] Verify output file contains at least 100 files
- [ ] Verify at least one import statement is correctly resolved to absolute path
- [ ] Verify frontend and backend sections both populated

## Constraints
- Read-only operation, no source code modifications
- Output file must not exceed 500 lines — if graph is larger, split by directory
- Use AST parsing where possible (e.g., TypeScript parser for `.ts/.tsx`, Python `ast` module for `.py`)
- For import resolution, use standard Node.js resolution for frontend, Python import semantics for backend

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-TASK-ALPHA-001-import-graph-RESPONSE.md`

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
