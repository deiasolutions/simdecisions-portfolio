"""
diff_algorithm
==============

diff_algorithm.py — Compute structural diffs between two PHASE-IR flows.

Port of browser/src/apps/sim/components/flow-designer/compare/diffAlgorithm.ts

Compares two flow snapshots (sets of nodes + edges) and categorizes every
element into one of five difference types:

| Difference Type            | Tag             |
|----------------------------|-----------------|
| Node only in Branch A      | "branch_a_only" |
| Node only in Branch B      | "branch_b_only" |
| Same node, different data  | "modified"      |
| Token path divergence      | "path_diverged" |
| Timing difference          | "timing_delta"  |
| Identical in both branches | "unchanged"     |

Dependencies:
- from __future__ import annotations
- from typing import Any, Optional
- from dataclasses import dataclass, field

Classes:
- FlowNode: A node in a PHASE-IR snapshot (id + ReactFlow position + domain data).
- FlowEdge: An edge in a PHASE-IR snapshot.
- FlowMetrics: Aggregate simulation metrics attached to a branch.
- FlowSnapshot: Complete flow snapshot used as input for the diff.
- NodeDiff: Diff for a single node.
- EdgeDiff: Diff for a single edge.
- MetricsDelta: Delta for a single metric.
- FlowDiffResult: Complete diff result.

Functions:
- deep_equal(a: Any, b: Any): Deep equality check for Python objects.
- diff_fields(a: dict[str, Any], b: dict[str, Any]): Return the list of top-level keys in data that differ between a and b.
- edge_timing_ms(edge: Optional[FlowEdge]): Get the fixed timing value from an edge's timing distribution (ms).
- pct_change(a: float, b: float): Calculate percentage change from a to b.
- compute_flow_diff(snapshot_a: FlowSnapshot,
    snapshot_b: FlowSnapshot,): Compute a full structural + metrics diff between two PHASE-IR flow snapshots.
- extract_diff_ids(result: FlowDiffResult): Convenience: extract only the node/edge IDs that are NOT unchanged.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
