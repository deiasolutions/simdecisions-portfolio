# SPEC: IR Density — Batch Scoring + Gate 0 Integration

## Priority
P1

## Depends On
IRD-01

## Objective
Add batch scoring and Gate 0 density check to `_tools/ir_density.py`. Batch scores all specs in a directory. Gate check returns pass/fail exit code for dispatch integration.

## Context
After IRD-01 created the core scorer, this task adds:
1. `batch` command — score all matching files in a directory, output table
2. `gate-check` command — pass/fail check for dispatch pipeline
3. Gate 0 hook — add density as 6th validation step in `gate0.py`

Plan doc: `.deia/hive/coordination/2026-04-06-PLAN-IR-DENSITY-IMPLEMENTATION.md`

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/_tools/ir_density.py` — core scorer (IRD-01 created this)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/scripts/queue/gate0.py` — Gate 0 validation (add 6th check)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/coordination/2026-04-06-PLAN-IR-DENSITY-IMPLEMENTATION.md` — full plan with CLI output formats

## CLI Design

```bash
# Batch score directory
python _tools/ir_density.py batch .deia/hive/queue/backlog/
python _tools/ir_density.py batch .deia/hive/queue/backlog/ --format json
python _tools/ir_density.py batch .deia/hive/queue/backlog/ --format csv

# Gate check (exit code 0 = pass, 1 = fail)
python _tools/ir_density.py gate-check SPEC-MW-011.md --min-density 0.4
python _tools/ir_density.py gate-check loan.prism.md --min-ird 10
```

## Batch Output Format

```
IR Density Report (spec mode)
═══════════════════════════════════════════════════════════════
File                          Instr   Ref    Clarity  Composite
───────────────────────────────────────────────────────────────
SPEC-MW-011-mobile-nav.md     0.81    0.68   0.86     0.78 ████████
SPEC-MW-012-tree-browser.md   0.65    0.72   0.71     0.69 ███████
SPEC-MW-014-terminal.md       0.18    0.12   0.43     0.24 ██ WEAK
───────────────────────────────────────────────────────────────
Average: 0.54    Min: 0.24    Max: 0.78
```

## Gate 0 Integration

Add `check_ir_density()` as 6th check in `gate0.py`:
- Warn if density < 0.4 (spec mode) or IRD < 10 (prism mode)
- Block if density < 0.2 (spec mode) or IRD < 5 (prism mode)
- Thresholds are initial estimates — configurable via function params
- Returns CheckResult (same pattern as existing 5 checks)

## Acceptance Criteria
- [ ] `batch <dir>` scores all SPEC-*.md and TASK-*.md files, outputs table
- [ ] `batch --format json` outputs JSON array
- [ ] `batch --format csv` outputs CSV
- [ ] `gate-check <file> --min-density 0.4` returns exit code 0 (pass) or 1 (fail)
- [ ] `gate-check <file> --min-ird 10` works for prism mode
- [ ] Gate 0 calls density check as 6th validation step
- [ ] Warn if density < 0.4 (spec) or IRD < 10 (prism)
- [ ] Block if density < 0.2 (spec) or IRD < 5 (prism)
- [ ] Thresholds configurable via flags (--min-density, --min-ird)
- [ ] Batch handles empty directories gracefully
- [ ] Batch handles mixed file types (skips non-matching files)
- [ ] 8+ tests covering batch, gate-check, Gate 0 hook
- [ ] All tests pass: `python -m pytest _tools/tests/test_ir_density.py -v`

## Smoke Test
- [ ] `python _tools/ir_density.py batch .deia/hive/queue/backlog/` — shows table of all specs
- [ ] `python _tools/ir_density.py batch .deia/hive/queue/backlog/ --format json` — valid JSON output
- [ ] `python _tools/ir_density.py gate-check .deia/hive/queue/backlog/SPEC-MW-011-mobile-nav-hub.md --min-density 0.4` — exit code 0

## Model Assignment
sonnet

## Constraints
- No changes to existing spec file format
- Thresholds are soft defaults, configurable via function params and CLI flags
- No file over 500 lines
- No stubs — all functions fully implemented
- TDD: tests first
- Response file: `.deia/hive/responses/20260406-TASK-IRD-02-RESPONSE.md`
