# SPEC: TEST — Command-Interpreter Coverage

## Priority
P1

## Objective
Write comprehensive test suite for the command-interpreter that validates fuzzy matching, confidence scoring, parameterized commands, and ambiguity handling with 100% coverage of parse() logic.

## Context
This is a TDD task — write tests FIRST, before implementation exists. Tests must fail initially, then pass after MW-001/MW-002/MW-003 implementation.

Test coverage must include:
- Exact match: "open terminal" → { command: "open", target: "terminal", confidence: 1.0 }
- Typo tolerance: "opn terminl" → { command: "open", target: "terminal", confidence: 0.75 }
- Ambiguous input: "open" → { alternatives: ["open-file", "open-folder", "open-app"], confidence: 0.5 }
- Parameterized commands: "search for TODO" → { command: "search", param: "TODO", confidence: 0.9 }
- Unknown command: "xyz" → { error: "Unknown command", confidence: 0.0 }
- Case insensitivity: "OPEN TERMINAL" → same as "open terminal"
- Multi-word targets: "open file browser" → { command: "open", target: "file-browser", confidence: 0.95 }

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/.deia/hive/queue/backlog/SPEC-MW-S01-command-interpreter.md` — spec to test against
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:69` — task context
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/` — shell module test patterns (if any exist)

## Acceptance Criteria
- [ ] Test file: `hivenode/shell/tests/test_command_interpreter.py` (pytest)
- [ ] 15+ test cases covering: exact match, typo, ambiguity, params, unknown, case, multi-word
- [ ] Test command dictionary loading from YAML (mock file read)
- [ ] Test confidence threshold logic: >0.9 auto, 0.7-0.9 confirm, <0.7 picker
- [ ] Test fuzzy match scoring: Levenshtein distance validation
- [ ] Test ParseResult serialization to JSON
- [ ] Test edge cases: empty input, special characters, very long input (>200 chars)
- [ ] Test error handling: missing command dict file, malformed YAML
- [ ] Tests initially FAIL (no implementation exists yet)
- [ ] Coverage report: `pytest --cov=hivenode.shell.command_interpreter --cov-report=term-missing` shows 0% (before implementation)
- [ ] All tests use pytest fixtures for command dict mocking
- [ ] No stubs in tests — real assertions with expected values

## Smoke Test
- [ ] Run `pytest hivenode/shell/tests/test_command_interpreter.py` → 15+ tests FAIL (ModuleNotFoundError or similar)
- [ ] Check test_exact_match() → asserts confidence == 1.0
- [ ] Check test_typo_tolerance() → asserts confidence between 0.7-0.9
- [ ] Check test_ambiguous() → asserts len(alternatives) >= 2
- [ ] All tests use clear docstrings explaining what they validate

## Model Assignment
sonnet

## Depends On
MW-S01

## Constraints
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/tests/test_command_interpreter.py` (new file)
- Location: `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/tests/__init__.py` (create if missing)
- TDD: tests MUST be written before implementation (they will fail initially)
- Max 250 lines for test file
- Use pytest fixtures for mocking command dictionary
- No implementation code in this task — tests only
- Tests must be runnable even if `command_interpreter.py` doesn't exist yet (import should be in test function, not module level)
