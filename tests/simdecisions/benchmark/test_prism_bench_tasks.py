"""
test_prism_bench_tasks
======================

Test suite for PRISM-bench tasks validation.

Validates that all 20 tasks:
- Load as valid JSON
- Have required metadata fields
- Have category-specific metadata
- Have unique node IDs
- Have valid edge references

Dependencies:
- import json
- from pathlib import Path
- import pytest

Functions:
- get_all_task_files(): Get all JSON files in prism_bench_tasks directory.
- test_task_loads_as_json(task_file): Test that task file is valid JSON.
- test_task_has_required_top_level_fields(task_file): Test that task has required top-level PRISM-IR fields.
- test_task_has_required_metadata(task_file): Test that task metadata has all required fields.
- test_task_category_valid(task_file): Test that task category is one of the 5 valid categories.
- test_node_ids_unique(task_file): Test that all node IDs within a task are unique.
- test_edge_references_valid(task_file): Test that all edge from_node/to_node references exist in nodes.
- test_recovery_tasks_have_failure_injection_metadata(task_file): Test that recovery tasks have failure_injection metadata.
- test_multi_agent_tasks_have_handoff_metadata(task_file): Test that multi-agent tasks have handoff_points metadata.
- test_branch_comparison_tasks_have_strategies_metadata(task_file): Test that branch-comparison tasks have strategies metadata.
- test_governance_tasks_have_governance_mode_metadata(task_file): Test that governance tasks have governance_mode metadata.
- test_task_count_per_category(): Test that there are exactly 4 tasks per category.
- test_total_task_count(): Test that there are exactly 20 tasks total.
- test_expected_runtime_positive(task_file): Test that expected_runtime_seconds is a positive number.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
