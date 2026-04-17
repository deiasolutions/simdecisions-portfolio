"""
test_des_replication
====================

Tests for DES Replication Manager — ADR-008, TASK-087.

30+ tests covering:
  - confidence_interval (correct CI, single value, two values)
  - _t_critical (common df, large df normal approx)
  - _norm_ppf (correct for 0.975, 0.95, 0.5)
  - detect_warmup_mser (stationary, trending, too-short)
  - ReplicationConfig (defaults, custom)
  - run_replications (correct count, different seeds, precision stopping)
  - ReplicationResults (CIs, summary structure)
  - PairedComparison (significant / not significant)
  - Seeds (auto deterministic, custom seeds)
  - ConfidenceInterval (relative_precision, zero mean)

Dependencies:
- from __future__ import annotations
- import math
- import uuid
- from simdecisions.des.replication import (
- from simdecisions.phase_ir.primitives import Edge, Flow, Node

Classes:
- TestNormPPF: Tests for inverse normal CDF approximation.
- TestTCritical: Tests for t-critical value approximation.
- TestConfidenceInterval: Tests for the confidence_interval() function.
- TestConfidenceIntervalDataclass: Tests for the ConfidenceInterval dataclass properties.
- TestDetectWarmupMSER: Tests for MSER-5 warm-up detection.
- TestReplicationConfig: Tests for ReplicationConfig defaults and custom values.
- TestSeeds: Tests for seed generation and usage.
- TestRunReplications: Tests for the run_replications() function.
- TestPrecisionStopping: Tests for relative-precision-based early stopping.
- TestReplicationResults: Tests for ReplicationResults aggregation and summary.
- TestPairedComparison: Tests for compare_configs_paired.
- TestReplicationResult: Tests for the ReplicationResult dataclass.

Functions:
- _tid(): Build a linear flow: N0 -> N1 -> ... -> N(n-1).
- _single_node_flow(): Build a single-node flow (source = sink).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
