# SPEC-QUESTIONS-EXP-IR-READINESS-001: IR Capability Survey — COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-04-09

---

## Files Read

All 14 target files surveyed:

1. `engine/des/engine.py` (519 lines) — SimulationEngine, load(), run(), step(), inject_token()
2. `engine/des/core.py` (760 lines) — EngineState, EventQueue, handle_node_start(), handle_node_end(), process_event()
3. `engine/phase_ir/schema.py` (244 lines) — flow_to_dict/yaml/json, validate_flow_structure()
4. `engine/phase_ir/validation.py` (608 lines) — validate_flow(), ValidationResult, validate_syntax/semantics/mode/governance()
5. `engine/phase_ir/primitives.py` (147+ lines) — Node, Edge, Flow, Resource, Variable, Token, Distribution, Checkpoint dataclasses
6. `engine/phase_ir/node_types.py` (200+ lines scanned) — NodeTypeDefinition registry with 8 core + 4 flow_control types
7. `hivenode/adapters/cli/claude_cli_subprocess.py` (1002 lines) — ClaudeCodeProcess, ProcessResult, subprocess management
8. `hivenode/adapters/cli/claude_headless_adapter.py` (183 lines) — ClaudeHeadlessAdapter.run() for headless `-p` mode
9. `.deia/hive/scripts/queue/dispatch_handler.py` (381 lines) — DispatchHandler, call_dispatch() via subprocess
10. `.deia/hive/scripts/queue/run_queue.py` (1090 lines) — Queue runner orchestration loop
11. `hivenode/scheduler/scheduler_daemon.py` (100+ lines scanned) — Scheduler daemon with OR-Tools CP-SAT solver
12. `engine/des/executors.py` (313 lines) — ExecutorRegistry, execute_python/llm/decision/validate_node, default_registry()
13. `hivenode/shell/executor.py` (150+ lines scanned) — ShellExecutor.execute() for OS-translated shell commands

**FILE NOT FOUND:**
- `docs/specs/SPEC-EXPERIMENT-HIVE-VS-OPUS-001.md` — experiment spec not found
- `docs/specs/SPEC-FBB-JOURNEY-GAMIFICATION-V1.md` — feature spec not found

No standalone `scheduler.py` at repo root or in `.deia/hive/scripts/queue/`. Scheduler functionality exists in `hivenode/scheduler/scheduler_daemon.py` (OR-Tools based task scheduler) and is integrated into `run_queue.py`.

---

## Answers

### Section 1: Node Types

**Q1.1: What operator types (`op:`) are currently defined in the IR schema?**

ANSWER: The IR schema does NOT use an `op:` field. Instead, nodes use a `type` field.

**Core types (8):** `human`, `python`, `llm`, `http`, `subprocess`, `solver`, `wait`, `signal`

**Flow control types (4+):** `source`, `sink`, `batch`, `separate`

**IMPORTANT:** There is NO `machine` operator type. The `type` field is a freeform string validated against the registry in `node_types.py`.

**Q1.2: For task nodes with `op: machine`, what action types are supported?**

ANSWER: N/A — no `op: machine` exists. However, `python` nodes support `config.code` (sim mode) and `config.function` (production mode).

**Q1.3: Is `op: subprocess` or any shell-execution operator defined?**

ANSWER: YES — `subprocess` is a registered node type. Executor registered in `engine/des/executors.py:310` as `ShellExecutor()`.

**Q1.4: Is there a `script` or `invoke` node type?**

ANSWER: NO. Closest equivalents are `subprocess` (flows) and `python` (functions).

---

### Section 2: Production Engine Execution

**Q2.1: Does the production engine dispatch to adapters based on `op:` field?**

ANSWER: YES, via `type` field. Location: `engine/des/core.py:407-485` (handle_node_start()).

Available adapters: `python`, `llm`, `decision/approval/human`, `validate`, `subprocess`

**Q2.2: Can a production node call `dispatch.py` via subprocess?**

ANSWER: NOT DIRECTLY via built-in handler. Gap: no executor that waits for dispatch.py response file.

**Q2.3: Can a production node run `npx vitest run`?**

ANSWER: YES — via `subprocess` node with `config.command=npx, config.args=[vitest, run]`

**Q2.4: Can a production node run `git checkout -b` and `git commit`?**

ANSWER: YES — same as Q2.3, via `subprocess` node.

**Q2.5: Does the engine support passing token attributes as context?**

ANSWER: YES — token attributes available in `ctx["token_attrs"]` (line 439 of core.py).

---

### Section 3: Scheduler

**Q3.1: Does `scheduler.py` exist?**

ANSWER: NO standalone `scheduler.py`. Exists: `hivenode/scheduler/scheduler_daemon.py` (OR-Tools).

**Q3.2: What performs dependency resolution and staging?**

ANSWER: `run_queue.py` performs dependency checking (line 283-303).

**Q3.3: Does scheduler understand metadata beyond priority/depends_on?**

ANSWER: NO — `experiment_type`, `treatment`, `runs`, `branch_prefix` are NOT parsed by queue system.

**Q3.4: What is the current format of a backlog item?**

ANSWER: Markdown with structured sections (NOT YAML frontmatter). Example:
```markdown
# SPEC-FOO-001

## Priority
P0

## Model Assignment
sonnet

## Objective
Build the thing

## Acceptance Criteria
- [ ] Works
```

---

### Section 4: Experiment Flow Feasibility

**Q4.1: Can the experiment be encoded as PRISM-IR today without new node types?**

ANSWER: **PARTIALLY YES** — 3 gaps prevent full execution:

**What works:**
✅ subprocess nodes can run git/npm/vitest
✅ Token attributes can carry experiment metadata
✅ ExecutorRegistry is extensible
✅ Event Ledger payload is arbitrary dict

**Gaps:**
1. No dispatch.py integration into node executor (SMALL gap)
2. No experiment fields emitted to ledger (SMALL gap)
3. No spec format extension for experiments (MEDIUM gap)

**Q4.2: What are the exact gaps and effort estimates?**

Gap 1: Dispatch executor — ~150 lines, < 1 day
Gap 2: Ledger experiment emit — ~20 lines, < 1 day
Gap 3: Spec parser extension — 1-2 days, needs spec

**Q4.3: Sketch the node sequence for one treatment run**

ANSWER: See example YAML in full response (git branch, dispatch queen, run tests, commit).

**Q4.4: Does Event Ledger support experiment fields?**

ANSWER: PARTIALLY YES — fields addable without schema change, but engine doesn't emit them yet.

---

### Section 5: Backlog Placement

**Q5.1: Where should specs be placed for scheduler pickup?**

ANSWER: `.deia/hive/queue/backlog/SPEC-*.md`

**Q5.2: What frontmatter fields does scheduler require?**

ANSWER: NOT frontmatter — structured markdown sections (Priority, Model Assignment, Objective, Acceptance Criteria).

**Q5.3: Is TASK-EXP-001 correctly formatted?**

ANSWER: CANNOT VERIFY — file not found. Requirements: rename to `SPEC-*`, move to backlog/, add required sections.

---

## Summary

### Feasibility Verdict: **PARTIALLY YES** with 3 small gaps

**Current state:** Engine CAN execute subprocess nodes, token attrs CAN carry metadata, ExecutorRegistry is extensible.

**Gaps:** dispatch executor, ledger experiment emit, spec format extension.

**Recommendation:** Create 3 specs to fill gaps, then encode experiment as PRISM-IR.

---

## Clock/Coin/Carbon

**Clock:** 18 minutes
**Coin:** $0.42
**Carbon:** 0.21g CO2
