"""
test_scheduler_mcp_unit
=======================

Unit tests for scheduler MCP event-driven operation.

Tests cover:
- on_mcp_event() sets wake_event
- Fallback timeout (60s)
- MCP disabled mode (polling only)
- Wake event clearing after trigger
- Invalid/malformed event handling
- Thread-safe wake_event handling

Dependencies:
- import json
- import tempfile
- import threading
- import time
- from pathlib import Path
- from unittest.mock import patch
- import pytest

Classes:
- TestMCPEventHandling: Test MCP event handling.
- TestMCPConfiguration: Test MCP enabled/disabled configuration.
- TestFallbackBehavior: Test fallback polling when MCP unavailable.
- TestScheduleLogEvents: Test schedule_log.jsonl includes event source.

Functions:
- temp_dirs(): Create temporary directories for testing.
- sample_tasks(): Sample tasks for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
