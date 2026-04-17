---
id: BENCH-008
priority: P1
model: sonnet
role: bee
depends_on: []
---

# SPEC-BENCH-008: PRISM-bench Evaluation Harness

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Implement a PRISM-bench evaluation harness that scores workflow execution results across 5 categories (multi-step, recovery, multi-agent, branch comparison, governance) using per-category scoring functions with partial credit, recovery measurement, and branch optimality detection. The harness integrates with existing significance.py (Mann-Whitney U) and metrics.py (CV, recovery rate) modules to provide statistical validation of benchmark results.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- simdecisions/benchmark/types.py
- simdecisions/benchmark/significance.py
- simdecisions/benchmark/metrics.py
- simdecisions/des/statistics.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] File `simdecisions/benchmark/harness.py` created with `PRISMBenchHarness` class
- [ ] Method `PRISMBenchHarness.evaluate_multi_step(workflow, result)` returns score 0.0-1.0 based on completion accuracy and cost efficiency
- [ ] Method `PRISMBenchHarness.evaluate_recovery(workflow, result)` returns recovery_rate (errors_recovered / errors_encountered) and recovery_cost
- [ ] Method `PRISMBenchHarness.evaluate_multi_agent(workflow, result)` returns coordination_overhead and handoff_error_rate
- [ ] Method `PRISMBenchHarness.evaluate_branch_comparison(workflow, result)` returns optimality_score comparing chosen strategy to expected best
- [ ] Method `PRISMBenchHarness.evaluate_governance(workflow, result)` returns accuracy_delta and cost_delta between governed/ungoverned variants
- [ ] Method `PRISMBenchHarness.evaluate(workflow, result)` dispatches to category-specific evaluator based on workflow.metadata.category
- [ ] All evaluation methods return dict with `score` (0.0-1.0), `partial_credit` (0.0-1.0), and category-specific metrics
- [ ] Recovery measurement counts injected failures from metadata.failure_injection and checks DES statistics for recovery events
- [ ] Branch comparison scoring compares metadata.strategies outcomes using CLOCK+COIN metrics from result
- [ ] Governance overhead computes delta between paired runs (with/without GateEnforcer) from metadata.governance_mode
- [ ] Integration with significance.py: harness calls mann_whitney_u() for multi-run statistical validation
- [ ] Integration with metrics.py: harness calls coefficient_of_variation() and recovery_rate() for variance analysis
- [ ] Test file `tests/simdecisions/benchmark/test_harness.py` with >= 20 tests covering all 5 categories
- [ ] Tests verify partial credit scoring (incomplete workflows get 0.0 < score < 1.0)
- [ ] Tests verify recovery rate calculation with injected failures
- [ ] Tests verify branch optimality detection using metadata.strategies
- [ ] Tests verify governance overhead measurement using paired runs

## Files to Modify

| File Path | Purpose |
|-----------|---------|
| `simdecisions/benchmark/harness.py` | PRISMBenchHarness class and category evaluators |
| `tests/simdecisions/benchmark/test_harness.py` | Comprehensive harness tests |

## Evaluation Criteria per Category

| Category | Score Components | Partial Credit |
|----------|-----------------|----------------|
| **Multi-step** | Completion accuracy (50%), cost efficiency vs baseline (30%), variance/CV (20%) | Incomplete: score = (nodes_completed / total_nodes) × 0.5 |
| **Recovery** | Recovery rate (60%), recovery cost overhead (40%) | Partial recovery: score = (errors_recovered / errors_encountered) |
| **Multi-agent** | Handoff success rate (70%), coordination overhead vs single-agent (30%) | Failed handoffs: score = (successful_handoffs / total_handoffs) |
| **Branch comparison** | Optimality: did simulation pick better strategy? (binary), cost delta (continuous) | Suboptimal choice: score = 1.0 - (cost_delta / baseline_cost) |
| **Governance** | Accuracy preserved (50%), cost overhead acceptable (50%) | Accuracy degradation: score = 1.0 - abs(accuracy_delta) |

## Smoke Test

- [ ] `python -c "from simdecisions.benchmark.harness import PRISMBenchHarness; h = PRISMBenchHarness(); print('OK')"` prints OK
- [ ] `pytest tests/simdecisions/benchmark/test_harness.py -v` passes all tests
- [ ] `pytest tests/simdecisions/benchmark/test_harness.py::test_multi_step_scoring -v` passes
- [ ] `pytest tests/simdecisions/benchmark/test_harness.py::test_recovery_measurement -v` passes

## Constraints

- No file over 500 lines (modularize if harness.py approaches limit)
- No stubs — every evaluation method fully implemented
- No git operations
- TDD: write tests first, then implementation
- Use existing simdecisions.benchmark.significance and simdecisions.benchmark.metrics modules (do not duplicate)
- Use simdecisions.des.statistics.RunningStats for variance computation
- All scoring functions return float in range [0.0, 1.0] for consistency
- Partial credit must be monotonic: more progress = higher score
- Recovery rate uses formula: errors_recovered / max(errors_encountered, 1) to avoid division by zero
- Branch comparison requires metadata.strategies with at least 2 entries
- Governance overhead requires metadata.governance_mode = "with_gate" or "without_gate"

## Implementation Guide

### PRISMBenchHarness Structure

```python
class PRISMBenchHarness:
    """Evaluation harness for PRISM-bench tasks."""

    def evaluate(self, workflow: dict, result: dict) -> dict:
        """Dispatch to category-specific evaluator."""
        category = workflow.get("metadata", {}).get("category")
        # Dispatch to evaluate_{category}() method
        pass

    def evaluate_multi_step(self, workflow: dict, result: dict) -> dict:
        """Score multi-step workflow: completion + cost + variance."""
        pass

    def evaluate_recovery(self, workflow: dict, result: dict) -> dict:
        """Score recovery: rate + cost overhead."""
        pass

    def evaluate_multi_agent(self, workflow: dict, result: dict) -> dict:
        """Score multi-agent: handoff success + overhead."""
        pass

    def evaluate_branch_comparison(self, workflow: dict, result: dict) -> dict:
        """Score branch choice: optimality + cost delta."""
        pass

    def evaluate_governance(self, workflow: dict, result: dict) -> dict:
        """Score governance: accuracy preserved + cost overhead."""
        pass
```

### Input Format

The `workflow` dict is the PRISM-IR task from prism_bench_tasks/*.json.
The `result` dict matches the result schema from SPEC-BENCHMARK-SUITE-001 Section 1.4:

```python
result = {
    "task_id": "multi_step_01",
    "track": "simdecisions",
    "score": {...},  # populated by harness
    "currencies": {
        "clock_seconds": 12.5,
        "coin_usd": 0.082,
        "carbon_kg": 0.003,
        "tokens_in": 5200,
        "tokens_out": 1800,
        "model_calls": 4
    },
    "recovery": {
        "errors_encountered": 2,
        "errors_recovered": 2,
        "human_interventions": 0
    },
    "metadata": {...}
}
```

### Output Format

Each evaluate_*() method returns:

```python
{
    "score": 0.85,           # 0.0-1.0
    "partial_credit": 0.85,  # same as score for simplicity
    "category_metrics": {
        # Category-specific fields
        # Multi-step: completion_rate, cost_efficiency, variance
        # Recovery: recovery_rate, recovery_cost_overhead
        # Multi-agent: handoff_success_rate, coordination_overhead
        # Branch: optimality_binary, cost_delta
        # Governance: accuracy_delta, cost_overhead
    }
}
```

### Test Structure

- 4 tests per category (20 total minimum)
- Test perfect score (1.0)
- Test partial credit (0.0 < score < 1.0)
- Test zero score (0.0)
- Test edge cases (empty result, missing metadata, division by zero)
