---
id: BENCH-DASHBOARD-001
priority: P2
model: sonnet
depends_on: BEE-TELEMETRY-001
area_code: factory
---

# SPEC-BENCH-DASHBOARD-001: Benchmark Auto-Report

## Priority
P2

## Depends On
SPEC-BEE-TELEMETRY-001 (reads bee_events for timing and concurrency data)

## Model Assignment
sonnet

## Objective

After every benchmark run, automatically generate a summary report with concurrency curve, cost burn rate, success/fail/rate-limit breakdown, and per-repo stats. No more digging through 726 raw files to answer "how did it go." The report is a markdown file written to `.deia/benchmark/results/` and optionally printed to stdout.

## Files to Read First

- `_tools/analyze_swebench.py`
  Existing analysis script — extend or replace
- `.deia/benchmark/results/swebench_analysis.json`
  Current analysis output format
- `.deia/hive/coordination/SWE-BENCH-PRO-ANALYSIS.md`
  Example of the report we want auto-generated
- `hivenode/telemetry/bee_events.py`
  Bee lifecycle events — source for timing data (from BEE-TELEMETRY-001)
- `.deia/benchmark/swebench/patches/`
  Patch files — source for success counting
- `.deia/hive/responses/`
  RAW and RESPONSE files — source for cost and duration data

## Deliverables

### Part 1: Report generator

- [ ] Create `_tools/benchmark_report.py` (or extend `analyze_swebench.py` if it stays under 500 lines)
- [ ] CLI: `python _tools/benchmark_report.py --start <iso> --end <iso> [--output <path>]`
- [ ] If `--output` not specified, write to `.deia/benchmark/results/YYYYMMDD-HHMM-benchmark-report.md`

### Part 2: Report contents

The generated markdown report MUST include:

- [ ] **Header**: Run ID, start time, end time, total wall-clock duration, model used
- [ ] **Summary table**: Total tasks, succeeded, failed, rate-limited, error, timeout — with percentages
- [ ] **Concurrency profile**: Minute-by-minute table showing concurrent bee count. Include mean, median, mode, peak.
- [ ] **Cost summary**: Total cost, cost per task (mean), cost per hour, cost per successful patch
- [ ] **Duration summary**: Mean, median, min, max task duration (excluding rate-limited)
- [ ] **Per-repo breakdown**: Table with repo name, total tasks, succeeded, failed, success rate — sorted by success rate descending
- [ ] **Per-language breakdown**: Same table grouped by language
- [ ] **Failure analysis**: Categorize failures: rate_limited, no_response, error, timeout — with counts and percentages
- [ ] **Rate limit events**: When rate limit was hit, reset time, how many tasks affected
- [ ] **Concurrency chart** (ASCII): Simple text-based bar chart showing concurrent bees over time (one row per 5-minute bucket)

### Part 3: Auto-trigger

- [ ] In `run_queue.py`, after a batch run completes (all specs in a batch are done), automatically invoke the report generator for that batch's time window
- [ ] Log: `[QUEUE] Benchmark report generated: <path>`
- [ ] If report generation fails, log warning but do NOT block queue processing

### Part 4: Backfill existing data

- [ ] The report generator MUST work with the existing RAW file format (for runs before BEE-TELEMETRY-001)
- [ ] If bee_events.db has data for the time window, use it. If not, fall back to parsing RAW files.
- [ ] Include a `--backfill` flag that parses all RAW files and populates bee_events.db retroactively

## Test Requirements

- [ ] Tests written FIRST (TDD)
- [ ] Unit test: report generator produces valid markdown
- [ ] Unit test: concurrency calculation matches known data (use SWE-bench run as test fixture: 204 real tasks, median 12, peak 18)
- [ ] Unit test: per-repo breakdown sums to total
- [ ] Unit test: fallback to RAW file parsing when bee_events.db is empty
- [ ] Unit test: backfill correctly populates bee_events.db from RAW files
- [ ] All existing tests still pass

## Constraints

- No file over 500 lines
- No stubs
- No git operations
- Report is MARKDOWN, not HTML, not JSON (human-readable first)
- ASCII chart, not image — must render in terminal and in markdown viewers
- CDT timestamps (UTC-5) in all output
