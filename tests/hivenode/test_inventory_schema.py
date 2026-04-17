"""
test_inventory_schema
=====================

Tests for inventory store — SQLAlchemy Core CRUD functions.

Dependencies:
- import pytest
- from hivenode.inventory.store import (
- from sqlalchemy import select

Functions:
- clean_db(): Fresh in-memory SQLite database for each test.
- test_add_feature_and_list(): Adding a feature and listing returns it.
- test_add_duplicate_feature_fails(): Adding duplicate feature returns error.
- test_backlog_defaults_to_backlog_column(): New backlog items default to kanban_column='backlog'.
- test_backlog_move_valid_column(): Moving backlog item to valid column works.
- test_backlog_move_invalid_column(): Moving to invalid column fails.
- test_backlog_move_nonexistent_item(): Moving nonexistent item fails.
- test_backlog_stage_creates_log_entry(): Setting stage creates entry in stage_log.
- test_backlog_stage_updates_current_state(): Setting stage updates backlog.stage and backlog.stage_status.
- test_backlog_stage_auto_ends_previous_active(): Setting a stage to active ends the previous active stage.
- test_backlog_stage_done_sets_timestamps(): Setting stage status to 'done' sets both started_at and ended_at.
- test_backlog_stage_pending_no_timestamps(): Setting stage status to 'pending' leaves timestamps null.
- test_backlog_stage_invalid_stage(): Invalid stage name fails.
- test_backlog_stage_invalid_status(): Invalid status fails.
- test_backlog_graduate_sets_feature_id(): Graduating sets feature_id on backlog item.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
