# TASK-040: 8os Remaining CLI Commands -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-13

## Files Modified

### Created
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_cli_commands.py`

### Modified
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\cli.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\schemas.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage_routes.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\node_local.py`

## What Was Done

### CLI Commands Added (7 new commands)
1. **`8os queue`** — Run build queue
   - `--status` flag shows pending/archived task counts
   - Imports and executes `run_queue()` from `.deia/hive/scripts/queue/run_queue.py`

2. **`8os dispatch <task_file>`** — Dispatch single task
   - `--model` (haiku/sonnet/opus, default: sonnet)
   - `--role` (bee/queen/oracle, default: bee)
   - `--inject-boot` flag to inject BOOT.md
   - Calls `.deia/hive/scripts/dispatch.py` via subprocess

3. **`8os index`** — Rebuild repo semantic search index
   - `--full` flag for full rebuild (not incremental)
   - Calls `_tools/build_index.py` via subprocess

4. **`8os inventory [args...]`** — Passthrough to inventory CLI
   - All arguments forwarded to `_tools/inventory.py`
   - Supports: `stats`, `add`, `bug add`, etc.

5. **`8os volumes`** — List mounted volumes
   - Shows volume name, type, online/offline status, path
   - Calls GET `/storage/volumes` on local hivenode

6. **`8os node list`** — Show connected nodes
   - Displays node ID, mode, IP, status, last seen (relative time)
   - Calls GET `/node/peers` on local hivenode

7. **`8os node announce`** — Force re-announce to cloud
   - Calls POST `/node/announce` on local hivenode

### Backend Routes Added
1. **GET `/storage/volumes`** (storage_routes.py)
   - Returns list of all mounted volumes with status
   - Uses VolumeRegistry to enumerate volumes
   - Returns VolumeInfo for each volume (name, type, online, path)

2. **POST `/node/announce`** (node_local.py)
   - Forces re-announcement to cloud
   - Uses NodeAnnouncementClient dependency
   - Returns announced_at timestamp

### Schemas Added
- `VolumeInfo` — name, type, online (bool), path
- `VolumesResponse` — volumes list

### Helper Functions Added (cli.py)
- `_run_queue()` — Dynamically imports and runs queue runner
- `_show_queue_status()` — Counts pending/archived tasks in `.deia/hive/tasks/`

### Test Suite (24 tests, all passing)
**Coverage:**
- Queue: status display, run execution, error handling (4 tests)
- Dispatch: task dispatch, option flags, missing script, errors (4 tests)
- Index: rebuild, full rebuild, missing script, errors (4 tests)
- Inventory: passthrough args, complex args, missing script, errors (4 tests)
- Volumes: list display, empty list, hivenode not running (3 tests)
- Node: list peers, announce, empty list, hivenode not running (5 tests)

**Test patterns:**
- Used `click.testing.CliRunner()` for CLI testing
- Mocked `subprocess.run()` for passthrough commands
- Mocked `httpx.get()/post()` for hivenode API calls
- Used isolated filesystem for queue tests
- Module cache clearing for queue error tests

## Test Results

```
tests/hivenode/test_cli_commands.py::test_queue_status_shows_counts PASSED
tests/hivenode/test_cli_commands.py::test_queue_status_empty PASSED
tests/hivenode/test_cli_commands.py::test_queue_run PASSED
tests/hivenode/test_cli_commands.py::test_queue_run_error PASSED
tests/hivenode/test_cli_commands.py::test_dispatch_task PASSED
tests/hivenode/test_cli_commands.py::test_dispatch_with_options PASSED
tests/hivenode/test_cli_commands.py::test_dispatch_missing_script PASSED
tests/hivenode/test_cli_commands.py::test_dispatch_error PASSED
tests/hivenode/test_cli_commands.py::test_index_rebuild PASSED
tests/hivenode/test_cli_commands.py::test_index_full_rebuild PASSED
tests/hivenode/test_cli_commands.py::test_index_missing_script PASSED
tests/hivenode/test_cli_commands.py::test_index_error PASSED
tests/hivenode/test_cli_commands.py::test_inventory_passthrough PASSED
tests/hivenode/test_cli_commands.py::test_inventory_passthrough_complex_args PASSED
tests/hivenode/test_cli_commands.py::test_inventory_missing_script PASSED
tests/hivenode/test_cli_commands.py::test_inventory_error PASSED
tests/hivenode/test_cli_commands.py::test_volumes_list PASSED
tests/hivenode/test_cli_commands.py::test_volumes_empty PASSED
tests/hivenode/test_cli_commands.py::test_volumes_hivenode_not_running PASSED
tests/hivenode/test_cli_commands.py::test_node_list PASSED
tests/hivenode/test_cli_commands.py::test_node_list_empty PASSED
tests/hivenode/test_cli_commands.py::test_node_list_hivenode_not_running PASSED
tests/hivenode/test_cli_announce PASSED
tests/hivenode/test_node_announce_hivenode_not_running PASSED

24 passed in 0.17s
```

Full test suite: 114 passed (CLI + storage tests)

## Acceptance Criteria Status

1. ✅ `8os queue` runs build queue
2. ✅ `8os queue --status` shows pending/archived counts
3. ✅ `8os dispatch TASK.md` dispatches single task with options
4. ✅ `8os index` rebuilds repo index (incremental)
5. ✅ `8os index --full` rebuilds repo index (full)
6. ✅ `8os inventory` passes args to inventory.py
7. ✅ `8os volumes` shows volume list with online/offline status
8. ✅ `8os node list` shows connected nodes
9. ✅ `8os node announce` forces re-announce to cloud
10. ✅ All commands handle "hivenode not running" gracefully
11. ✅ All tests pass (24/24)

## Implementation Notes

- **No file over 500 lines** — cli.py: 445 lines (within limit)
- **TDD approach** — Tests written first, then implementation
- **No stubs** — All functions fully implemented
- **Error handling** — All commands exit with code 1 on error, write to stderr
- **Passthrough commands** — Use `subprocess.run()` to avoid import cycles
- **Queue runner** — Dynamically imported at runtime using sys.path manipulation
- **Module caching** — Test suite clears `run_queue` from sys.modules to prevent cache interference
- **Relative time formatting** — Node list shows "just now", "2m ago", "3h ago", "5d ago"
- **Volume type display** — Converts "local_filesystem" to "local filesystem" for readability

## Dependencies Met

- Queue runner: ✅ (already built)
- Dispatch script: ✅ (already built)
- Inventory CLI: ✅ (already built)
- VolumeRegistry: ✅ (already built)
- Node client (TASK-039): ✅ (already built)

## What's Next

All Wave 4 CLI commands complete. 8os CLI tool is now fully functional with:
- Server management (up, down, status)
- Sync operations (sync, sync --status)
- Build pipeline (queue, dispatch, index)
- Feature tracking (inventory)
- Infrastructure (volumes, node list/announce)
