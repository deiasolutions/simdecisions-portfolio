# SPEC: PRISM-IR Command Vocabulary Definition

## Priority
P2

## Objective
Define the formal PRISM-IR command vocabulary for the Mobile Workdesk. PRISM-IR (Primitive Invocation Schema for Mobile IR) is the intermediate representation that bridges natural language commands to executable actions. This spec creates the JSON schema, command dictionary, and validation logic for PRISM-IR.

## Context
The command-interpreter (MW-001-003) parses natural language to structured commands, but needs a formal output schema. PRISM-IR defines the contract between the interpreter and the execution layer. Commands map to primitives (e.g., `{ "command": "open", "target": "terminal" }` → open terminal pane).

Files to read first:
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/prism/ir.py` — existing PRISM-IR infrastructure (if exists)
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/irExtractor.ts` — existing IR extraction patterns
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/browser/src/primitives/terminal/irRouting.ts` — existing IR routing
- `C:/Users/davee/OneDrive/Documents/GitHub/shiftcenter/hivenode/scheduler/scheduler_mobile_workdesk.py:156` — task context in scheduler

## Dependencies
- MW-V01 (command-interpreter must be verified before defining vocabulary)

## Acceptance Criteria
- [ ] JSON Schema file: `hivenode/prism/mobile_ir_schema.json` with formal PRISM-IR structure
- [ ] Schema defines:
  - `command: string` (required) — verb (open, close, navigate, execute, search, toggle)
  - `target: string` (optional) — object (terminal, file, pane, notification)
  - `arguments: object` (optional) — key-value params (e.g., `{ "filename": "foo.txt" }`)
  - `confidence: number` (required) — 0.0-1.0 confidence score from interpreter
  - `alternatives: array` (optional) — alternative interpretations for low-confidence commands
- [ ] Command dictionary: `hivenode/prism/mobile_commands.yml` with 30+ commands:
  - Navigation: `open`, `close`, `navigate`, `back`, `home`, `switch`
  - Execution: `execute`, `run`, `cancel`, `retry`, `pause`
  - Search: `search`, `find`, `filter`, `grep`
  - State: `toggle`, `enable`, `disable`, `show`, `hide`
  - Data: `save`, `load`, `export`, `import`, `copy`, `paste`
- [ ] Python validator: `hivenode/prism/ir_validator.py` with `validate_ir(ir: dict) -> ValidationResult`
- [ ] TypeScript validator: `browser/src/services/prism/irValidator.ts` with `validateIR(ir: object) -> boolean`
- [ ] Backend endpoint: `POST /api/prism/validate` — accepts IR, returns validation result
- [ ] Frontend hook: `useIRValidator()` — validates IR before routing to execution
- [ ] 12+ unit tests covering schema validation, edge cases (missing fields, invalid types)
- [ ] Documentation: `docs/PRISM-IR.md` with examples and schema reference

## Smoke Test
- [ ] Validate valid IR: `{ "command": "open", "target": "terminal", "confidence": 0.95 }` → passes
- [ ] Validate invalid IR: `{ "command": 123, "target": "terminal" }` → fails (command not string)
- [ ] Validate missing required field: `{ "target": "terminal" }` → fails (command required)
- [ ] Load command dictionary → 30+ commands defined
- [ ] 12+ tests pass with 100% coverage of validator logic
- [ ] Endpoint `/api/prism/validate` returns: `{ "valid": true/false, "errors": [...] }`

## Model Assignment
sonnet

## Constraints
- Location: `hivenode/prism/mobile_ir_schema.json` (new file)
- Location: `hivenode/prism/mobile_commands.yml` (new file)
- Location: `hivenode/prism/ir_validator.py` (new file)
- Location: `browser/src/services/prism/irValidator.ts` (new file)
- Location: `docs/PRISM-IR.md` (new file)
- Schema: follow JSON Schema Draft 7 spec
- Max 200 lines for Python validator
- Max 150 lines for TypeScript validator
- Max 100 lines for tests (each lang)
- TDD: tests first, then implementation
- All backend endpoints use `verify_jwt_or_local()` auth pattern
