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
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-0353-SPEC-fix-spotlight-tests.md
Fix cycle: 1 of 2

### Regression Details
POST-BEE VERIFICATION FAILED: 11 regressions
  - tests/hivenode/test_auth_routes.py::test_jwt_issuer_must_be_ra96it
  - tests/hivenode/test_auth_routes.py::test_whoami_returns_user_id_field
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_existing_database_url_tests_unaffected
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_all_modes_get_default
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_constant_used
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_defaults_to_railway_pg
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_empty_string_uses_default
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_explicit_none_uses_default
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_local_keyword
  - tests/hivenode/test_config_inventory_url.py::TestInventoryUrlDefaults::test_inventory_url_sqlite_path_is_absolute
  - tests/hivenode/test_efemera.py::TestEfemeraStore::test_list_messages_since

Output (last 3000 chars):
::test_storage_list_directory - httpx.Connect...
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
11 failed, 2507 passed, 22 skipped, 985 warnings, 28 errors in 268.70s (0:04:28)


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
