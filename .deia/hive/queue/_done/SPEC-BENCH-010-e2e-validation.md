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
