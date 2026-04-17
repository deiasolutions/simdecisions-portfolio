---
id: BENCH-007
priority: P1
model: opus
role: bee
depends_on: []
---

# SPEC-BENCH-007: Design 20 PRISM-bench Tasks Across 5 Categories

## Priority
P1

## Depends On
None

## Model Assignment
opus

## Objective

Design 20 PRISM-IR workflow tasks across 5 benchmark categories (multi-step workflow, recovery, multi-agent coordination, branch comparison, governance overhead) for the native PRISM-bench suite. Each task is a valid PRISM-IR JSON workflow with metadata specifying evaluation criteria, expected runtime, and category-specific parameters for failure injection, strategy comparison, and governance testing.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json
- simdecisions/phase_ir/primitives.py
- simdecisions/des/core.py
- simdecisions/des/engine.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] Directory `simdecisions/benchmark/prism_bench_tasks/` created with 20 JSON workflow files
- [ ] File `simdecisions/benchmark/prism_bench_tasks/README.md` documents all 20 tasks with ID, category, description, evaluation criteria
- [ ] 4 tasks in category "multi-step" with 5-20 nodes, branching, resource contention
- [ ] 4 tasks in category "recovery" with metadata.failure_injection describing injection points and failure types
- [ ] 4 tasks in category "multi-agent" with handoff edges and metadata documenting coordination points
- [ ] 4 tasks in category "branch-comparison" with metadata.strategies listing valid approaches and expected outcomes
- [ ] 4 tasks in category "governance" as paired variants (with and without GateEnforcer node) in metadata.governance_mode
- [ ] All 20 tasks have metadata.category, metadata.evaluation_criteria, metadata.expected_runtime_seconds
- [ ] All workflows validate against PRISM-IR schema: id, nodes[], edges[], optional resources[], optional variables[]
- [ ] Each task file is valid JSON loadable via json.load()
- [ ] Test file `tests/simdecisions/benchmark/test_prism_bench_tasks.py` validates all 20 tasks load and parse
- [ ] Test verifies each task has required metadata fields for its category
- [ ] Test verifies all node IDs are unique within each workflow
- [ ] Test verifies all edge from_node/to_node references exist in nodes

## Files to Modify

| File Path | Purpose |
|-----------|---------|
| `simdecisions/benchmark/prism_bench_tasks/multi_step_01_parallel_branches.json` | Multi-step workflow with parallel branches |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_02_resource_contention.json` | Multi-step with shared resource bottleneck |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_03_nested_loops.json` | Multi-step with repeat edges and loop detection |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_04_decision_tree.json` | Multi-step with deep decision tree (4+ levels) |
| `simdecisions/benchmark/prism_bench_tasks/recovery_01_service_timeout.json` | Recovery from service node timeout |
| `simdecisions/benchmark/prism_bench_tasks/recovery_02_resource_unavailable.json` | Recovery when resource pool exhausted |
| `simdecisions/benchmark/prism_bench_tasks/recovery_03_guard_failure.json` | Recovery when guard condition prevents edge |
| `simdecisions/benchmark/prism_bench_tasks/recovery_04_retry_backoff.json` | Recovery with retry logic and exponential backoff |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_01_handoff.json` | Two agents with single handoff point |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_02_pipeline.json` | Three agents in pipeline topology |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_03_fork_join.json` | Fork to multiple agents, join results |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_04_round_robin.json` | Round-robin routing across agent pool |
| `simdecisions/benchmark/prism_bench_tasks/branch_01_cost_vs_speed.json` | Branch choice: fast/expensive vs slow/cheap |
| `simdecisions/benchmark/prism_bench_tasks/branch_02_quality_tradeoff.json` | Branch choice: high quality vs acceptable quality |
| `simdecisions/benchmark/prism_bench_tasks/branch_03_risk_mitigation.json` | Branch choice: risky shortcut vs safe path |
| `simdecisions/benchmark/prism_bench_tasks/branch_04_load_balancing.json` | Branch choice: load balance across servers |
| `simdecisions/benchmark/prism_bench_tasks/governance_01_approval_gate.json` | Same workflow with/without approval gate |
| `simdecisions/benchmark/prism_bench_tasks/governance_02_audit_trail.json` | Same workflow with/without audit logging |
| `simdecisions/benchmark/prism_bench_tasks/governance_03_compliance_check.json` | Same workflow with/without compliance validation |
| `simdecisions/benchmark/prism_bench_tasks/governance_04_budget_limit.json` | Same workflow with/without budget enforcement |
| `simdecisions/benchmark/prism_bench_tasks/README.md` | Documentation of all 20 tasks |
| `tests/simdecisions/benchmark/test_prism_bench_tasks.py` | Validation tests for all tasks |

## Smoke Test

- [ ] `ls simdecisions/benchmark/prism_bench_tasks/*.json | wc -l` returns 20
- [ ] `python -c "import json; [json.load(open(f)) for f in __import__('pathlib').Path('simdecisions/benchmark/prism_bench_tasks').glob('*.json')]"` runs without error
- [ ] `pytest tests/simdecisions/benchmark/test_prism_bench_tasks.py -v` passes all tests

## Constraints

- No file over 500 lines
- No stubs — every workflow is a complete, executable PRISM-IR flow
- No git operations
- All workflows use PRISM-IR v1.0 or v2.0 schema from simdecisions/phase_ir/primitives.py
- Multi-step workflows must have >= 5 nodes
- Recovery workflows must document failure injection points in metadata
- Branch comparison workflows must list >= 2 valid strategies in metadata
- Governance workflows must provide both governed and ungoverned variants (can be in metadata or as separate files)
- All expected_runtime_seconds values must be realistic for DES execution (1-30 seconds per task)
- Use resource pools where appropriate (recovery, multi-step with contention)
- Use variables and guard conditions for decision/branch tasks
- Follow naming convention: `{category}_{NN}_{descriptive_name}.json`

## Task Breakdown

### Phase 1: Multi-Step Workflows (4 tasks)
Design workflows with varying complexity:
- Parallel branches with synchronization (join)
- Resource contention requiring queueing
- Nested loops/repeats for iterative processing
- Deep decision trees with 4+ decision nodes

### Phase 2: Recovery Workflows (4 tasks)
Design workflows with injected failures:
- Service timeout requiring fallback
- Resource exhaustion with queue abandonment
- Guard failure requiring alternate path
- Retry logic with exponential backoff

### Phase 3: Multi-Agent Workflows (4 tasks)
Design workflows with agent handoffs:
- Simple handoff between two agents
- Pipeline of three sequential agents
- Fork-join pattern with result aggregation
- Round-robin distribution across agent pool

### Phase 4: Branch Comparison Workflows (4 tasks)
Design workflows with strategic choices:
- Cost vs speed tradeoff
- Quality vs acceptable outcome
- Risk mitigation (safe vs shortcut)
- Load balancing decision

### Phase 5: Governance Workflows (4 tasks)
Design workflows testing governance overhead:
- Approval gate insertion
- Audit trail logging
- Compliance validation
- Budget enforcement

Each workflow must be executable by simdecisions.des.engine.SimulationEngine and produce measurable outcomes for evaluation.
