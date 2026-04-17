"""
test_dispatcher_capacity_config
===============================

Test dispatcher reads max_parallel_bees from queue.yml (CAP-01).

Dependencies:
- import json
- import time
- from pathlib import Path
- from unittest.mock import patch
- import pytest
- import yaml
- from hivenode.scheduler.dispatcher_daemon import (

Functions:
- test_env(tmp_path): Create test environment with queue directories.
- write_config(config_file: Path, max_parallel_bees: int, min_parallel_bees: int = 5): Write queue.yml with specified bee capacity.
- test_load_max_bees_from_config_reads_queue_yml(test_env): Test _load_max_bees_from_config reads max_parallel_bees from queue.yml.
- test_load_max_bees_from_config_defaults_to_10_if_missing(test_env): Test _load_max_bees_from_config returns 10 if queue.yml is missing.
- test_load_max_bees_from_config_clamps_to_1_20_range(test_env): Test _load_max_bees_from_config clamps values to 1-20 range.
- test_load_max_bees_from_config_handles_malformed_yaml(test_env): Test _load_max_bees_from_config returns 10 if yaml is malformed.
- test_dispatcher_init_reads_from_queue_yml_by_default(test_env): Test dispatcher reads max_bees from queue.yml by default.
- test_dispatcher_init_cli_override_wins_if_not_default(test_env): Test dispatcher uses CLI arg if explicitly set (not default).
- test_dispatcher_init_falls_back_to_10_if_no_config(test_env): Test dispatcher falls back to 10 if queue.yml missing.
- test_dispatch_cycle_hot_reloads_max_bees(test_env): Test dispatcher re-reads queue.yml on each cycle.
- test_dispatch_cycle_uses_hot_reloaded_capacity(test_env): Test dispatcher uses hot-reloaded capacity for slot calculation.
- test_dispatcher_daemon_hot_reloads_during_loop(test_env): Test dispatcher hot-reloads max_bees while running.
- test_dispatcher_handles_missing_budget_section(test_env): Test dispatcher falls back to 10 if budget section missing.
- test_dispatcher_handles_non_integer_max_bees(test_env): Test dispatcher casts non-integer max_bees to int.
- test_dispatcher_cli_override_still_works(test_env): Test --max-bees CLI arg still works as override.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
