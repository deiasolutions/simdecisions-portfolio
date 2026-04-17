"""
tokens
======

Token Lifecycle Manager — ADR-008 / TASK-081

Runtime token state management for the DES engine: creation, destruction,
state transitions, position tracking, batch operations, fork/join, preemption,
and snapshot/restore.

SimToken is the runtime token (distinct from the PHASE-IR Token primitive
which merely describes the *shape* of tokens flowing through a process).

Components:
    TokenState    — 12-value enum of all possible token states
    SimToken      — runtime token dataclass with full lifecycle tracking
    TokenRegistry — central registry for token CRUD, queries, and batch ops

Dependencies:
- from __future__ import annotations
- from dataclasses import dataclass, field
- from enum import Enum
- from typing import Any, Optional

Classes:
- TokenState: All possible states a runtime token can occupy.
- SimToken: Runtime token with full lifecycle tracking.
- TokenRegistry: Central registry for all simulation tokens.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
