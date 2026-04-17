# SPEC-BENCH-WAVE-B-DECOMPOSE: Decompose Wave B into Factory Specs

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Read the benchmark suite master spec and the Wave A codebase, then produce 4 factory-ready SPEC files for Wave B (PRISM-bench native benchmark). Drop the output specs directly into `.deia/hive/queue/backlog/`. Each output spec must conform to `.deia/hive/queue/SUBMISSION-CHECKLIST.md` and pass Gate 0.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- .deia/hive/queue/SUBMISSION-CHECKLIST.md
- .deia/skills/internal/spec-writer/SKILL.md
- simdecisions/benchmark/adapter.py
- simdecisions/benchmark/adapters/prism_bench.py
- simdecisions/benchmark/runner.py
- simdecisions/benchmark/executor.py
- simdecisions/benchmark/collector.py
- simdecisions/benchmark/publisher.py
- simdecisions/benchmark/types.py
- simdecisions/benchmark/significance.py
- simdecisions/benchmark/metrics.py
- simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json
- simdecisions/des/core.py
- simdecisions/des/engine.py

## Wave B Tasks to Decompose

The master spec (Section 7, Wave B) defines these tasks. **Renumber to avoid collision with BENCH-006 (already used for Wave A integration).**

| New ID | Original Spec ID | Description | Model |
|--------|-----------------|-------------|-------|
| BENCH-007 | BENCH-006 | Design 20 PRISM-bench tasks across 5 categories | opus |
| BENCH-008 | BENCH-007 | Evaluation harness: per-category scoring, partial credit, recovery measurement | sonnet |
| BENCH-009 | BENCH-008 | PRISM-bench adapter: replace placeholders with real DES execution | sonnet |
| BENCH-010 | BENCH-009 | End-to-end: run PRISM-bench, publish results, verify reproducibility | haiku |

### Category definitions (from spec Section 2.2)

| Category | Task Type | Evaluation |
|----------|-----------|------------|
| Multi-step workflow | PRISM-IR workflows with 5-20 steps, branching, resource contention | Completion accuracy, cost efficiency, variance |
| Recovery | Workflows with injected failures at known points | Recovery rate, recovery cost, time to recover |
| Multi-agent coordination | Workflows requiring 2+ agents with handoffs | Coordination overhead, error at handoff points |
| Branch comparison | Workflows with multiple valid strategies | Did simulation pick the better branch? Measured by outcome + cost |
| Governance overhead | Same workflow with and without GateEnforcer | Accuracy preserved? Cost of governance layer quantified |

### Dependency chain

```
BENCH-007 (tasks)  ──┐
                     ├──> BENCH-009 (adapter wiring)  ──> BENCH-010 (e2e)
BENCH-008 (harness) ──┘
```

### Wave B exit criteria (from master spec)

PRISM-bench runs, produces published results, two consecutive runs show statistical consistency. Repository structure matches Section 4.1.

## Output Spec Requirements

Each output SPEC file MUST:

1. **Follow the SUBMISSION-CHECKLIST format** — read `.deia/hive/queue/SUBMISSION-CHECKLIST.md` and the spec-writer skill at `.deia/skills/internal/spec-writer/SKILL.md` before writing
2. **Use YAML frontmatter** with `id`, `priority`, `model`, `role`, `depends_on` fields
3. **Have `## Acceptance Criteria`** with `- [ ]` checkbox items (minimum 8 per spec)
4. **Have `## Smoke Test`** with `- [ ]` checkbox items
5. **Have `## Files to Read First`** with existing file paths the bee needs
6. **Have `## Constraints`** including: no file over 500 lines, no stubs, no git ops, TDD
7. **Maintain IR density >= 0.200** — use tables, checklists, concrete file paths, code blocks
8. **Reference concrete files** — every deliverable must name the exact file path to create/modify
9. **Set `role: bee`** in frontmatter
10. **Set correct `depends_on`** per the dependency chain above

### YAML frontmatter template for each output spec

```yaml
---
id: BENCH-NNN
priority: P1
model: <opus|sonnet|haiku>
role: bee
depends_on: [<list of BENCH-NNN IDs>]
---
```

### Key context for each spec

**BENCH-007 (20 tasks, opus):**
- Output: 20 JSON workflow files in `simdecisions/benchmark/prism_bench_tasks/` (separate from the 5 test workflows in `test_workflows/`)
- Each must be valid PRISM-IR: `id`, `nodes`, `edges`, optional `resources`
- 4 tasks per category (multi-step, recovery, multi-agent, branch comparison, governance overhead)
- Each task has `metadata.category`, `metadata.evaluation_criteria`, `metadata.expected_runtime`
- Recovery tasks must include `metadata.failure_injection` describing where/how failures are injected
- Branch comparison tasks must include `metadata.strategies` listing the valid approaches
- Governance tasks must include paired variants: with and without GateEnforcer
- Include a README.md documenting all 20 tasks
- Tests: validation test file loading all 20 and checking schema
- Depends on: nothing

**BENCH-008 (harness, sonnet):**
- Output: `simdecisions/benchmark/harness.py` with `PRISMBenchHarness` class
- Per-category scoring functions matching the evaluation table above
- Partial credit scoring (not just pass/fail)
- Recovery measurement: count injected failures vs recovered
- Branch comparison scoring: did the chosen strategy produce better outcome + cost?
- Governance overhead measurement: delta in accuracy and cost between governed/ungoverned
- Uses `significance.py` (Mann-Whitney U) and `metrics.py` (CV, recovery rate) already built
- Tests: minimum 20 tests covering all 5 categories
- Depends on: nothing (can be built in parallel with BENCH-007)

**BENCH-009 (adapter wiring, sonnet):**
- Modify: `simdecisions/benchmark/adapters/prism_bench.py` — replace placeholder returns with real DES execution
- `load_tasks()`: load from `prism_bench_tasks/` (the 20 real tasks, not test_workflows)
- `run_baseline()`: execute workflow directly (raw model, no simulation)
- `run_simdecisions()`: execute through `SimulationEngine` from `simdecisions/des/engine.py`
- `evaluate()`: call `PRISMBenchHarness` from BENCH-008
- Must handle DES statistics collection (wired in DES-STATS-WIRING-001)
- Tests: integration tests that run a simple workflow through both tracks
- Depends on: BENCH-007, BENCH-008

**BENCH-010 (e2e, haiku):**
- Run `python _tools/benchmark.py run prism-bench --trials 2` end-to-end
- Verify results written to `.deia/benchmark/results/`
- Verify statistics computed by `collector.py`
- Verify summary published by `publisher.py`
- Run twice and compare: statistical consistency (same task, two runs, results within expected variance)
- Tests: integration test that runs the full pipeline
- Depends on: BENCH-009

## Acceptance Criteria

- [ ] File `backlog/SPEC-BENCH-007-prism-bench-tasks.md` exists with YAML frontmatter, >= 8 acceptance criteria items, and `depends_on: []`
- [ ] File `backlog/SPEC-BENCH-008-evaluation-harness.md` exists with YAML frontmatter, >= 8 acceptance criteria items, and `depends_on: []`
- [ ] File `backlog/SPEC-BENCH-009-adapter-wiring.md` exists with YAML frontmatter, >= 8 acceptance criteria items, and `depends_on: [BENCH-007, BENCH-008]`
- [ ] File `backlog/SPEC-BENCH-010-e2e-validation.md` exists with YAML frontmatter, >= 8 acceptance criteria items, and `depends_on: [BENCH-009]`
- [ ] All 4 specs have `## Priority` section with P1
- [ ] All 4 specs have `## Acceptance Criteria` with `- [ ]` checkbox items
- [ ] All 4 specs have `## Smoke Test` with `- [ ]` checkbox items
- [ ] All 4 specs have `## Files to Read First` with valid paths
- [ ] All 4 specs have `## Constraints` section
- [ ] All 4 specs reference `docs/specs/SPEC-BENCHMARK-SUITE-001.md` as context
- [ ] No spec exceeds 500 lines
- [ ] All file paths in `## Files to Read First` exist on disk

## Smoke Test

- [ ] `ls .deia/hive/queue/backlog/SPEC-BENCH-00{7,8,9}-*.md .deia/hive/queue/backlog/SPEC-BENCH-010-*.md` lists exactly 4 files
- [ ] Each file starts with `---` (YAML frontmatter)
- [ ] `grep -c '\- \[ \]' .deia/hive/queue/backlog/SPEC-BENCH-007-*.md` returns >= 8

## Constraints

- No code changes — this task only writes SPEC markdown files
- No git operations
- Output specs go to `.deia/hive/queue/backlog/` only
- Each spec must be self-contained: a bee with only BOOT.md context can execute it
- Do not reuse IDs BENCH-001 through BENCH-006 (already used in Wave A)
