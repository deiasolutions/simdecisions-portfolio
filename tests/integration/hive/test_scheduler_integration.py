"""
test_scheduler_integration
==========================

Integration test for scheduler fixes.

Tests that the scheduler correctly:
1. Extracts unique task IDs from DISPATCH-QUEEN specs
2. Parses comma-separated dependencies into individual array elements
3. Generates correct schedule.json with separate tasks

Dependencies:
- import sys
- import tempfile
- from pathlib import Path
- from scheduler_daemon import scan_backlog, extract_task_id

Functions:
- test_dispatch_queen_specs_integration(): Test that DISPATCH-QUEEN specs generate separate tasks with correct deps.
- test_task_id_extraction_uniqueness(): Test that similar spec names produce unique task IDs.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
