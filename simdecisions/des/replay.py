"""
replay
======

DES Replay Controller — ADR-008 / TASK-091

Replay system that can replay recorded simulation traces step-by-step,
supporting forward/backward navigation, speed control, bookmarks,
and frame callbacks.

Components:
    ReplayState       — current state of the replay (position, derived sim state)
    ReplayController  — controls replay of a recorded simulation trace

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from typing import Any, Callable
- from simdecisions.des.trace_writer import DESTraceEvent, TraceBuffer

Classes:
- ReplayState: Current state of the replay.
- ReplayController: Controls replay of a recorded simulation trace.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
