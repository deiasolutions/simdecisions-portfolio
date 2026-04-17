# TASK-143: Port PHASE-IR CLI module with modularization

## Objective
Port the PHASE-IR CLI from platform repo to shiftcenter, splitting the 578-line file into two modules (cli.py + cli_commands.py) to comply with the 500-line limit, and create the __main__.py entry point.

## Context
The platform repo contains a fully-functional CLI at `../platform/efemera/src/efemera/phase_ir/cli.py` (578 lines) with 13 subcommands. All PHASE-IR dependencies (primitives, schema, validation, expressions, node_types, pie, bpmn_compiler, mermaid, formalism) were ported on 2026-03-14 and all 248 tests pass.

The CLI provides:
1. `phase init` - Create PIE scaffold
2. `phase validate` - Validate flow (syntax/semantic/mode/governance)
3. `phase lint` - Validate with governance level
4. `phase export` - Export to mermaid/bpmn/json/yaml
5. `phase compile` - BPMN XML → PHASE-IR JSON
6. `phase decompile` - PHASE-IR → BPMN XML
7. `phase pack` - Pack PIE dir to .pie.zip
8. `phase unpack` - Unpack .pie.zip
9. `phase inspect` - Show flow summary
10. `phase rules` - List validation rules
11. `phase node-types` - List node types
12. `phase eval` - Evaluate expression
13. `phase formalism` - Show formalism mapping

The 578-line CLI exceeds the 500-line limit and must be split into:
- **cli.py** (~135 lines): argparse setup, main(), dispatch table, exit codes, color helpers, file I/O helpers
- **cli_commands.py** (~443 lines): All 13 cmd_* handler functions

All imports must change from relative (`.schema`) to absolute (`engine.phase_ir.schema`).

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\cli.py` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\phase_ir\__main__.py` (source)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__init__.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\schema.py` (verify imports available)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\validation.py` (verify VALIDATION_RULES)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\expressions\__init__.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\node_types.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\pie.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\bpmn_compiler.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\mermaid.py` (verify exports)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\formalism.py` (verify exports)

## Deliverables
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli.py` created (~135 lines)
  - Exit codes (EXIT_OK, EXIT_ERROR, EXIT_VALIDATION_FAIL)
  - Color helpers (_supports_color, _color, _green, _yellow, _red, _bold)
  - File I/O helpers (_load_flow_from_file, _read_text)
  - Argparse setup (_build_parser with all 13 subcommands)
  - Dispatch table (_DISPATCH dict)
  - main() function
  - Imports cli_commands.cmd_* functions
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\cli_commands.py` created (~443 lines)
  - All 13 cmd_* functions moved here
  - Imports from engine.phase_ir.* (absolute paths)
  - Imports file I/O helpers from .cli
- [ ] `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\engine\phase_ir\__main__.py` created (4 lines)
  - Import and call cli.main()
- [ ] All relative imports (`.schema`, `.primitives`, etc.) converted to absolute (`engine.phase_ir.schema`, etc.)
- [ ] No file exceeds 500 lines
- [ ] All 13 subcommands functional (will be tested in TASK-144)

## Module Split Strategy

### cli.py contains:
```python
# Exit codes
EXIT_OK = 0
EXIT_ERROR = 1
EXIT_VALIDATION_FAIL = 2

# Color helpers (6 functions: _supports_color, _color, _green, _yellow, _red, _bold)
# File I/O helpers (2 functions: _load_flow_from_file, _read_text)
# Argparse setup (_build_parser function ~80 lines)
# Dispatch table (_DISPATCH dict)
# main() function

# Import all command handlers from cli_commands
from engine.phase_ir.cli_commands import (
    cmd_init, cmd_validate, cmd_lint, cmd_export,
    cmd_compile, cmd_decompile, cmd_pack, cmd_unpack,
    cmd_inspect, cmd_rules, cmd_node_types, cmd_eval, cmd_formalism
)
```

### cli_commands.py contains:
```python
# All 13 cmd_* functions
# Import dependencies from engine.phase_ir modules
# Import file I/O and exit codes from .cli
```

## Test Requirements
Tests will be written in TASK-144. This task focuses on the port and modularization only. However:
- [ ] Run `python -m engine.phase_ir --help` to verify entry point works
- [ ] Verify all 13 subcommands appear in help output
- [ ] Verify no import errors when running `python -c "from engine.phase_ir import cli"`

## Constraints
- No file over 500 lines (cli.py ~135, cli_commands.py ~443)
- All imports must be absolute (`engine.phase_ir.*`)
- No stubs - every function fully ported
- Preserve all ANSI color helpers (terminal output feature)
- Preserve all argparse help text exactly as in source
- CSS: var(--sd-*) only (N/A - this is Python CLI)

## Import Mapping (Relative → Absolute)

Source (platform):
```python
from .primitives import Flow
from .schema import dict_to_flow, flow_to_dict, ...
from .validation import VALIDATION_RULES, validate_flow
from .expressions import parse_expression, evaluate, validate_expression
from .node_types import get_node_type, list_node_types
from .pie import create_pie_scaffold, pack_pie, unpack_pie, validate_pie
from .bpmn_compiler import compile_bpmn, decompile_to_bpmn
from .mermaid import export_mermaid
from .formalism import get_all_mappings, explain_mapping
```

Target (shiftcenter):
```python
from engine.phase_ir.primitives import Flow
from engine.phase_ir.schema import dict_to_flow, flow_to_dict, ...
from engine.phase_ir.validation import VALIDATION_RULES, validate_flow
from engine.phase_ir.expressions import parse_expression, evaluate, validate_expression
from engine.phase_ir.node_types import get_node_type, list_node_types
from engine.phase_ir.pie import create_pie_scaffold, pack_pie, unpack_pie, validate_pie
from engine.phase_ir.bpmn_compiler import compile_bpmn, decompile_to_bpmn
from engine.phase_ir.mermaid import export_mermaid
from engine.phase_ir.formalism import get_all_mappings, explain_mapping
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-143-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — manual verification of entry point and help output
5. **Build Verification** — no import errors, help works
6. **Acceptance Criteria** — copy from above, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
