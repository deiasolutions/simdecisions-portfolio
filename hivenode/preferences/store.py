"""
store
=====

User preferences store (SQLite, opaque JSON blob).

Stores per-user preferences as a JSON blob. Backend does not
interpret the blob — the frontend owns the schema. Last-write-wins
for conflict resolution.

Dependencies:
- import json
- import sqlite3
- from datetime import datetime, UTC
- from typing import Any

Classes:
- PreferencesStore: SQLite store for user preferences.

Functions:
- create_preferences_schema(conn: sqlite3.Connection): Create user_preferences table.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
