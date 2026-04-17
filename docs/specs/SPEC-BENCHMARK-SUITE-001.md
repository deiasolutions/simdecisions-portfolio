# SPEC-BENCHMARK-SUITE-001: SimDecisions Benchmark Suite

**Created:** 2026-04-13
**Author:** Q88N (Human Sovereign)
**Priority:** P0
**Status:** DRAFT
**Model:** opus (Q33NR review), sonnet (bee implementation), haiku (BAT)

---

## Vision Anchor

SimDecisions is a process orchestration engine. The benchmark suite proves the thesis: simulating a workflow before executing it produces better outcomes than executing directly. The suite runs established industry benchmarks and a native PRISM-IR benchmark in parallel, constrained by factory capacity, measuring accuracy, cost (CLOCK/COIN/CARBON), variance, and recovery rate.

---

## Objective

Build a factory-integrated benchmark runner that:

1. Runs SimDecisions-augmented tracks against established industry benchmarks alongside raw-model baselines
2. Runs a native PRISM-bench suite for process-level evaluation no existing benchmark covers
3. Respects factory concurrency limits; benchmarks are hive workloads like any other
4. Publishes reproducible, versioned results with full three-currency accounting
5. Runs on release tags automatically and on-demand manually

---

## 1. Architecture

### 1.1 Two-Track Design

Every benchmark task runs twice:

| Track | Description |
|-------|-------------|
| **Baseline** | Model receives task, produces answer directly. No SimDecisions in the loop. Same model, same temperature, same tools. |
| **SimDecisions** | Model receives task, SimDecisions wraps it: DEF (express as IR) → SIM (simulate approaches) → BRA (branch and compare) → COMP (pick winner) → DEC/EXE (produce output). |

The only variable between tracks is SimDecisions. Same model. Same task. Same evaluation harness.

### 1.2 Factory Integration

Benchmark runs are hive workloads. They enter the queue like any task and respect factory capacity.

```
benchmark_suite_runner
    ├── loads benchmark manifest (benchmarks.yml)
    ├── generates BenchmarkTask items per (benchmark × task × track × trial)
    ├── submits to factory queue as priority=P2 workload
    ├── factory scheduler dispatches within capacity limits
    ├── results collector aggregates as tasks complete
    └── publisher emits results when all tasks for a benchmark version finish
```

Concurrency is governed by the factory's existing resource pool and queue discipline. No special scheduling. If the factory has 5 slots, 5 benchmark tasks run. The rest wait. Three currencies are tracked per task automatically via Event Ledger.

### 1.3 Benchmark Adapter Interface

Each external benchmark gets an adapter. The adapter is the only benchmark-specific code.

```python
class BenchmarkAdapter:
    """One per benchmark. Translates between benchmark format and SimDecisions."""

    name: str                   # e.g. "swe-bench-verified"
    version: str                # pinned benchmark version

    def load_tasks(self) -> list[BenchmarkTask]:
        """Pull task set. Version-pinned. Cached locally."""

    def task_to_ir(self, task: BenchmarkTask) -> dict:
        """Translate benchmark task into PRISM-IR workflow for SimDecisions track."""

    def run_baseline(self, task: BenchmarkTask, model: str) -> BaselineResult:
        """Execute task with raw model, no SimDecisions. Returns output + metrics."""

    def run_simdecisions(self, task: BenchmarkTask, ir: dict, model: str) -> SimResult:
        """Execute task through SimDecisions loop. Returns output + metrics."""

    def evaluate(self, task: BenchmarkTask, output) -> EvalResult:
        """Score output using benchmark's own evaluation harness. Returns score + metadata."""
```

### 1.4 Results Schema

Every benchmark task produces a result record:

```yaml
result:
  benchmark: swe-bench-verified
  benchmark_version: "2026-04"
  simdecisions_version: "0.x.y"
  task_id: "django__django-16527"
  track: baseline | simdecisions
  trial: 3                          # which trial (1..N)
  model: claude-sonnet-4-6
  
  score:
    passed: true | false
    partial_credit: 0.0-1.0         # if benchmark supports it
    
  currencies:
    clock_seconds: 142.7
    coin_usd: 0.0834
    carbon_kg: 0.012                # computed from model + tokens
    tokens_in: 48200
    tokens_out: 12400
    model_calls: 7
    
  recovery:
    errors_encountered: 2
    errors_recovered: 2
    human_interventions: 0
    
  metadata:
    started_at: "2026-04-13T14:22:00Z"
    completed_at: "2026-04-13T14:24:23Z"
    factory_task_id: "BENCH-SWE-0142-B-03"
    event_ledger_range: [evt_88401, evt_88447]
```

---

## 2. Benchmark Registry

### 2.1 Layer One: Established Benchmarks

Ship adapters in this order. One at a time. First adapter ships with the suite; others follow.

| Priority | Benchmark | What It Tests | Why It Matters for SimDecisions |
|----------|-----------|---------------|--------------------------------|
| **Ship first** | SWE-bench Verified | Coding agent on real GitHub issues | Gold standard. Most cited. Most comparison points. Coding workflows express cleanly in PRISM-IR. |
| Second | GAIA | Multi-step reasoning + tool use | Planning-heavy tasks where simulate-first should show clear gains. |
| Third | TAU-bench | Tool-agent-user interaction | Directly relevant to governance layer; tests agent behavior under constraints. |
| Fourth | AgentBench | Multi-domain agent evaluation | Wide coverage across domains. Validates "wide benchmark" thesis. |

### 2.2 Layer Two: PRISM-bench (Native)

For what existing benchmarks don't measure. This is the benchmark SimDecisions hosts.

| Category | Task Type | Evaluation |
|----------|-----------|------------|
| Multi-step workflow | PRISM-IR workflows with 5-20 steps, branching, resource contention | Completion accuracy, cost efficiency, variance |
| Recovery | Workflows with injected failures at known points | Recovery rate, recovery cost, time to recover |
| Multi-agent coordination | Workflows requiring 2+ agents with handoffs | Coordination overhead, error at handoff points |
| Branch comparison | Workflows with multiple valid strategies | Did simulation pick the better branch? Measured by outcome + cost. |
| Governance overhead | Same workflow with and without GateEnforcer | Accuracy preserved? Cost of governance layer quantified. |

PRISM-bench task set is public (Apache 2.0). Evaluation harness is public. Anyone can run it against their own system. PRISM-IR adoption is the structural goal.

---

## 3. Execution Protocol

### 3.1 Trial Configuration

```yaml
benchmark_config:
  trials_per_task: 5              # minimum for variance reporting
  trials_preferred: 10            # if budget allows
  models:
    - claude-sonnet-4-6           # primary
    - gpt-5.4                     # comparison (if API available)
  tracks:
    - baseline
    - simdecisions
  factory_priority: P2            # below production work, above background
  
  budget_limits:
    max_coin_per_run: 50.00       # USD; abort if exceeded
    max_clock_per_task: 600       # seconds; timeout per individual task
```

### 3.2 Concurrency Model

The benchmark runner does NOT manage concurrency. It submits tasks to the factory queue. The factory's existing scheduler, resource pools, and queue discipline handle everything.

```
Total work items = benchmarks × tasks × tracks × trials

Example: SWE-bench Verified (300 tasks) × 2 tracks × 5 trials = 3,000 items
Factory capacity: 5 concurrent → ~600 batches
At ~3 min/task average → ~30 hours wall clock

Reducible by:
  - Sampling: run 50 representative tasks instead of 300 (clearly disclosed)
  - Fewer trials: 5 instead of 10
  - Higher factory capacity (more resource pool slots)
```

Budget estimation is a pre-run step. The runner calculates estimated COIN before starting and requires explicit approval if above threshold.

### 3.3 Run Lifecycle

```
1. MANIFEST     Load benchmarks.yml, resolve adapter versions, pin task sets
2. ESTIMATE     Calculate total work items, estimate COIN/CLOCK, display to operator
3. APPROVE      Operator confirms budget (or auto-approve if within preset limit)
4. GENERATE     Create factory task files for all work items
5. DISPATCH     Submit to factory queue at configured priority
6. EXECUTE      Factory runs tasks within capacity; Event Ledger captures everything
7. COLLECT      Results collector polls for completed tasks, aggregates per benchmark
8. ANALYZE      Compute deltas, variance, statistical significance per benchmark
9. PUBLISH      Write results to benchmarks.simdecisions.com + raw JSON to repo
```

### 3.4 Statistical Reporting

For each benchmark, report:

| Metric | Baseline | SimDecisions | Delta | p-value |
|--------|----------|-------------|-------|---------|
| Accuracy (%) | mean ± std | mean ± std | +/- | < 0.05? |
| CLOCK (seconds) | mean ± std | mean ± std | +/- | |
| COIN (USD) | mean ± std | mean ± std | +/- | |
| CARBON (kg) | mean ± std | mean ± std | +/- | |
| Variance (CV) | coefficient of variation | coefficient of variation | +/- | |
| Recovery rate | errors / recoveries | errors / recoveries | +/- | |

Use Welford's algorithm for online statistics (already implemented in `statistics.py`). Use Mann-Whitney U for significance testing between tracks (non-parametric; don't assume normal distribution).

---

## 4. Publishing

### 4.1 Results Repository

Public repository: `github.com/deiasolutions/prism-bench`

```
prism-bench/
├── README.md                     # methodology, how to reproduce
├── benchmarks.yml                # registry of all benchmarks + adapter versions
├── adapters/
│   ├── swe_bench/
│   │   ├── adapter.py
│   │   └── README.md
│   ├── gaia/
│   ├── tau_bench/
│   └── agent_bench/
├── prism_bench/
│   ├── tasks/                    # PRISM-IR task set (public)
│   ├── evaluation/               # evaluation harness (public)
│   └── README.md
├── runner/
│   ├── benchmark_runner.py       # main runner
│   ├── results_collector.py
│   ├── budget_estimator.py
│   └── publisher.py
├── results/
│   ├── 2026-04-v0.1.0/
│   │   ├── swe_bench_summary.md
│   │   ├── swe_bench_raw.json
│   │   └── swe_bench_analysis.md
│   └── latest -> 2026-04-v0.1.0/
└── LICENSE                       # Apache 2.0
```

### 4.2 Results Page

`benchmarks.simdecisions.com` -- static site generated from results directory.

Content per benchmark: summary table, delta charts, variance comparison, trend line across SimDecisions versions, methodology link, raw data download.

### 4.3 Versioning

| What | Versioned How |
|------|---------------|
| Benchmark task set | Pinned per benchmark release (e.g., SWE-bench Verified 2026-04) |
| SimDecisions | Git tag on release |
| Results | Tagged as `{benchmark_version}-{simdecisions_version}` |
| PRISM-bench tasks | Semver; additions increment minor, removals increment major |

---

## 5. Cadence

| Trigger | What Runs |
|---------|-----------|
| SimDecisions release tag | Full suite, all registered benchmarks |
| Manual `hive> benchmark run {name}` | Single benchmark, on demand |
| Weekly (if enabled) | PRISM-bench only (lower cost, catches regressions) |

---

## 6. Factory Task Format

Each benchmark work item becomes a standard factory task:

```yaml
---
task_id: BENCH-SWE-0142-SD-03
type: benchmark
priority: P2
benchmark: swe-bench-verified
benchmark_version: "2026-04"
task_ref: "django__django-16527"
track: simdecisions
trial: 3
model: claude-sonnet-4-6
budget_limit_usd: 0.50
timeout_seconds: 600
depends_on: []
---

## Objective

Run SWE-bench Verified task django__django-16527 through SimDecisions loop (trial 3 of 5).

## Steps

1. Load task from adapter cache
2. Translate to PRISM-IR via adapter.task_to_ir()
3. Execute SimDecisions loop: DEF → SIM → BRA → COMP → DEC → EXE
4. Capture output patch
5. Run adapter.evaluate() with benchmark's test harness
6. Emit result record to Event Ledger
7. Write result to .deia/benchmark/results/

## Acceptance Criteria

- [ ] Result record written with all fields from results schema
- [ ] Event Ledger entries exist for the full run (ledger range recorded)
- [ ] Three currencies captured (CLOCK, COIN, CARBON)
- [ ] Output submitted to benchmark evaluation harness
- [ ] Score recorded (pass/fail + partial credit if applicable)
```

---

## 7. Implementation Waves

### Wave A: Infrastructure (no external benchmarks yet)

| Task | Description | Bee |
|------|-------------|-----|
| BENCH-001 | BenchmarkAdapter base class, BenchmarkTask/EvalResult/SimResult dataclasses, results schema | BEE-SONNET |
| BENCH-002 | BenchmarkRunner: manifest loader, budget estimator, factory task generator | BEE-SONNET |
| BENCH-003 | ResultsCollector: poll completed tasks, aggregate per benchmark, compute statistics (Welford + Mann-Whitney U) | BEE-SONNET |
| BENCH-004 | Publisher: markdown summary generator, raw JSON exporter, trend chart data | BEE-HAIKU |
| BENCH-005 | Factory integration: benchmark tasks enter queue, Event Ledger captures three currencies, results written on completion | BEE-SONNET |

**Wave A exit criteria:** `hive> benchmark run prism-bench` works end-to-end with 5 trivial PRISM-IR test tasks. Budget estimation displays before run. Results written. Statistics computed. No external benchmark adapters yet.

### Wave B: PRISM-bench (native benchmark)

| Task | Description | Bee |
|------|-------------|-----|
| BENCH-006 | Design 20 PRISM-bench tasks across 5 categories (multi-step, recovery, multi-agent, branch comparison, governance overhead) | BEE-OPUS |
| BENCH-007 | PRISM-bench evaluation harness: per-category scoring, partial credit, recovery measurement | BEE-SONNET |
| BENCH-008 | PRISM-bench adapter (self-referential: SimDecisions benchmarking itself via its own IR) | BEE-SONNET |
| BENCH-009 | End-to-end: run PRISM-bench, publish results, verify reproducibility by running twice and comparing | BEE-HAIKU (BAT) |

**Wave B exit criteria:** PRISM-bench runs, produces published results, two consecutive runs show statistical consistency. Repository structure matches Section 4.1.

### Wave C: SWE-bench Verified (first external benchmark)

| Task | Description | Bee |
|------|-------------|-----|
| BENCH-010 | SWE-bench adapter: task loader (pin version), baseline runner, SimDecisions runner | BEE-SONNET |
| BENCH-011 | SWE-bench IR translator: GitHub issue → PRISM-IR coding workflow | BEE-OPUS |
| BENCH-012 | SWE-bench evaluation integration: wire to their Docker-based test harness | BEE-SONNET |
| BENCH-013 | Sampling strategy: select representative 50-task subset for initial runs (full 300 after validation) | BEE-HAIKU |
| BENCH-014 | First run: 50 tasks × 2 tracks × 5 trials = 500 work items. Publish results. | BEE-SONNET + BAT |

**Wave C exit criteria:** Published SWE-bench Verified results with baseline vs SimDecisions delta. Statistical significance reported. Three currencies reported. Results reproducible.

### Wave D: Additional Benchmarks (after C ships)

One adapter per benchmark. Same pattern. GAIA first, then TAU-bench, then AgentBench.

### Wave E: Automation

| Task | Description | Bee |
|------|-------------|-----|
| BENCH-020 | CI hook: on release tag, trigger full benchmark suite | BEE-HAIKU |
| BENCH-021 | benchmarks.simdecisions.com: static site generator from results directory | BEE-SONNET |
| BENCH-022 | Weekly PRISM-bench regression runner (cron or scheduler daemon) | BEE-HAIKU |

**Wave E exit criteria:** Benchmarks run automatically on release. Results page updates. Regression detected within one week.

---

## Acceptance Criteria (Spec-Level)

- [ ] BenchmarkAdapter interface implemented with at least 2 adapters (PRISM-bench + SWE-bench)
- [ ] Two-track execution (baseline + SimDecisions) produces results for same task set
- [ ] Factory queue integration: benchmark tasks respect capacity limits
- [ ] Three currencies (CLOCK, COIN, CARBON) captured per task via Event Ledger
- [ ] Statistical reporting with variance and significance testing
- [ ] Budget estimation before run with operator approval gate
- [ ] Results published to public repository in documented format
- [ ] Reproducibility verified: two runs of same benchmark produce statistically consistent results
- [ ] PRISM-bench task set and evaluation harness are Apache 2.0 public

## Smoke Test

```bash
# Wave A
hive> benchmark estimate prism-bench
# Should display: N tasks × 2 tracks × 5 trials = M items, estimated COIN: $X.XX

hive> benchmark run prism-bench --trials 2 --dry-run
# Should display: task list without executing

hive> benchmark run prism-bench --trials 2
# Should complete, write results to .deia/benchmark/results/

# Wave C
hive> benchmark run swe-bench --sample 10 --trials 2
# Should complete with 10 tasks × 2 tracks × 2 trials = 40 items
```

## Constraints

- Benchmark tasks are P2 priority; production work (P0, P1) preempts
- No benchmark run starts without budget estimation display
- All raw results stored; no silent aggregation without raw data preserved
- External benchmark evaluation harnesses run unmodified; we never fork their scoring
- CARBON computed from model + token count using published emission factors, not placeholder values

## depends_on

- Event Ledger (ADR-001) -- exists
- Factory queue + scheduler -- exists
- DES engine + PRISM-IR runtime -- exists
- Statistics module (Welford's) -- exists
- Three-currency tracking -- exists (CARBON computation needed)

---

*SPEC-BENCHMARK-SUITE-001 -- Q88N -- 2026-04-13*
