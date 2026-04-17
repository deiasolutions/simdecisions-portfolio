"""
test_des_engine
===============

Tests for DES Unified Engine & Routes — ADR-008 / TASK-089

SimulationEngine: lifecycle, inspection, injection, hooks, breakpoints,
watches, checkpoints, and the 4 API routes.

35+ tests covering all specified areas.

Dependencies:
- from __future__ import annotations
- import uuid
- import pytest
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.core import SimConfig, EngineState
- from simdecisions.des.tokens import TokenRegistry, SimToken, TokenState
- from simdecisions.des.resources import ResourceManager
- from simdecisions.des.distributions import RNGManager
- from simdecisions.des.trace_writer import TraceBuffer
- from simdecisions.des.checkpoints import Checkpoint

Classes:
- TestLoad: Tests for SimulationEngine.load().
- TestRun: Tests for SimulationEngine.run().
- TestStep: Tests for SimulationEngine.step().
- TestRunUntilRunFor: Tests for run_until and run_for.
- TestPauseResume: Tests for pause and resume.
- TestCheckpoints: Tests for checkpoint, restore, and fork.
- TestInspection: Tests for inspection methods.
- TestInjection: Tests for inject_token and set_variable.
- TestHooks: Tests for hook registration and firing.
- TestBreakpoints: Tests for breakpoint management.
- TestWatches: Tests for watch expressions.
- TestRoutes: Tests for the 4 DES engine API endpoints.
- TestIntegration: End-to-end integration tests.

Functions:
- _tid(): Build a linear flow: N0 -> N1 -> ... -> N(n-1).
- _fork_flow(): Build a forking flow: A -> B, A -> C.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
