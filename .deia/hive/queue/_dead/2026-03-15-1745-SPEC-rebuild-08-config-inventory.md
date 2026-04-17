# SPEC: Rebuild config and inventory (sim.egg.md, inventory export, EGG system wiring)

## Priority
P0.40

## Model Assignment
haiku

## Objective
Re-apply configuration and inventory changes lost in a git reset.

### 1. eggs/sim.egg.md
Verify or rebuild the sim EGG definition. Check if the untracked file survived or if it was a tracked modification. If it needs rebuilding, reference TASK-140 response for the full EGG content.

### 2. EGG system wiring
Several EGG-related files were modified:
- `browser/src/eggs/eggInflater.ts` — check if changes from shell chrome work are needed
- `browser/src/eggs/eggLoader.ts` — same
- `browser/src/eggs/eggResolver.ts` — same
- `browser/src/eggs/index.ts` — same
- `browser/src/eggs/__tests__/eggResolver.test.ts` — same
- `browser/src/shell/eggToShell.ts` — same
- `browser/src/shell/useEggInit.ts` — same
- `browser/src/shell/__tests__/useEggInit.test.ts` — same

Read the current state of each file and compare to what the TASK response files say should be there. Only modify if something is actually missing/broken.

### 3. Feature inventory re-export
Run `python _tools/inventory.py export-md` to regenerate docs/FEATURE-INVENTORY.md and the 3 CSV files.

### 4. browser/package.json
Review current package.json. If any dependencies are missing that other rebuild specs need, add them. Check TASK-140 and TASK-141 responses for any npm dependency additions.

## Recovery Sources
- `.deia/hive/responses/20260315-TASK-140-RESPONSE.md` (sim.egg.md content)
- `.deia/hive/responses/20260315-TASK-164-RESPONSE.md` (shell chrome EGG wiring)
- `docs/specs/SPEC-EGG-SCHEMA-v1.md` (EGG schema reference)
- `docs/specs/SPEC-EGG-FORMAT-v0.3.1.md` (EGG format reference)

## Acceptance Criteria
- [ ] sim.egg.md exists and is valid
- [ ] EGG system files are consistent (no missing imports/exports)
- [ ] `cd browser && npx vitest run src/eggs/ src/shell/__tests__/useEggInit.test.ts` passes
- [ ] `python _tools/inventory.py export-md` succeeds
- [ ] docs/FEATURE-INVENTORY.md is regenerated
- [ ] browser builds without errors (`cd browser && npx vite build`)

## Constraints
- Max 500 lines per file
- No stubs
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1745-SPEC-rebuild-08-config-inventory", "status": "running", "model": "haiku", "message": "working"}

## File Claims (IMPORTANT — parallel bees)
Before modifying any file, claim it:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-1745-SPEC-rebuild-08-config-inventory", "files": ["eggs/sim.egg.md", "browser/src/eggs/eggInflater.ts", "browser/src/eggs/eggLoader.ts", "browser/src/eggs/eggResolver.ts", "browser/src/eggs/index.ts", "browser/src/shell/eggToShell.ts", "browser/src/shell/useEggInit.ts", "browser/package.json"]}
2. If response has conflicts (ok=false), poll GET http://localhost:8420/build/claims every 30s until yours.
