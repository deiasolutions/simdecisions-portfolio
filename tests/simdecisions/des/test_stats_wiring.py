"""
test_stats_wiring
=================

Tests for statistics collection wiring into DES event loop.

Verifies that StatisticsCollector methods are called during simulation runs
and produce non-zero meaningful statistics.

Dependencies:
- from simdecisions.des.core import SimConfig, load_flow
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.phase_ir.primitives import Flow, Node, Edge

Functions:
- test_basic_flow_cycle_time_collected(): Simple flow should produce non-zero cycle time.
- test_basic_flow_throughput(): Simple flow should produce non-zero throughput.
- test_arrivals_counter(): Arrivals counter should match tokens_created.
- test_completions_counter(): Completions counter should match tokens_completed.
- test_per_node_service_time(): Per-node service time should be recorded.
- test_per_node_throughput(): Per-node throughput should be recorded for sink.
- test_abandonment_counter_with_renege(): Abandonment counter should increase when renege_timeout fires.
- test_wip_tracking(): WIP tracking should produce non-zero mean WIP.
- test_multi_server_flow_node_throughput(): Multi-server flow should track throughput for each server node.
- test_summary_dict_keys_present(): Summary dict should have all expected keys and non-zero values.
- test_replication_confidence_intervals(): Multiple replications should each collect non-zero statistics.
- test_parameter_sweep_non_zero_metrics(): Stats should vary across different parameter settings.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
