"""
des_investigation_sims
======================

DES Investigation — Live Simulation Runs
TASK-DES-INVESTIGATE-001, Part 3
Read-only investigation: runs simulations and captures output.

Dependencies:
- import json
- import time
- import sys
- from simdecisions.phase_ir.primitives import Flow, Node, Edge, Resource
- from simdecisions.des.core import SimConfig, load_flow, run
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.replication import ReplicationConfig, run_replications
- from simdecisions.des.sweep import SweepConfig, SweepParameter, parameter_sweep, sensitivity_analysis

Functions:
- build_mmc_flow(arrival_rate=10.0, service_mean=5.0, server_count=3, queue_capacity=20): Build a minimal PHASE-IR v2.0 flow:
- build_mmc_flow_v2(arrival_rate=10.0, service_mean=5.0, server_count=3, queue_capacity=20): Build a v2.0 flow using generators for Poisson arrivals.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
