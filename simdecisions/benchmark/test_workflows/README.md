# Benchmark Test Workflows

This directory contains 5 minimal PRISM-IR workflow files for Wave A exit validation of the benchmark suite infrastructure. These workflows are used by the benchmark runner to verify end-to-end functionality before external benchmarks are added in Waves B and C.

All workflows are designed to:
- Complete in <10 seconds when simulated
- Use valid PRISM-IR format (Flow schema)
- Have clear pass/fail evaluation criteria
- Test different aspects of the DES engine

---

## Workflow 01: Simple Queue

**File:** `workflow_01_simple_queue.json`

**Topology:** Source → Queue → Service → Sink

**Description:** Basic M/M/1 queueing system. Single server with FIFO queue discipline. Tests fundamental queueing behavior.

**Nodes:**
- **Source:** Poisson arrivals (λ=5/min), max 100 tokens
- **Queue:** FIFO discipline, capacity 10
- **Service:** Exponential service time (μ=6/min), 1 server
- **Sink:** Completion

**Evaluation Criteria:**
- Throughput > 4 entities/min
- Mean cycle time < 3 min

**Expected Runtime:** ~5 seconds

---

## Workflow 02: Multi-Server Queue

**File:** `workflow_02_multi_server.json`

**Topology:** Source → Queue → Service (3 servers) → Sink

**Description:** M/M/c queueing system with 3 parallel servers. Tests server utilization and parallel processing.

**Nodes:**
- **Source:** Poisson arrivals (λ=10/min), max 100 tokens
- **Queue:** FIFO discipline, capacity 20
- **Service:** Exponential service time (μ=4/min), 3 servers
- **Sink:** Completion

**Evaluation Criteria:**
- Server utilization < 90%
- Queue depth < 15

**Expected Runtime:** ~5 seconds

---

## Workflow 03: Priority Queue

**File:** `workflow_03_priority_queue.json`

**Topology:** Source → Priority Queue → Service → Sink

**Description:** Priority queueing system where tokens have priority levels (1-3). Tests priority queue discipline and fairness.

**Nodes:**
- **Source:** Poisson arrivals (λ=8/min), tokens tagged with priority 1-3 (uniform), max 100 tokens
- **Queue:** PRIORITY discipline (based on priority property)
- **Service:** Exponential service time (μ=10/min), 2 servers
- **Sink:** Completion

**Evaluation Criteria:**
- High-priority tokens (priority=1) have mean cycle time < low-priority tokens (priority=3)

**Expected Runtime:** ~5 seconds

---

## Workflow 04: Branch-Merge

**File:** `workflow_04_branch_merge.json`

**Topology:** Source → Branch → [Path A, Path B] → Merge → Sink

**Description:** Forking and joining workflow with two parallel paths. Tests branch/fork edge types and merge logic.

**Nodes:**
- **Source:** Poisson arrivals (λ=10/min), max 100 tokens
- **Branch:** 50/50 random split
- **Service A:** Exponential service time (μ=0.5/min), 1 server
- **Service B:** Exponential service time (μ=0.25/min), 1 server
- **Merge:** Join point for both paths
- **Sink:** Completion

**Evaluation Criteria:**
- 45-55% of tokens went through each branch (statistical balance)

**Expected Runtime:** ~5 seconds

---

## Workflow 05: Resource Contention

**File:** `workflow_05_resource_contention.json`

**Topology:** [Source 1, Source 2] → Merge → Service (with shared resource) → Sink

**Description:** Two independent sources competing for a shared resource pool. Tests resource contention and queueing under resource constraints.

**Nodes:**
- **Source 1:** Poisson arrivals (λ=3/min), max 50 tokens
- **Source 2:** Poisson arrivals (λ=3/min), max 50 tokens
- **Merge:** Combines both streams
- **Service:** Exponential service time (μ=8/min), requires shared resource
- **Sink:** Completion

**Resources:**
- **shared_pool:** Capacity 2, FIFO discipline

**Evaluation Criteria:**
- Resource utilization 70-90%
- No deadlocks

**Expected Runtime:** ~5 seconds

---

## Usage

These workflows are loaded by the benchmark runner during Wave A validation. They serve as fixtures for testing:

1. **BenchmarkRunner:** Task manifest loading, budget estimation, factory task generation
2. **ResultsCollector:** Result aggregation, statistics computation
3. **Publisher:** Markdown summary generation, raw JSON export

To validate manually:

```python
from simdecisions.des.engine import SimulationEngine
import json

# Load workflow
with open("workflow_01_simple_queue.json") as f:
    flow = json.load(f)

# Run simulation
engine = SimulationEngine()
ctx = engine.load(flow)
ctx = engine.run(ctx)

# Inspect results
print(engine.statistics(ctx))
```

---

## Schema Validation

All workflows are validated by `tests/simdecisions/benchmark/test_workflows_valid.py` to ensure:

- Valid JSON format
- Required PRISM-IR fields present (`id`, `nodes`, `edges`)
- Node count ≤ 8
- Workflow 05 includes `resources` field

---

**Created:** 2026-04-13
**Author:** BEE (TASK-BENCH-001.5)
**Purpose:** Wave A exit validation for SPEC-BENCHMARK-SUITE-001
