# SPEC-AUDIT-BUILD-PROCESS-INFRA-001: Build Process Infrastructure Audit

## Priority
P0

## Depends On
None

## Model Assignment
sonnet

## Objective

Produce an evidence-based inventory of build process orchestration capabilities in the simdecisions repo. This audit feeds SPEC-BUILD-PROCESS-TEMPLATE-001 (the PRISM-IR template for our build process). Do not build anything. Do not modify anything. Report only.

## Files to Read First

- simdecisions/des/engine.py
- simdecisions/phase_ir/models.py
- simdecisions/phase_ir/validation.py
- simdecisions/des/engine.py
- hivenode/scheduler/scheduler_daemon.py
- hivenode/scheduler/dispatcher_daemon.py
- hivenode/relay/store.py
- _tools/inventory.py
- _tools/inventory_db.py
- .deia/hive/scripts/queue/run_queue.py
- .deia/hive/scripts/queue/gate0.py
- .deia/hive/scripts/queue/spec_processor.py
- .deia/hive/scripts/dispatch/dispatch.py

## Audit Sections

### 1. DES Engine Production Mode (EXEC-01 Status)

**Question:** Can the DES engine execute IR nodes in production mode (not just simulate timing)?

**Search targets:**
- `simdecisions/des/` — simulation engine core
- `simdecisions/flows/` — flow runner, node execution
- Any file containing: `execute`, `production`, `run_flow`, `run_node`, `dispatch`, `invoke`
- Look for: `LLMAdapter`, `OperatorBinding`, `HumanGate`, `PythonExecutor`

**Report as YAML block:**
```yaml
production_execution:
  can_execute_python: [true | false | partial]
  can_call_llm: [true | false | partial]
  can_emit_human_gate: [true | false | partial]
  llm_adapter_exists: [true | false]
  evidence:
    - file: "path/to/file.py"
      line_count: N
      relevant_code: "brief excerpt or function names"
  findings: "1-2 sentence summary"
```

### 2. Factory IR Flow (EXEC-02 Status)

**Question:** Does a PRISM-IR flow file exist that defines the build process?

**Search targets:**
- Any `.prism.md`, `.phase`, `.ir.json`, `.ir.yaml` file in the repo
- Files named: `factory.*`, `build-process.*`, `process-0013.*`, `build-flow.*`
- `simdecisions/phase_ir/` directory contents
- `.deia/hive/` directory for orchestration files
- `docs/specs/` directory for flow definitions

**Report as YAML block:**
```yaml
factory_flow:
  exists: [true | false]
  file_path: "path if exists"
  phases_defined: [list of phase names if exists]
  wired_to_runner: [true | false]
  evidence:
    - file: "path"
      description: "what it contains"
  findings: "1-2 sentence summary"
```

### 3. Queue Runner (EXEC-03 Status)

**Question:** What runs the factory? Is it IR-driven or procedural Python?

**Search targets:**
- `.deia/hive/scripts/queue/run_queue.py` — main queue runner
- `.deia/hive/scripts/queue/gate0.py` — pre-dispatch gate
- `.deia/hive/scripts/queue/spec_processor.py` — spec parsing
- `.deia/hive/scripts/dispatch/dispatch.py` — bee dispatch
- `hivenode/scheduler/scheduler_daemon.py` — scheduler
- `hivenode/scheduler/dispatcher_daemon.py` — dispatcher

**Report as YAML block:**
```yaml
queue_runner:
  exists: [true | false]
  type: [ir_driven | procedural_python | hybrid | none]
  reads_from: "path to queue directory"
  dispatches_to: "how bees are invoked"
  evidence:
    - file: "path"
      line_count: N
      description: "what it does"
  findings: "1-2 sentence summary"
```

### 4. Post-Build Gates

**Question:** What happens after a bee writes a response? Is there ANY post-build processing?

**Search targets:**
- `.deia/hive/scripts/queue/` — look for post-dispatch hooks
- `.deia/hive/responses/` — any code that reads response files
- `hivenode/scheduler/` — triage or post-processing daemons
- Search for: `smoke`, `test`, `verify`, `acceptance`, `hat`, `review`, `catalog`, `inventory`

**Report as YAML block:**
```yaml
post_build_gates:
  smoke_test:
    exists: [true | false]
    how: "description if exists"
  hat_gate:
    exists: [true | false]
    how: "description if exists"
  bat_gate:
    exists: [true | false]
    how: "description if exists"
  catalog_step:
    exists: [true | false]
    how: "description if exists"
  response_processing:
    any_code_reads_responses: [true | false]
    what_it_does: "description"
  evidence:
    - file: "path"
      description: "what it does"
  findings: "1-2 sentence summary of post-build state"
```

### 5. Human Gate Mechanisms

**Question:** What mechanisms exist for human-in-the-loop gates?

**Search targets:**
- `hivenode/relay/` — relay bus, efemera integration
- Search for: `efemera`, `relay`, `notification`, `human_gate`
- Search for: `smtp`, `sendgrid`, `email`, `mail`, `twilio`, `sms`
- Search for: `await_human`, `wait_for_approval`, `approval_gate`
- Webhook or callback patterns for human response

**Report as YAML block:**
```yaml
human_gates:
  efemera:
    exists: [true | false]
    wired: [true | false]
    can_send: [true | false]
    can_receive_response: [true | false]
  email:
    exists: [true | false]
    wired: [true | false]
  sms:
    exists: [true | false]
    wired: [true | false]
  other_channels: [list any others found]
  evidence:
    - file: "path"
      description: "what it does"
  findings: "1-2 sentence summary"
```

### 6. Capability Inventory Integration

**Question:** Does the build process update the capability inventory?

**Search targets:**
- `_tools/inventory.py` — CLI interface
- `_tools/inventory_db.py` — database connection
- `hivenode/inventory/store.py` — SQLAlchemy models
- Search for: `inv_features`, `catalog`, `features_delivered`, `register_feature`
- Check if any queue runner code calls inventory after build completes

**Report as YAML block:**
```yaml
capability_inventory:
  table_exists: [true | false]
  row_count: N
  auto_populated_after_build: [true | false]
  manual_only: [true | false]
  code_that_writes:
    exists: [true | false]
    file: "path if exists"
  evidence:
    - "query results or file paths"
  findings: "1-2 sentence summary"
```

### 7. PRISM-IR Spec Location

**Question:** Where is the canonical PRISM-IR spec, and is it importable by the engine?

**Search targets:**
- `simdecisions/phase_ir/` — parser, validator, schema
- `docs/specs/` — spec documents referencing PRISM-IR
- Search for: `PRISM`, `phase_ir`, `PhaseIR`, `prism_ir`

**Report as YAML block:**
```yaml
prism_ir:
  spec_location: "path"
  parser_exists: [true | false]
  parser_location: "path if exists"
  validator_exists: [true | false]
  validator_location: "path if exists"
  findings: "1-2 sentence summary"
```

## Acceptance Criteria

- [ ] All 7 audit sections answered with evidence (file paths, line numbers, or code excerpts)
- [ ] Every YAML block is valid, copy-pasteable YAML
- [ ] Executive summary clearly states: can we run an IR-driven build process today? yes/no/partial
- [ ] Blocking issues for SPEC-BUILD-PROCESS-TEMPLATE-001 are specific and actionable
- [ ] Quick wins section identifies low-effort changes that unblock progress
- [ ] No files modified — audit is read-only
- [ ] Each audit section references at least 2 source files with line numbers
- [ ] Gap analysis: each section rates capability maturity as none/partial/complete
- [ ] Response includes a dependency graph showing which systems connect to each other
- [ ] File inventory table lists every file examined with its line count and purpose

## Smoke Test

- [ ] Response file exists at `.deia/hive/responses/AUDIT-BUILD-PROCESS-INFRA-2026-04-14.md`
- [ ] Response contains all 7 YAML evidence blocks
- [ ] Executive summary section is present and answers the yes/no/partial question

## Constraints

- No code changes — this is a read-only audit
- No file modifications of any kind
- No git operations
- Report findings for simdecisions repo only (shiftcenter was flattened into simdecisions)
- Output file: `.deia/hive/responses/AUDIT-BUILD-PROCESS-INFRA-2026-04-14.md`

*SPEC-AUDIT-BUILD-PROCESS-INFRA-001 — Q88N — 2026-04-14*
