# Briefing: Check Overnight Commit for Reverted/Lost Changes

## Objective
Investigate commit `43f447f` ("Crash recovery checkpoint: Wave 2-3 bee output + queue pool upgrade") and the current working tree to identify changes that may have been silently reverted by stale specs during the 30-item overnight batch on 2026-03-17.

## Context
On 2026-03-17, we ran a 30-item batch of specs through the queue runner. Some of those specs were written at different times. We discovered that stale specs (written before other work completed) may have overwritten newer changes. Specifically, changes to the build monitor Active list that had been working for hours were silently reverted by a later bee working from an older spec.

## What To Do

### 1. Examine the overnight commit
Run `git show --stat 43f447f` to see all files in that commit.
Run `git log --oneline -20` to see the surrounding commits.

### 2. Compare key files between commits
For each file in the overnight commit, check if the CURRENT working tree version differs from the committed version:
- `git diff 43f447f -- <file>` for important files

Focus especially on:
- `hivenode/routes/build_monitor.py` — the file we know was reverted
- `browser/src/App.tsx` — heavily modified by multiple specs
- `.deia/hive/scripts/queue/run_queue.py` — queue runner itself
- Any files touched by multiple specs in the overnight batch

### 3. Check for specs that touched the same files
Look at the specs in `.deia/hive/queue/_done/` from 2026-03-17. For each one that has a `## Files to Read First` or `## File Claims` section, list which files they targeted. Identify any file that was targeted by MORE THAN ONE spec — those are the collision candidates.

### 4. Check git log for sequential overwrites
Run `git log --all --oneline -- hivenode/routes/build_monitor.py` to see the full history of the file we know was affected.

### 5. Write report
List:
- Files that were modified by multiple specs (collision candidates)
- Files where the current version appears to be an older/reverted version
- Changes that appear recoverable from git history
- Recommended actions (cherry-pick, manual merge, re-spec)

## Files to Read First
- `.deia/hive/session-logs/2026-03-17-Q33NR-BUILD-LOG.md` (if it exists — overnight session log)
- `.deia/hive/queue/_done/` — completed specs from overnight batch

## Model: sonnet

## Response
Write response to: `.deia/hive/responses/20260318-OVERNIGHT-REVERT-CHECK.md`
