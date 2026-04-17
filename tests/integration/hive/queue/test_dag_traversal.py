"""
test_dag_traversal
==================

Tests for DAG traversal utilities.

FACTORY-007: DAG traversal with cycle detection.

Dependencies:
- from pathlib import Path
- import sys
- from spec_parser import SpecFile
- from dag_traversal import (

Functions:
- test_traverse_dag_linear(): Test DAG traversal on linear dependency chain.
- test_traverse_dag_diamond(): Test DAG traversal on diamond-shaped dependencies.
- test_traverse_dag_with_shared_ref(): Test DAG traversal with SHARED_REF nodes.
- test_traverse_dag_cycle_detected(): Test DAG traversal detects and handles cycles.
- test_find_all_dependencies(): Test finding all dependencies (transitive closure).
- test_check_circular_dependencies(): Test cycle detection in dependency graph.
- test_check_no_circular_dependencies(): Test cycle detection on acyclic graph.
- test_topological_sort_linear(): Test topological sort on linear dependency chain.
- test_topological_sort_diamond(): Test topological sort on diamond-shaped dependencies.
- test_topological_sort_with_cycle(): Test topological sort handles cycles gracefully.
- test_visit_function_called(): Test that visit function is called for each visited spec.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
