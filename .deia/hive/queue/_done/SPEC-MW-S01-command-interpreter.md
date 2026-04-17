# SPEC: Command-Interpreter Natural Language Parser

## Priority
P1

## Objective
Design the natural language command interpreter for the Mobile Workdesk. This is the foundation that converts user voice/text input into actionable commands with semantic matching, fuzzy matching, and confidence scoring.

## Context
The command-interpreter is a core primitive for the Mobile Workdesk that bridges natural language input to PRISM-IR execution. It must handle:
- Natural language → command disambiguation (e.g., "open terminal" vs "term" vs "show shell")
- Fuzzy matching to handle typos and variations
- Confidence scoring to handle ambiguous inputs
- Command confirmation flow for low-confidence matches

Files to read first:
- `hivenode/prism/ir.py` — PRISM-IR specification (target output format)
- `browser/src/primitives/command-palette/useCommandPalette.ts` — existing command routing pattern
- `hivenode/scheduler/scheduler_mobile_workdesk.py:57` — task context in scheduler

## Acceptance Criteria
- [ ] `CommandInterpreter` class with `parse(natural_lang: str) -> ParseResult` method
- [ ] ParseResult includes: `command_name`, `arguments`, `confidence_score`, `alternatives`
- [ ] Fuzzy matching using Levenshtein distance (can use `difflib` stdlib) for typo tolerance
- [ ] Built-in command dictionary with ~30 core commands: open, close, navigate, execute, search, toggle, etc.
- [ ] Confidence threshold logic: >0.9 auto-execute, 0.7-0.9 show confirmation, <0.7 show picker
- [ ] Support for parameterized commands: "open file _" → { command: "open", target: "file", param: "_" }
- [ ] All matching logic covered by unit tests (15+ tests)
- [ ] No hardcoded strings — all commands in external dictionary
- [ ] ParseResult serializable to JSON for PRISM-IR emission

## Smoke Test
- [ ] Parse "open terminal" → { command: "open", target: "terminal", confidence: 0.95 }
- [ ] Parse "opn terminal" (typo) → { command: "open", target: "terminal", confidence: 0.78, show_confirmation: true }
- [ ] Parse "open" (ambiguous) → { alternatives: ["open-file", "open-folder", "open-app"], confidence: 0.5 }
- [ ] 15+ unit tests pass with 100% coverage of parse() logic

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/shell/command_interpreter.py` (new file)
- No stubs — implement full fuzzy matching logic
- Command dictionary in `hivenode/shell/commands.yml` (YAML, not hardcoded)
- No dependencies beyond stdlib (difflib, json, yaml)
- Max 300 lines for interpreter class
- Max 100 lines for tests
- TDD: tests first, then implementation
