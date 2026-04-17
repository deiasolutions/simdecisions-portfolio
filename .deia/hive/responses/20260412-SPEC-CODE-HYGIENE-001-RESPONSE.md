# SPEC-CODE-HYGIENE-001: Repo Code Hygiene Audit — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-12

## Files Modified

All files created (no source code modified per spec — audit only):
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\vulture.txt`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\ruff.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\mypy.txt`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\knip.json`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\tsc.txt`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\code-hygiene-2026-04-12.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\reports\analyze_hygiene.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\config\hygiene-whitelist.txt`

## What Was Done

- Installed missing tools: `vulture`, `ruff` (mypy, tsc, knip already installed)
- Ran all 5 code hygiene tools across Python and TypeScript codebases
- Generated raw reports for each tool (vulture.txt, ruff.json, mypy.txt, knip.json, tsc.txt)
- Created consolidated analysis report (`code-hygiene-2026-04-12.md`) with:
  - Dead code analysis (vulture): 93 findings, 78 false positives, 15 real issues
  - Lint violations (ruff): 446 violations, primarily 313 unused imports (F401)
  - Type errors (mypy): 481 errors, categorized by severity
  - TypeScript errors (tsc): 1887 errors, primarily test type mismatches
  - Unused dependencies (knip): 1 unused devDependency (`@types/p5`)
  - Stranded files (knip): 55 unreferenced files
  - Unused exports (knip): 126 exports (requires manual triage)
- Created whitelist for false positives (`.deia/config/hygiene-whitelist.txt`)
- Added detailed appendices with file:line breakdown for top offenders

## Acceptance Criteria Status

- [x] All 5 tools run without crashing (installed vulture and ruff)
- [x] `vulture.txt` generated — 93 findings catalogued, false positives identified
- [x] `ruff.json` generated — 446 violations, zero critical (all are style/unused code)
- [x] `mypy.txt` generated — 481 type errors catalogued, critical errors separated
- [x] `knip.json` generated — 1 unused dep, 55 stranded files, 126 unused exports
- [x] `tsc.txt` generated — 1887 TypeScript errors catalogued (pre-existing)
- [x] Consolidated summary written to `code-hygiene-2026-04-12.md`
- [x] Summary includes all 5 sections with file:line details
- [x] Each finding includes file path and line number where applicable
- [x] False positives triaged and added to `hygiene-whitelist.txt`

## Key Findings Summary

### Python (vulture + ruff + mypy)
- **Dead Code:** 15 real unused imports (after filtering 78 false positives)
- **Unused Imports (F401):** 313 violations — top offender: `_tools/inventory_db.py` (49 imports)
- **Type Errors:** 481 mypy errors — 28 missing stubs, 39 implicit Optional, 106 type mismatches
- **F-strings:** 46 f-strings missing placeholders (F541)
- **Bare excepts:** 3 instances (E722) — should use specific exception types

### TypeScript (tsc + knip)
- **Total Errors:** 1887 — primarily test files
- **TS2322 (638):** Type mismatches — string literals vs union types, enum value changes
- **TS2304 (344):** Missing Node.js types (`global`, `__dirname`) — need `@types/node`
- **TS2339 (273):** Deprecated properties (`conversation_id` → `conversationId`)
- **Stranded Files:** 55 unreferenced files (legacy tests, obsolete adapters, Vite artifacts)
- **Unused Deps:** `@types/p5` devDependency not used

## Recommendations (Priority Order)

1. **P1 — Install missing type stubs**
   - `pip install types-PyYAML types-requests`
   - Add `@types/node` to browser/tsconfig.json `types` array

2. **P2 — Fix critical type errors**
   - Fix 3 bare except clauses (E722) — use specific exceptions
   - Fix `builtins.any` → `typing.Any` in storage adapters (2 files)
   - Fix implicit Optional violations (39 function signatures)

3. **P3 — Clean unused imports**
   - Start with `_tools/inventory_db.py` (49 unused imports)
   - Clean `phase_ir/validation.py` (9 imports)
   - Clean `hive_mcp/local_server.py` (7 imports)

4. **P4 — Remove stranded files**
   - Delete legacy test files (`test-build-monitor-page.mjs`, `test-runner.mjs`)
   - Delete obsolete adapters (`factoryAdapter.tsx`, `responseBrowserAdapter.tsx`)
   - Delete Vite build artifacts (`vitest.config.ts.timestamp-*.mjs`)
   - Remove `@types/p5` from package.json devDependencies

5. **P5 — Fix TypeScript test errors**
   - Update enum literals in tests (`"home"` → `"home-only"`)
   - Rename test mock props (`_paneId` → `paneId`)
   - Fix `conversation_id` → `conversationId` in test data

## Blockers
None — all tools ran successfully

## Tests Run
None — this is an audit-only task per spec

## Next Steps
- Create follow-up specs for P1-P3 cleanup work
- Triage "unused exports" manually — many are legitimate public API surface
- Run hygiene audit quarterly to prevent accumulation

---

**Response file:** `.deia/hive/responses/20260412-SPEC-CODE-HYGIENE-001-RESPONSE.md`
