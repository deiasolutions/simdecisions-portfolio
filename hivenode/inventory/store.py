"""
store
=====

Inventory store — SQLAlchemy Core tables + CRUD functions.

Single source of truth for feature, backlog, bug, and stage_log data.
All db_* functions ported 1:1 from _tools/inventory_db.py.

Dependencies:
- from datetime import datetime, timezone
- from sqlalchemy import (
- from sqlalchemy.pool import StaticPool

Functions:
- init_engine(url: str, force: bool = False): Called once at startup from main.py lifespan.
- get_engine(): Get the current engine. Raises if not initialized.
- reset_engine(): For tests only — reset global engine.
- _migrate_backlog_project(eng): Add project column to inv_backlog if missing (for existing DBs).
- _migrate_estimates_tables(eng): Create inv_estimates and inv_calibration tables if missing (idempotent).
- _now(): Get the next available BL-NNN ID by scanning existing entries.
- db_add_backlog(bid, title, category, priority, source, notes, project=None): Update bug fields. Returns (success, error_msg).
- db_search_bugs(query): Search bugs by title, component, or description (case-insensitive).
- db_remove_bug(bug_id, notes): Mark bug as REMOVED. Returns (success, error_msg).
- db_update_backlog(bid, updates_dict): Update backlog fields. Returns (success, error_msg).
- db_search_backlog(query): Search backlog by title, category, or notes (case-insensitive).
- db_remove_backlog(bid, notes): Soft-delete backlog item by marking removed_at. Returns (success, error_msg).
- db_next_test_id(): Get the next available TEST-NNN ID by scanning existing entries.
- db_add_test(test_id, title, component, layer, test_file, test_count,
                framework, notes): Update test status and last_run_at. Optionally update test_count.
- db_update_test(test_id, updates_dict): Update test fields. Returns (success, error_msg).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
