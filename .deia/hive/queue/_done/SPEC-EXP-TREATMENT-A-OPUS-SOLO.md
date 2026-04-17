# SPEC-EXP-TREATMENT-A-OPUS-SOLO

**Spec ID:** SPEC-EXP-TREATMENT-A-OPUS-SOLO
**Created:** 2026-04-09
**Author:** Q88N + Mr. AI
**Type:** BUILD
**Status:** READY
**Experiment:** HIVE-VS-OPUS-001 / Treatment A

---

## Priority

P1

## Depends On

None

## Model Assignment

opus

## Purpose

**Experiment Treatment A** — Single Opus bee builds a small, well-defined deliverable without Q33N coordination. This is one side of an A/B comparison; Treatment B uses Q33N+Sonnet swarm for the same deliverable.

**Deliverable:** A Python module that parses spec files and extracts structured metadata.

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

- Single bee, single session — no sub-agents, no Q33N coordination
- Model: Opus only
- Max 4 hours wall clock
- Commit message prefix: `[EXP-A-OPUS]`

---

## Experiment Metadata

```yaml
experiment_id: HIVE-VS-OPUS-001
treatment: A
treatment_name: opus-solo
model: opus
coordination: none
run_number: 1
```

---

## Response File

`.deia/hive/responses/20260409-EXP-A-OPUS-SOLO-RESPONSE.md`

Report at end:
- CLOCK: wall time in minutes
- COIN: estimated cost in USD
- CARBON: estimated CO2e in grams
- Files created (with line counts)
- Test results (pass/fail counts)

---

*SPEC-EXP-TREATMENT-A-OPUS-SOLO — 2026-04-09*
