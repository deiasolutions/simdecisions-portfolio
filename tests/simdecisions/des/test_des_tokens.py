"""
test_des_tokens
===============

Tests for Token Lifecycle Manager — ADR-008 / TASK-081

35+ tests covering: creation, destruction, state transitions, position
tracking, wait-time accounting, queries, batch ops, fork/join, preemption,
and checkpoint round-trip.

Dependencies:
- from __future__ import annotations
- import pytest
- from simdecisions.des.tokens import (

Classes:
- TestCreate: Suspended tokens can transition to any non-terminal state.
- TestMove: Full lifecycle: created -> traveling -> waiting_resource -> processing -> completed.

Functions:
- reg(): Fresh token registry for each test.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
