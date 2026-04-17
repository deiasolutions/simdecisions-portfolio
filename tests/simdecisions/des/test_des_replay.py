"""
test_des_replay
===============

Tests for DES Replay Controller — TASK-091

Covers: ReplayState, ReplayController (construction, step_forward,
        step_backward, seek, seek_time, play/pause/stop, set_speed,
        step_to_next_time, progress, at_end, at_start, events_at_time,
        unique_times, bookmarks, callbacks, state tracking, _rebuild_state_at,
        trace_summary, empty trace, from_trace_buffer, from_jsonl).

Dependencies:
- from __future__ import annotations
- import time
- import pytest
- from simdecisions.des.trace_writer import DESTraceEvent, TraceBuffer, TraceConfig
- from simdecisions.des.replay import ReplayController

Classes:
- TestReplayControllerCreation: Create from a plain list of DESTraceEvent.
- TestStepForwardBackward: step_forward returns the current event and advances index.
- TestSeek: seek moves the cursor to a specific index.
- TestPlayPauseStop: stop resets current_index to 0 and clears derived state.
- TestSetSpeed: Speed cannot go below 0.1.
- TestStepToNextTime: step_to_next_time returns all events at the current sim_time.
- TestProgressAndBounds: Round-trip: bookmark a position, move away, return.
- TestCallbacks: Event callback fires with correct arguments.
- TestStateTracking: token_create adds token to tokens_active.
- TestRebuildState: Rebuilding state at an index matches stepping forward to it.

Functions:
- _evt(id: str = "evt-1",
    event_type: str = "node_start",
    sim_time: float = 0.0,
    token_id: str | None = None,
    node_id: str | None = None,
    resource_id: str | None = None,
    **kwargs,): Create a DESTraceEvent with sensible defaults.
- _sample_events(): A small but realistic trace: create -> start -> end -> complete.
- _resource_events(): Trace with resource acquire and release events.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
