"""
loader_v2
=========

TASK-040: v2.0 IR Loader — Load PHASE-IR v2.0 flows with generators, pools, and reneging

Extends the DES engine to load v2.0 IR flows with:
- Automatic version detection
- Generator wiring (GeneratorManager)
- Resource pool loading (PoolManager)
- Reneging/balking configuration
- Node duration sampling

Components:
    _is_v2_flow        — detect v2.0 features in Flow metadata
    load_flow_v2       — load a v2.0 flow into EngineState
    validate_v2_flow   — validate v2.0 flow configuration

Dependencies:
- from __future__ import annotations
- from typing import Optional
- from simdecisions.des.core import (
- from simdecisions.des.generators import GeneratorManager
- from simdecisions.des.pools import PoolManager
- from simdecisions.des.distributions import RNGManager
- from simdecisions.des.resources import ResourceManager
- import uuid

Functions:
- _is_v2_flow(flow: dict): Detect if a flow uses v2.0 features.
- load_flow_v2(flow: dict, config: Optional[SimConfig] = None): Load a v2.0 flow with generators, pools, durations, and reneging.
- validate_v2_flow(flow: dict): Validate a v2.0 flow, return list of errors (empty = valid).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
