# PRISM-bench Task Set

This directory contains 20 PRISM-IR workflow tasks designed for the PRISM-bench benchmark suite. Each task is a valid, executable PRISM-IR workflow with metadata specifying evaluation criteria and expected runtime.

## Task Categories

### Multi-Step Workflows (4 tasks)

Tasks that test complex workflow execution with varying topology and control flow patterns.

| ID | Name | Description | Key Features |
|----|------|-------------|--------------|
| `multi_step_01_parallel_branches` | Parallel Branches Workflow | Fork-join with 3 parallel branches | Fork/join synchronization, parallel execution |
| `multi_step_02_resource_contention` | Resource Contention Workflow | Sequential workflow with shared resource bottleneck | Resource queueing, FIFO discipline |
| `multi_step_03_nested_loops` | Nested Loops Workflow | Nested iteration with loop detection | Repeat edges, loop counters, iteration tracking |
| `multi_step_04_decision_tree` | Deep Decision Tree Workflow | 4-level decision tree with exclusive routing | Deep branching, guard evaluation, exclusive mode |

### Recovery Workflows (4 tasks)

Tasks that test failure injection and recovery path execution.

| ID | Name | Description | Failure Type | Recovery Strategy |
|----|------|-------------|--------------|-------------------|
| `recovery_01_service_timeout` | Service Timeout Recovery | Primary service with timeout fallback | Timeout | Fallback service |
| `recovery_02_resource_unavailable` | Resource Exhaustion Recovery | Queue renege on resource wait timeout | Resource exhaustion | Alternate path |
| `recovery_03_guard_failure` | Guard Condition Failure Recovery | Validation guard with retry logic | Guard false | Retry with escalation |
| `recovery_04_retry_backoff` | Exponential Backoff Retry Recovery | Service retry with exponential backoff | Transient error | Exponential backoff |

### Multi-Agent Workflows (4 tasks)

Tasks that test coordination overhead and handoff correctness across multiple agents.

| ID | Name | Description | Agent Count | Handoff Points |
|----|------|-------------|-------------|----------------|
| `multi_agent_01_handoff` | Two-Agent Handoff | Simple handoff between two agents | 2 | 1 |
| `multi_agent_02_pipeline` | Three-Agent Pipeline | Sequential pipeline topology | 3 | 2 |
| `multi_agent_03_fork_join` | Multi-Agent Fork-Join | Fork to workers, aggregate results | 4 | 6 |
| `multi_agent_04_round_robin` | Round-Robin Agent Pool | Round-robin routing to worker pool | 4 | 3 |

### Branch Comparison Workflows (4 tasks)

Tasks that test strategic decision-making with multiple valid approaches and measurable trade-offs.

| ID | Name | Description | Tradeoff Dimension |
|----|------|-------------|-------------------|
| `branch_01_cost_vs_speed` | Cost vs Speed Tradeoff | Fast/expensive vs slow/cheap paths | Time vs cost |
| `branch_02_quality_tradeoff` | Quality Tradeoff Branch Selection | High quality vs acceptable quality | Time vs quality |
| `branch_03_risk_mitigation` | Risk Mitigation Branch Selection | Risky shortcut vs safe path | Time vs risk |
| `branch_04_load_balancing` | Load Balancing Branch Selection | Route to least loaded server | Load distribution |

### Governance Workflows (4 tasks)

Tasks that test governance overhead by comparing governed vs ungoverned execution modes.

| ID | Name | Description | Governance Mechanism |
|----|------|-------------|----------------------|
| `governance_01_approval_gate` | Approval Gate Governance | Optional approval gate insertion | Human approval |
| `governance_02_audit_trail` | Audit Trail Governance | Optional audit logging between steps | Audit logging |
| `governance_03_compliance_check` | Compliance Check Governance | Optional compliance validation | Compliance checks |
| `governance_04_budget_limit` | Budget Limit Governance | Optional budget enforcement | Budget checks |

## Metadata Schema

Every task includes the following metadata fields:

```json
{
  "metadata": {
    "category": "multi-step | recovery | multi-agent | branch-comparison | governance",
    "description": "Human-readable description of the workflow",
    "evaluation_criteria": "Pass/fail criteria for evaluation harness",
    "expected_runtime_seconds": 5
  }
}
```

### Category-Specific Metadata

**Multi-step workflows:**
- `node_count`: Total number of nodes
- `branch_count` (optional): Number of parallel branches
- `loop_depth` (optional): Nesting level for loops
- `decision_depth` (optional): Depth of decision tree
- `resource_contention` (optional): Boolean indicating resource bottleneck

**Recovery workflows:**
- `failure_injection`: Object describing failure scenario
  - `node_id`: Where to inject failure
  - `failure_type`: Type of failure (timeout, resource_exhaustion, guard_false, transient_error)
  - `injection_probability` (optional): Probability of failure
  - `recovery_path`: Node ID of recovery path
  - `escalation_path` (optional): Node ID of escalation path

**Multi-agent workflows:**
- `agent_count`: Number of agents/groups
- `handoff_points`: Array of handoff edges
  - `from`: Source agent group
  - `to`: Target agent group
  - `edge`: Edge ID

**Branch comparison workflows:**
- `strategies`: Array of valid strategies with expected outcomes
  - `name`: Strategy name
  - `path`: Node ID of strategy path
  - `expected_time`: Expected completion time
  - Additional strategy-specific fields (cost, quality, risk, etc.)

**Governance workflows:**
- `governance_mode`: Object comparing ungoverned vs governed execution
  - `ungoverned`: Expected metrics without governance
  - `governed`: Expected metrics with governance

## Execution Requirements

All tasks require:
- PRISM-IR v1.0 or v2.0 compatible DES engine
- Support for all node types used: start, sink, service, decision, human, wait
- Support for all edge types used: then, fork, join, switch, any, repeat, emit, on, timeout
- Resource management (capacity, queueing, discipline)
- Variable evaluation (guards, effects, expressions)
- Distribution sampling (constant, exponential)

## Evaluation Harness Integration

The evaluation harness (defined in SPEC-BENCH-008) will:

1. Load each task JSON
2. Execute via SimulationEngine with specified configuration
3. Measure:
   - Completion time (CLOCK)
   - Cost (COIN) based on resource usage
   - Carbon (CARBON) computed from model + tokens
   - Accuracy: did all acceptance criteria pass?
4. Compare against expected outcomes from metadata
5. Score based on category-specific criteria

## Version

PRISM-bench tasks v1.0.0 (2026-04-13)

## License

Apache 2.0

These tasks are part of the public PRISM-bench benchmark suite. Anyone can run them against their own process orchestration system.
