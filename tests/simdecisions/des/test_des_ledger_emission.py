"""
test_des_ledger_emission
========================

Tests for DES Ledger Emission — Per-Node Training Data

Verifies that the DES engine emits training data to the ledger
after every node execution, capturing input_state, output_state,
duration_ms, cost_usd, and cost_carbon.

Dependencies:
- from __future__ import annotations
- import uuid
- from typing import Any
- from simdecisions.des.core import SimConfig
- from simdecisions.des.engine import SimulationEngine

Classes:
- MockLedger: Simple mock ledger for testing event emission.
- TestLedgerEmission: Tests for ledger emission during simulation runs.

Functions:
- _tid(): Generate a short unique ID.
- _linear_flow(n: int = 3): Build a linear flow: N0 -> N1 -> ... -> N(n-1).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
