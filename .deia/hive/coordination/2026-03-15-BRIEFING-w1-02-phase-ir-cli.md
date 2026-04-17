# BRIEFING: Port PHASE-IR CLI toolchain (13 subcommands)

**Date:** 2026-03-15
**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-15-0753-SPE)
**To:** Q33N
**Model Assignment:** Sonnet
**Priority:** P0.10

---

## Objective

Port the PHASE-IR CLI from the platform repo to shiftcenter. The CLI provides 13 subcommands for flow management, validation, compilation, and analysis.

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\cli.py` (578 lines)
**Target:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py`

---

## Context from Spec

The original spec (`.deia/hive/queue/2026-03-15-0753-SPEC-w1-02-phase-ir-cli.md`) states:
- Port CLI with all 13 subcommands
- Port domain vocabulary YAMLs to `engine/phase_ir/vocabularies/`
- `python -m engine.phase_ir --help` should work
- Tests for CLI commands required

**FINDING:** After examination of the platform repo, there is NO `vocabularies/` directory in `platform/efemera/src/efemera/phase_ir/`. The CLI code does NOT reference any vocabulary files. The spec's mention of "domain vocabulary YAMLs" appears to be incorrect or refers to something not yet implemented in platform.

**DECISION:** Port the CLI as-is. Do NOT create a vocabularies directory unless Q33N finds evidence in the codebase that it exists and is referenced.

---

## Source Files to Port

1. **CLI Module:** `../platform/efemera/src/efemera/phase_ir/cli.py` (578 lines)
2. **Main Entry Point:** `../platform/efemera/src/efemera/phase_ir/__main__.py` (4 lines)

---

## CLI Commands (13 subcommands)

From the source code, the CLI provides these commands:

1. `phase init <name>` — Create a new PIE scaffold directory
2. `phase validate <file>` — Validate a flow file (syntax/semantic/mode/governance)
3. `phase lint <file>` — Validate with governance level (alias for validate --level=governance)
4. `phase export <file> --format mermaid|bpmn|json|yaml` — Export flow to different format
5. `phase compile <bpmn_file>` — Compile BPMN XML to PHASE-IR JSON
6. `phase decompile <file>` — Decompile PHASE-IR to BPMN XML
7. `phase pack <dir>` — Pack a PIE directory into .pie.zip
8. `phase unpack <file> <dir>` — Unpack a .pie.zip archive
9. `phase inspect <file>` — Show flow summary (nodes, edges, groups, resources)
10. `phase rules` — List all validation rules
11. `phase node-types` — List all registered node types
12. `phase eval <expression>` — Evaluate a PHASE-IR expression
13. `phase formalism --target petri|bpmn|csp|des` — Show formalism mapping

---

## Dependencies Already in Shiftcenter

The following imports are used by the CLI and should already exist in `engine/phase_ir/`:

- `primitives.Flow` ✓ exists
- `schema` module (dict_to_flow, flow_to_dict, flow_to_json, etc.) ✓ exists
- `validation` module (VALIDATION_RULES, validate_flow) ✓ exists
- `expressions` module (parse_expression, evaluate, validate_expression) ✓ exists
- `node_types` module (get_node_type, list_node_types) ✓ exists
- `pie` module (create_pie_scaffold, pack_pie, unpack_pie, validate_pie) ✓ exists
- `bpmn_compiler` module (compile_bpmn, decompile_to_bpmn) ✓ exists
- `mermaid` module (export_mermaid) ✓ exists
- `formalism` module (get_all_mappings, explain_mapping) ✓ exists

All dependencies already ported in PHASE-IR port (completed 2026-03-14).

---

## Import Path Changes

The CLI imports from `.primitives`, `.schema`, etc. (relative imports).

In shiftcenter, these become `from engine.phase_ir.primitives import Flow`, etc.

Q33N should verify all imports resolve correctly.

---

## Entry Point

The CLI should be invocable via:
```bash
python -m engine.phase_ir
```

This requires `engine/phase_ir/__main__.py` to exist and call `cli.main()`.

---

## Task Breakdown Guidance

Q33N should write task files that cover:

1. **TASK: Port CLI module**
   - Copy `cli.py` to `engine/phase_ir/cli.py`
   - Update all imports from relative (`.schema`) to absolute (`engine.phase_ir.schema`)
   - Create `engine/phase_ir/__main__.py` entry point
   - Verify no file exceeds 500 lines (current: 578 lines — EXCEEDS LIMIT)
   - **MODULARIZATION REQUIRED:** Split into `cli.py` (argparse setup + main) and `cli_commands.py` (all cmd_* functions)

2. **TASK: Write CLI tests**
   - Test each of the 13 subcommands
   - Test file I/O helpers (_load_flow_from_file, _read_text)
   - Test error handling (file not found, parse errors, validation failures)
   - Test exit codes (EXIT_OK, EXIT_ERROR, EXIT_VALIDATION_FAIL)
   - Test color output (ANSI codes)
   - Use pytest with tmp_path fixtures for file-based tests
   - Target: `tests/engine/phase_ir/test_cli.py` + `test_cli_commands.py`

3. **TASK: Smoke test**
   - Verify `python -m engine.phase_ir --help` works
   - Verify all 13 subcommands listed in help
   - Verify no regressions in existing phase_ir tests

---

## Constraints (from spec + BOOT.md)

- **No file over 500 lines.** Current CLI is 578 lines — MUST modularize.
- **TDD:** Tests first, then implementation.
- **No stubs.** Every function fully implemented.
- **Response file:** All 8 sections mandatory.
- **Heartbeats:** POST to `http://localhost:8420/build/heartbeat` every 3 minutes.

---

## Acceptance Criteria (from spec)

- [ ] CLI module ported with all 13 subcommands
- [ ] `python -m engine.phase_ir --help` works
- [ ] Tests for CLI commands written and passing
- [ ] All files under 500 lines
- [ ] No new test failures in existing phase_ir tests

---

## File Locations

| Artifact | Path |
|----------|------|
| Source CLI | `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\cli.py` |
| Source __main__ | `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\__main__.py` |
| Target CLI | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py` |
| Target CLI commands | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli_commands.py` |
| Target __main__ | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__main__.py` |
| Test files | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli.py` |
| | `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli_commands.py` |

---

## Q33N Action Items

1. Read the source files listed above.
2. Verify all dependencies exist in `engine/phase_ir/`.
3. Write task files for:
   - CLI port + modularization (split into cli.py + cli_commands.py)
   - CLI tests (comprehensive coverage of all 13 subcommands)
   - Smoke test verification
4. Return task files to Q33NR for review.
5. DO NOT dispatch bees until Q33NR approves.

---

## Notes

- The platform repo is at `C:\Users\davee\OneDrive\Documents\GitHub\platform\` (parent directory of shiftcenter).
- PHASE-IR core modules were ported on 2026-03-14. All 248 tests pass.
- No vocabularies directory exists in platform — ignore that part of the spec.
- The CLI uses argparse (not click or typer).
- ANSI color helpers are included in CLI — keep them for terminal output.

---

**END BRIEFING**
