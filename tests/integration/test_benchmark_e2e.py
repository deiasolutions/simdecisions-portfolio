"""
test_benchmark_e2e
==================

End-to-end integration test for PRISM-bench pipeline.

SPEC-BENCH-010 - Validates full benchmark execution flow:
- Run PRISM-bench with 2 trials
- Verify 80 result files (20 tasks × 2 tracks × 2 trials)
- Verify aggregated statistics
- Verify published summary
- Verify statistical consistency across runs

Dependencies:
- import json
- import pytest
- import shutil
- from pathlib import Path
- from simdecisions.benchmark.runner import BenchmarkRunner
- from simdecisions.benchmark.collector import ResultsCollector
- from simdecisions.benchmark.publisher import Publisher
- from simdecisions.benchmark.adapters.prism_bench import PRISMBenchAdapter
- from simdecisions.benchmark.executor import BenchmarkTaskExecutor
- from simdecisions.benchmark.types import BenchmarkTask, BenchmarkResult

Functions:
- clean_output_dir(): Clean test output directory before and after test.
- clean_ledger(): Clean test ledger database before and after test.
- write_benchmark_result(exec_result, task, trial, output_dir): Helper to convert execution result to BenchmarkResult and write YAML.
- test_run_prism_bench(clean_output_dir, clean_ledger): Run full PRISM-bench pipeline and verify 80 results.
- test_aggregated_statistics(clean_output_dir, clean_ledger): Verify collector computes and exports aggregated statistics.
- test_published_summary(clean_output_dir, clean_ledger): Verify publisher generates summary markdown with comparison table.
- test_statistical_consistency(clean_output_dir, clean_ledger): Run PRISM-bench twice and verify statistical consistency.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
