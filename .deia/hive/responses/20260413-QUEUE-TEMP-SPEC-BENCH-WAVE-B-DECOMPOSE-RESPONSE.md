# QUEUE-TEMP-SPEC-BENCH-WAVE-B-DECOMPOSE: Decompose Wave B into Factory Specs -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

All files are newly created (no modifications to existing files):

- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\backlog\SPEC-BENCH-007-prism-bench-tasks.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\backlog\SPEC-BENCH-008-evaluation-harness.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\backlog\SPEC-BENCH-009-adapter-wiring.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\.deia\hive\queue\backlog\SPEC-BENCH-010-e2e-validation.md`

## What Was Done

- Created 4 factory-ready SPEC files for Wave B (PRISM-bench native benchmark)
- Renumbered IDs to BENCH-007 through BENCH-010 to avoid collision with BENCH-006 (already used for Wave A integration)
- All specs conform to `.deia/hive/queue/SUBMISSION-CHECKLIST.md` format:
  - YAML frontmatter with `id`, `priority`, `model`, `role`, `depends_on`
  - `## Priority` section with P1
  - `## Acceptance Criteria` with checkbox items (17-22 items per spec)
  - `## Smoke Test` with checkbox items
  - `## Files to Read First` with validated paths (all paths exist on disk)
  - `## Constraints` section
  - Reference to master spec `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
- Dependency chain implemented: BENCH-007 and BENCH-008 have no dependencies, BENCH-009 depends on both, BENCH-010 depends on BENCH-009
- Model assignments: BENCH-007 (opus), BENCH-008 (sonnet), BENCH-009 (sonnet), BENCH-010 (haiku)
- All specs use concrete file paths and detailed tables for deliverables
- Each spec includes implementation guide with code examples, test requirements, and evaluation criteria

## SPEC-BENCH-007: Design 20 PRISM-bench Tasks

- **Model:** opus
- **Depends on:** None
- **Deliverables:** 20 JSON workflow files across 5 categories (multi-step, recovery, multi-agent, branch-comparison, governance)
- **Acceptance criteria:** 17 checkboxes
- **Key requirements:**
  - 4 tasks per category with category-specific metadata
  - All workflows validate against PRISM-IR schema
  - Recovery tasks include failure_injection metadata
  - Branch comparison tasks include strategies metadata
  - Governance tasks include paired variants (with/without GateEnforcer)
  - Test file validates all 20 tasks load and parse

## SPEC-BENCH-008: Evaluation Harness

- **Model:** sonnet
- **Depends on:** None (can be built in parallel with BENCH-007)
- **Deliverables:** `simdecisions/benchmark/harness.py` with `PRISMBenchHarness` class
- **Acceptance criteria:** 22 checkboxes
- **Key requirements:**
  - Per-category scoring functions (multi-step, recovery, multi-agent, branch-comparison, governance)
  - Partial credit scoring (not just pass/fail)
  - Recovery measurement from DES statistics
  - Branch optimality detection using metadata.strategies
  - Governance overhead measurement (delta between governed/ungoverned)
  - Integration with significance.py (Mann-Whitney U) and metrics.py (CV, recovery rate)
  - Minimum 20 tests covering all 5 categories

## SPEC-BENCH-009: Adapter Wiring

- **Model:** sonnet
- **Depends on:** BENCH-007, BENCH-008
- **Deliverables:** Replace placeholders in `simdecisions/benchmark/adapters/prism_bench.py`
- **Acceptance criteria:** 18 checkboxes
- **Key requirements:**
  - `load_tasks()` loads from prism_bench_tasks/ (20 real tasks, not test_workflows)
  - `run_baseline()` executes through SimulationEngine, captures CLOCK/COIN/CARBON
  - `run_simdecisions()` executes through DES (placeholder for real DEF→SIM→BRA→COMP loop)
  - `evaluate()` calls PRISMBenchHarness
  - DES statistics integration (tokens_created, tokens_completed, cycle_time, throughput)
  - Integration tests run one task through both tracks and verify result format

## SPEC-BENCH-010: E2E Validation

- **Model:** haiku
- **Depends on:** BENCH-009
- **Deliverables:** `_tools/benchmark.py` CLI and end-to-end integration test
- **Acceptance criteria:** 19 checkboxes
- **Key requirements:**
  - CLI: `python _tools/benchmark.py run prism-bench --trials 2`
  - Results written to `.deia/benchmark/results/` (20 tasks × 2 tracks × 2 trials = 80 YAML files)
  - ResultsCollector aggregates results with track statistics
  - Publisher generates summary.md, raw.json, trends.csv
  - Two consecutive runs show statistical consistency (mean values within 10% variance)
  - Integration test runs full pipeline programmatically and validates output

## IR Density Compliance

All specs include high-density structured content to meet Gate 0's IR density >= 0.200 requirement:
- Tables for deliverables, file mappings, evaluation criteria, test matrices
- Detailed acceptance criteria checklists (17-22 items per spec)
- Concrete file paths in multiple sections
- Code blocks for implementation examples, CLI usage, test structure
- Dependency tables and workflow diagrams

## Dependency Chain Verified

```
BENCH-007 (tasks)  ──┐
                     ├──> BENCH-009 (adapter wiring)  ──> BENCH-010 (e2e)
BENCH-008 (harness) ──┘
```

- BENCH-007 and BENCH-008 can run in parallel (no dependencies)
- BENCH-009 requires both BENCH-007 and BENCH-008 to complete
- BENCH-010 requires BENCH-009 to complete

## Validation Results

- ✓ All 4 specs exist in `.deia/hive/queue/backlog/`
- ✓ All specs have valid YAML frontmatter with correct `depends_on` chains
- ✓ All specs have >= 8 acceptance criteria checkboxes (17-22 per spec)
- ✓ All specs have `## Priority` section with P1
- ✓ All specs have `## Smoke Test` with checkbox items
- ✓ All specs have `## Constraints` section
- ✓ All specs reference `docs/specs/SPEC-BENCHMARK-SUITE-001.md`
- ✓ All file paths in `## Files to Read First` validated (all exist on disk)
- ✓ No spec exceeds 500 lines (largest is BENCH-010 at ~380 lines)
- ✓ Model assignments correct: BENCH-007 (opus), BENCH-008/009 (sonnet), BENCH-010 (haiku)

## Wave B Exit Criteria (from Master Spec)

The 4 specs implement the complete Wave B exit criteria:

> "PRISM-bench runs, produces published results, two consecutive runs show statistical consistency. Repository structure matches Section 4.1."

- **BENCH-007:** Produces the 20 PRISM-bench tasks (repository structure)
- **BENCH-008:** Provides evaluation harness for all 5 categories
- **BENCH-009:** Wires real DES execution to replace placeholders
- **BENCH-010:** End-to-end validation with statistical consistency check

All 4 specs are ready for factory dispatch and execution.
