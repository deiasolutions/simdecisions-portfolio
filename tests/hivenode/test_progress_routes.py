"""
test_progress_routes
====================

Tests for progress/stage tracking API routes.

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from sqlalchemy import select
- from hivenode.inventory.store import (
- from hivenode.main import app

Functions:
- inventory_engine(): Initialize in-memory inventory engine for each test.
- client(): Test client.
- sample_progress(): Create sample backlog items with stage data for testing.
- test_progress_items_get_all(client, sample_progress): Test GET /api/progress/items returns all items with stages.
- test_progress_items_response_structure(client, sample_progress): Test response structure matches spec.
- test_progress_items_filter_active(client, sample_progress): Test filtering by active status.
- test_progress_items_filter_failed(client, sample_progress): Test filtering by failed status.
- test_progress_items_filter_done(client, sample_progress): Test filtering by done status.
- test_progress_stages_get_single_item(client, sample_progress): Test GET /api/progress/stages/:item_id returns stage history.
- test_progress_stages_get_nonexistent_item(client, sample_progress): Test GET /api/progress/stages/:item_id with nonexistent item.
- test_progress_stage_post_new_stage(client, sample_progress): Test POST /api/progress/stage creates new stage log entry.
- test_progress_stage_post_ends_previous_active(client, sample_progress): Test POST /api/progress/stage with status=active ends previous active stage.
- test_progress_stage_post_updates_backlog_current_stage(client, sample_progress): Test POST /api/progress/stage updates backlog.stage and stage_status.
- test_progress_stage_post_invalid_stage(client, sample_progress): Test POST /api/progress/stage with invalid stage name.
- test_progress_stage_post_invalid_status(client, sample_progress): Test POST /api/progress/stage with invalid status.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
