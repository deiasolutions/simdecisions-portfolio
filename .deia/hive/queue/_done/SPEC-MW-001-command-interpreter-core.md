# SPEC: Command-Interpreter Core Parser + Fuzzy Matching

## Priority
P1

## Depends On
MW-T01

## Objective
Build the core command-interpreter parser with fuzzy matching engine that converts natural language input into parsed command objects with confidence scoring. This is the foundation for all Mobile Workdesk voice/text command routing.

## Context
The command-interpreter is the critical bridge between user input (voice or text) and PRISM-IR execution. It must:
- Parse natural language strings into structured command objects
- Handle fuzzy matching with typo tolerance (e.g., "opn terminal" → "open terminal")
- Score confidence to determine auto-execute vs confirm vs disambiguate flows
- Support parameterized commands with argument extraction
- Be extensible for adding new command vocabularies

This task implements the core parsing engine. Subsequent tasks will add PRISM-IR emission (MW-002) and confirmation flows (MW-003).

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/command-palette/fuzzyMatch.ts` — existing fuzzy match implementation for reference
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py` — task registry context

## Acceptance Criteria
- [ ] `CommandInterpreter` class in `hivenode/shell/command_interpreter.py`
- [ ] `parse(input: str) -> ParseResult` method that returns structured result
- [ ] `ParseResult` dataclass with fields: `command`, `arguments`, `confidence`, `alternatives`, `requires_confirmation`
- [ ] Fuzzy matching using `difflib.SequenceMatcher` for Levenshtein-style matching
- [ ] Command dictionary loaded from `hivenode/shell/commands.yml` (YAML format)
- [ ] Initial command vocabulary: 30+ core commands (open, close, navigate, execute, search, toggle, create, delete, show, hide, etc.)
- [ ] Confidence thresholds: >0.9 auto-execute, 0.7-0.9 confirmation required, <0.7 show alternatives
- [ ] Parameter extraction: "open file README.md" → { command: "open", target: "file", param: "README.md" }
- [ ] Multi-word command support: "create new terminal" → { command: "create-new-terminal" }
- [ ] Case-insensitive matching with original case preserved in params
- [ ] Unit tests: 15+ tests covering exact match, fuzzy match, typos, ambiguity, parameter extraction
- [ ] All tests pass with 100% coverage of core parse logic

## Smoke Test
- [ ] Parse "open terminal" → `ParseResult(command="open-terminal", confidence=0.95, requires_confirmation=False)`
- [ ] Parse "opn terminal" (typo) → `ParseResult(command="open-terminal", confidence=0.78, requires_confirmation=True)`
- [ ] Parse "open file test.py" → `ParseResult(command="open-file", arguments={"filename": "test.py"}, confidence=0.92)`
- [ ] Parse "open" (ambiguous) → `ParseResult(confidence=0.5, alternatives=["open-file", "open-folder", "open-terminal"])`
- [ ] Run `pytest hivenode/shell/tests/test_command_interpreter.py` — all 15+ tests pass

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/shell/command_interpreter.py` (new file)
- Location: `hivenode/shell/commands.yml` (new file for command dictionary)
- Location: `hivenode/shell/tests/test_command_interpreter.py` (new file)
- TDD: Write tests first, then implement parser
- No external dependencies beyond stdlib (`difflib`, `dataclasses`, `yaml`)
- Max 400 lines for command_interpreter.py
- Max 200 lines for tests
- NO STUBS — full implementation of fuzzy matching and parameter extraction
- Commands.yml must be structured, not flat list: categories, parameters, aliases
- All string matching case-insensitive, but preserve original case in extracted params
