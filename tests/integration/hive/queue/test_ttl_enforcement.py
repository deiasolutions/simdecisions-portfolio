"""
test_ttl_enforcement
====================

Tests for TTL enforcement in queue system.

Tests PRISM-IR v1.1 Section 4.2 — TTL Enforcement.

Verifies:
- building_ttl_seconds config value
- building_started_at timestamp tracking
- Periodic stale detection (60s scan cycle)
- Stale spec marking with failure_reason
- Movement to _needs_review/ directory

Dependencies:
- import json
- from datetime import datetime, timedelta, timezone
- from pathlib import Path
- import pytest

Functions:
- temp_queue_dir(tmp_path): Create temporary queue directory structure.
- config_with_ttl(tmp_path): Create queue config with TTL settings.
- stale_spec(temp_queue_dir): Create a spec that has been BUILDING for too long.
- fresh_spec(temp_queue_dir): Create a spec that has been BUILDING for acceptable time.
- spec_without_timestamp(temp_queue_dir): Create a spec without building_started_at timestamp.
- test_default_ttl_config(): TTL config has sensible defaults if not specified.
- test_load_ttl_from_config(config_with_ttl): TTL config can be loaded from queue.yml.
- test_ttl_config_from_env_var(monkeypatch): TTL can be overridden via FACTORY_BUILDING_TTL environment variable.
- test_ttl_env_var_overrides_config(config_with_ttl, monkeypatch): Environment variable takes precedence over config file.
- test_detect_stale_spec(temp_queue_dir, stale_spec): Specs exceeding TTL are detected as stale.
- test_fresh_spec_not_flagged(temp_queue_dir, fresh_spec): Specs within TTL are NOT flagged as stale.
- test_mixed_fresh_and_stale(temp_queue_dir, stale_spec, fresh_spec): Only stale specs are flagged when both fresh and stale exist.
- test_spec_without_timestamp_skipped(temp_queue_dir, spec_without_timestamp): Specs without building_started_at are handled gracefully.
- test_empty_active_dir(temp_queue_dir): TTL scan handles empty _active/ directory gracefully.
- test_nonexistent_active_dir(): TTL scan handles missing _active/ directory gracefully.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
