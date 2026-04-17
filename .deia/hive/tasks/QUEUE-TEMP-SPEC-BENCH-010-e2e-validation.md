# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

---
id: BENCH-010
priority: P1
model: haiku
role: bee
depends_on: [BENCH-009]
---

# SPEC-BENCH-010: End-to-End PRISM-bench Validation

## Priority
P1

## Depends On
- BENCH-009 (PRISMBenchAdapter fully wired)

## Model Assignment
haiku

## Objective

Run the complete PRISM-bench pipeline end-to-end using the benchmark CLI (`python _tools/benchmark.py run prism-bench --trials 2`), verify results are written to `.deia/benchmark/results/`, verify statistics are computed by collector.py, verify summary is published by publisher.py, and validate statistical consistency by running twice and comparing variance between runs. This is the acceptance test for Wave B proving the native PRISM-bench infrastructure is production-ready.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- simdecisions/benchmark/runner.py
- simdecisions/benchmark/collector.py
- simdecisions/benchmark/publisher.py
- _tools/benchmark.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] File `_tools/benchmark.py` exists as CLI entry point for benchmark suite
- [ ] Command `python _tools/benchmark.py run prism-bench --trials 2` completes without error
- [ ] Results written to `.deia/benchmark/results/prism-bench/` directory with 20 tasks × 2 tracks × 2 trials = 80 YAML files
- [ ] Each result YAML file matches result schema from SPEC-BENCHMARK-SUITE-001 Section 1.4
- [ ] ResultsCollector aggregates results and writes `prism-bench_aggregated.json` with track statistics
- [ ] Publisher generates `prism-bench_summary.md` with comparison table
- [ ] Publisher generates `prism-bench_raw.json` with all 80 result objects
- [ ] Two consecutive runs produce results with statistical consistency: mean values within 10% variance
- [ ] Comparison table includes CLOCK, COIN, CARBON rows with baseline vs simdecisions columns
- [ ] Integration test `tests/integration/test_benchmark_e2e.py` runs the full pipeline programmatically and validates output
- [ ] Test verifies all 20 tasks executed (check result files exist)
- [ ] Test verifies aggregated statistics computed (mean, std_dev, min, max per track)
- [ ] Test verifies p-values computed for baseline vs simdecisions comparison
- [ ] CLI supports `--trials N` flag to control trial count

## Files to Modify

| File Path | Purpose |
|-----------|---------|
| `_tools/benchmark.py` | CLI entry point for benchmark suite |
| `tests/integration/test_benchmark_e2e.py` | End-to-end integration test |

## Smoke Test

- [ ] `python _tools/benchmark.py --help` shows usage information
- [ ] `python _tools/benchmark.py run prism-bench --trials 2` completes in < 5 minutes
- [ ] `ls .deia/benchmark/results/prism-bench/*.yml | wc -l` returns 80 (20 tasks × 2 tracks × 2 trials)
- [ ] `cat .deia/benchmark/results/prism-bench/prism-bench_summary.md` displays comparison table
- [ ] `pytest tests/integration/test_benchmark_e2e.py -v` passes

## Constraints

- No file over 500 lines
- No stubs — every CLI command fully functional
- No git operations
- TDD: write integration test first, then CLI
- Use existing BenchmarkRunner, ResultsCollector, Publisher from Wave A
- Do not duplicate runner/collector/publisher logic in CLI
- CLI uses argparse for command-line parsing
- Results directory `.deia/benchmark/results/` created if missing
- Trial count defaults to 5 if not specified
- CLI returns exit code 0 on success, non-zero on failure

## CLI Design

### Command Structure

```bash
python _tools/benchmark.py run <benchmark> [options]
python _tools/benchmark.py estimate <benchmark> [options]
python _tools/benchmark.py publish <benchmark>
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `benchmark` | positional | Benchmark name (e.g., `prism-bench`) | required |
| `--trials` | int | Number of trials per task | 5 |
| `--sample` | int | Sample N tasks instead of full set | None (run all) |
| `--models` | str | Comma-separated model list | from manifest |
| `--output-dir` | str | Results output directory | `.deia/benchmark/results/` |
| `--dry-run` | flag | Show plan without executing | False |

### Example Usage

```bash
# Run full PRISM-bench with 2 trials
python _tools/benchmark.py run prism-bench --trials 2

# Estimate budget before running
python _tools/benchmark.py estimate prism-bench --trials 5

# Run sample of 5 tasks only
python _tools/benchmark.py run prism-bench --trials 2 --sample 5

# Publish existing results
python _tools/benchmark.py publish prism-bench
```

## CLI Implementation

```python
#!/usr/bin/env python
"""
Benchmark suite CLI for SimDecisions.

SPEC-BENCH-010 - Entry point for running benchmarks, estimating costs,
and publishing results.
"""
import argparse
import sys
from pathlib import Path
from simdecisions.benchmark.runner import BenchmarkRunner
from simdecisions.benchmark.collector import ResultsCollector
from simdecisions.benchmark.publisher import Publisher
from simdecisions.benchmark.estimator import format_budget_summary


def run_benchmark(args):
    """Run benchmark with specified configuration."""
    # Initialize runner
    manifest_path = ".deia/config/benchmarks.yml"
    runner = BenchmarkRunner(manifest_path, output_dir=args.output_dir)

    # Load manifest
    runner.load_manifest()

    # Estimate budget
    estimates = runner.estimate_budget(
        benchmark_name=args.benchmark,
        trials=args.trials,
        sample_size=args.sample,
    )

    print(format_budget_summary(estimates))

    # Dry run: stop here
    if args.dry_run:
        print("\nDry run — no tasks executed.")
        return 0

    # Get adapter
    adapter = runner.get_adapter(args.benchmark)

    # Load tasks
    all_tasks = adapter.load_tasks()
    tasks = all_tasks[:args.sample] if args.sample else all_tasks

    # Execute tasks
    from simdecisions.benchmark.executor import BenchmarkTaskExecutor
    from hivenode.ledger.writer import LedgerWriter

    # Create ledger writer (placeholder for now)
    ledger = LedgerWriter(db_path=".deia/ledger/benchmark.db")

    executor = BenchmarkTaskExecutor(ledger, adapter)

    print(f"\nRunning {len(tasks)} tasks × 2 tracks × {args.trials} trials...")

    results = []
    for task_data in tasks:
        for track in ["baseline", "simdecisions"]:
            for trial in range(1, args.trials + 1):
                # Create BenchmarkTask
                from simdecisions.benchmark.types import BenchmarkTask
                task = BenchmarkTask(
                    id=f"{task_data.id}-{track}-T{trial}",
                    benchmark_name=args.benchmark,
                    benchmark_version=adapter.version,
                    track=track,
                    trial=trial,
                    model=args.models.split(",")[0] if args.models else "claude-sonnet-4-5",
                    task_data=task_data.task_data,
                )

                # Execute
                if track == "baseline":
                    result = executor.execute_baseline(task)
                else:
                    ir = adapter.task_to_ir(task)
                    result = executor.execute_simdecisions(task, ir)

                # Write result
                executor.write_result(result, args.output_dir)
                results.append(result)

                print(f"  ✓ {task.id}")

    print(f"\n✓ Completed {len(results)} executions")

    # Collect and publish
    collector = ResultsCollector(args.output_dir)
    collector.export_aggregated_results(
        args.benchmark,
        f"{args.output_dir}/{args.benchmark}_aggregated.json"
    )

    publisher = Publisher(args.output_dir)
    # Load results for publishing
    from simdecisions.benchmark.types import BenchmarkResult
    benchmark_results = []  # Convert results to BenchmarkResult format
    # For now, skip publishing (will be implemented with full result conversion)

    print(f"\n✓ Results written to {args.output_dir}")
    return 0


def estimate_benchmark(args):
    """Estimate benchmark costs without running."""
    manifest_path = ".deia/config/benchmarks.yml"
    runner = BenchmarkRunner(manifest_path)
    runner.load_manifest()

    estimates = runner.estimate_budget(
        benchmark_name=args.benchmark,
        trials=args.trials,
        sample_size=args.sample,
    )

    print(format_budget_summary(estimates))
    return 0


def publish_benchmark(args):
    """Publish results from previous run."""
    collector = ResultsCollector(args.output_dir)
    publisher = Publisher(args.output_dir)

    # Publish all outputs
    publisher.publish_all(args.benchmark, collector)

    print(f"✓ Published results to {args.output_dir}")
    return 0


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="SimDecisions Benchmark Suite")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # run command
    run_parser = subparsers.add_parser("run", help="Run benchmark")
    run_parser.add_argument("benchmark", help="Benchmark name (e.g., prism-bench)")
    run_parser.add_argument("--trials", type=int, default=5, help="Trials per task")
    run_parser.add_argument("--sample", type=int, help="Sample N tasks")
    run_parser.add_argument("--models", help="Comma-separated model list")
    run_parser.add_argument("--output-dir", default=".deia/benchmark/results", help="Output directory")
    run_parser.add_argument("--dry-run", action="store_true", help="Show plan without executing")

    # estimate command
    est_parser = subparsers.add_parser("estimate", help="Estimate costs")
    est_parser.add_argument("benchmark", help="Benchmark name")
    est_parser.add_argument("--trials", type=int, default=5, help="Trials per task")
    est_parser.add_argument("--sample", type=int, help="Sample N tasks")

    # publish command
    pub_parser = subparsers.add_parser("publish", help="Publish results")
    pub_parser.add_argument("benchmark", help="Benchmark name")
    pub_parser.add_argument("--output-dir", default=".deia/benchmark/results", help="Output directory")

    args = parser.parse_args()

    if args.command == "run":
        return run_benchmark(args)
    elif args.command == "estimate":
        return estimate_benchmark(args)
    elif args.command == "publish":
        return publish_benchmark(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## Integration Test Structure

Minimum 4 tests:
1. `test_run_prism_bench()` — run full pipeline, verify 80 results
2. `test_aggregated_statistics()` — verify collector output format
3. `test_published_summary()` — verify summary markdown table
4. `test_statistical_consistency()` — run twice, compare variance
