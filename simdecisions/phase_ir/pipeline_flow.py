"""
pipeline_flow
=============

Phase-IR Pipeline Flow Analysis Module (TASK-226).

Converts Phase-IR execution traces into pipeline stage metrics for performance
analysis, bottleneck identification, and capacity planning.

Functions:
    calculate_stage_durations - Compute stage duration statistics
    identify_bottleneck - Identify stage with highest average WIP
    calculate_throughput - Calculate specs per hour throughput
    calculate_wip_distribution - Compute average WIP by stage
    calculate_cycle_time - Analyze end-to-end cycle time

Dependencies:
- from typing import Dict, List
- import statistics

Functions:
- calculate_stage_durations(trace_data: List[dict]): Calculate stage duration statistics from trace data.
- identify_bottleneck(wip_distribution: Dict[str, float]): Identify bottleneck stage (highest average WIP).
- calculate_throughput(specs_completed: int, sim_time_hours: float): Calculate throughput in specs per hour.
- calculate_wip_distribution(trace_data: List[dict]): Calculate average work-in-progress (WIP) by stage.
- calculate_cycle_time(trace_data: List[dict]): Calculate end-to-end cycle time statistics.
- _percentile(data: List[float], p: float): Calculate percentile using linear interpolation.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
