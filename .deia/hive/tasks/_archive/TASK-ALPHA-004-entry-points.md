# TASK-ALPHA-004: Catalog Entry Points and First-Level Dependencies

## Objective
Identify all entry points in the ShiftCenter codebase and map their first-level dependencies (direct imports).

## Context
Entry points are files that start execution chains. They are not imported by other modules in the application but are loaded by external systems (build tools, servers, test runners).

**Dependencies:**
- TASK-ALPHA-001 must complete first
- Read `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`

**Known entry points to catalog:**

**Frontend:**
- `browser/src/main.tsx` (Vite entry)
- `browser/app.html` (HTML entry, may load scripts)
- Any files referenced in `browser/vite.config.ts`

**Backend:**
- `hivenode/main.py` (FastAPI app)
- `hivenode/scheduler/scheduler_daemon.py` (scheduler service)
- `hivenode/scheduler/dispatcher_daemon.py` (dispatcher service)
- `hodeia_auth/main.py` (auth service)

**CLI/Scripts:**
- Files in `_tools/` that are run directly (e.g., `inventory.py`, `restart-services.sh`)
- Files in `.deia/hive/scripts/` (e.g., `dispatch.py`, `run_queue.py`)

**Tests:**
- Test entry points (pytest discovers `test_*.py`, vitest discovers `*.test.ts`)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\IMPORT-GRAPH.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\vite.config.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\package.json` (check "main", "scripts")

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\audits\2026-04-08\alpha\ENTRY-POINTS.md` with structure:

```markdown
# Entry Points

## Summary
- Total entry points identified: X
- Frontend entry points: Y
- Backend entry points: Z
- CLI/Script entry points: W
- Test entry points: V

## Frontend Entry Points

### browser/src/main.tsx
**Type:** Vite entry point
**First-level imports:**
- `./App` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\App.tsx`
- `react` → external package
- `./index.css` → stylesheet

**Total transitive dependency files:** [estimated or "see IMPORT-GRAPH.md"]

[Repeat for each frontend entry point]

## Backend Entry Points

### hivenode/main.py
**Type:** FastAPI application
**First-level imports:**
- `fastapi.FastAPI` → external package
- `.routes.des_routes` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\des_routes.py`
- `.inventory.routes` → `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\inventory\routes.py`

**Total transitive dependency files:** [estimated or "see IMPORT-GRAPH.md"]

[Repeat for each backend entry point]

## CLI/Script Entry Points

[Same format]

## Test Entry Points

[Same format — or summarize if too many]

## Dependency Overlap Analysis

### Shared by Multiple Entry Points
- [List modules imported by 3+ entry points — indicates core infrastructure]

### Entry Point Isolation
- [List entry points with zero dependency overlap — indicates isolated subsystems]
```

## Test Requirements
- [ ] No tests required (read-only analysis)
- [ ] Verify at least 5 entry points identified
- [ ] Verify each entry point has at least one first-level import listed
- [ ] Verify both frontend and backend entry points present

## Constraints
- Read-only operation, no source code modifications
- Output file must not exceed 500 lines
- Depend on IMPORT-GRAPH.md for import data, do not re-scan
- For test entry points, summarize by pattern (e.g., "12 pytest files in hivenode/tests/") rather than listing all

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260408-TASK-ALPHA-004-entry-points-RESPONSE.md`

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
