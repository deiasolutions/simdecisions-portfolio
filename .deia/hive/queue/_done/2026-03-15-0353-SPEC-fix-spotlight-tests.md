# SPEC: Fix regressions from spotlight-tests

## Priority
P0

## Role Override
queen

## Model Assignment
sonnet

## Override Approval
You have scoped approval to edit code files to fix the regressions below.
This approval is limited to the original task scope. Do not touch unrelated code.

## Objective
Fix post-bee regressions introduced while processing spotlight-tests.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-0338-SPEC-fix-spotlight-tests.md
Fix cycle: 2 of 2

### Regression Details
POST-BEE VERIFICATION FAILED: 2 regressions
  - tests/hivenode/test_auth_routes.py::test_jwt_issuer_must_be_ra96it
  - tests/hivenode/test_auth_routes.py::test_whoami_returns_user_id_field

Output (last 3000 chars):
y::test_storage_list_directory - httpx.Connect...
ERROR tests/hivenode/test_e2e.py::test_storage_list_empty_directory - httpx.C...
ERROR tests/hivenode/test_e2e.py::test_storage_stat_file - httpx.ConnectTimeo...
ERROR tests/hivenode/test_e2e.py::test_storage_stat_nonexistent_returns_404
ERROR tests/hivenode/test_e2e.py::test_storage_delete_file - httpx.ConnectTim...
ERROR tests/hivenode/test_e2e.py::test_storage_delete_nonexistent_returns_404
ERROR tests/hivenode/test_e2e.py::test_node_announce_rejects_without_jwt - ht...
ERROR tests/hivenode/test_e2e.py::test_node_discover_rejects_without_jwt - ht...
ERROR tests/hivenode/test_e2e.py::test_node_heartbeat_rejects_without_jwt - h...
ERROR tests/hivenode/test_e2e.py::test_node_routes_reject_local_mode - httpx....
ERROR tests/hivenode/test_e2e.py::test_storage_invalid_volume_returns_400 - h...
ERROR tests/hivenode/test_e2e.py::test_root_endpoint - httpx.ConnectTimeout: ...
ERROR tests/hivenode/test_e2e.py::test_storage_roundtrip_binary_data - httpx....
ERROR tests/hivenode/test_e2e.py::test_storage_large_file - httpx.ConnectTime...
ERROR tests/hivenode/test_e2e.py::test_storage_unicode_filenames - httpx.Conn...
ERROR tests/hivenode/test_e2e.py::test_health_uptime_increases - httpx.Connec...
ERROR tests/hivenode/test_e2e.py::test_concurrent_storage_writes - httpx.Conn...
ERROR tests/hivenode/test_kanban_routes.py::test_kanban_items_get_all - sqlal...
2 failed, 2516 passed, 22 skipped, 985 warnings, 28 errors in 284.47s (0:04:44)


[VITEST] Error: unsupported operand type(s) for +: 'NoneType' and 'str'

## Acceptance Criteria
- [ ] All regression failures listed above are resolved
- [ ] No new test regressions introduced
- [ ] Original task functionality preserved

## Constraints
- ONLY fix files related to the original task scope
- Do not refactor or restructure code
- Do not add new features
- Do not modify unrelated tests
