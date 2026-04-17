# SPEC-EXP-TREATMENT-B-Q33N-SWARM

**Spec ID:** SPEC-EXP-TREATMENT-B-Q33N-SWARM
**Created:** 2026-04-09
**Author:** Q88N + Mr. AI
**Type:** BUILD
**Status:** READY
**Experiment:** HIVE-VS-OPUS-001 / Treatment B

---

## Priority

P1

## Depends On

None

## Model Assignment

sonnet

## Purpose

**Experiment Treatment B** — Q33N (Sonnet) coordinates a swarm of Sonnet bees to build the same deliverable as Treatment A. This tests whether coordination overhead is worth it vs a single high-capability model.

**Deliverable:** A Python module that parses spec files and extracts structured metadata — identical target to Treatment A.

---

## Read First

- `.deia/hive/queue/backlog/` — example spec files to understand format
- `.deia/hive/scripts/queue/gate0.py` — current spec validation logic

---

## Build Target

Create `hivenode/spec_parser/parser.py` (~150 lines) that:

1. Reads a markdown spec file from disk
2. Extracts YAML-style frontmatter fields: `Spec ID`, `Priority`, `Model Assignment`, `Depends On`, `Status`
3. Extracts `## Acceptance Criteria` section and parses `- [ ]` checkboxes into a list
4. Returns a dataclass `ParsedSpec` with all extracted fields
5. Raises `SpecParseError` on malformed input (no frontmatter, missing required fields)

Also create `tests/test_spec_parser.py` (~100 lines) with:
- Test for valid spec with all fields
- Test for spec missing Priority (should raise)
- Test for spec with no acceptance criteria (should return empty list)
- Test for spec with mixed checkbox states `- [x]` and `- [ ]`

---

## Q33N Instructions

You are the coordinator. Do NOT write code yourself. Your job:

1. **Read the spec and codebase** — understand the target
2. **Decompose into bee tasks** — split into 2-3 task files:
   - TASK-B-01: `ParsedSpec` dataclass + `SpecParseError` exception (~30 lines)
   - TASK-B-02: `parse_spec()` function with frontmatter extraction (~80 lines)
   - TASK-B-03: Test suite + integration verification (~100 lines)
3. **Dispatch bees** — use `dispatch.py` to launch all tasks
4. **Review results** — verify each bee's output, request fixes if needed
5. **Integrate** — ensure all pieces work together, run final `pytest`
6. **Report** — file response with metrics

Bees are Sonnet. You may dispatch 2-3 in parallel.

---

## Acceptance Criteria

- [ ] `hivenode/spec_parser/__init__.py` exists and exports `ParsedSpec`, `parse_spec`, `SpecParseError`
- [ ] `hivenode/spec_parser/parser.py` is < 200 lines
- [ ] `ParsedSpec` dataclass has fields: `spec_id`, `priority`, `model`, `depends_on`, `status`, `acceptance_criteria`
- [ ] `parse_spec(path: Path) -> ParsedSpec` works on any valid spec file
- [ ] `tests/test_spec_parser.py` has 4+ test cases
- [ ] All tests pass: `pytest tests/test_spec_parser.py -v`
- [ ] No stubs — all functions fully implemented
- [ ] TDD: tests written before implementation

---

## Smoke Test

```bash
pytest tests/test_spec_parser.py -v
# All tests should pass
python -c "from hivenode.spec_parser import parse_spec; print('import OK')"
```

---

## Constraints

- Q33N coordinates, bees execute — Q33N does NOT write code
- Bees: Sonnet only
- Max 4 hours wall clock (including coordination overhead)
- Commit message prefix: `[EXP-B-SWARM]`

---

## Experiment Metadata

```yaml
experiment_id: HIVE-VS-OPUS-001
treatment: B
treatment_name: q33n-swarm
model: sonnet
coordination: q33n
bee_count: 2-3
run_number: 1
```

---

## Response File

`.deia/hive/responses/20260409-EXP-B-Q33N-SWARM-RESPONSE.md`

Report at end:
- CLOCK: wall time in minutes (total, including coordination)
- COIN: estimated cost in USD (Q33N + all bees)
- CARBON: estimated CO2e in grams
- Files created (with line counts)
- Test results (pass/fail counts)
- Bee dispatch count
- Coordination overhead (Q33N tokens used)

---

*SPEC-EXP-TREATMENT-B-Q33N-SWARM — 2026-04-09*
