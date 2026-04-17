# TASK-SYNC-AUTOSTART-A: Enable Sync Auto-Start by Default

## Objective

Make sync enabled by default in hivenode startup so the PeriodicSyncWorker auto-starts and SyncQueue auto-flushes without requiring manual config.

## Context

The sync infrastructure is fully built (`SyncEngine`, `PeriodicSyncWorker`, `SyncQueue`, startup logic in `main.py`). However, sync is **disabled by default** because `main.py` checks for `config.yml` with `sync.enabled: true`. Most users don't have this config file, so sync never starts.

**Current behavior (main.py:86-94)**:
- Loads `~/.shiftcenter/config.yml`
- If file missing → `sync_enabled = False`
- If file exists but no `sync.enabled` key → `sync_enabled = False`

**Desired behavior**:
- Default to `sync_enabled = True` if config file missing
- Default to 60s interval if not specified
- Allow config file to override (e.g., set `enabled: false` to disable)

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\main.py` (lines 86-138)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\config.py`

## Deliverables

- [ ] Modify `main.py` lifespan to default `sync_enabled = True`
- [ ] Modify `main.py` to default `interval_seconds = 60`
- [ ] Config file still allows override (user can set `sync.enabled: false`)
- [ ] No changes to existing sync engine/worker/queue logic (only startup defaults)

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - No config file → sync starts with 60s interval
  - Config file with `enabled: false` → sync does not start
  - Config file with `enabled: true, interval_seconds: 120` → sync starts with 120s interval
  - Config file missing `sync` section → sync starts with 60s interval

## Constraints

- No file over 500 lines (main.py is currently 340 lines, safe to modify)
- TDD
- Python 3.13
- Must not break existing config file overrides
- Must not block hivenode startup if Railway is down

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260325-TASK-SYNC-AUTOSTART-A-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
