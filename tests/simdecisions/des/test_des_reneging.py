"""
test_des_reneging
=================

Tests for Reneging and Balking — ADR-008 / TASK-038

Covers: enqueue_with_renege, cancel_renege, process_renege,
should_balk, renege_timeout handler, and state checkpointing.

Target: 9+ tests covering all requirements.

Dependencies:
- from simdecisions.des.core import (
- from simdecisions.des.resources import (
- from simdecisions.phase_ir.primitives import Flow, Node

Classes:
- TestEnqueueWithRenege: Tests for enqueue_with_renege.
- TestCancelRenege: Tests for cancel_renege.
- TestProcessRenege: Tests for process_renege.
- TestShouldBalk: Tests for should_balk.
- TestRenegeTimeoutHandler: Tests for handle_renege_timeout event handler.
- TestRenegeStateCheckpoint: Tests for snapshot/restore of renege state.
- TestRenegeIntegration: Integration tests for reneging workflow.

Functions:
- _make_manager(): Create a ResourceManager with one resource pre-registered.
- _make_engine_state(): Create a basic EngineState for handler testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
