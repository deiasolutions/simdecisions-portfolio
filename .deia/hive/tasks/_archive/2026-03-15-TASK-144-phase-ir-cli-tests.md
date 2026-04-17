# TASK-144: Write comprehensive CLI tests for PHASE-IR

## Objective
Write comprehensive pytest tests for all 13 PHASE-IR CLI subcommands, covering happy paths, error cases, file I/O, validation, and exit codes.

## Context
TASK-143 ported the CLI from platform to shiftcenter, split into cli.py + cli_commands.py. All 13 subcommands are now available:
1. init, 2. validate, 3. lint, 4. export, 5. compile, 6. decompile, 7. pack, 8. unpack, 9. inspect, 10. rules, 11. node-types, 12. eval, 13. formalism

The CLI uses argparse and returns exit codes (0=OK, 1=ERROR, 2=VALIDATION_FAIL). Color output is conditional based on TTY detection.

All dependencies (schema, validation, expressions, pie, bpmn_compiler, mermaid, formalism) exist and are tested (248 tests pass from prior port).

## Dependencies (Must Complete First)
- **TASK-143** (CLI port) must be COMPLETE before starting this task.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py` (ported CLI)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli_commands.py` (command handlers)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__main__.py` (entry point)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\cli.py` (reference for expected behavior)

Look at existing test patterns:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_schema.py` (for test style)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_validation.py` (for test style)

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli.py` created
  - Test main() function
  - Test _build_parser()
  - Test file I/O helpers (_load_flow_from_file, _read_text)
  - Test color helpers (with mocked TTY)
  - Test exit codes
  - Test dispatch table
  - ~100-150 lines
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli_commands.py` created
  - Test all 13 cmd_* functions
  - Test happy paths (correct inputs)
  - Test error cases (missing files, parse errors, validation failures)
  - Test output modes (--output flag vs stdout)
  - Test format variants (JSON/YAML/BPMN/Mermaid for export)
  - ~350-450 lines
- [ ] All tests pass
- [ ] No file exceeds 500 lines
- [ ] Coverage: all 13 subcommands tested, all exit codes tested, all error paths tested

## Test Coverage Requirements

### test_cli.py (~100-150 lines)
- `test_main_no_command()` - No command given, prints help, returns EXIT_ERROR
- `test_main_unknown_command()` - Unknown command, returns EXIT_ERROR
- `test_main_valid_command()` - Valid command dispatches correctly
- `test_build_parser()` - Parser has all 13 subcommands
- `test_load_flow_from_file_json()` - Load JSON flow
- `test_load_flow_from_file_yaml()` - Load YAML flow
- `test_load_flow_from_file_not_found()` - File not found, exits
- `test_load_flow_from_file_parse_error()` - Parse error, exits
- `test_read_text()` - Read text file
- `test_read_text_not_found()` - File not found, exits
- `test_supports_color()` - TTY detection
- `test_color_helpers()` - ANSI codes when TTY=true, plain when false

### test_cli_commands.py (~350-450 lines)
Each cmd_* function needs:
- Happy path test (correct input, correct output)
- Error path test (missing file, invalid input)
- Exit code test (verify EXIT_OK, EXIT_ERROR, EXIT_VALIDATION_FAIL)

**cmd_init:**
- `test_cmd_init_default()` - Create PIE scaffold in cwd
- `test_cmd_init_with_output()` - Create in specified dir
- `test_cmd_init_with_metadata()` - Create with intent/author

**cmd_validate:**
- `test_cmd_validate_valid_flow()` - Returns EXIT_OK, prints "Valid"
- `test_cmd_validate_invalid_flow()` - Returns EXIT_VALIDATION_FAIL, prints errors
- `test_cmd_validate_levels()` - Test --level syntax/semantic/mode/governance
- `test_cmd_validate_modes()` - Test --mode sim/production

**cmd_lint:**
- `test_cmd_lint()` - Alias for validate --level=governance

**cmd_export:**
- `test_cmd_export_json()` - Export to JSON
- `test_cmd_export_yaml()` - Export to YAML
- `test_cmd_export_mermaid()` - Export to Mermaid
- `test_cmd_export_bpmn()` - Export to BPMN
- `test_cmd_export_to_file()` - --output flag writes to file
- `test_cmd_export_unknown_format()` - Returns EXIT_ERROR

**cmd_compile:**
- `test_cmd_compile()` - BPMN XML → PHASE-IR JSON
- `test_cmd_compile_error()` - Invalid BPMN, returns EXIT_ERROR

**cmd_decompile:**
- `test_cmd_decompile()` - PHASE-IR → BPMN XML
- `test_cmd_decompile_error()` - Invalid flow, returns EXIT_ERROR

**cmd_pack:**
- `test_cmd_pack()` - Pack PIE dir to .pie.zip
- `test_cmd_pack_invalid_pie()` - Validation fails, returns EXIT_VALIDATION_FAIL
- `test_cmd_pack_not_found()` - Dir not found, returns EXIT_ERROR

**cmd_unpack:**
- `test_cmd_unpack()` - Unpack .pie.zip
- `test_cmd_unpack_not_found()` - Archive not found, returns EXIT_ERROR

**cmd_inspect:**
- `test_cmd_inspect()` - Show flow summary (nodes, edges, groups, etc.)

**cmd_rules:**
- `test_cmd_rules()` - List all validation rules

**cmd_node_types:**
- `test_cmd_node_types()` - List all node types
- `test_cmd_node_types_category()` - Filter by category

**cmd_eval:**
- `test_cmd_eval()` - Evaluate expression
- `test_cmd_eval_with_context()` - --context flag
- `test_cmd_eval_parse_error()` - Invalid expression, returns EXIT_ERROR

**cmd_formalism:**
- `test_cmd_formalism_petri()` - Show Petri net mapping
- `test_cmd_formalism_bpmn()` - Show BPMN mapping
- `test_cmd_formalism_csp()` - Show CSP mapping
- `test_cmd_formalism_des()` - Show DES mapping
- `test_cmd_formalism_unknown()` - Invalid target, returns EXIT_ERROR

## Test Fixtures

Use `tmp_path` fixture for all file-based tests. Example:

```python
def test_cmd_validate_valid_flow(tmp_path):
    flow_file = tmp_path / "test.yaml"
    flow_file.write_text("""
id: test-flow
name: Test Flow
phase_ir_version: "0.3.0"
nodes:
  - id: start
    type: start
    """)

    args = argparse.Namespace(file=str(flow_file), level="semantic", mode="sim")
    result = cmd_validate(args)
    assert result == EXIT_OK
```

## Constraints
- No file over 500 lines
- TDD: tests written FIRST (CLI already ported in TASK-143, so tests verify behavior)
- No stubs
- Use pytest fixtures (tmp_path, capsys, monkeypatch)
- All tests must pass
- CSS: var(--sd-*) only (N/A - this is Python)

## Test Requirements
- [ ] All tests pass
- [ ] Test count: minimum 40 tests (13 commands × ~3 tests each + helpers)
- [ ] Edge cases: file not found, parse errors, validation failures, unknown formats
- [ ] Exit codes verified for all paths
- [ ] Color output tested with mocked TTY

## Smoke Test Commands
```bash
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter
python -m pytest tests/engine/phase_ir/test_cli.py -v
python -m pytest tests/engine/phase_ir/test_cli_commands.py -v
python -m pytest tests/engine/phase_ir/ -v  # All phase_ir tests (should still be 248 + new CLI tests)
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-144-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — pytest output (pass counts, failures)
5. **Build Verification** — full test suite still passes
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
