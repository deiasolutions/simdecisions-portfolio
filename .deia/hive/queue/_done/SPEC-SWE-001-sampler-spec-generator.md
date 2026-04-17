# SPEC-SWE-001-sampler-spec-generator: SWE-bench Task Sampler and Factory Spec Generator

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Build `_tools/swebench_runner.py` — a CLI that downloads SWE-bench Verified tasks from HuggingFace, samples N tasks, and generates factory-compatible SPEC files that tell bees to produce patches. Each generated spec gives a bee the problem statement, repo, base commit, and instructions to write a unified diff. This is the first half of the SWE-bench pipeline: task selection and spec generation. Evaluation is a separate spec.

## Files to Read First

- _tools/benchmark.py
- _tools/benchmark_preflight.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md
- .deia/config/benchmarks.yml

## Acceptance Criteria

- [ ] `_tools/swebench_runner.py` exists with three subcommands: `sample`, `generate`, `list-repos`
- [ ] `sample` subcommand downloads SWE-bench Verified (`princeton-nlp/SWE-bench_Verified`, split=test) via `datasets.load_dataset`, selects N tasks (default 50, configurable via `--count`), optionally filters by repo (`--repo`), difficulty (`--difficulty`), and random seed (`--seed`), writes sampled tasks to `.deia/benchmark/swebench/sample.json`
- [ ] `generate` subcommand reads `.deia/benchmark/swebench/sample.json`, produces one SPEC-*.md file per task in `.deia/benchmark/swebench/specs/`, each spec tells the bee to clone the repo at base_commit, read the problem statement, and write a unified diff to `.deia/benchmark/swebench/patches/{instance_id}.diff`
- [ ] Generated specs pass gate 0 format requirements: have `## Priority` (P2), `## Depends On` (None), `## Model Assignment` (sonnet), `## Objective`, `## Acceptance Criteria` (with `- [ ]` checkboxes), `## Smoke Test`, `## Constraints`
- [ ] Generated spec objective includes the full `problem_statement` text from the SWE-bench task so the bee has complete context without needing external access
- [ ] Generated spec acceptance criteria include: patch file exists, patch is valid unified diff, patch applies cleanly to repo at base_commit
- [ ] Generated spec constraints include: do not modify any files in the simdecisions repo, work in a temporary clone, no file over 500 lines, produce only the diff file
- [ ] `list-repos` subcommand prints all unique repos in SWE-bench Verified with task counts per repo
- [ ] `sample` writes a JSON file with fields: instance_id, repo, base_commit, problem_statement, hints_text, version, difficulty, created_at for each sampled task
- [ ] `sample --count 5 --seed 42` produces deterministic output (same 5 tasks every time)
- [ ] `.deia/benchmark/swebench/` directory structure created: `sample.json`, `specs/`, `patches/`, `results/`
- [ ] Tests in `tests/integration/test_swebench_runner.py` with 12+ tests covering: sample writes valid JSON, sample respects --count, sample respects --seed determinism, sample filters by --repo, generate produces correct number of specs, generated spec has all required sections, generated spec contains problem_statement, generate creates patches directory, list-repos prints repo names, sample handles empty filter gracefully, generate skips if spec already exists, sample.json schema matches expected fields
- [ ] All tests pass via `pytest tests/integration/test_swebench_runner.py -v`

## Smoke Test

- [ ] `python _tools/swebench_runner.py sample --count 3 --seed 42` produces `.deia/benchmark/swebench/sample.json` with exactly 3 tasks
- [ ] `python _tools/swebench_runner.py generate` produces 3 SPEC files in `.deia/benchmark/swebench/specs/`
- [ ] `python _tools/swebench_runner.py list-repos` prints repo list with counts

## Constraints

- No file over 500 lines
- No stubs — every function complete
- No git operations (no commits, no pushes)
- Use `datasets` package to load from HuggingFace (already installed)
- Do NOT import `swebench.harness` modules — they use `import resource` which fails on Windows. Only use `datasets.load_dataset` for data access
- Generated specs must NOT reference files outside the simdecisions repo in their `## Files to Read First` section (use inline problem_statement instead)
- Sampled task JSON must be self-contained — include all fields the evaluation step will need later
- TDD: write tests first, then implementation

## Files to Modify

- _tools/swebench_runner.py (create)
- tests/integration/test_swebench_runner.py (create)
- .deia/benchmark/swebench/ (create directory structure)
