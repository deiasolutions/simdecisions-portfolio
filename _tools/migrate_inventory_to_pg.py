"""
migrate_inventory_to_pg
=======================

One-time migration: SQLite feature-inventory.db → PostgreSQL via hivenode store.

Usage:
    INVENTORY_DATABASE_URL=postgresql://... python _tools/migrate_inventory_to_pg.py

Reads from local docs/feature-inventory.db (SQLite) and writes to the
PostgreSQL database specified by INVENTORY_DATABASE_URL.

Dependencies:
- import os
- import sqlite3
- import sys
- from pathlib import Path
- from hivenode.inventory.store import (

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
