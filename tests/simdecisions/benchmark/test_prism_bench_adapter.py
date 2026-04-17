"""
test_prism_bench_adapter
========================

Integration tests for PRISM-bench adapter wiring.

SPEC-BENCH-009 - Tests that verify the adapter loads tasks from
prism_bench_tasks/, executes workflows through DES, captures statistics,
and evaluates results using PRISMBenchHarness.

Dependencies:
- import pytest
- from pathlib import Path
- from simdecisions.benchmark.adapters.prism_bench import PRISMBenchAdapter
- from simdecisions.benchmark.types import BenchmarkTask, BaselineResult, SimResult, EvalResult

Functions:
- adapter(): Create PRISMBenchAdapter instance.
- test_adapter_name(adapter): Test adapter name property.
- test_adapter_version(adapter): Test adapter version property.
- test_load_tasks_from_prism_bench_tasks(adapter): Test that load_tasks() loads all 20 tasks from prism_bench_tasks/.
- test_load_tasks_has_correct_ids(adapter): Test that loaded tasks have IDs matching workflow files.
- test_baseline_execution(adapter): Test run_baseline() executes workflow and returns valid result.
- test_simdecisions_execution(adapter): Test run_simdecisions() executes workflow and returns valid SimResult.
- test_evaluate_returns_eval_result(adapter): Test evaluate() calls PRISMBenchHarness and returns EvalResult.
- test_des_statistics_captured(adapter): Test that DES statistics are captured in result metadata.
- test_all_tasks_load_and_execute(adapter): Smoke test: verify all 20 tasks can load and execute.
- test_result_currencies_complete(adapter): Test that result has all 6 currency fields.
- test_task_to_ir(adapter): Test translation to PRISM-IR (should be identity).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
