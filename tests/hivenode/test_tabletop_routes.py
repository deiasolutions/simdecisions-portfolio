"""
test_tabletop_routes
====================

Tests for Tabletop Mode Backend API — TASK-CANVAS-007

Tests the /api/tabletop/interact endpoint which provides a unified
interface for tabletop session management (start, decide, ask, end).

TDD: Tests written first, then implementation.

Dependencies:
- from __future__ import annotations
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app

Functions:
- client(): Create test client.
- sample_flow(): A simple flow: start -> task -> checkpoint -> decision -> task -> end
- empty_flow(): A flow with no nodes
- single_node_flow(): A flow with only a start node
- test_tabletop_endpoint_exists(client: TestClient): Test that the /api/tabletop/interact endpoint exists.
- test_start_session_minimal(client: TestClient, sample_flow): Test starting a session with minimal payload.
- test_start_session_empty_flow_error(client: TestClient, empty_flow): Test that starting a session with an empty flow returns an error.
- test_start_session_single_node(client: TestClient, single_node_flow): Test starting a session with only a start node (completes immediately).
- test_decision_flow_advance(client: TestClient, sample_flow): Test advancing through a decision flow step-by-step.
- test_decision_submission(client: TestClient, sample_flow): Test submitting a decision at a checkpoint.
- test_decision_invalid_option(client: TestClient, sample_flow): Test submitting an invalid decision option ID.
- test_ask_question(client: TestClient, sample_flow): Test asking a question about the current node.
- test_ask_question_with_history(client: TestClient, sample_flow): Test asking a question with message history.
- test_end_session(client: TestClient, sample_flow): Test ending a session.
- test_restart_session(client: TestClient, sample_flow): Test restarting a completed session.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
