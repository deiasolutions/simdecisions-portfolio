# SPEC-QUESTIONS-EXP-IR-READINESS-001

**MODE: EXECUTE**

**Spec ID:** SPEC-QUESTIONS-EXP-IR-READINESS-001
**Created:** 2026-04-09
**Author:** Q88N
**Type:** RESEARCH — answers required before TASK-EXP-001 can be revised
**Status:** NEEDS_ANSWERS
**Blocks:** TASK-EXP-001 (revised), SPEC-EXPERIMENT-HIVE-VS-OPUS-001 (IR encoding)

---

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Purpose

Before encoding SPEC-EXPERIMENT-HIVE-VS-OPUS-001 as a PRISM-IR flow,
the factory needs to know which execution capabilities are currently wired
in the production engine. This spec is a research task: survey the engine,
answer each question, report findings.

**Assigned to:** BEE (Sonnet)
**Deliverable:** Answers written to `.deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md`

---

## Survey Targets

Read these files before answering anything:

- `engine/des/engine.py` — production engine core
- `engine/des/core.py` — event loop, node types
- `engine/phase_ir/schema.py` — IR schema, node type definitions
- `engine/phase_ir/validation.py` — what node types are valid
- `hivenode/adapters/cli/claude_cli_subprocess.py` — CLI dispatch adapter
- `hivenode/adapters/cli/claude_headless_adapter.py` — headless adapter
- `.deia/hive/scripts/queue/dispatch_handler.py` — current dispatch flow
- `.deia/hive/scripts/queue/run_queue.py` — queue runner entry point
- `.deia/hive/scripts/queue/scheduler.py` — if it exists; report if absent
- `docs/specs/SPEC-EXPERIMENT-HIVE-VS-OPUS-001.md` — the experiment being encoded
- `docs/specs/SPEC-FBB-JOURNEY-GAMIFICATION-V1.md` — the feature being built

Report exact file paths, line counts, and relevant function/class names
for every file you read. Do not answer from memory.

---

## Questions

### Section 1: Node Types

**Q1.1** What operator types (`op:`) are currently defined in the IR schema?
List every valid value. Specifically: is `machine` defined as a valid operator
type, distinct from `llm` and `human`?

**Q1.2** For task nodes with `op: machine` (or equivalent), what action
types are supported? Is there a field (e.g. `action`, `command`, `exec`)
that specifies what the machine does? What values are valid?

**Q1.3** Is `op: subprocess` or any shell-execution operator defined?
If not, what is the closest existing mechanism for executing an arbitrary
shell command as a node action?

**Q1.4** Is there a `script` node type or `invoke` node type that can call
a Python function or external process? If so, where is it implemented and
what does its schema look like?

---

### Section 2: Production Engine Execution

**Q2.1** Does the production engine (`engine.py`) currently execute task
nodes by dispatching to adapters? Which adapters does it know about?
Is the adapter selection driven by the `op:` field in the node definition?

**Q2.2** Can a production engine node today call `dispatch.py` via
subprocess and wait for the response file? Is there any existing node
handler that does something like this, even partially?

**Q2.3** Can a production engine node run `npx vitest run` (or any npm
script) as a subprocess and capture stdout/stderr as node output? If not,
what would need to be added?

**Q2.4** Can a production engine node run `git checkout -b {branch}` and
`git commit` as subprocess calls? Same question — exists or what's needed?

**Q2.5** Does the production engine support passing token attributes
(e.g. `treatment`, `run_number`, `branch`) as context into node execution?
How are token attributes accessed inside a node handler?

---

### Section 3: Scheduler

**Q3.1** Does `scheduler.py` exist? If yes: what is its entry point, what
does it read from (backlog directory, database, queue.yml?), and what does
it write to (staging directory, database?)? Report the full path.

**Q3.2** If `scheduler.py` does not exist: what currently performs
dependency resolution and moves items from backlog to staging? Is this
`run_queue.py`, a separate script, or a manual step by Q88N?

**Q3.3** Does the scheduler (or equivalent) currently understand any
metadata beyond `priority` and `depends_on` when deciding what to stage?
For example: does it understand `experiment_type`, `treatment`, `runs`,
or `branch_prefix`?

**Q3.4** What is the current format of a backlog item? Is it a markdown
file with YAML frontmatter, a plain markdown file with sections, a database
row, or something else? Provide an example of a real backlog item's header.

---

### Section 4: Experiment Flow Feasibility

**Q4.1** Given your findings above, can the experiment in
SPEC-EXPERIMENT-HIVE-VS-OPUS-001 be encoded as a PRISM-IR flow today,
with the production engine executing it without new node types?
Answer yes/no with brief justification.

**Q4.2** If no: list the exact gaps — what node types or executor
capabilities need to be added first. For each gap, estimate: is this
a small addition (< 1 day, 1 bee) or a larger build (> 1 day, spec needed)?

**Q4.3** If yes (or partially yes): sketch the node sequence for one
treatment run as you would write it in PRISM-IR. Just the node IDs and
`op:` types — no need for full YAML. This confirms your understanding
is correct before a full encoding spec is written.

**Q4.4** Regardless of current state: does the Event Ledger emit schema
already include fields for `experiment_id`, `treatment`, and `run_number`?
If not, are these addable as arbitrary `context` payload fields without
a schema change?

---

### Section 5: Backlog Placement

**Q5.1** Where should `SPEC-EXPERIMENT-HIVE-VS-OPUS-001.md` and
`SPEC-FBB-JOURNEY-GAMIFICATION-V1.md` be placed so the scheduler
picks them up? Provide the exact directory path.

**Q5.2** What frontmatter fields does the scheduler require on a spec
file to process it? Provide a minimal valid frontmatter example.

**Q5.3** Is `TASK-EXP-001-EXPERIMENT-INFRASTRUCTURE.md` correctly
formatted as a backlog item, or does it need to be converted to match
the current backlog item format? If conversion needed, describe what
changes are required.

---

## Acceptance Criteria

- [ ] Every file in "Survey Targets" read and reported with path, line count, and key functions/classes
- [ ] All 17 questions (Q1.1–Q5.3) answered with file+line citations
- [ ] Files that do not exist explicitly reported as absent (no guessing)
- [ ] Feasibility verdict in summary section with clear yes/no and gap list if no
- [ ] Response written to `.deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md`
- [ ] Response follows the required structure: Files Read, Answers, Summary, Clock/Coin/Carbon

## Smoke Test

```bash
test -f .deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md && echo "Response exists" || echo "MISSING"
grep -c "^##" .deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md
# Should show at least 4 sections (Files Read, Answers, Summary, Clock/Coin/Carbon)
```

## Constraints

- RESEARCH ONLY — do not modify any code files
- Answer from actual file reads, not from memory or assumptions
- If a file does not exist, state "FILE NOT FOUND" — do not guess contents
- No stubs. Every question answered.
- Max response length: 500 lines

## Response File

`.deia/hive/responses/20260409-EXP-IR-READINESS-RESPONSE.md`

---

*SPEC-QUESTIONS-EXP-IR-READINESS-001 — Q88N — 2026-04-09*
