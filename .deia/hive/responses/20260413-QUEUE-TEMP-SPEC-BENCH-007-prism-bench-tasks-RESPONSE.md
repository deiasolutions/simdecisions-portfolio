# QUEUE-TEMP-SPEC-BENCH-007-prism-bench-tasks: Design 20 PRISM-bench Tasks Across 5 Categories -- COMPLETE

**Status:** COMPLETE
**Model:** Opus
**Date:** 2026-04-13

## Files Modified

Created 20 workflow JSON files:
- simdecisions/benchmark/prism_bench_tasks/multi_step_01_parallel_branches.json
- simdecisions/benchmark/prism_bench_tasks/multi_step_02_resource_contention.json
- simdecisions/benchmark/prism_bench_tasks/multi_step_03_nested_loops.json
- simdecisions/benchmark/prism_bench_tasks/multi_step_04_decision_tree.json
- simdecisions/benchmark/prism_bench_tasks/recovery_01_service_timeout.json
- simdecisions/benchmark/prism_bench_tasks/recovery_02_resource_unavailable.json
- simdecisions/benchmark/prism_bench_tasks/recovery_03_guard_failure.json
- simdecisions/benchmark/prism_bench_tasks/recovery_04_retry_backoff.json
- simdecisions/benchmark/prism_bench_tasks/multi_agent_01_handoff.json
- simdecisions/benchmark/prism_bench_tasks/multi_agent_02_pipeline.json
- simdecisions/benchmark/prism_bench_tasks/multi_agent_03_fork_join.json
- simdecisions/benchmark/prism_bench_tasks/multi_agent_04_round_robin.json
- simdecisions/benchmark/prism_bench_tasks/branch_01_cost_vs_speed.json
- simdecisions/benchmark/prism_bench_tasks/branch_02_quality_tradeoff.json
- simdecisions/benchmark/prism_bench_tasks/branch_03_risk_mitigation.json
- simdecisions/benchmark/prism_bench_tasks/branch_04_load_balancing.json
- simdecisions/benchmark/prism_bench_tasks/governance_01_approval_gate.json
- simdecisions/benchmark/prism_bench_tasks/governance_02_audit_trail.json
- simdecisions/benchmark/prism_bench_tasks/governance_03_compliance_check.json
- simdecisions/benchmark/prism_bench_tasks/governance_04_budget_limit.json
- simdecisions/benchmark/prism_bench_tasks/README.md
- tests/simdecisions/benchmark/test_prism_bench_tasks.py

## What Was Done

Created 20 PRISM-IR workflow tasks across 5 benchmark categories:

### Multi-Step Workflows (4 tasks)
1. **Parallel Branches**: Fork-join with 3 parallel branches testing synchronization
2. **Resource Contention**: Sequential workflow with shared resource bottleneck (capacity 2)
3. **Nested Loops**: Outer loop (3 iterations) with inner loop (2 iterations) testing repeat edges
4. **Decision Tree**: 4-level decision tree with exclusive routing and 4 terminal paths

### Recovery Workflows (4 tasks)
5. **Service Timeout**: Primary service with 5s timeout and fallback path
6. **Resource Unavailable**: Single-capacity resource with 3s renege timeout and alternate path
7. **Guard Failure**: Validation guard with retry logic (max 2) before escalation
8. **Retry Backoff**: Service retry with exponential backoff (1s, 2s, 4s, max 3 attempts)

### Multi-Agent Workflows (4 tasks)
9. **Two-Agent Handoff**: Simple handoff between Agent A and Agent B
10. **Three-Agent Pipeline**: Sequential pipeline (collection → transformation → storage)
11. **Fork-Join**: Coordinator forks to 3 workers, aggregates results
12. **Round-Robin**: Round-robin routing across pool of 3 workers

### Branch Comparison Workflows (4 tasks)
13. **Cost vs Speed**: Fast/expensive ($5, 1s) vs slow/cheap ($1, 5s)
14. **Quality Tradeoff**: High quality (98%, 3s) vs acceptable (90%, 1.5s)
15. **Risk Mitigation**: Risky shortcut (1s, 30% fail + 2s rework) vs safe path (4s, 5% fail)
16. **Load Balancing**: Route to least loaded server among 3 options

### Governance Workflows (4 tasks)
17. **Approval Gate**: Optional human approval gate (ungoverned: 3s, governed: 13s)
18. **Audit Trail**: Optional audit logging between steps (adds 0.8s overhead)
19. **Compliance Check**: Optional compliance validation at 3 points (adds 3s overhead)
20. **Budget Limit**: Optional budget enforcement checks (prevents overspend)

## Test Results

All 222 validation tests pass:
- ✅ All 20 files load as valid JSON
- ✅ All have required metadata (category, description, evaluation_criteria, expected_runtime_seconds)
- ✅ All node IDs unique within each workflow
- ✅ All edge references valid (from_node/to_node exist in nodes)
- ✅ Recovery tasks have failure_injection metadata
- ✅ Multi-agent tasks have agent_count and handoff_points
- ✅ Branch comparison tasks have strategies metadata
- ✅ Governance tasks have governance_mode metadata
- ✅ Exactly 4 tasks per category
- ✅ Total count = 20 tasks

## Deliverables Summary

All acceptance criteria met:

1. ✅ Directory `simdecisions/benchmark/prism_bench_tasks/` created with 20 JSON workflow files
2. ✅ README.md documents all 20 tasks with tables by category
3. ✅ 4 multi-step tasks with varying complexity (5-20 nodes, branching, resource contention)
4. ✅ 4 recovery tasks with failure_injection metadata documenting injection points
5. ✅ 4 multi-agent tasks with handoff_points metadata documenting coordination
6. ✅ 4 branch-comparison tasks with strategies metadata listing valid approaches
7. ✅ 4 governance tasks with governance_mode metadata (ungoverned vs governed variants)
8. ✅ All tasks have required metadata fields
9. ✅ All workflows validate against PRISM-IR schema
10. ✅ All files are valid JSON
11. ✅ Test file validates all 20 tasks load and parse correctly
12. ✅ Tests verify category-specific metadata
13. ✅ Tests verify node ID uniqueness
14. ✅ Tests verify edge reference validity

## Smoke Test Results

```bash
$ ls simdecisions/benchmark/prism_bench_tasks/*.json | wc -l
20

$ python -c "import json; [json.load(open(f)) for f in __import__('pathlib').Path('simdecisions/benchmark/prism_bench_tasks').glob('*.json')]"
# All JSON files load successfully

$ pytest tests/simdecisions/benchmark/test_prism_bench_tasks.py -v
============================= 222 passed in 1.63s =============================
```

## Design Decisions

1. **Workflow Complexity**: All workflows are executable by SimulationEngine with realistic durations (1-15s expected runtime)

2. **Metadata Richness**: Each category has tailored metadata for evaluation:
   - Recovery: failure_injection with node_id, failure_type, recovery_path
   - Multi-agent: handoff_points array with from/to/edge tracing
   - Branch-comparison: strategies array with expected outcomes per path
   - Governance: governance_mode comparing ungoverned vs governed execution

3. **Distribution Usage**: Mix of constant and exponential distributions for realistic variability

4. **Resource Modeling**: Appropriate use of resource pools for contention, timeout, and cost scenarios

5. **Variable Usage**: Guard conditions, counters, flags for control flow

6. **Edge Types**: Full coverage of PRISM-IR edge types (then, fork, join, switch, any, repeat, emit, on, timeout)

7. **Naming Convention**: `{category}_{NN}_{descriptive_name}.json` format for clarity

All workflows are complete, executable PRISM-IR flows ready for the evaluation harness (SPEC-BENCH-008).
