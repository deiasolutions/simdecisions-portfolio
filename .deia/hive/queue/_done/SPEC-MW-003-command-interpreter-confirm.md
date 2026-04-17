# SPEC: Command-Interpreter Confirmation + Ambiguity Resolution

## Priority
P1

## Depends On
MW-002

## Objective
Build the confirmation and ambiguity resolution logic for the command-interpreter. This handles medium-confidence commands (0.7-0.9) that require user confirmation and low-confidence commands (<0.7) that need disambiguation.

## Context
MW-001 built the parser, MW-002 added PRISM-IR emission. Now we need the interactive flows:
- **Confirmation flow**: Show "Did you mean X?" for medium-confidence matches
- **Disambiguation flow**: Show picker with alternatives for low-confidence matches
- **Auto-execute flow**: Direct execution for high-confidence matches

This task adds the state machine and confirmation handlers. The UI components will be built in Phase 2 (MW-006, MW-007).

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/command_interpreter.py` — ParseResult with confidence thresholds
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/prism_emitter.py` — PRISM-IR execution modes

## Acceptance Criteria
- [ ] `ConfirmationHandler` class in `hivenode/shell/confirmation_handler.py`
- [ ] `resolve(parse_result: ParseResult, user_choice: Optional[str]) -> Resolution` method
- [ ] `Resolution` dataclass with: `action` (execute/cancel/choose), `final_command`, `ir_output`
- [ ] State machine: PENDING → (AUTO_EXECUTE | CONFIRM | DISAMBIGUATE) → RESOLVED
- [ ] Auto-execute: confidence >0.9 → immediately return execution Resolution
- [ ] Confirm: confidence 0.7-0.9 → return confirmation prompt, await user yes/no
- [ ] Disambiguate: confidence <0.7 → return alternatives list, await user selection
- [ ] User can cancel at any point → return cancel Resolution
- [ ] Integration with PRISM-IR emitter for final command execution
- [ ] Unit tests: 12+ tests covering all state transitions and edge cases
- [ ] Edge case: user selects "none of the above" in disambiguate flow

## Smoke Test
- [ ] Parse "open terminal" (0.95) → auto-execute → `Resolution(action="execute", final_command="open-terminal")`
- [ ] Parse "opn terminal" (0.78) → confirm → user says yes → `Resolution(action="execute", final_command="open-terminal")`
- [ ] Parse "opn terminal" (0.78) → confirm → user says no → `Resolution(action="cancel")`
- [ ] Parse "open" (0.5) → disambiguate → user selects "open-file" → `Resolution(action="execute", final_command="open-file")`
- [ ] Run `pytest hivenode/shell/tests/test_confirmation_handler.py` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/shell/confirmation_handler.py` (new file)
- Location: `hivenode/shell/tests/test_confirmation_handler.py` (new file)
- TDD: Write tests first
- No external dependencies beyond stdlib
- Max 350 lines for confirmation_handler.py
- Max 200 lines for tests
- NO STUBS — full state machine implementation
- Must support async user input (callbacks, not blocking)
- Clear error messages for invalid user choices
