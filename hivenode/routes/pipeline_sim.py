"""
pipeline_sim
============

Pipeline Simulation Routes — TASK-228

DES runner for unified build pipeline. Loads PHASE-IR flow from TASK-226,
instantiates InMemoryPipelineStore from TASK-225, runs through DES engine
with statistical service time distributions.

Returns: throughput, bottleneck analysis, WIP distribution, optimal pool size.

Dependencies:
- import json
- from pathlib import Path
- from fastapi import APIRouter, HTTPException
- from pydantic import BaseModel, Field
- from simdecisions.des.engine import SimulationEngine
- from simdecisions.des.core import SimConfig

Classes:
- PipelineSimRequest: Request parameters for pipeline simulation.
- PipelineSimResponse: Response with simulation results.

Functions:
- _load_pipeline_ir(pool_size: int, failure_rate: float): Load pipeline IR from file and adjust resource capacity.
- _calculate_bottleneck(wip_dist: dict[str, float]): Identify bottleneck stage (highest average WIP).
- _estimate_optimal_pool_size(throughput: float,
    pool_size: int,
    bottleneck_stage: str): Estimate optimal pool size based on bottleneck analysis.
- simulate_pipeline(request: PipelineSimRequest): Run DES simulation of build pipeline and return performance metrics.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
