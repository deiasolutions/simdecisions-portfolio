# SPEC: Fix regressions from engine-import-paths

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
Fix post-bee regressions introduced while processing engine-import-paths.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-15-0158-SPEC-fix-engine-import-paths.md
Fix cycle: 1 of 2

### Regression Details
POST-BEE VERIFICATION FAILED: 13 regressions
  - tests/hivenode/rag/test_integration.py::TestBackwardCompatibility::test_existing_index_endpoint
  - tests/hivenode/rag/test_integration.py::TestBackwardCompatibility::test_existing_search_endpoint
  - tests/hivenode/rag/test_integration.py::TestBokEnrichment::test_bok_enrichment_adds_context
  - tests/hivenode/rag/test_integration.py::TestCloudSync::test_cloud_sync_all
  - tests/hivenode/rag/test_integration.py::TestEntityVectors::test_entity_vector_calculation
  - tests/hivenode/rag/test_integration.py::TestFullIndexingPipeline::test_index_repository_creates_records
  - tests/hivenode/rag/test_integration.py::TestSyncDaemonImmediate::test_immediate_sync_policy
  - tests/hivenode/test_auth_routes.py::test_jwt_issuer_must_be_ra96it
  - tests/hivenode/test_auth_routes.py::test_whoami_returns_user_id_field
  - tests/hivenode/test_smoke_backup.py::test_smoke_full_flow
  - tests/hivenode/test_smoke_backup.py::test_smoke_ledger_query_by_type
  - tests/hivenode/test_smoke_backup.py::test_smoke_sync_trigger
  - tests/test_inventory_schema.py::test_add_feature_and_list

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
13 failed, 2507 passed, 20 skipped, 985 warnings, 28 errors in 287.13s (0:04:47)


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
