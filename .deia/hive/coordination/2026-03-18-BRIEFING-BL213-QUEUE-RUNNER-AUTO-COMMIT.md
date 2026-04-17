# Briefing: BL-213 — Queue Runner Auto-Commits Bee Output on File Release

## Objective
Implement auto-commit in the queue runner so that when a bee completes and releases file claims, its code changes are immediately committed as a crash-recovery checkpoint.

## Why
Today we lost ~280 lines of uncommitted queue runner changes to a git stash incident. If deconfliction fails or the queue runner crashes, all uncommitted bee work is gone. Each bee's output needs to be checkpointed via git commit immediately on completion.

## What To Build

In `run_queue.py`, in the `_handle_spec_result()` function (or right after it in the pool loop), add logic that:

1. After a bee's spec result comes back (CLEAN, NEEDS_DAVE, or FAILED), run:
   - `git add <files>` for the files the bee modified
   - `git commit -m "[BEE-MODEL] SPEC-ID: objective"`
2. On NEEDS_DAVE or FAILED, include status: `[BEE-MODEL] SPEC-ID: objective (NEEDS_DAVE)`
3. If `git add` or `git commit` fails (nothing to commit, merge conflict), log a warning but do NOT crash the queue runner
4. No `git push` — commit only
5. No `git merge`, `git rebase`, or any destructive git operation

## How To Know Which Files

Option A: Query `/build/claims` before the bee releases to see what files it held
Option B: Use `git diff --name-only` to detect all changed files, commit them all
Option C: Track file claims in the queue runner when the bee is submitted

Option B is simplest and safest — just commit whatever changed.

## Rule 10 Carve-Out
Already documented in `.deia/BOOT.md` Rule 10: "Exception: The queue runner (run_queue.py) may auto-commit bee output when a bee completes and releases file claims."

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py` — specifically `_handle_spec_result` and the pool completion loop
- `.deia/BOOT.md` — Rule 10 carve-out
- `hivenode/routes/build_monitor.py` — file claim API (`/build/claim`, `/build/release`, `/build/claims`)

## Constraints
- No file over 500 lines
- TDD — tests first
- Must not break existing queue runner flow if git is unavailable
- Use `subprocess.run(["git", ...])` for git operations
- At least 6 tests (mock subprocess calls, verify commit message format, verify failure handling, verify no-push)

## Model: sonnet

## Response
Write response to: `.deia/hive/responses/20260318-BL-213-RESPONSE.md`
