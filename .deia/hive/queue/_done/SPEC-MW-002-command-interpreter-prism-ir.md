# SPEC: Command-Interpreter PRISM-IR Emission

## Priority
P1

## Depends On
MW-001

## Objective
Add PRISM-IR emission to the command-interpreter so that parsed commands can be serialized into PRISM Intermediate Representation format for execution by the PRISM runtime.

## Context
MW-001 built the core parser. Now we need to convert ParseResult objects into PRISM-IR format that the execution engine can consume. PRISM-IR is a JSON-serializable format that represents:
- Command intent (action + target)
- Parameters and arguments
- Context metadata (confidence, alternatives)
- Execution hints (confirmation required, user-facing messages)

The emitter should be a separate module that takes ParseResult and produces PRISM-IR dict/JSON.

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/shell/command_interpreter.py` — ParseResult structure (from MW-001)
- Search for existing PRISM-IR examples in codebase (if any)

## Acceptance Criteria
- [ ] `PRISMEmitter` class in `hivenode/shell/prism_emitter.py`
- [ ] `emit(parse_result: ParseResult) -> dict` method that converts to PRISM-IR format
- [ ] PRISM-IR schema includes: `action`, `target`, `parameters`, `confidence`, `metadata`
- [ ] Support for execution modes: `auto`, `confirm`, `disambiguate` based on confidence
- [ ] Metadata includes: `original_input`, `alternatives`, `confidence_score`
- [ ] JSON-serializable output (all values are str/int/float/bool/list/dict, no custom objects)
- [ ] Validation: emitted IR must be valid according to PRISM-IR schema
- [ ] Error handling: invalid ParseResult raises `EmissionError` with clear message
- [ ] Unit tests: 10+ tests covering emission of exact match, fuzzy match, ambiguous commands
- [ ] Integration test: parse → emit → serialize to JSON → deserialize → validate

## Smoke Test
- [ ] Parse "open terminal" → emit → `{"action": "open", "target": "terminal", "mode": "auto", "confidence": 0.95}`
- [ ] Parse "opn terminal" → emit → `{"action": "open", "target": "terminal", "mode": "confirm", "confidence": 0.78, "metadata": {"typo_corrected": true}}`
- [ ] Parse "open" (ambiguous) → emit → `{"mode": "disambiguate", "alternatives": [...], "confidence": 0.5}`
- [ ] Emit result serializes to valid JSON with no exceptions
- [ ] Run `pytest hivenode/shell/tests/test_prism_emitter.py` — all tests pass

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/shell/prism_emitter.py` (new file)
- Location: `hivenode/shell/tests/test_prism_emitter.py` (new file)
- TDD: Write tests first
- No external dependencies beyond stdlib (`json`, `dataclasses`)
- Max 300 lines for prism_emitter.py
- Max 150 lines for tests
- NO STUBS — full implementation of emission and validation
- PRISM-IR schema must be documented in module docstring
- All emitted dicts must pass `json.dumps()` without errors
