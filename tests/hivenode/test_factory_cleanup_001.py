"""
test_factory_cleanup_001
========================

Tests for SPEC-FACTORY-CLEANUP-001: dead wiring cleanup.

Tests:
1. Task pruning preserves aggregates
2. JSONL log rotation
3. Shared extract_task_id_from_spec function import

Dependencies:
- import json
- import pytest
- from datetime import datetime, timedelta
- from pathlib import Path
- from tempfile import TemporaryDirectory
- from hivenode.routes.build_monitor import BuildState, BuildStatus
- from hivenode.queue_watcher import QueueEventHandler
- from hivenode.spec_utils import extract_task_id_from_spec

Classes:
- TestTaskPruning: Test BuildState task pruning in _save_to_disk().
- TestLogRotation: Test queue_events.jsonl log rotation.
- TestSharedFunctionImport: Test extract_task_id_from_spec shared function.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
