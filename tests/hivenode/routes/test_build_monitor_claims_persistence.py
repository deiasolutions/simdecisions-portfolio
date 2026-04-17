"""
test_build_monitor_claims_persistence
=====================================

Tests for file claims persistence across restarts.

Ensures claims survive hivenode restarts and stale claims are pruned on load.

Dependencies:
- import json
- from datetime import datetime, timedelta
- from pathlib import Path
- from tempfile import TemporaryDirectory
- import pytest
- from hivenode.routes.build_monitor import BuildState, BuildStatus

Classes:
- TestClaimsPersistence: Test claims survive restart and stale claims are pruned on load.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
