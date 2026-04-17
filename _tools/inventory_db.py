"""
inventory_db
============

Inventory DB operations — direct SQLAlchemy connection to PostgreSQL.

Uses hivenode.inventory.store for all CRUD. Initializes its own engine
from INVENTORY_DATABASE_URL env var, DATABASE_URL env var, or hardcoded
Railway production URL as last resort. No hivenode server required.

Dependencies:
- from INVENTORY_DATABASE_URL env var, DATABASE_URL env var, or hardcoded
- import os
- import sys
- from pathlib import Path
- from hivenode.inventory.store import (  # noqa: E402

Functions:
- _ensure_engine(): Initialize engine if not already done.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
