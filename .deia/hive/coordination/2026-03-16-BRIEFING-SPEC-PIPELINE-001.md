# BRIEFING: SPEC-PIPELINE-001 — Unified Build Pipeline

**To:** Q33N (Queen Coordinator)
**From:** Q88NR (Regent)
**Date:** 2026-03-16
**Spec ID:** SPEC-PIPELINE-001
**Priority:** P1

---

## Mission

Break down **SPEC-PIPELINE-001: Unified Build Pipeline** into task files for bee execution.

The spec defines a unified build pipeline with:
- One pipeline, two runtimes (filesystem production mode + in-memory DES simulation mode)
- PipelineStore protocol with two implementations
- Directory state machine with manifests and triage
- PHASE-IR encoding of the entire pipeline
- Event Ledger integration for all stages

---

## Spec Location

**Primary spec:** `.deia/hive/queue/_done/2026-03-16-2030-SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE.md`

---

## Build Plan (from Section 8)

The spec provides a 4-wave build plan:

### Wave 1 (no dependencies)
- **W1-A:** PipelineStore interface + FilesystemPipelineStore (~130 lines, Haiku)
- **W1-B:** Validation ledger events schema + emission (~40 lines, Haiku)

### Wave 2 (depends on W1-A)
- **W2-A:** Directory state machine transitions (~110 lines, Sonnet)
- **W2-B:** InMemoryPipelineStore (~60 lines, Haiku)

### Wave 3 (depends on W2-A + W2-B)
- **W3-A:** PHASE-IR flow encoding of build pipeline (~200 lines IR JSON, Sonnet)
- **W3-B:** LLM triage functions (3 integration points, ~100 lines, Sonnet)

### Wave 4 (depends on W3-A)
- **W4-A:** DES runner for build pipeline (~120 lines, Sonnet)

---

## Your Task

Create **7 task files** (one per build plan task: W1-A, W1-B, W2-A, W2-B, W3-A, W3-B, W4-A).

For each task file:

1. **Follow the task template** from HIVE.md
2. **Include all success criteria** from Section 10 of the spec (as applicable to that task)
3. **Specify absolute file paths** (Rule 8)
4. **Reference the spec's detailed descriptions** in Sections 6 (PipelineStore), 4 (Directory State Machine), 7 (DES Model), 5 (LLM Triage)
5. **Include test requirements:**
   - W1-A: ~15 tests (store interface + filesystem implementation)
   - W1-B: ~5 tests (ledger event emission)
   - W2-A: ~15 tests (transitions, crash recovery, failure log)
   - W2-B: ~10 tests (in-memory store mirrors filesystem tests)
   - W3-A: ~5 tests (IR load, validate structure)
   - W3-B: ~10 tests (3 triage functions × scenarios)
   - W4-A: ~5 tests (simulation runs, returns expected metrics)
6. **Enforce no stubs** (Rule 6) — every function must be fully implemented
7. **CSS rule does NOT apply** (this is backend Python only)
8. **500-line modularization** (Rule 4) — if any file approaches 500 lines, split it

---

## Dependency Chain

Ensure task files reflect these dependencies:

```
W1-A, W1-B (parallel, no deps)
  ↓
W2-A, W2-B (depend on W1-A)
  ↓
W3-A, W3-B (depend on W2-A + W2-B)
  ↓
W4-A (depends on W3-A)
```

Use `## Depends On` section in task files.

---

## Key Patterns to Enforce

From the spec:

1. **PipelineStore is an ABC** (Section 6.1) — two implementations share same interface
2. **All stages emit to Event Ledger** (Section 3.1) — no exceptions
3. **Manifests append to spec files** (Section 4.6) — not separate files
4. **Triage uses Haiku** (Section 5.4) unless crash recovery needs Sonnet (Open Question 2)
5. **Tests use pytest** — existing queue runner test patterns in `tests/.deia/hive/scripts/queue/`

---

## Open Questions (DO NOT BLOCK ON THESE)

The spec lists 5 open questions for Q88N (Section 11). These are for AFTER implementation, to tune parameters based on data. Proceed with defaults:

1. Fidelity threshold: **0.85** (as specified)
2. Triage model: **Haiku** for all three points (cost control)
3. `_needs_review/` timeout: **24 hours** (as specified)
4. DES endpoint: **Part of existing Railway backend** (add to hivenode/routes/)
5. PROCESS-0020 naming: **"Unified Build Pipeline"** (as specified)

---

## Mechanical Review Checklist

When you submit task files, I (Q88NR) will verify:

- [ ] Deliverables match spec acceptance criteria (Section 10)
- [ ] File paths are absolute
- [ ] Test requirements present (counts + scenarios)
- [ ] CSS rule N/A (backend only)
- [ ] No file over 500 lines (split if needed)
- [ ] No stubs or TODOs
- [ ] Response file template included in each task

---

## Timeline Expectation

This is a **P1 spec** (current wave). After your task files are approved, bees will execute in wave order:
- Wave 1: 2 bees in parallel
- Wave 2: 2 bees in parallel (after W1 completes)
- Wave 3: 2 bees in parallel (after W2 completes)
- Wave 4: 1 bee (after W3 completes)

Estimated total: **2–3 overnight queue runs** (per spec Section 8).

---

## Deliverable

Write 7 task files to `.deia/hive/tasks/`:

- `2026-03-16-TASK-W1-A-PIPELINE-STORE-PROTOCOL.md`
- `2026-03-16-TASK-W1-B-VALIDATION-LEDGER-EVENTS.md`
- `2026-03-16-TASK-W2-A-DIRECTORY-STATE-MACHINE.md`
- `2026-03-16-TASK-W2-B-INMEMORY-PIPELINE-STORE.md`
- `2026-03-16-TASK-W3-A-PHASE-IR-FLOW-ENCODING.md`
- `2026-03-16-TASK-W3-B-LLM-TRIAGE-FUNCTIONS.md`
- `2026-03-16-TASK-W4-A-DES-PIPELINE-RUNNER.md`

When done, report back to me (Q88NR) for review.

---

**End of Briefing.**
