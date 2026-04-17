# BRIEFING: Forensic Investigation — Unauthorized git reset + Rebuild Plan

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Priority:** P0 — EMERGENCY

---

## Situation

At approximately 16:57 local time, a `git reset --hard HEAD` was executed on the shiftcenter repo. This wiped ALL uncommitted tracked-file modifications across ~40+ files. The git reflog shows:

```
a9e050c HEAD@{0}: reset: moving to HEAD
```

**This is a Hard Rule #10 violation.** No bee, Q33N, or Q33NR is authorized to run git write operations without Q88N approval. Someone ran `git reset --hard HEAD` without authorization.

## What Was Lost

All files that were unstaged-modified (` M` in git status) were reverted to HEAD (`a9e050c`). This includes work from today's bee dispatches that was never committed:

### Lost Tracked-File Modifications (` M` → clean)
- `.deia/config/queue.yml`
- `.deia/hive/scripts/queue/run_queue.py`
- `.deia/hive/scripts/queue/ship_feeder.py`
- `_tools/inventory.py`
- `browser/package.json`
- `browser/src/App.tsx`
- `browser/src/apps/__tests__/simAdapter.test.tsx`
- `browser/src/apps/authAdapter.tsx`
- `browser/src/apps/index.ts`
- `browser/src/apps/sim/components/flow-designer/FlowDesigner.tsx`
- `browser/src/apps/simAdapter.tsx`
- `browser/src/apps/treeBrowserAdapter.tsx`
- `browser/src/eggs/__tests__/eggResolver.test.ts`
- `browser/src/eggs/eggInflater.ts`
- `browser/src/eggs/eggLoader.ts`
- `browser/src/eggs/eggResolver.ts`
- `browser/src/eggs/index.ts`
- `browser/src/infrastructure/relay_bus/constants.ts`
- `browser/src/primitives/apps-home/AppCard.tsx`
- `browser/src/primitives/apps-home/__tests__/AppCard.test.tsx`
- `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx`
- `browser/src/primitives/auth/LoginPage.css`
- `browser/src/primitives/auth/LoginPage.tsx`
- `browser/src/primitives/tree-browser/TreeNodeRow.tsx`
- `browser/src/primitives/tree-browser/types.ts`
- `browser/src/services/identity/__tests__/identityService.test.ts`
- `browser/src/services/identity/identityService.ts`
- `browser/src/shell/__tests__/useEggInit.test.ts`
- `browser/src/shell/components/MenuBar.tsx`
- `browser/src/shell/components/Shell.tsx`
- `browser/src/shell/components/ShellTabBar.tsx`
- `browser/src/shell/components/WorkspaceBar.tsx`
- `browser/src/shell/components/__tests__/MenuBar.test.tsx`
- `browser/src/shell/components/__tests__/WorkspaceBar.test.tsx`
- `browser/src/shell/eggToShell.ts`
- `browser/src/shell/useEggInit.ts`
- `commit-msg.txt`
- `docs/FEATURE-INVENTORY.md`
- `docs/feature-inventory-backlog.csv`
- `docs/feature-inventory-bugs.csv`
- `docs/feature-inventory-features.csv`
- `eggs/sim.egg.md`
- `hivenode/rag/indexer/__init__.py`
- `hivenode/rag/indexer/indexer_service.py`
- `hivenode/rag/indexer/models.py`
- `hivenode/rag/indexer/scanner.py`
- `hivenode/rag/indexer/storage.py`
- `hivenode/routes/__init__.py`
- `hivenode/routes/build_monitor.py`
- `pyproject.toml`
- `ra96it/services/audit.py`
- `tests/hivenode/rag/indexer/test_cloud_sync.py`
- `tests/hivenode/rag/indexer/test_indexer_service.py`
- `tests/hivenode/rag/indexer/test_markdown_exporter.py`
- `tests/hivenode/rag/indexer/test_metrics_updater.py`
- `tests/hivenode/rag/indexer/test_models.py`
- `tests/hivenode/rag/indexer/test_reliability.py`
- `tests/hivenode/rag/indexer/test_scanner.py`
- `tests/hivenode/rag/indexer/test_storage.py`
- `tests/hivenode/rag/test_rag_routes.py`
- `tests/hivenode/test_build_monitor.py`

### What Survived (untracked `??` files — not affected by reset)
All new files created by bees survived. The `canvas/`, `des_routes.py`, `rag_routes.py`, `chunker.py`, `embedder.py`, MaximizedOverlay, all test files in `__tests__/` dirs that were new — these are fine.

### What's Currently Modified (new bee work on top of HEAD)
A bee (or bees) made NEW modifications after the reset:
- `browser/src/apps/appsHomeAdapter.tsx`
- `browser/src/primitives/apps-home/AppCard.tsx`
- `browser/src/primitives/apps-home/AppsHome.css`
- `browser/src/primitives/apps-home/AppsHome.tsx`
- `browser/src/primitives/apps-home/__tests__/AppCard.test.tsx`
- `browser/src/primitives/apps-home/__tests__/AppsHome.test.tsx`
- `browser/src/primitives/apps-home/index.ts`
- `browser/src/primitives/apps-home/mockData.ts`
- `browser/src/primitives/apps-home/types.ts`
- `browser/src/primitives/terminal/types.ts`
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/services/egg-registry/__tests__/eggRegistryService.test.ts`
- `browser/src/services/egg-registry/eggRegistryService.ts`
- `browser/src/services/egg-registry/index.ts`
- `browser/src/services/egg-registry/types.ts`

---

## Your Assignment (Q33N)

### Part 1: Forensic Investigation

1. **Find who ran `git reset --hard HEAD`.** Check ALL bee RAW response files (`.deia/hive/responses/20260315-*-RAW.txt`) for any mention of `git reset`, `git checkout`, `git restore`, `git clean`, `git stash`, or any git write command. Check EVERY file — not just the ones from 16:28-16:50. The reset could have been triggered by ANY bee at ANY time today.

2. **Check the queue runner and dispatch system.** Read `.deia/hive/scripts/queue/run_queue.py` and `.deia/hive/scripts/dispatch/dispatch.py` — do either of these run git operations as part of their workflow? Could the queue runner have triggered a reset?

3. **Check the build monitor.** Read `hivenode/routes/build_monitor.py` — does the build monitor or watchdog run any git operations?

4. **Check ship_feeder.py.** Read `.deia/hive/scripts/queue/ship_feeder.py` — does it run git operations?

5. **Determine the exact sequence.** The Vite HMR logs show a massive file reload at 16:57. Cross-reference bee dispatch timestamps to determine which bee was active at that exact moment.

### Part 2: Damage Assessment

For each lost file, determine:
1. Which TASK originally modified it (check all TASK response files)
2. Whether the response file contains enough detail to reconstruct the change
3. Whether the change was a NEW file creation (survived as `??`) or a MODIFICATION of an existing tracked file (lost)

Categorize each lost file as:
- **RECOVERABLE** — response file has exact code or enough detail to rebuild
- **PARTIALLY RECOVERABLE** — response file describes what was done but lacks exact code
- **NOT RECOVERABLE** — no response file covers this change (was done interactively by Q88N/Q33NR)

### Part 3: Rebuild Plan

Write a prioritized rebuild plan. For each rebuild task:
- Source: which response file(s) to reference
- Target: which file(s) to modify
- Complexity: trivial (1-line change) / small (< 20 lines) / medium (20-100 lines) / large (> 100 lines)
- Priority: P0 (blocks everything) / P1 (needed for builds) / P2 (needed for tests) / P3 (nice to have)

---

## Deliverables

Write your full report to: `.deia/hive/coordination/2026-03-15-COORDINATION-REPORT-forensic-git-reset.md`

The report MUST contain:
1. **Forensic findings** — who/what ran the reset, evidence
2. **Complete damage manifest** — every lost file, its task, recoverability
3. **Rebuild plan** — prioritized task list with sources
4. **Preventive recommendation** — what guardrail failed, what to add

---

## Constraints
- Do NOT run any git write operations
- Do NOT modify any source files
- Read-only investigation: git log, git diff, git reflog, file reads only
- Report back to Q33NR when complete

## Model Assignment
sonnet
