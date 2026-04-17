"""
test_des_trace_writer
=====================

Tests for DES Trace Writer — TASK-088

Covers: DESTraceEvent, TraceConfig, TraceBuffer, TRACE_LEVELS,
        to_ledger_event, checkpoint get_state/set_state.

Dependencies:
- from __future__ import annotations
- import json
- import time
- from simdecisions.des.trace_writer import (

Classes:
- TestDESTraceEvent: to_dict with no optional fields omits None/empty values.
- TestTraceConfig: When write_to_file is False, flush does not create a file.
- TestTraceBufferQueries: Events that were in _buffer are restored to _buffer.

Functions:
- _make_event(**overrides): Create a DESTraceEvent with sensible defaults.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
