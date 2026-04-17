# BRIEFING: SPEC-EXP-TREATMENT-B-Q33N-SWARM

**To:** Q33N (Coordinator)
**From:** Q88NR
**Date:** 2026-04-09
**Spec:** `.deia/hive/queue/_active/SPEC-EXP-TREATMENT-B-Q33N-SWARM.md`
**Priority:** P1
**Type:** Experiment - Treatment B (Q33N Swarm)

---

## Mission

You are coordinating **Treatment B** of experiment HIVE-VS-OPUS-001. Your job is to coordinate a swarm of Sonnet bees to build a spec parser module.

**DO NOT write code yourself.** You coordinate bees who write code.

---

## Deliverable

Build `hivenode/spec_parser/parser.py` with:

1. `ParsedSpec` dataclass with fields: `spec_id`, `priority`, `model`, `depends_on`, `status`, `acceptance_criteria`
2. `SpecParseError` exception class
3. `parse_spec(path: Path) -> ParsedSpec` function that:
   - Reads markdown spec file
   - Extracts frontmatter fields (Spec ID, Priority, Model Assignment, Depends On, Status)
   - Parses `## Acceptance Criteria` section for `- [ ]` checkboxes
   - Raises `SpecParseError` on malformed input

Plus `tests/test_spec_parser.py` with 4+ test cases.

---

## Your Coordination Tasks

1. **Decompose into 2-3 bee tasks:**
   - TASK-B-01: Dataclass + exception (~30 lines)
   - TASK-B-02: Parse function (~80 lines)
   - TASK-B-03: Test suite (~100 lines)

2. **Dispatch bees** using `dispatch.py` (Sonnet model, 2-3 bees in parallel if possible)

3. **Review results** - verify each bee completed their task correctly

4. **Integration** - ensure all pieces work together, run `pytest tests/test_spec_parser.py -v`

5. **Report** to response file with experiment metrics

---

## Acceptance Criteria (from spec)

- [ ] `hivenode/spec_parser/__init__.py` exists and exports `ParsedSpec`, `parse_spec`, `SpecParseError`
- [ ] `hivenode/spec_parser/parser.py` is < 200 lines
- [ ] `ParsedSpec` dataclass has required fields
- [ ] `parse_spec(path: Path) -> ParsedSpec` works on valid spec files
- [ ] `tests/test_spec_parser.py` has 4+ test cases
- [ ] All tests pass: `pytest tests/test_spec_parser.py -v`
- [ ] No stubs — all functions fully implemented
- [ ] TDD: tests written before implementation

---

## Smoke Test

```bash
pytest tests/test_spec_parser.py -v
python -c "from hivenode.spec_parser import parse_spec; print('import OK')"
```

---

## Context Files

- `.deia/hive/queue/backlog/` — example spec files to understand format
- `.deia/hive/scripts/queue/gate0.py` — current spec validation logic

---

## Constraints

- You coordinate, you do NOT code
- Bees: Sonnet model only
- Max 4 hours wall clock
- Commit message prefix: `[EXP-B-SWARM]`
- Max 2-3 bees in parallel (cost control)

---

## Response File

`.deia/hive/responses/20260409-EXP-B-Q33N-SWARM-RESPONSE.md`

Include experiment metrics:
- **CLOCK:** Total wall time in minutes (including coordination overhead)
- **COIN:** Total cost in USD (your coordination + all bee dispatches)
- **CARBON:** Estimated CO2e in grams
- **Files created:** With line counts
- **Test results:** Pass/fail counts
- **Bee count:** How many bees dispatched
- **Coordination overhead:** Your token usage

---

## Notes

This is an **experiment**. The deliverable is identical to Treatment A (single Opus). The question is: does Q33N coordination add value or just overhead?

Execute your coordination role exactly as designed. Report accurate metrics.

**Proceed when ready.**
