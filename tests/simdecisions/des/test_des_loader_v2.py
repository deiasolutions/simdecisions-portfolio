"""
test_des_loader_v2
==================

TASK-040: v2.0 IR Loader Tests

Tests for v2.0 PHASE-IR flow loading with generators, pools, and resource
dispatch configuration.

Dependencies:
- from __future__ import annotations
- from simdecisions.des.core import EngineState, SimConfig, load_flow
- from simdecisions.des.loader_v2 import (

Classes:
- TestIsV2Flow: Tests for v2 detection logic.
- TestLoadFlowV1Unchanged: Tests for backward compatibility with v1.0 flows.
- TestV2GeneratorsLoaded: Tests for v2.0 generators loading.
- TestV2PoolsLoaded: Tests for v2.0 resource pools loading.
- TestValidateV2Flow: Tests for v2 flow validation.
- TestLoadFlowV2EntryPoint: Tests for load_flow routing to v2 loader.
- TestV2IntegrationGeneratorsAndPools: Integration tests: v2 flows with both generators and pools.
- TestEdgeCases: Edge case tests.
- TestRegressionV1Tests: Ensure v1 behavior is preserved.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
