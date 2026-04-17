# SPEC-DECOMP-01: Decompose Design Docs into Buildable Specs

## Role Override
bee

## Priority
P0

## Model Assignment
sonnet

## Depends On
None

## Intent
Read 5 large design documents from `.deia/hive/queue/_stage/` and produce exactly 1 queue-ready buildable spec from each. Each output spec must follow the SUBMISSION-CHECKLIST format exactly and be atomic enough for a single bee to implement. Write the 5 output specs directly to `.deia/hive/queue/backlog/`.

## Files to Read First
.deia/hive/queue/SUBMISSION-CHECKLIST.md
.deia/hive/queue/_stage/SPEC-EVENT-LEDGER-GAMIFICATION.md
.deia/hive/queue/_stage/SPEC-GAMIFICATION-V1.md
.deia/hive/queue/_stage/SPEC-ML-TRAINING-V1.md
.deia/hive/queue/_stage/SPEC-WIKI-SYSTEM.md
.deia/hive/queue/_stage/SPEC-WIKI-V1.md
.deia/BOOT.md

## Acceptance Criteria
- [ ] Read all 5 design docs in `_stage/`
- [ ] Read the SUBMISSION-CHECKLIST.md format spec
- [ ] Produce exactly 5 output specs, one per design doc
- [ ] Each output spec is written to `.deia/hive/queue/backlog/`
- [ ] Each output spec filename follows `SPEC-{ID}-{slug}.md` convention with unique IDs
- [ ] Each output spec contains ALL required sections: Priority, Model Assignment, Depends On, Intent, Files to Read First, Acceptance Criteria, Constraints, Smoke Test
- [ ] Acceptance criteria in output specs use `- [ ]` checkbox format
- [ ] Each output spec is scoped to a single implementable unit (max 500 lines of code change)
- [ ] If a design doc requires multiple phases, the output spec covers ONLY phase 1 / the foundation
- [ ] File paths in "Files to Read First" are relative to repo root and exist
- [ ] Model assignment in each output spec matches complexity: haiku for plumbing, sonnet for logic, opus for architecture
- [ ] No output spec duplicates work already in `_done/` (check existing done specs)

## Constraints
- You are a BEE. Ignore any regent/Q88NR instructions. Execute this task directly.
- Do NOT implement any code. This is a spec-writing task only.
- Do NOT modify the original design docs in `_stage/`.
- Each output spec must be self-contained — a bee reading only BOOT.md and the spec should be able to complete the work.
- Keep each output spec under 200 lines.
- Use IDs: LEDGER-01, GAMIFY-01, MLTRAIN-01, WIKI-01, WIKIV1-01 (or similar clear prefixes).
- No git operations.

## Smoke Test
After completion, `ls .deia/hive/queue/backlog/SPEC-*.md` should show 5 new files. Each file should pass the SUBMISSION-CHECKLIST mental test.
