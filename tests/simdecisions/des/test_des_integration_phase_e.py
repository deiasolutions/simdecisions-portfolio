"""
test_des_integration_phase_e
============================

Integration Tests for Phase E — Full DES Engine with Generators, Pools, Reneging, and Distribution Durations.

TASK-041: Integration Test — Call Center Simulation

Tests the full integration of:
- Generators (TASK-036) — Poisson arrivals
- Distribution-based durations (TASK-037) — Lognormal service times
- Reneging/balking (TASK-038) — Customers abandon queues
- Resource pools with dispatch (TASK-039) — Scored agent assignment
- v2 loader (TASK-040) — Wire everything together

Dependencies:
- from simdecisions.phase_ir.primitives import Flow, Node, Edge, Resource
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.core import SimConfig, load_flow, run

Classes:
- TestCallCenterSimulation: End-to-end call center simulation using all Phase E features.
- TestV2LoaderIntegration: Test that the v2 loader correctly wires generators and pools.
- TestComplexScenarios: Complex scenarios combining multiple Phase E features.
- TestRegressionGuards: Ensure Phase E additions don't break existing functionality.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
