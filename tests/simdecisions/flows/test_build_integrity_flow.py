"""
test_build_integrity_flow
=========================

Tests for Build Integrity PRISM-IR Flow

Tests the build-integrity.prism.md flow definition:
1. Flow loads from .prism.md without errors
2. Structural validation passes
3. PRISM round-trip fidelity (when conversion functions exist)
4. Sim run happy path (all gates pass)
5. Sim run with Gate 0 failure (token hits escalation)

Dependencies:
- import pytest
- import yaml
- from pathlib import Path

Functions:
- load_prism_flow(filepath: str): Load a .prism.md file and extract the YAML content.
- test_flow_loads_without_errors(): Test that the build-integrity.prism.md file loads successfully.
- test_structural_validation(): Test that the flow passes structural validation checks.
- test_happy_path_structure(): Test that the happy path (all gates pass) has a complete path from start to build_approved.
- test_escalation_paths_exist(): Test that escalation paths exist for each phase.
- test_healing_loops_exist(): Test that healing loops exist (decision -> heal -> back to validation node).
- test_all_task_nodes_have_operators(): Test that all task nodes have operator definitions.
- test_all_decision_nodes_have_mode(): Test that all decision nodes have mode specified.
- test_edge_conditions_use_valid_syntax(): Test that edge conditions use valid PRISM-IR expression syntax.
- test_prism_round_trip_fidelity(): Test PRISM round-trip: flow_to_prism(prism_to_flow(flow)) produces equivalent flow.
- test_sim_run_happy_path(): Test simulation run where all gates pass (happy path).
- test_sim_run_gate0_failure(): Test simulation run with Gate 0 failure (token hits escalation).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
