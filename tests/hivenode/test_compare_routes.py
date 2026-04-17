"""
test_compare_routes
===================

Tests for Compare API Routes — POST /api/compare/diff, /snapshot, GET /snapshots, DELETE /snapshot.

Tests verify:
1. Diff computation between two flows
2. Snapshot storage and retrieval
3. Snapshot deletion
4. Edge cases (identical flows, empty flows, large flows, missing snapshots)

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- client(): Create test client.
- flow_a(): Flow A: 3 nodes, 2 edges.
- flow_b(): Flow B: 4 nodes (1 added, n2 modified), 3 edges.
- flow_identical(): Identical flow to flow_a (for testing identical diff).
- flow_empty(): Empty flow (no nodes, no edges).
- test_diff_two_different_flows(client): Test diff between two different flows.
- test_diff_identical_flows(client): Test diff between two identical flows — should return empty diff.
- test_diff_empty_flows(client): Test diff between two empty flows.
- test_diff_completely_different_flows(client): Test diff where flows have no nodes in common.
- test_diff_missing_snapshot_a(client): Test diff with missing snapshotA.
- test_diff_missing_snapshot_b(client): Test diff with missing snapshotB.
- test_store_snapshot_success(client): Test storing a flow snapshot.
- test_store_snapshot_with_label(client): Test storing a snapshot with a custom label.
- test_store_snapshot_empty_flow(client): Test storing an empty flow snapshot.
- test_store_snapshot_large_flow(client): Test storing a snapshot with 1000+ nodes.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
