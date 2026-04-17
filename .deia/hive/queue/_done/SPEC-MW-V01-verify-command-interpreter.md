# VERIFY: Command-Interpreter Integration

## Priority
P1

## Depends On
MW-003

## Objective
Comprehensive verification of the complete command-interpreter pipeline: parse → emit → confirm/disambiguate → execute. Includes E2E tests, integration tests, edge case coverage, and performance checks.

## Context
MW-001, MW-002, MW-003 built the command-interpreter core. This task verifies the full pipeline works correctly end-to-end with real command inputs, edge cases, and error conditions.

This is a VERIFY task — focused on testing, not building new features.

Files to verify:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/command_interpreter.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/prism_emitter.py`
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/confirmation_handler.py`

## Acceptance Criteria
- [ ] E2E test: "open terminal" → parse → emit → auto-execute → valid PRISM-IR
- [ ] E2E test: "opn terminal" (typo) → parse → emit → confirm → user yes → execute
- [ ] E2E test: "open" (ambiguous) → parse → emit → disambiguate → user picks → execute
- [ ] E2E test: user cancels confirmation → no execution, clean state
- [ ] Edge case: empty input → graceful error, no crash
- [ ] Edge case: gibberish input ("qwerty zxcvb") → low confidence, show alternatives or error
- [ ] Edge case: very long input (500 chars) → handled gracefully, possibly truncated
- [ ] Edge case: special characters in params → preserved correctly in PRISM-IR
- [ ] Performance: parse 100 commands in <500ms (fast enough for real-time voice)
- [ ] Coverage: existing unit tests cover 95%+ of command-interpreter logic
- [ ] Integration test file: `hivenode/shell/tests/test_command_interpreter_e2e.py`
- [ ] All E2E tests pass

## Smoke Test
- [ ] Run `pytest hivenode/shell/tests/test_command_interpreter_e2e.py -v` — all tests pass
- [ ] Run `pytest hivenode/shell/tests/ --cov=hivenode.shell --cov-report=term` — coverage >95%
- [ ] Manual test: enter "open terminal" → receives valid PRISM-IR JSON
- [ ] Manual test: enter "asdfghjkl" → receives error or empty alternatives, no crash

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/shell/tests/test_command_interpreter_e2e.py` (new file)
- 8-12 E2E test cases covering full pipeline
- Max 300 lines for E2E tests
- Use pytest fixtures for command-interpreter setup
- NO STUBS — real implementations must be tested
- Test output: clear pass/fail messages with actual vs expected
