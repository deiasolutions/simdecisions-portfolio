"""
test_playback_routes
====================

Test playback routes — TDD for TASK-CANVAS-006.

Tests CRUD operations on playback events (store, retrieve, list, delete).
Edge cases: non-existent flow_id, large event sets, concurrent reads.

Dependencies:
- from __future__ import annotations
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from hivenode.playback.store import PlaybackStore

Functions:
- client(): TestClient for playback routes.
- playback_store(): Playback store instance for direct testing.
- test_store_events_creates_new_run(client: TestClient): POST /api/playback/store creates a new run with events.
- test_retrieve_events_for_existing_run(client: TestClient): GET /api/playback/{flow_id}/{run_id} retrieves stored events.
- test_retrieve_events_nonexistent_run_returns_404(client: TestClient): GET /api/playback/{flow_id}/{run_id} returns 404 for non-existent run.
- test_list_runs_for_flow(client: TestClient): GET /api/playback/{flow_id}/runs lists all runs for a flow.
- test_list_runs_empty_flow(client: TestClient): GET /api/playback/{flow_id}/runs returns empty list for flow with no runs.
- test_delete_playback_session(client: TestClient): DELETE /api/playback/{flow_id}/{run_id} deletes events.
- test_delete_nonexistent_session_returns_404(client: TestClient): DELETE /api/playback/{flow_id}/{run_id} returns 404 for non-existent run.
- test_store_large_event_set(client: TestClient): Store 1000+ events and retrieve successfully.
- test_store_overwrites_existing_run(client: TestClient): Storing events for existing run_id overwrites previous events.
- test_events_ordered_by_event_index(client: TestClient): Retrieved events maintain insertion order.
- test_concurrent_reads_same_run(client: TestClient): Multiple concurrent reads of same run succeed (read-only, no conflicts).
- test_store_with_empty_events_list(client: TestClient): Storing empty events list succeeds but creates no events.
- test_store_create_and_retrieve(playback_store: PlaybackStore): Direct store test: create and retrieve events.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
