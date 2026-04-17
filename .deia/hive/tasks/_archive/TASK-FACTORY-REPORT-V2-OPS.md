# TASK-FACTORY-REPORT-V2-OPS

**Role:** Q33N
**Priority:** P0
**Model:** sonnet

---

## Mission

Enhance `_tools/factory_report.py` (created by TASK-HOURLY-REPORT-SYSTEM) with ops manager-grade metrics. If the base script doesn't exist yet, build it from scratch with all these requirements.

---

## Ops Manager Requirements

The report must answer these questions at a glance:

### 1. LOAD PROFILE

**Peak / Current / Min load over the reporting window.**

```
LOAD PROFILE (last 24h)
  Current:     3 active  (2 queens, 1 bee)  | 20% of 15 max
  Peak:        7 active  at 11:05           | 47% of 15 max
  Trough:      0 active  at 03:00-08:00     | IDLE 5.0h
  Avg load:    2.3 active                   | 15% utilization

  Zero-load windows:  03:00-08:00 (5.0h idle)
  Saturation events:  0 (never hit 15 max)
```

Track when load = 0 (nothing running) and when load approaches max. This tells Q88N if we're under-utilizing or hitting ceilings.

**Data source:** Build/status `active` array length over time. For historical, compute from completed task timestamps (first_seen, last_seen overlaps).

### 2. QUEUE WAIT TIMES

**How long did specs sit in backlog before being picked up?**

```
QUEUE WAIT TIMES
  Avg wait:      12.3 min  (time in backlog before dispatch)
  Max wait:      45.2 min  (SPEC-WIKI-108, blocked on deps)
  Min wait:       0.8 min  (SPEC-FACTORY-003, dispatched immediately)
  Currently waiting:  3 specs  (oldest: 2.1h — SPEC-MCP-002)

  Starvation alert: SPEC-MCP-002 waiting 2.1h (deps unmet)
```

**Data source:** Compare spec file creation time (filesystem mtime or `first_seen` in build/status) against dispatch time.

### 3. ESTIMATED vs ACTUAL TIME

**Human estimates vs reality, broken down by compute and wall time.**

```
TIME ANALYSIS
  Spec estimates vs actuals (last 24h, 12 tasks):

  | Task                    | Est (h) | Wall  | Compute | Factor |
  |-------------------------|---------|-------|---------|--------|
  | DISPATCH-QUEEN-ALPHA    | 4.0h    | 8.7m  | 8.7m    | 27.6x  |
  | DISPATCH-QUEEN-CHARLIE  | 4.0h    | 16.8m | 16.8m   | 14.3x  |
  | DISPATCH-QUEEN-ECHO     | 4.0h    | 14.4m | 14.4m   | 16.7x  |
  | FACTORY-003-ttl         | 2.0h    | 12.0m | 12.0m   | 10.0x  |

  Avg overestimate factor:  17.2x  (specs estimate 17x more than actual)

  Insight: Time budgets can be reduced to ~15min for sonnet queen tasks
```

**Estimated hours** come from spec's `## Estimated Hours` field or the schedule.json `estimated_hours`. **Actual** comes from build/status duration.

### 4. CONCURRENCY FACTOR

**How much parallelism are we actually achieving?**

```
CONCURRENCY ANALYSIS
  Total compute time:   53.2 min  (sum of all task durations)
  Total wall time:      20.0 min  (first dispatch to last completion)
  Concurrency factor:   2.66x     (53.2 / 20.0)

  Theoretical max:      5.0x      (5 parallel queens)
  Efficiency:           53%       (2.66 / 5.0)

  Bottleneck:  CHARLIE (16.8 min) — longest-running task
               set wall time floor at 16.8 min regardless of parallelism

  If sequential:  53.2 min wall time
  Actual:         20.0 min wall time
  Time saved:     33.2 min (62% reduction from parallelism)
```

**Concurrency factor** = total_compute_time / wall_time. Higher = better use of parallelism. Max theoretical = max_parallel_bees.

### 5. THREE CURRENCIES (Enhanced)

```
COST SUMMARY (3 currencies)

  USD                    Today        Lifetime      Rate
  ────────────────────────────────────────────────────────
  Total spend:           $70.18       $3,226.25     $8.77/h
  Per-task avg:          $11.70       $10.86
  Per-LOC changed:       $0.62        —
  Most expensive:        FOXTROT $18.53 (synthesis)
  Cheapest:              DELTA $1.52 (partial)

  TOKENS                 Today        Lifetime      Rate
  ────────────────────────────────────────────────────────
  Input:                 385K         1.05B         48K/h
  Output:                52K          8.9M          6.5K/h
  Efficiency:            13.5%        0.85%         (out/in ratio)

  TIME                   Today        Lifetime
  ────────────────────────────────────────────────────────
  Compute hours:         0.89h        —
  Wall hours:            0.33h        —
  Concurrency factor:    2.66x        —
  Human-equiv hours:     ~40h         —             (estimated manual effort)
```

**Human-equivalent hours:** Rough estimate of how long a human would take. Use heuristic: 1 bee-minute ≈ 30-60 human-minutes for code tasks, 1 bee-minute ≈ 10-20 human-minutes for research tasks.

### 6. PRODUCTIVITY METRICS

```
PRODUCTIVITY
  Tasks completed:      12          (today)
  Tasks failed:          0          (today)
  Fix tasks:             1          (rework)
  Success rate:        100%
  Rework rate:          8.3%

  Throughput:           1.5 tasks/h  (wall clock)
  Throughput:           4.0 tasks/h  (compute, accounting for parallelism)

  Files modified:       47          (today)
  Lines changed:        ~2,400      (estimated from task responses)
```

---

## Implementation

### Architecture

```python
# _tools/factory_report.py

class FactoryReport:
    def __init__(self, build_status, schedule, queue_state):
        self.build = build_status      # from /build/status
        self.schedule = schedule        # from schedule.json
        self.queue = queue_state        # from queue/ dir listing

    def load_profile(self, window_hours=24) -> dict
    def queue_wait_times(self) -> dict
    def time_analysis(self) -> dict
    def concurrency_factor(self, window_hours=24) -> dict
    def cost_summary(self) -> dict
    def productivity(self) -> dict

    def render_text(self) -> str       # formatted terminal output
    def render_json(self) -> dict      # machine-readable
```

### Computing Load Over Time (from completed tasks)

Since we don't have a time-series DB, reconstruct load from task timestamps:

```python
def compute_load_timeline(completed_tasks):
    """Build load-over-time from task start/end timestamps."""
    events = []
    for t in completed_tasks:
        start = parse_iso(t['first_seen'])
        end = parse_iso(t['last_seen'])
        events.append((start, +1))  # task started
        events.append((end, -1))    # task ended

    events.sort()
    load = 0
    timeline = []
    for time, delta in events:
        load += delta
        timeline.append((time, load))

    return timeline  # [(timestamp, concurrent_count), ...]
```

### Computing Queue Wait Time

```python
def compute_wait_time(task):
    """Time between spec entering backlog and dispatch starting."""
    # first_seen in build/status = when dispatcher picked it up
    # For file-based: compare file mtime in backlog vs first_seen
    spec_created = get_file_mtime(f"queue/backlog/{task['spec_file']}")
    dispatched = parse_iso(task['first_seen'])
    return dispatched - spec_created
```

### CLI Interface

```
python _tools/factory_report.py              # Full report, last 1h
python _tools/factory_report.py --since 24   # Last 24 hours
python _tools/factory_report.py --json        # JSON output
python _tools/factory_report.py --watch       # Refresh every 60s
python _tools/factory_report.py --section load   # Just load profile
python _tools/factory_report.py --section cost   # Just cost summary
```

---

## Acceptance Criteria

- [ ] Load profile: peak, trough, zero-load windows, saturation events
- [ ] Queue wait times: avg, max, min, starvation alerts
- [ ] Estimated vs actual time with overestimate factor
- [ ] Concurrency factor with theoretical max and efficiency %
- [ ] 3 currencies: USD (with per-task, per-LOC), tokens (with efficiency ratio), time (with human-equiv)
- [ ] Productivity: throughput, success rate, rework rate
- [ ] Reconstructs load timeline from completed task timestamps
- [ ] Handles missing data gracefully (no crashes on empty fields)
- [ ] `--json` output mode
- [ ] Under 500 lines, stdlib only

## Smoke Test

```bash
python _tools/factory_report.py --since 24
python _tools/factory_report.py --json --since 24
python _tools/factory_report.py --section load
```

## Constraints

- Stdlib only (no pip)
- Read-only (no writes to build state or queue)
- Must work even if hivenode is offline (degrade gracefully)
- Single file, under 500 lines
- If `_tools/factory_report.py` already exists from the base task, enhance it — do not start from scratch
