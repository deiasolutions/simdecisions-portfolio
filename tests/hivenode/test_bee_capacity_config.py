"""
test_bee_capacity_config
========================

Tests for bee capacity configuration loading.

Tests that max_parallel_bees is read from queue.yml as the single source
of truth, with proper fallbacks and validation.

Dependencies:
- import yaml

Functions:
- test_load_capacity_from_valid_queue_yml(tmp_path): Test _load_capacity() returns value from queue.yml.
- test_load_capacity_missing_file(tmp_path): Test _load_capacity() returns 10 on missing file.
- test_load_capacity_clamps_to_range(tmp_path): Test _load_capacity() clamps to 1-20 range.
- test_load_capacity_invalid_yaml(tmp_path): Test _load_capacity() falls back on invalid YAML.
- test_load_capacity_missing_key(tmp_path): Test _load_capacity() falls back when key is missing.
- test_load_bee_constraints_from_valid_queue_yml(tmp_path): Test _load_bee_constraints() reads both max and min.
- test_load_bee_constraints_clamps_min_to_max(tmp_path): Test _load_bee_constraints() clamps min <= max.
- test_load_bee_constraints_falls_back_gracefully(tmp_path): Test _load_bee_constraints() falls back gracefully on bad YAML.
- test_load_bee_constraints_missing_min_key(tmp_path): Test _load_bee_constraints() uses default min when key missing.
- test_buildstate_slot_capacity_from_config(tmp_path): Test BuildState.slot_capacity reads from queue.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
