# TASK-145: Smoke test PHASE-IR CLI entry point

## Objective
Verify the PHASE-IR CLI entry point works correctly, all 13 subcommands are listed in help, and no regressions occurred in the existing phase_ir test suite.

## Context
TASK-143 ported the CLI (cli.py + cli_commands.py + __main__.py).
TASK-144 wrote comprehensive tests for all 13 subcommands.

This task verifies the integration:
1. `python -m engine.phase_ir --help` works
2. All 13 subcommands appear in help output
3. Existing 248 phase_ir tests still pass (no regressions)

## Dependencies (Must Complete First)
- **TASK-143** (CLI port) must be COMPLETE
- **TASK-144** (CLI tests) must be COMPLETE

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__main__.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli_commands.py`

## Deliverables
- [ ] Verify `python -m engine.phase_ir --help` runs without errors
- [ ] Verify all 13 subcommands listed in help output:
  - init
  - validate
  - lint
  - export
  - compile
  - decompile
  - pack
  - unpack
  - inspect
  - rules
  - node-types
  - eval
  - formalism
- [ ] Run full phase_ir test suite: `python -m pytest tests/engine/phase_ir/ -v`
- [ ] Verify test count matches expected: 248 (prior) + ~40-50 (CLI tests) = ~288-298 tests
- [ ] Zero test failures
- [ ] No import errors

## Test Commands

```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter

# Test entry point
python -m engine.phase_ir --help

# Verify each subcommand help works
python -m engine.phase_ir init --help
python -m engine.phase_ir validate --help
python -m engine.phase_ir lint --help
python -m engine.phase_ir export --help
python -m engine.phase_ir compile --help
python -m engine.phase_ir decompile --help
python -m engine.phase_ir pack --help
python -m engine.phase_ir unpack --help
python -m engine.phase_ir inspect --help
python -m engine.phase_ir rules --help
python -m engine.phase_ir node-types --help
python -m engine.phase_ir eval --help
python -m engine.phase_ir formalism --help

# Run all phase_ir tests
python -m pytest tests/engine/phase_ir/ -v --tb=short

# Run just CLI tests
python -m pytest tests/engine/phase_ir/test_cli.py tests/engine/phase_ir/test_cli_commands.py -v
```

## Acceptance Criteria
- [ ] `python -m engine.phase_ir --help` outputs help text with all 13 subcommands
- [ ] Each subcommand `--help` works (13 commands)
- [ ] All phase_ir tests pass (248 existing + ~40-50 new = ~288-298 total)
- [ ] No import errors
- [ ] No regressions (existing 248 tests still pass)

## Constraints
- No code changes allowed (this is verification only)
- If failures found, document them in response file for follow-up task
- CSS: var(--sd-*) only (N/A - this is Python)

## What to Do If Tests Fail

If any test fails or `--help` doesn't work:
1. Document the exact error in response file
2. Mark status as FAILED
3. List all failures in "Issues / Follow-ups" section
4. Do NOT attempt to fix (report back to Q33N for new task)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-145-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — None (verification only) OR list fixes if issues found
3. **What Was Done** — commands run, output verified
4. **Test Results** — full pytest output, pass/fail counts
5. **Build Verification** — help output, subcommand list
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — any failures, regressions, edge cases

DO NOT skip any section.
