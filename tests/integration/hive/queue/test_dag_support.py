"""
test_dag_support
================

Tests for DAG support (SHARED_REF nodes and traversal).

FACTORY-007: DAG support for shared module references.

Dependencies:
- from pathlib import Path
- import pytest
- import sys
- from spec_parser import SpecFile, parse_spec

Functions:
- temp_queue_dir(tmp_path): Create temporary queue directory structure.
- test_shared_ref_node_creation(temp_queue_dir): Test SHARED_REF node type is parsed correctly from frontmatter.
- test_original_node_default_type(temp_queue_dir): Test that nodes default to ORIGINAL type when not specified.
- test_find_dangling_refs_empty(): Test find_dangling_refs with no SHARED_REF nodes.
- test_find_dangling_refs_valid_target(): Test find_dangling_refs with valid SHARED_REF pointing to ORIGINAL.
- test_find_dangling_refs_invalid_target(): Test find_dangling_refs detects SHARED_REF with non-existent target.
- test_resolve_shared_refs_no_refs(): Test resolve_shared_refs with no SHARED_REF nodes.
- test_resolve_shared_refs_inherit_phase(): Test SHARED_REF inherits phase from target ORIGINAL.
- test_resolve_shared_refs_target_not_built(): Test SHARED_REF mirrors target phase even when target not BUILT.
- test_dag_traversal_no_cycles(temp_queue_dir): Test DAG traversal with visited set prevents infinite loops.
- test_shared_ref_no_own_acceptance_criteria(): Test SHARED_REF nodes do not define their own acceptance criteria.
- test_multiple_refs_to_same_target(): Test multiple SHARED_REF nodes can reference the same ORIGINAL.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
