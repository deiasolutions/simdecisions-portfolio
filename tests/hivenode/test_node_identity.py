"""
test_node_identity
==================

Tests for node identity generation and persistence.

Dependencies:
- from hivenode.node_identity import generate_node_id, get_or_create_node_id

Functions:
- test_generate_node_id_format(): Generated node ID should match node-{8hex} format.
- test_generate_creates_different_ids(): Multiple calls should generate different IDs.
- test_get_or_create_persists_to_file(tmp_path): get_or_create_node_id should persist to file.
- test_get_or_create_reloads_same_id(tmp_path): Subsequent calls should reload same ID from file.
- test_creates_directory_if_missing(tmp_path): Should create base_dir directory if missing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
