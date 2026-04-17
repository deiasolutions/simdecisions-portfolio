# SPEC-SWE-001-sampler-spec-generator: SWE-bench Task Sampler and Factory Spec Generator -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-13

## Files Modified

- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\_tools\swebench_runner.py (created)
- C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\tests\integration\test_swebench_runner.py (created)

## What Was Done

### 1. Created swebench_runner.py CLI Tool

Implemented `_tools/swebench_runner.py` with three subcommands:

- **sample**: Downloads SWE-bench Verified dataset from HuggingFace (`princeton-nlp/SWE-bench_Verified`, split=test), samples N tasks (default 50, configurable), optionally filters by repo and difficulty, uses random seed for reproducibility, writes self-contained JSON to `.deia/benchmark/swebench/sample.json`

- **generate**: Reads `sample.json`, produces one factory-compatible SPEC file per task in `.deia/benchmark/swebench/specs/`, each spec includes full problem_statement, repo details, base_commit, and instructions to generate a unified diff patch, skips existing specs to avoid overwrites

- **list-repos**: Lists all unique repositories in SWE-bench Verified with task counts, sorted by count descending

### 2. Directory Structure Creation

The tool creates the following structure:
- `.deia/benchmark/swebench/sample.json` - sampled tasks
- `.deia/benchmark/swebench/specs/` - generated SPEC files
- `.deia/benchmark/swebench/patches/` - target directory for bee-generated patches
- `.deia/benchmark/swebench/results/` - reserved for evaluation results

### 3. Generated Spec Format

Each generated spec follows gate 0 requirements:
- `## Priority` (P2)
- `## Depends On` (None)
- `## Model Assignment` (sonnet)
- `## Objective` with full problem_statement embedded
- `## Acceptance Criteria` in `- [ ]` checkbox format
- `## Smoke Test` with verification steps
- `## Constraints` including no-stub requirement, 500-line limit, no git ops
- `## Repository Details` section with instance_id, repo, base_commit

### 4. Self-Contained Sample JSON

The sample.json includes all fields needed for both spec generation and later evaluation:
- instance_id
- repo
- base_commit
- problem_statement (full text)
- hints_text
- version
- difficulty
- created_at

### 5. Comprehensive Test Suite

Created 12 integration tests in `tests/integration/test_swebench_runner.py`:
- test_sample_writes_valid_json
- test_sample_respects_count
- test_sample_seed_determinism
- test_sample_filters_by_repo
- test_generate_produces_correct_number_of_specs
- test_generated_spec_has_required_sections
- test_generated_spec_contains_problem_statement
- test_generate_creates_patches_directory
- test_list_repos_prints_repo_names
- test_sample_handles_empty_filter_gracefully
- test_generate_skips_if_spec_exists
- test_sample_json_schema_matches_expected

All tests pass.

## Verification

### Smoke Tests Executed

```bash
# Smoke test 1: Sample 3 tasks with seed 42
python _tools/swebench_runner.py sample --count 3 --seed 42
# Result: Created .deia/benchmark/swebench/sample.json with 3 tasks

# Smoke test 2: Generate specs
python _tools/swebench_runner.py generate
# Result: Created 3 SPEC files in .deia/benchmark/swebench/specs/

# Smoke test 3: List repositories
python _tools/swebench_runner.py list-repos
# Result: Printed 12 repositories with task counts:
#   django/django: 231 tasks
#   sympy/sympy: 75 tasks
#   sphinx-doc/sphinx: 44 tasks
#   ... (9 more repos)
#   Total: 12 repositories, 500 tasks
```

### Test Suite Results

```
============================= 12 passed in 55.49s =============================
```

### Generated Spec Sample

Verified that generated specs follow gate 0 format. Example: `SPEC-SWE-django-django-11734.md` contains all required sections, uses checkbox format for acceptance criteria, includes full problem statement, and specifies absolute paths for patch output.

## Acceptance Criteria Status

- [x] `_tools/swebench_runner.py` exists with three subcommands: `sample`, `generate`, `list-repos`
- [x] `sample` subcommand downloads SWE-bench Verified, selects N tasks, filters by repo/difficulty, writes to sample.json
- [x] `generate` subcommand reads sample.json, produces one SPEC per task with problem_statement, creates patches/ directory
- [x] Generated specs pass gate 0 format requirements
- [x] Generated spec objective includes full problem_statement text
- [x] Generated spec acceptance criteria include: patch file exists, valid unified diff, applies cleanly
- [x] Generated spec constraints include: no simdecisions repo modification, work in temp clone, no file over 500 lines, produce only diff
- [x] `list-repos` subcommand prints all unique repos with task counts
- [x] `sample` writes JSON with all required fields
- [x] `sample --count 5 --seed 42` produces deterministic output
- [x] `.deia/benchmark/swebench/` directory structure created
- [x] Tests in `tests/integration/test_swebench_runner.py` with 12+ tests
- [x] All tests pass via `pytest tests/integration/test_swebench_runner.py -v`

## Constraints Compliance

- [x] No file over 500 lines (swebench_runner.py: 401 lines, test file: 238 lines)
- [x] No stubs — every function complete
- [x] No git operations
- [x] Uses `datasets` package (already installed)
- [x] Does NOT import `swebench.harness` modules (avoided Windows compatibility issue)
- [x] Generated specs do NOT reference external files in "Files to Read First"
- [x] Sampled JSON is self-contained
- [x] TDD: tests written first, then implementation

## Notes

1. **Dataset Source**: Uses HuggingFace datasets (`princeton-nlp/SWE-bench_Verified`, split=test) which contains 500 verified tasks across 12 repositories

2. **Deterministic Sampling**: Using `--seed` parameter ensures reproducible sampling for benchmarking consistency

3. **Windows Compatibility**: Avoided importing `swebench.harness` modules which fail on Windows due to `import resource` (Unix-only). Only uses `datasets.load_dataset` for data access.

4. **Gate 0 Compliance**: All generated specs follow `.deia/hive/queue/SUBMISSION-CHECKLIST.md` requirements and will pass gate 0 validation

5. **Self-Contained Design**: The sample.json includes all fields needed for later evaluation step (SPEC-SWE-002), enabling complete pipeline execution without re-downloading dataset

6. **Extensibility**: The sampler supports filtering by repo and difficulty, enabling targeted sampling for specific benchmark scenarios

## Next Steps (Not In Scope)

This completes the first half of the SWE-bench pipeline (task selection and spec generation). The evaluation harness (SPEC-SWE-002) will:
- Execute the generated patches against SWE-bench test suites
- Collect pass/fail results
- Compute aggregate metrics
- Compare baseline vs SimDecisions tracks
