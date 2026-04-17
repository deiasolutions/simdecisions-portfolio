# TASK-REFACTOR-MONITOR-003: Monitor Phase 2 Architecture Cleanup

## Role
Queen (Q33N)

## Context

Overnight refactor pipeline on branch `refactor/auto-2026-04-07`.

- Phase 0 (inventory): COMPLETE (010-013)
- Phase 1 (validation baseline): COMPLETE (020-023) — 98.2% pass rate (221/225)
- Phase 2 (architecture cleanup): IN PROGRESS — REFACTOR-030 active

Phase 2 specs (sequential):
- 030: consolidate directory structure
- 031: set-md configs
- 032: wire egg loading
- 033: dedupe utilities
- 034: remove dead code

These are the first specs that MODIFY CODE. Previous phases were read-only analysis.

## Your Job

### 1. Check Current State
```bash
echo "=== DONE ===" && ls .deia/hive/queue/_done/ | grep REFACTOR
echo "=== ACTIVE ===" && ls .deia/hive/queue/_active/ | grep REFACTOR
echo "=== NEEDS REVIEW ===" && ls .deia/hive/queue/_needs_review/ | grep REFACTOR
echo "=== OUTPUTS ===" && ls .deia/hive/refactor/
```

### 2. Monitor Phase 2 Progress
Check every 5 minutes for up to 45 minutes. Phase 2 specs are sequential so they'll run one at a time.

For each active spec, check:
- Is the bee producing output? (`ls .deia/hive/refactor/ | grep changes`)
- Is the bee still alive? (`curl -s http://127.0.0.1:8420/build/status`)
- Has it exceeded 30 minutes without progress? (Possible stall)

### 3. Fix Any Stalls
If a spec moves to `_needs_review/`:
1. Check if there's an output file for it in `.deia/hive/refactor/`
2. If output exists and is valid, manually move spec to `_done/`
3. If no output, move to `backlog/` for re-dispatch
4. If re-dispatch also fails, manually dispatch via dispatch.py

### 4. Verify Code Changes
Phase 2 specs modify actual code. After each spec completes, do a quick sanity check:
```bash
git diff --stat  # See what files changed
git log --oneline -5  # See commit messages
```

### 5. Report Pipeline State
When your monitoring window ends, report:
- Which Phase 2 specs completed
- What code changes were made
- Any issues encountered
- Current pipeline position

## Expected Output Files from Phase 2
- `changes-030.json` (directory consolidation)
- `changes-031.json` (set-md configs)
- `changes-032.json` (egg loading wiring)
- `changes-033.json` (utility deduplication)
- `changes-034.json` (dead code removal)

## Response
Write to `.deia/hive/responses/20260407-REFACTOR-MONITOR-003-RESPONSE.md`

## Constraints
- Stay on branch `refactor/auto-2026-04-07`
- Do NOT modify code yourself — only move spec files and dispatch bees
- If a bee's code change breaks the build, document it but do NOT fix it — that's for Q88N to decide
