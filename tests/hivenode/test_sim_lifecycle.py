"""
test_sim_lifecycle
==================

Integration tests for full simulation lifecycle.

Tests the complete simulation lifecycle including:
- load → start → status=running → pause → status=paused → resume → status=running
- Step mode progression
- Checkpoint/restore state reversion
- Fork with independent run_ids
- Parameter sweep with multiple results
- Event emission and retrieval

Dependencies:
- import pytest
- import sqlite3
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from hivenode import dependencies
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.ledger.reader import LedgerReader

Functions:
- client(): Create test client.
- ledger_db(tmp_path): Create temporary ledger database.
- ledger_writer(ledger_db): Create ledger writer with thread-safe connection.
- ledger_reader(ledger_db, ledger_writer): Create ledger reader with same thread-safe connection.
- demo_flow(): Minimal demo PHASE-IR flow with 2 tasks, 1 edge.
- test_full_lifecycle_load_start_pause_resume(client, ledger_writer, ledger_reader, demo_flow): Test full lifecycle: load → start → status=running → pause → status=paused → resume → status=running.
- test_step_mode_advances_sim_time(client, ledger_writer, ledger_reader, demo_flow): Test step mode: load → step → sim_time increases → step → sim_time increases.
- test_checkpoint_restore_reverts_state(client, ledger_writer, ledger_reader, demo_flow): Test checkpoint/restore: load → start → checkpoint → advance → restore → sim_time reverts.
- test_fork_creates_independent_runs(client, ledger_writer, ledger_reader, demo_flow): Test fork: load → start → advance → fork → new run_id → both runs independent.
- test_sweep_returns_multiple_results(client, ledger_writer, ledger_reader, demo_flow): Test sweep: load → sweep with 3 param sets → 3 results returned.
- test_events_retrieval_from_ledger(client, ledger_writer, ledger_reader, demo_flow): Test events: load → start → get events → events list not empty.
- test_invalid_run_id_returns_404(client, ledger_writer, ledger_reader): Test that invalid run_id returns 404 for all endpoints.
- test_adapter_without_bus_handles_null_gracefully(client, ledger_writer, ledger_reader, demo_flow): Test that simulation endpoints work even if adapter doesn't have bus context.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
