# SPEC: IR Density — Core Scorer (Dual-Mode)

## Priority
P1

## Depends On
None

## Objective
Create `_tools/ir_density.py` with dual-mode scoring (spec + prism). Pure static analysis, no LLM calls, no external dependencies.

## Context
IR Density measures how much actionable instruction a spec/task file contains relative to its size. Two modes:
1. **spec mode** — scores SPEC-*.md, TASK-*.md, IMPL-*.md files (acceptance criteria, file paths, code blocks)
2. **prism mode** — scores PRISM-IR process definitions (nodes, actions, guards, SLAs)

Plan doc: `.deia/hive/coordination/2026-04-06-PLAN-IR-DENSITY-IMPLEMENTATION.md`
Briefing: `.deia/hive/coordination/2026-04-06-BRIEFING-IR-DENSITY-MEASUREMENT.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/coordination/2026-04-06-PLAN-IR-DENSITY-IMPLEMENTATION.md` — full plan with algorithm code, CLI design, benchmarks
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/scripts/queue/spec_parser.py` — existing section parsing
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/inventory.py` — CLI pattern (argparse, subcommands)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/scripts/queue/gate0.py` — Gate 0 validation pattern

## Algorithm (spec mode)

```python
instruction_density = (acceptance_criteria + deliverables + smoke_tests) / total_lines
reference_density = (file_paths + code_block_lines) / total_lines
constraint_clarity = sections_present / expected_sections  # 7 expected

ir_density_spec = 0.40 * instruction_density + 0.30 * reference_density + 0.30 * constraint_clarity
```

Expected sections: Priority, Depends On, Model Assignment, Objective, Acceptance Criteria, Smoke Test, Constraints.

Executable elements to count:
- `- [ ]` or `- [x]` checkboxes (acceptance criteria)
- Bullet points under `## Deliverables`
- Code blocks or bullets under `## Smoke Test`
- File path pattern matches (`/path/to/file.py`, `src/...`, `C:/...`)
- Fenced code block count and lines inside them
- Bullets under `## Constraints`

## Algorithm (prism mode)

```python
def estimate_tokens(text: str) -> int:
    return len(text) // 4  # chars/4 approximation, no external deps

def calculate_ird_prism(text: str) -> dict:
    tokens = estimate_tokens(text)
    kilotokens = tokens / 1000
    elements = count_prism_elements(text)  # weighted sum
    ird = elements / kilotokens if kilotokens > 0 else 0
    return {"tokens": tokens, "kilotokens": kilotokens, "elements": elements, "ird": ird, "rating": get_ird_rating(ird)}
```

PRISM elements (weight 1.0): nodes, actions, conditions/guards, SLAs, resources, timings, events, generators, join policies, constraints. (weight 0.5): entity attrs, lifecycle states.

Ratings: <10/kt verbose, 10-20 acceptable, 20-30 efficient, >30 optimal.

## Mode Detection

```python
def detect_doc_type(text: str) -> str:
    if re.search(r'^v:\s*["\']?\d', text, re.MULTILINE) and ('nodes:' in text or 'Process:' in text or 'flow:' in text):
        return "prism"
    if '## Acceptance Criteria' in text or '## Smoke Test' in text or '## Objective' in text:
        return "spec"
    return "unknown"
```

## Acceptance Criteria
- [ ] `detect_doc_type(text)` returns "spec" | "prism" | "unknown"
- [ ] `score_spec(text)` returns dict with instruction_density, reference_density, constraint_clarity, composite
- [ ] `score_prism(text)` returns dict with tokens, kilotokens, elements, ird, rating
- [ ] `score(text)` auto-detects mode and delegates
- [ ] CLI: `ir_density.py score <file>` works for both types
- [ ] CLI: `--mode spec|prism` forces mode
- [ ] Validate on 5+ real spec files from `.deia/hive/queue/backlog/`
- [ ] No LLM calls — pure static analysis
- [ ] Token estimation via chars/4 (no external dependencies)
- [ ] Benchmarks match plan: spec <0.2 Poor, 0.2-0.4 Weak, 0.4-0.6 Acceptable, 0.6-0.8 Good, >0.8 Excellent
- [ ] 10+ tests covering both modes, edge cases
- [ ] All tests pass: `python -m pytest _tools/tests/test_ir_density.py -v`

## Smoke Test
- [ ] `python _tools/ir_density.py score .deia/hive/queue/backlog/SPEC-MW-011-mobile-nav-hub.md` — outputs mode: spec, composite: 0.XX
- [ ] `python _tools/ir_density.py score .deia/hive/queue/backlog/SPEC-MW-011-mobile-nav-hub.md --mode spec` — forced mode works
- [ ] `python _tools/ir_density.py score --help` — shows usage

## Model Assignment
sonnet

## Constraints
- Match `inventory.py` CLI pattern (argparse, subcommands)
- File < 400 lines
- TDD: tests first
- No external dependencies (no tiktoken, no numpy — use chars/4 for token estimation)
- No stubs — all functions fully implemented
- Response file: `.deia/hive/responses/20260406-TASK-IRD-01-RESPONSE.md`
