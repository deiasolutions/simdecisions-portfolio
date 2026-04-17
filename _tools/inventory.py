"""
inventory
=========

Feature Inventory CLI — PostgreSQL-backed feature + backlog tracking for ShiftCenter.

Usage: python _tools/inventory.py <command> [args]

Commands: add, update, verify, break, remove, list, search, stats, export-md, import-md
          backlog {add, list, done, move, stage, graduate, update, search, remove, export-md}
          bug {add, list, fix, update, search, remove, export-md}
          test {add, list, run, update, search, remove, export-md}

Dependencies:
- import argparse
- import sys
- from pathlib import Path
- from inventory_db import (

Functions:
- _print_table(rows, columns): Update an existing backlog item.
- cmd_bl_search(args): Search backlog items by title, category, or notes.
- cmd_bl_remove(args): Soft-delete backlog item (mark as removed).
- cmd_bl_export_md(args): Appends backlog section to FEATURE-INVENTORY.md (called by export-md too).
- cmd_bug(args): Update an existing bug.
- cmd_bug_search(args): Search bugs by title, component, or description.
- cmd_bug_remove(args): Mark bug as REMOVED.
- cmd_bug_export_md(args): Returns bug section lines for FEATURE-INVENTORY.md.
- cmd_test(args): Returns test section lines for FEATURE-INVENTORY.md.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
