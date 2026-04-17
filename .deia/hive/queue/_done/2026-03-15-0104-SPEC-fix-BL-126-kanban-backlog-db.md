# SPEC: Fix regressions from BL-126-kanban-backlog-db

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
Fix post-bee regressions introduced while processing BL-126-kanban-backlog-db.

## Context
Original spec: C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\queue\2026-03-14-2100-SPEC-BL-126-kanban-backlog-db.md
Fix cycle: 1 of 2

### Regression Details
POST-BEE VERIFICATION FAILED: 50 regressions
  - tests/engine/des/test_des_durations.py::TestConstantDuration::test_constant_duration_5
  - tests/engine/des/test_des_durations.py::TestConstantDuration::test_constant_duration_linear_flow
  - tests/engine/des/test_des_durations.py::TestDefaultDuration::test_linear_flow_all_default
  - tests/engine/des/test_des_durations.py::TestExistingTestsStillPass::test_fork_flow_default_duration
  - tests/engine/des/test_des_durations.py::TestExistingTestsStillPass::test_linear_three_nodes_default_duration
  - tests/engine/des/test_des_generators.py::TestGenerator::test_active_window_filters_arrivals
  - tests/engine/des/test_des_generators.py::TestGeneratorManager::test_no_arrivals_outside_active_window
  - tests/engine/des/test_des_guards.py::TestEndToEndWithGuards::test_simulation_parallel_fork_completes_all
  - tests/engine/des/test_des_guards.py::TestExclusiveGateway::test_first_matching_guard_wins
  - tests/engine/des/test_des_guards.py::TestExclusiveGateway::test_no_match_no_default_produces_nothing
  - tests/engine/des/test_des_guards.py::TestExclusiveGateway::test_only_one_edge_fires
  - tests/engine/des/test_des_guards.py::TestExclusiveGateway::test_switch_default_fallback_fires
  - tests/engine/des/test_des_guards.py::TestGuardFailsTokenBlocked::test_any_edge_fails_guard
  - tests/engine/des/test_des_guards.py::TestGuardFailsTokenBlocked::test_invalid_guard_blocks_token
  - tests/engine/des/test_des_guards.py::TestGuardFailsTokenBlocked::test_repeat_edge_fails_guard_exits_loop
  - tests/engine/des/test_des_guards.py::TestGuardFailsTokenBlocked::test_switch_edge_fails_guard
  - tests/engine/des/test_des_guards.py::TestGuardPassesTokenFollows::test_any_edge_passes_guard
  - tests/engine/des/test_des_guards.py::TestGuardPassesTokenFollows::test_repeat_edge_passes_guard
  - tests/engine/des/test_des_guards.py::TestGuardPassesTokenFollows::test_switch_edge_passes_guard
  - tests/engine/des/test_des_guards.py::TestMixedEdgeTypes::test_then_and_switch_coexist
  - tests/engine/des/test_des_guards.py::TestParallelGateway::test_fork_all_edges_fire
  - tests/engine/des/test_des_guards.py::TestParallelGateway::test_fork_all_get_same_token_id
  - tests/engine/des/test_des_guards.py::TestParallelGateway::test_fork_preserves_token_properties
  - tests/engine/des/test_des_guards.py::TestUnconditionalEdge::test_sink_node_increments_completed
  - tests/engine/des/test_des_guards.py::TestUnconditionalEdge::test_then_edge_empty_guard_fires
  - tests/engine/des/test_des_guards.py::TestUnconditionalEdge::test_then_edge_no_guard_fires
  - tests/engine/des/test_des_integration_phase_e.py::TestCallCenterSimulation::test_all_existing_tests_pass
  - tests/engine/des/test_des_integration_phase_e.py::TestCallCenterSimulation::test_call_center_simulation
  - tests/engine/des/test_des_integration_phase_e.py::TestCallCenterSimulation::test_distribution_durations
  - tests/engine/des/test_des_integration_phase_e.py::TestCallCenterSimulation::test_generator_creates_multiple_tokens
  - tests/engine/des/test_des_integration_phase_e.py::TestCallCenterSimulation::test_replication_with_v2
  - tests/engine/des/test_des_integration_phase_e.py::TestComplexScenarios::test_distribution_duration_variability
  - tests/engine/des/test_des_integration_phase_e.py::TestComplexScenarios::test_generator_with_entity_attributes
  - tests/engine/des/test_des_integration_phase_e.py::TestComplexScenarios::test_mixed_arrival_types
  - tests/engine/des/test_des_integration_phase_e.py::TestRegressionGuards::test_v1_flows_still_work
  - tests/engine/des/test_des_integration_phase_e.py::TestV2LoaderIntegration::test_v2_loader_creates_generators
  - tests/engine/des/test_des_integration_phase_e.py::TestV2LoaderIntegration::test_v2_loader_creates_pools
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
50 failed, 2470 passed, 13 skipped, 985 warnings, 35 errors in 282.19s (0:04:42)


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
