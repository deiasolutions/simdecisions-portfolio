# SPEC: BL-213 — Queue runner auto-commits bee output on file release

## Priority: P0

## Problem
When bees complete work but the queue runner crashes, gets stashed, or deconfliction fails, all uncommitted bee output is lost. Today we lost ~280 lines of queue runner changes to a git stash incident. There's no checkpoint between "bee writes code" and "human manually commits."

## Objective
When a bee completes and releases its file claims, the queue runner should immediately `git commit` the bee's changed files as a crash-recovery checkpoint.

## Model: sonnet

## Acceptance Criteria
- [ ] After a bee's spec result comes back CLEAN, queue runner runs `git add` on files the bee touched (from file claims) and `git commit`
- [ ] Commit message format: `[BEE-MODEL] SPEC-ID: objective` (e.g. `[BEE-HAIKU] SPEC-TASK-BUG022: fix canvas palette icon clicks`)
- [ ] On NEEDS_DAVE or FAILED results, still commit with status in message: `[BEE-MODEL] SPEC-ID: objective (NEEDS_DAVE)`
- [ ] If `git add` or `git commit` fails (nothing to commit, merge conflict), log warning but don't crash the queue runner
- [ ] No `git push` — commit only, push is manual by Q88N
- [ ] No `git merge`, `git rebase`, or any other destructive git operation
- [ ] Queue runner must query `/build/claims` to know which files the bee touched, OR track submitted spec file claims
- [ ] This is a Rule 10 carve-out — already documented in BOOT.md
- [ ] Tests: at least 6 tests (mock git subprocess calls, verify commit message format, verify failure handling)
- [ ] No file over 500 lines

## Implementation Notes
- Use `subprocess.run(["git", "add", ...])` and `subprocess.run(["git", "commit", "-m", ...])`
- Get file list from `/build/claims` endpoint before the bee releases, or from the spec's file claim record
- Add this logic in `_handle_spec_result()` in `run_queue.py`, right before moving spec to `_done/`
- The commit happens in the queue runner process (not in the bee process)

## Smoke Test
- Queue runner processes a spec, bee completes, `git log -1` shows auto-commit with correct format
- If bee fails, commit still happens with failure status in message
- If no files changed, no empty commit created

## Constraints
- No file over 500 lines
- TDD — tests first
- No git push, no git merge, no destructive operations
- Must not break existing queue runner flow if git is unavailable

## Files to Read First
- `.deia/hive/scripts/queue/run_queue.py` (specifically `_handle_spec_result`)
- `.deia/BOOT.md` (Rule 10 carve-out)
- `hivenode/routes/build_monitor.py` (file claim API)
