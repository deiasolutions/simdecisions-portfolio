# TASK-REVIEW-QUEEN-ALPHA: Task Plan for Q33NR Review

**Status:** AWAITING REVIEW
**Model:** Sonnet
**Date:** 2026-04-08

---

## Context

I am Q33N responding to a watchdog restart. The previous queen dispatched for TASK-REVIEW-QUEEN-ALPHA produced no deliverables. The alpha audit directory (`.deia/audits/2026-04-08/alpha/`) exists but is empty.

I need to build four static analysis deliverables:
1. IMPORT-GRAPH.md — complete dependency graph
2. ORPHANED-MODULES.md — modules never imported
3. DEAD-EXPORTS.md — exported symbols never consumed
4. ENTRY-POINTS.md — entry points and their first-level dependencies

---

## Task Files Created

I have created four task files, to be executed sequentially (each depends on the previous):

### TASK-ALPHA-001: Build Complete Import Graph
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-001-import-graph.md`
**Model:** Sonnet (complex AST parsing required)
**Estimated time:** 20-30 minutes
**Deliverable:** `.deia/audits/2026-04-08/alpha/IMPORT-GRAPH.md`

**What it does:**
- Scans all `.ts`, `.tsx`, `.js`, `.jsx`, `.py` files in `browser/src/`, `hivenode/`, `hodeia_auth/`, `engine/`
- Uses AST parsing (TypeScript parser for frontend, Python `ast` module for backend)
- Extracts all import statements and export statements
- Resolves relative imports to absolute paths
- Outputs structured markdown with imports/exports per file

**Dependencies:** None

**Output format:**
```
# Import Graph
## Summary
- Total files: X
- Total imports: Y
- Total exports: Z

## Frontend (browser/src/)
### [file path]
**Imports:** [list]
**Exports:** [list]
```

**Constraints:**
- If output exceeds 500 lines, split by directory
- Exclude test files, node_modules, dist, build, etc.
- Use AST parsing, not regex

---

### TASK-ALPHA-002: Identify Orphaned Modules
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-002-orphaned-modules.md`
**Model:** Haiku (graph analysis, simpler than AST parsing)
**Estimated time:** 10-15 minutes
**Deliverable:** `.deia/audits/2026-04-08/alpha/ORPHANED-MODULES.md`

**What it does:**
- Reads IMPORT-GRAPH.md from TASK-ALPHA-001
- Identifies modules with zero incoming imports
- Excludes known entry points (main.tsx, main.py, CLI scripts, tests)
- Categorizes orphans by likely reason (dead code, config, utility, unknown)
- Uses git timestamps to identify when files were last modified

**Dependencies:** TASK-ALPHA-001 (must complete first)

**Output format:**
```
# Orphaned Modules
## Summary
- Total modules: X
- Orphaned: Y
- Entry points excluded: Z

## Frontend Orphans
### [file path]
**Last modified:** [date]
**Exports:** [what it exports]
**Likely reason:** [dead code | config | etc.]

## Recommendations
- Files safe to delete
- Files to investigate
```

**Constraints:**
- Depend on IMPORT-GRAPH.md, do not re-scan codebase
- Max 500 lines
- Use `git log -1 --format=%ai -- <file>` for timestamps

---

### TASK-ALPHA-003: Identify Dead Exports
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-003-dead-exports.md`
**Model:** Haiku (graph cross-reference)
**Estimated time:** 10-15 minutes
**Deliverable:** `.deia/audits/2026-04-08/alpha/DEAD-EXPORTS.md`

**What it does:**
- Reads IMPORT-GRAPH.md from TASK-ALPHA-001
- Cross-references exports with imports
- Identifies symbols exported but never imported anywhere
- Categorizes by type (function, const, class, type, default)
- Prioritizes by severity (safe to remove, investigate, keep)

**Dependencies:** TASK-ALPHA-001 (must complete first)

**Output format:**
```
# Dead Exports
## Summary
- Total exports: X
- Dead exports: Y
- Files with dead exports: Z

## Frontend Dead Exports
### [file path]
#### `exportedSymbol`
**Type:** function | const | class | type | default
**Line:** [line number]
**Recommendation:** Remove | Investigate | Keep

## Recommendations by Severity
### High Priority (safe to remove)
### Medium Priority (investigate)
### Low Priority (keep)
```

**Constraints:**
- Depend on IMPORT-GRAPH.md
- Max 500 lines (split by priority if needed)
- Handle re-exports carefully

---

### TASK-ALPHA-004: Catalog Entry Points and First-Level Dependencies
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-004-entry-points.md`
**Model:** Haiku (dependency extraction from graph)
**Estimated time:** 10-15 minutes
**Deliverable:** `.deia/audits/2026-04-08/alpha/ENTRY-POINTS.md`

**What it does:**
- Reads IMPORT-GRAPH.md from TASK-ALPHA-001
- Identifies entry points (files not imported by other application files)
- Known entry points: main.tsx, main.py, scheduler_daemon.py, dispatcher_daemon.py, CLI scripts
- Lists first-level imports for each entry point
- Analyzes dependency overlap (shared imports across entry points)

**Dependencies:** TASK-ALPHA-001 (must complete first)

**Output format:**
```
# Entry Points
## Summary
- Total entry points: X
- Frontend: Y
- Backend: Z
- CLI/Scripts: W
- Tests: V

## Frontend Entry Points
### browser/src/main.tsx
**Type:** Vite entry
**First-level imports:** [list with resolved paths]

## Backend Entry Points
### hivenode/main.py
**Type:** FastAPI app
**First-level imports:** [list]

## Dependency Overlap Analysis
### Shared by Multiple Entry Points
### Entry Point Isolation
```

**Constraints:**
- Depend on IMPORT-GRAPH.md
- Max 500 lines
- Summarize test entry points by pattern, not individual files

---

## Execution Plan

**Sequential execution required** because tasks 2-4 depend on task 1:

1. **Dispatch TASK-ALPHA-001** (Sonnet, ~20-30 min)
2. **Wait for completion**, verify IMPORT-GRAPH.md exists
3. **Dispatch TASK-ALPHA-002, TASK-ALPHA-003, TASK-ALPHA-004 in parallel** (all Haiku, ~10-15 min each)
4. **Wait for all three to complete**
5. **Verify all four deliverables exist** and meet acceptance criteria
6. **Create ALPHA-COMPLETE.flag** to signal completion

**Total estimated time:** 40-60 minutes (wall time, accounting for parallelization)

---

## Acceptance Criteria Review

From original task spec:

- [ ] IMPORT-GRAPH.md covers all source files with proper import/export tracking → **TASK-ALPHA-001 deliverable**
- [ ] ORPHANED-MODULES.md identifies all modules never imported → **TASK-ALPHA-002 deliverable**
- [ ] DEAD-EXPORTS.md identifies all exported symbols never consumed → **TASK-ALPHA-003 deliverable**
- [ ] ENTRY-POINTS.md catalogs all entry points and first-level dependencies → **TASK-ALPHA-004 deliverable**
- [ ] All outputs written to `.deia/audits/2026-04-08/alpha/` → **All tasks write here**
- [ ] ALPHA-COMPLETE.flag created when done → **I create this after verifying all deliverables**

---

## Smoke Test Plan

After all tasks complete:

1. **Verify all 4 files exist:**
   ```bash
   ls -la .deia/audits/2026-04-08/alpha/
   ```
   Should show: IMPORT-GRAPH.md, ORPHANED-MODULES.md, DEAD-EXPORTS.md, ENTRY-POINTS.md

2. **Spot-check orphaned module list:**
   - Read ORPHANED-MODULES.md
   - Pick 2-3 files listed as orphaned
   - Grep codebase to confirm they're truly not imported

3. **Verify entry-points file contains frontend and backend routes:**
   - Read ENTRY-POINTS.md
   - Confirm main.tsx is listed (frontend)
   - Confirm main.py is listed (backend)

4. **Create completion flag:**
   ```bash
   touch .deia/audits/2026-04-08/alpha/ALPHA-COMPLETE.flag
   ```

---

## Constraints Verification

All task files comply with:
- ✅ Read-only operation (no source code modifications)
- ✅ No file over 500 lines (tasks split output if needed)
- ✅ Write to `.deia/audits/2026-04-08/alpha/` only
- ✅ Absolute file paths in all task docs
- ✅ All 8 response sections required
- ✅ No stubs, no TODOs

---

## Request for Q33NR

**Action requested:** Review the four task files and approve dispatch.

**Task files to review:**
1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-001-import-graph.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-002-orphaned-modules.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-003-dead-exports.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\TASK-ALPHA-004-entry-points.md`

**Questions for Q33NR:**
- Are the task scopes appropriate (not too broad, not too narrow)?
- Should TASK-ALPHA-001 use Sonnet or can Haiku handle the AST parsing?
- Are there additional entry points I should list in TASK-ALPHA-004?
- Should I split the work differently (e.g., frontend/backend as separate tasks)?

**Once approved, I will:**
1. Dispatch TASK-ALPHA-001 immediately
2. Monitor completion
3. Dispatch TASK-ALPHA-002, 003, 004 in parallel once 001 completes
4. Verify all deliverables and create ALPHA-COMPLETE.flag
5. Report final results to Q33NR

---

## Clock / Cost / Carbon (Planning Phase)

- **Clock:** 15 minutes (task file creation + planning doc)
- **Cost:** ~$0.05 (planning only, no bees dispatched yet)
- **Carbon:** Negligible (text generation only)

**Estimated bee execution:**
- TASK-ALPHA-001 (Sonnet): ~$0.50-1.00 (large codebase scan)
- TASK-ALPHA-002 (Haiku): ~$0.05-0.10 (graph analysis)
- TASK-ALPHA-003 (Haiku): ~$0.05-0.10 (graph analysis)
- TASK-ALPHA-004 (Haiku): ~$0.05-0.10 (graph analysis)
- **Total estimated:** ~$0.65-1.30 USD

---

**Awaiting Q33NR approval to dispatch.**
