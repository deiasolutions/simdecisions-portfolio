# TASK-ALPHA-003: Identify Dead Exports

## Objective
Identify all exported symbols in the ShiftCenter codebase that are never imported/consumed by any other module.

## Context
Using the import graph from TASK-ALPHA-001, cross-reference exports with imports to find symbols that are exported but never consumed. These are candidates for removal or indicate incomplete features.

**Dependencies:**
- TASK-ALPHA-001 must complete first
- Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`

**Export types to track:**
- Named exports: `export function foo()`, `export const bar`
- Default exports: `export default Baz`
- Re-exports: `export { x } from './other'`
- Type exports: `export type MyType` (TypeScript)
- Class exports: `export class MyClass`

**Known exclusions:**
- Exports from entry point files (main.tsx, main.py)
- Public API exports from index files (may be used by external consumers)
- Framework hooks (e.g., React component exports used by React Router)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\DEAD-EXPORTS.md` with structure:

```markdown
# Dead Exports

## Summary
- Total exports analyzed: X
- Dead exports found: Y
- Files with dead exports: Z

## Frontend Dead Exports (browser/src/)

### [File Path]

#### `exportedSymbol`
**Type:** function | const | class | type | default
**Line:** [line number]
**Exported but never imported**
**Recommendation:** Remove | Investigate | Keep (explain why)

[Repeat for each dead export in file]

[Repeat for each file with dead exports]

## Backend Dead Exports (hivenode/)

[Same format]

## Auth Service Dead Exports (hodeia_auth/)

[Same format]

## Recommendations by Severity

### High Priority (safe to remove)
- [List exports that are clearly unused and safe to delete]

### Medium Priority (investigate)
- [List exports that might be work-in-progress or used dynamically]

### Low Priority (keep)
- [List exports that should be kept for API surface or future use]
```

## Test Requirements
- [ ] No tests required (read-only analysis)
- [ ] Verify at least 5 dead exports found (codebases always have some)
- [ ] Verify default exports are tracked separately from named exports
- [ ] Spot-check 3 random dead exports to confirm they're not imported anywhere

## Constraints
- Read-only operation, no source code modifications
- Output file must not exceed 500 lines — if too long, split by priority or directory
- Depend on IMPORT-GRAPH.md, do not re-scan codebase
- Handle re-exports carefully: `export { x } from './y'` consumes `x` from `y` but also exports it

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-TASK-ALPHA-003-dead-exports-RESPONSE.md`

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
