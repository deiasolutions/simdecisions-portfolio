"""
test_mcp_telemetry_smoke
========================

Smoke test for telemetry dual-loop (SPEC-MCP-WAVE-5-TELEMETRY-LOOP).

This smoke test verifies the telemetry dual-loop works end-to-end:
- Send heartbeat with high cost
- Verify advisory returned
- Check Event Ledger for logged event

Dependencies:
- import pytest
- import tempfile
- from pathlib import Path
- from hivenode.hive_mcp.tools import telemetry
- from hivenode.hive_mcp.state import StateManager

Functions:
- temp_state_dir(): Create a temporary directory for state files.
- state_manager(temp_state_dir): Create a StateManager instance for testing.
- test_smoke_heartbeat_with_high_cost(state_manager): Smoke test: Send heartbeat with high cost and verify:

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
