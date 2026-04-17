# Q33N Response: BRIEFING-w1-02-phase-ir-cli

**From:** Q33N (QUEEN-2026-03-15-BRIEFING-w1-02-phas)
**To:** Q33NR
**Date:** 2026-03-15
**Status:** TASK FILES READY FOR REVIEW

---

## Summary

I have read the briefing and analyzed the source CLI in the platform repo. I've written 3 task files to port the PHASE-IR CLI toolchain to shiftcenter.

**Key Finding:** The spec mentions "domain vocabulary YAMLs" but no `vocabularies/` directory exists in platform repo. The CLI code does NOT reference any vocabulary files. I am ignoring this part of the spec per the briefing's decision.

---

## Task Files Created

| Task ID | Title | Model | Lines | Dependency |
|---------|-------|-------|-------|------------|
| TASK-143 | Port PHASE-IR CLI module with modularization | Haiku | Port work | None |
| TASK-144 | Write comprehensive CLI tests | Haiku | Test work | TASK-143 |
| TASK-145 | Smoke test CLI entry point | Haiku | Verification | TASK-143, TASK-144 |

**File Paths:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-143-phase-ir-cli-port.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-144-phase-ir-cli-tests.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-15-TASK-145-phase-ir-cli-smoke-test.md`

---

## TASK-143: Port CLI Module (Haiku)

**Objective:** Port cli.py (578 lines) → split into cli.py (~135 lines) + cli_commands.py (~443 lines) to meet 500-line limit. Create __main__.py entry point.

**Deliverables:**
- `engine/phase_ir/cli.py` - argparse setup, dispatch, main(), color helpers, file I/O
- `engine/phase_ir/cli_commands.py` - all 13 cmd_* handler functions
- `engine/phase_ir/__main__.py` - entry point (4 lines)
- All relative imports → absolute imports (`.schema` → `engine.phase_ir.schema`)

**Key Changes:**
- Exit codes: EXIT_OK, EXIT_ERROR, EXIT_VALIDATION_FAIL
- Color helpers: _supports_color, _color, _green, _yellow, _red, _bold
- File I/O: _load_flow_from_file, _read_text
- 13 subcommands: init, validate, lint, export, compile, decompile, pack, unpack, inspect, rules, node-types, eval, formalism

**Dependencies Verified:** All imports exist in `engine/phase_ir/`:
- primitives.Flow ✓
- schema (dict_to_flow, flow_to_dict, json_to_flow, yaml_to_flow, etc.) ✓
- validation (VALIDATION_RULES, validate_flow) ✓
- expressions (parse_expression, evaluate, validate_expression) ✓
- node_types (get_node_type, list_node_types) ✓
- pie (create_pie_scaffold, pack_pie, unpack_pie, validate_pie) ✓
- bpmn_compiler (compile_bpmn, decompile_to_bpmn) ✓
- mermaid (export_mermaid) ✓
- formalism (get_all_mappings, explain_mapping) ✓

**File Split:**
- cli.py: 135 lines (exit codes, colors, I/O, argparse, dispatch, main)
- cli_commands.py: 443 lines (13 cmd_* functions)
- Total: 578 lines (same as source, just split)

---

## TASK-144: CLI Tests (Haiku)

**Objective:** Write comprehensive pytest tests for all 13 CLI subcommands.

**Deliverables:**
- `tests/engine/phase_ir/test_cli.py` (~100-150 lines) - test main, parser, helpers
- `tests/engine/phase_ir/test_cli_commands.py` (~350-450 lines) - test all 13 commands

**Coverage:**
- Happy paths: correct inputs → EXIT_OK
- Error paths: missing files, parse errors → EXIT_ERROR or EXIT_VALIDATION_FAIL
- Output modes: stdout vs --output file
- Format variants: JSON/YAML/BPMN/Mermaid
- TTY detection for color output
- All exit codes verified

**Test Count:** Minimum 40 tests (13 commands × ~3 tests each + helpers)

**Dependencies:** TASK-143 must complete first.

---

## TASK-145: Smoke Test (Haiku)

**Objective:** Verify entry point works, all 13 subcommands listed, no regressions.

**Deliverables:**
- Run `python -m engine.phase_ir --help` → verify works
- Verify all 13 subcommands appear
- Run full phase_ir test suite → 248 existing + ~40-50 new = ~288-298 total
- Zero failures

**Dependencies:** TASK-143 and TASK-144 must complete first.

**Verification Only:** No code changes. If failures found, report back to Q33N.

---

## Source Analysis

**Source File:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\cli.py`
- 578 lines (exceeds 500-line limit)
- 13 subcommands
- Uses argparse (not click/typer)
- ANSI color helpers for terminal output
- Exit codes: 0 (OK), 1 (ERROR), 2 (VALIDATION_FAIL)

**Import Dependencies:**
All 9 dependencies already ported on 2026-03-14 (248 tests pass). No new dependencies required.

**Vocabularies Directory:** Does NOT exist in platform repo. Spec mention is incorrect. Ignoring.

---

## Modularization Strategy

**Problem:** 578 lines exceeds 500-line limit.

**Solution:** Split into 2 files:

1. **cli.py** (~135 lines):
   - Exit codes (3 constants)
   - Color helpers (6 functions, ~30 lines)
   - File I/O helpers (2 functions, ~35 lines)
   - Argparse setup (1 function, ~80 lines)
   - Dispatch table (1 dict, ~15 lines)
   - main() function (~15 lines)
   - Import cmd_* from cli_commands

2. **cli_commands.py** (~443 lines):
   - All 13 cmd_* handler functions
   - Import dependencies from engine.phase_ir.*
   - Import helpers from .cli

**No Functionality Lost:** Every line ported. No stubs. Complete port.

---

## Import Path Changes

**All relative imports converted to absolute:**

| Source (platform) | Target (shiftcenter) |
|-------------------|----------------------|
| `from .primitives import Flow` | `from engine.phase_ir.primitives import Flow` |
| `from .schema import ...` | `from engine.phase_ir.schema import ...` |
| `from .validation import ...` | `from engine.phase_ir.validation import ...` |
| `from .expressions import ...` | `from engine.phase_ir.expressions import ...` |
| `from .node_types import ...` | `from engine.phase_ir.node_types import ...` |
| `from .pie import ...` | `from engine.phase_ir.pie import ...` |
| `from .bpmn_compiler import ...` | `from engine.phase_ir.bpmn_compiler import ...` |
| `from .mermaid import ...` | `from engine.phase_ir.mermaid import ...` |
| `from .formalism import ...` | `from engine.phase_ir.formalism import ...` |

---

## Acceptance Criteria (from briefing)

- [ ] CLI module ported with all 13 subcommands → TASK-143
- [ ] `python -m engine.phase_ir --help` works → TASK-145
- [ ] Tests for CLI commands written and passing → TASK-144
- [ ] All files under 500 lines → TASK-143 (cli.py 135, cli_commands.py 443)
- [ ] No new test failures in existing phase_ir tests → TASK-145

---

## Task Execution Plan

**Sequential execution required:**
1. **TASK-143** (port CLI) → Haiku
2. **TASK-144** (write tests) → Haiku (depends on TASK-143)
3. **TASK-145** (smoke test) → Haiku (depends on TASK-143, TASK-144)

**Recommended dispatch order:**
1. Dispatch TASK-143 alone, wait for completion
2. Dispatch TASK-144 alone, wait for completion
3. Dispatch TASK-145 alone, verify

**Reason:** Sequential dependencies. Cannot test what hasn't been ported yet.

---

## Estimated Scope

| Task | Complexity | Est. Lines Written | Est. Time |
|------|------------|-------------------|-----------|
| TASK-143 | Medium | ~580 lines (port) | 20-30 min |
| TASK-144 | High | ~400-600 lines (tests) | 40-60 min |
| TASK-145 | Low | 0 lines (verification) | 5-10 min |

**Total:** ~980-1180 lines of code, ~65-100 minutes of bee time.

---

## Files That Will Be Created

| File Path | Lines | Task |
|-----------|-------|------|
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py` | ~135 | TASK-143 |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli_commands.py` | ~443 | TASK-143 |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__main__.py` | 4 | TASK-143 |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli.py` | ~100-150 | TASK-144 |
| `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\engine\phase_ir\test_cli_commands.py` | ~350-450 | TASK-144 |

**Total:** 5 new files, ~1,032-1,182 lines.

---

## Risks / Edge Cases

1. **Import errors:** If any dependency export is missing in `engine/phase_ir/__init__.py`, bee will fail. Mitigation: I verified all exports exist.

2. **ANSI color codes:** CLI uses ANSI escape codes. Windows terminal may not support. Mitigation: CLI detects TTY and disables color if not supported.

3. **File path separators:** Source uses `/`, Windows uses `\`. Mitigation: Python's `os.path` handles this automatically.

4. **Test fixture setup:** CLI tests need temp files (flows, PIE dirs, BPMN XML). Mitigation: Task file specifies `tmp_path` fixture usage.

5. **Exit code testing:** pytest captures sys.exit(). Mitigation: Task file notes this, tests will use `pytest.raises(SystemExit)` or test return values directly.

---

## Open Questions

**None.** All dependencies verified. Source code is clean and well-structured. No ambiguities in porting strategy.

---

## Next Steps (Awaiting Q33NR Approval)

1. **Q33NR reviews these 3 task files.**
2. **If corrections needed:** I fix and return updated task files.
3. **If approved:** Q33NR tells me to dispatch bees.
4. **Dispatch order:**
   - TASK-143 (Haiku, port CLI)
   - Wait for TASK-143 completion
   - TASK-144 (Haiku, write tests)
   - Wait for TASK-144 completion
   - TASK-145 (Haiku, smoke test)
5. **Q33N monitors bee responses, reports results to Q33NR.**

---

## Notes

- No vocabularies directory exists in platform. Spec was incorrect. Not porting anything that doesn't exist.
- All dependencies already ported (PHASE-IR port completed 2026-03-14, 248 tests pass).
- CLI is 578 lines → split into 135 + 443 to meet 500-line limit.
- All 13 subcommands preserved exactly as in platform.
- Entry point: `python -m engine.phase_ir` will work after TASK-143.

---

**END RESPONSE**
