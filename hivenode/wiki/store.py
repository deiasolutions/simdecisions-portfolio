"""
store
=====

Wiki store — SQLAlchemy Core tables for wiki pages and edit log.

Single source of truth for wiki data.
Follows the same pattern as hivenode/inventory/store.py.

Dependencies:
- from datetime import datetime, timezone
- from sqlalchemy import (
- from sqlalchemy.pool import StaticPool

Functions:
- init_engine(url: str, force: bool = False): Initialize the wiki database engine and create tables.
- get_engine(): Get the current engine. Raises if not initialized.
- reset_engine(): For tests only — reset global engine.
- _migrate_schema(eng): Add missing columns to existing tables (idempotent).
- _now(): Return current UTC timestamp in ISO 8601 format.
- _row_to_dict(row): Convert SQLAlchemy row to dict.
- _rows_to_dicts(rows): Convert list of SQLAlchemy rows to list of dicts.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
