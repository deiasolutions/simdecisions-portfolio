"""
test_metrics_updater
====================

Tests for MetricsUpdater.

This module tests async event processing and metrics updates based on
Event Ledger feedback.

Ported from platform/efemera/tests/indexer/test_metrics_updater.py.

Dependencies:
- from datetime import datetime, timedelta
- from pathlib import Path
- from tempfile import TemporaryDirectory
- from unittest.mock import MagicMock
- import pytest
- from hivenode.rag.chunkers import CodeChunk
- from hivenode.rag.indexer.metrics_updater import MetricsUpdater
- from hivenode.rag.indexer.models import (
- from hivenode.rag.indexer.storage import IndexStorage

Functions:
- temp_storage(): Create temporary storage for testing.
- mock_db_session(): Create mock database session for event ledger queries.
- updater(temp_storage, mock_db_session): Create metrics updater with temp storage and mock session.
- create_test_record(artifact_id: str = "test-artifact-001",
    retrieval_count: int = 100,
    llm_used: int = 50,
    llm_ignored: int = 50,
    helpful_feedback: int = 30,
    not_helpful_feedback: int = 10,
    verified_count: int = 8,
    failed_count: int = 2,
    untested_count: int = 0,): Create test IndexRecord with specified metrics.
- test_handle_context_loaded_increments_retrieval_count(temp_storage, updater): Test _handle_context_loaded increments retrieval_count.
- test_handle_context_loaded_increments_llm_used_when_true(temp_storage, updater): Test _handle_context_loaded increments llm_used when event.data.llm_used=True.
- test_handle_context_loaded_increments_llm_ignored_when_false(temp_storage, updater): Test _handle_context_loaded increments llm_ignored when event.data.llm_used=False.
- test_handle_context_loaded_updates_staleness_days_stale(temp_storage, updater): Test _handle_context_loaded updates staleness.days_stale.
- test_handle_ir_pair_verified_increments_verified_count(temp_storage, updater): Test _handle_ir_pair_verified increments verified_count.
- test_handle_ir_pair_failed_increments_failed_count(temp_storage, updater): Test _handle_ir_pair_failed increments failed_count.
- test_handle_human_responded_increments_helpful_feedback(temp_storage, updater): Test _handle_human_responded increments helpful_feedback.
- test_handle_human_responded_increments_not_helpful_feedback(temp_storage, updater): Test _handle_human_responded increments not_helpful_feedback.
- test_recalculate_ir_summary_recounts_from_chunks(temp_storage, updater): Test _recalculate_ir_summary recounts IR pairs from chunks.
- test_process_new_events_routes_to_correct_handlers(temp_storage, mock_db_session, updater): Test _process_new_events routes events to correct handlers.
- test_start_and_stop(temp_storage, mock_db_session): Test updater can start and stop gracefully.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
