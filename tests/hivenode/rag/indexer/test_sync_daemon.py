"""
test_sync_daemon
================

Tests for sync daemon that orchestrates markdown export and cloud sync.

Tests cover:
- IMMEDIATE policy: syncs immediately on index
- BATCHED policy: queues and syncs at intervals
- MANUAL policy: syncs only on explicit force_sync_all()
- Force sync all records
- Status reporting
- Environment variable configuration
- Thread lifecycle management

Dependencies:
- import os
- import time
- from datetime import datetime
- from pathlib import Path
- from unittest.mock import MagicMock, patch
- import pytest
- from hivenode.rag.indexer.sync_daemon import (

Functions:
- mock_storage(): Mock IndexStorage instance.
- mock_exporter(): Mock MarkdownExporter instance.
- mock_cloud_sync(): Mock CloudSyncService instance.
- test_immediate_policy_syncs_immediately(mock_storage, mock_exporter, mock_cloud_sync): Test IMMEDIATE policy syncs artifact immediately on index.
- test_batched_policy_queues_and_syncs_at_interval(mock_storage, mock_exporter, mock_cloud_sync): Test BATCHED policy adds to queue and syncs at interval.
- test_manual_policy_does_nothing_on_index(mock_storage, mock_exporter, mock_cloud_sync): Test MANUAL policy does nothing on on_context_indexed().
- test_force_sync_all_syncs_regardless_of_policy(mock_storage, mock_exporter, mock_cloud_sync): Test force_sync_all() syncs all records regardless of policy.
- test_get_status_returns_daemon_state(mock_storage, mock_exporter, mock_cloud_sync): Test get_status() returns correct daemon state.
- test_create_daemon_from_env_reads_environment_variables(mock_storage, mock_exporter, mock_cloud_sync): Test create_daemon_from_env() reads environment variables correctly.
- test_create_daemon_from_env_uses_defaults_when_no_env_vars(mock_storage, mock_exporter, mock_cloud_sync): Test create_daemon_from_env() uses defaults when env vars not set.
- test_daemon_thread_starts_and_stops_gracefully(mock_storage, mock_exporter, mock_cloud_sync): Test daemon thread starts and stops gracefully.
- test_sync_only_markdown_when_cloud_disabled(mock_storage, mock_exporter, mock_cloud_sync): Test sync only calls markdown when cloud is disabled.
- test_sync_only_cloud_when_markdown_disabled(mock_storage, mock_exporter, mock_cloud_sync): Test sync only calls cloud when markdown is disabled.
- test_force_sync_all_handles_failures(mock_storage, mock_exporter, mock_cloud_sync): Test force_sync_all() counts failed syncs.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
