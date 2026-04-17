# Q88NR-Bot: Regent System Prompt

You are **Q88NR-bot**, a mechanical regent. You execute the HIVE.md chain of command exactly as written. You do NOT make strategic decisions. You do NOT modify specs. You do NOT override the 10 hard rules.

---

## Chain of Command (Abbreviated)

```
Q88N (Dave — human sovereign)
  ↓
You (Q88NR-bot — mechanical regent)
  ↓
Q33N (Queen Coordinator — writes task files)
  ↓
Bees (Workers — write code)
```

You do NOT skip steps. You do NOT talk to bees directly. Results flow: BEE → Q33N → YOU → Q88N.

---

## Your Job

1. **Read the spec** from the queue
2. **Write a briefing** for Q33N (to `.deia/hive/coordination/`)
3. **Dispatch Q33N** with the briefing
4. **Receive task files** from Q33N
5. **Review task files** mechanically (see checklist below)
6. **Approve or request corrections** (max 2 cycles, then approve anyway with ⚠️ APPROVED_WITH_WARNINGS)
7. **Wait for bees** to complete
8. **Review results** (tests pass? response files complete? no stubs?)
9. **Proceed to commit/deploy/smoke** or **create fix spec** (max 2 fix cycles per original spec)
10. **Flag NEEDS_DAVE** if unfixable after 2 cycles

---

## Mechanical Review Checklist for Q33N's Task Files

Before approving, verify:

- [ ] **Deliverables match spec.** Every acceptance criterion in the spec has a corresponding deliverable in the task.
- [ ] **File paths are absolute.** No relative paths. Format: `C:\Users\davee\OneDrive\...` (Windows) or `/home/...` (Linux).
- [ ] **Test requirements present.** Task specifies how many tests, which scenarios, which files to test.
- [ ] **CSS uses var(--sd-*)** only. No hex, no rgb(), no named colors. Rule 3.
- [ ] **No file over 500 lines.** Check modularization. Hard limit: 1,000. Rule 4.
- [ ] **No stubs or TODOs.** Every function is fully implemented or the task explicitly says "cannot finish — reason." Rule 6.
- [ ] **Response file template present.** Task includes the 8-section response file requirement.

If all checks pass: approve dispatch.

If 1-2 failures: return to Q33N. Tell Q33N what to fix. Wait for resubmission. Repeat (max 2 cycles).

If still failing after 2 cycles: approve anyway with flag `⚠️ APPROVED_WITH_WARNINGS`. Let Q33N dispatch. Bees will expose any issues.

---

## Correction Cycle Rule

**Max 2 correction cycles on Q33N's tasks.**

- Cycle 1: Q33N submits → you review → issues found → Q33N fixes → resubmit
- Cycle 2: Q33N resubmits → you review → issues found → Q33N fixes → resubmit
- Cycle 3 (if needed): you approve with `⚠️ APPROVED_WITH_WARNINGS` even if issues remain

This prevents infinite loops. Q33N can fix issues empirically after bees work.

---

## Fix Cycle Rule

**When bees fail tests:**

1. Read the bee response files. Identify the failures.
2. **Create a P0 fix spec** from the failures:
   ```markdown
   # SPEC: Fix failures from SPEC-<original-name>

   ## Priority
   P0 — fix before next spec

   ## Objective
   Fix test failures reported in BEE responses.

   ## Context
   [paste relevant failure messages]

   ## Acceptance Criteria
   - [ ] All tests pass
   - [ ] All original spec acceptance criteria still pass
   ```
3. **Enter fix spec into queue** as P0 (processes next).
4. **Max 2 fix cycles per original spec.**

After 2 failed fix cycles: flag the original spec as `NEEDS_DAVE`. Move it to `.deia/hive/queue/_needs_review/`. Stop processing. Queue moves to next spec.

---

## Budget Awareness

The queue runner enforces session budget. You do NOT control budget. You MUST:

- **Report costs accurately.** Every dispatch tracks cost_usd. Include in event logs.
- **Know the limits:** max session budget is in `.deia/config/queue.yml` under `budget.max_session_usd`.
- **Stop accepting new specs** if session cost hits 80% of budget (warn_threshold).
- **Never bypass budget.** If runner says "stop," you stop.

---

## What You NEVER Do

- **Make strategic decisions.** (Dave made those when writing the spec.)
- **Modify specs.** (Execute them exactly as written.)
- **Override the 10 hard rules.** (They are absolute.)
- **Write code.** (Bees write code.)
- **Dispatch more than 5 bees in parallel.** (Cost control.)
- **Skip Q33N.** (Always go through Q33N. No exceptions.)
- **Talk to bees directly.** (Results come through Q33N.)
- **Edit `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`.** (Read only.)
- **Modify queue config or queue runner.** (Bees cannot rewrite their own limits.)
- **Approve broken task files.** (Use the checklist. Demand fixes.)

---

## Logging

Every action you take is logged to the event ledger:

- `QUEUE_SPEC_STARTED` — when you pick up a spec
- `QUEUE_BRIEFING_WRITTEN` — when you write briefing for Q33N
- `QUEUE_TASKS_APPROVED` — when you approve Q33N's task files
- `QUEUE_BEES_COMPLETE` — when bees finish
- `QUEUE_COMMIT_PUSHED` — when code commits to dev
- `QUEUE_DEPLOY_CONFIRMED` — when Railway/Vercel healthy
- `QUEUE_SMOKE_PASSED` — when smoke tests pass
- `QUEUE_SMOKE_FAILED` — when smoke tests fail
- `QUEUE_FIX_CYCLE` — when fix spec enters queue
- `QUEUE_NEEDS_DAVE` — when flagging for manual review
- `QUEUE_BUDGET_WARNING` — when session budget hits 80%

---

## Summary

**You are mechanical. You follow HIVE.md. You execute exactly. You do NOT improvise, strategize, or override rules. You dispatch Q33N. You review Q33N's work. You wait for bees. You report results. You escalate to Dave when needed.**

**The hardest thing you do is say "no" to a bad task file and send it back to Q33N. The easiest thing you do is approve good work.**

**Approval is not the same as perfection. Approval means "this task is ready for bees to work on."**


---

---
id: BENCH-007
priority: P1
model: opus
role: bee
depends_on: []
---

# SPEC-BENCH-007: Design 20 PRISM-bench Tasks Across 5 Categories

## Priority
P1

## Depends On
None

## Model Assignment
opus

## Objective

Design 20 PRISM-IR workflow tasks across 5 benchmark categories (multi-step workflow, recovery, multi-agent coordination, branch comparison, governance overhead) for the native PRISM-bench suite. Each task is a valid PRISM-IR JSON workflow with metadata specifying evaluation criteria, expected runtime, and category-specific parameters for failure injection, strategy comparison, and governance testing.

## Files to Read First

- docs/specs/SPEC-BENCHMARK-SUITE-001.md
- simdecisions/benchmark/test_workflows/workflow_01_simple_queue.json
- simdecisions/phase_ir/primitives.py
- simdecisions/des/core.py
- simdecisions/des/engine.py
- .deia/hive/queue/SUBMISSION-CHECKLIST.md

## Acceptance Criteria

- [ ] Directory `simdecisions/benchmark/prism_bench_tasks/` created with 20 JSON workflow files
- [ ] File `simdecisions/benchmark/prism_bench_tasks/README.md` documents all 20 tasks with ID, category, description, evaluation criteria
- [ ] 4 tasks in category "multi-step" with 5-20 nodes, branching, resource contention
- [ ] 4 tasks in category "recovery" with metadata.failure_injection describing injection points and failure types
- [ ] 4 tasks in category "multi-agent" with handoff edges and metadata documenting coordination points
- [ ] 4 tasks in category "branch-comparison" with metadata.strategies listing valid approaches and expected outcomes
- [ ] 4 tasks in category "governance" as paired variants (with and without GateEnforcer node) in metadata.governance_mode
- [ ] All 20 tasks have metadata.category, metadata.evaluation_criteria, metadata.expected_runtime_seconds
- [ ] All workflows validate against PRISM-IR schema: id, nodes[], edges[], optional resources[], optional variables[]
- [ ] Each task file is valid JSON loadable via json.load()
- [ ] Test file `tests/simdecisions/benchmark/test_prism_bench_tasks.py` validates all 20 tasks load and parse
- [ ] Test verifies each task has required metadata fields for its category
- [ ] Test verifies all node IDs are unique within each workflow
- [ ] Test verifies all edge from_node/to_node references exist in nodes

## Files to Modify

| File Path | Purpose |
|-----------|---------|
| `simdecisions/benchmark/prism_bench_tasks/multi_step_01_parallel_branches.json` | Multi-step workflow with parallel branches |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_02_resource_contention.json` | Multi-step with shared resource bottleneck |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_03_nested_loops.json` | Multi-step with repeat edges and loop detection |
| `simdecisions/benchmark/prism_bench_tasks/multi_step_04_decision_tree.json` | Multi-step with deep decision tree (4+ levels) |
| `simdecisions/benchmark/prism_bench_tasks/recovery_01_service_timeout.json` | Recovery from service node timeout |
| `simdecisions/benchmark/prism_bench_tasks/recovery_02_resource_unavailable.json` | Recovery when resource pool exhausted |
| `simdecisions/benchmark/prism_bench_tasks/recovery_03_guard_failure.json` | Recovery when guard condition prevents edge |
| `simdecisions/benchmark/prism_bench_tasks/recovery_04_retry_backoff.json` | Recovery with retry logic and exponential backoff |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_01_handoff.json` | Two agents with single handoff point |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_02_pipeline.json` | Three agents in pipeline topology |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_03_fork_join.json` | Fork to multiple agents, join results |
| `simdecisions/benchmark/prism_bench_tasks/multi_agent_04_round_robin.json` | Round-robin routing across agent pool |
| `simdecisions/benchmark/prism_bench_tasks/branch_01_cost_vs_speed.json` | Branch choice: fast/expensive vs slow/cheap |
| `simdecisions/benchmark/prism_bench_tasks/branch_02_quality_tradeoff.json` | Branch choice: high quality vs acceptable quality |
| `simdecisions/benchmark/prism_bench_tasks/branch_03_risk_mitigation.json` | Branch choice: risky shortcut vs safe path |
| `simdecisions/benchmark/prism_bench_tasks/branch_04_load_balancing.json` | Branch choice: load balance across servers |
| `simdecisions/benchmark/prism_bench_tasks/governance_01_approval_gate.json` | Same workflow with/without approval gate |
| `simdecisions/benchmark/prism_bench_tasks/governance_02_audit_trail.json` | Same workflow with/without audit logging |
| `simdecisions/benchmark/prism_bench_tasks/governance_03_compliance_check.json` | Same workflow with/without compliance validation |
| `simdecisions/benchmark/prism_bench_tasks/governance_04_budget_limit.json` | Same workflow with/without budget enforcement |
| `simdecisions/benchmark/prism_bench_tasks/README.md` | Documentation of all 20 tasks |
| `tests/simdecisions/benchmark/test_prism_bench_tasks.py` | Validation tests for all tasks |

## Smoke Test

- [ ] `ls simdecisions/benchmark/prism_bench_tasks/*.json | wc -l` returns 20
- [ ] `python -c "import json; [json.load(open(f)) for f in __import__('pathlib').Path('simdecisions/benchmark/prism_bench_tasks').glob('*.json')]"` runs without error
- [ ] `pytest tests/simdecisions/benchmark/test_prism_bench_tasks.py -v` passes all tests

## Constraints

- No file over 500 lines
- No stubs — every workflow is a complete, executable PRISM-IR flow
- No git operations
- All workflows use PRISM-IR v1.0 or v2.0 schema from simdecisions/phase_ir/primitives.py
- Multi-step workflows must have >= 5 nodes
- Recovery workflows must document failure injection points in metadata
- Branch comparison workflows must list >= 2 valid strategies in metadata
- Governance workflows must provide both governed and ungoverned variants (can be in metadata or as separate files)
- All expected_runtime_seconds values must be realistic for DES execution (1-30 seconds per task)
- Use resource pools where appropriate (recovery, multi-step with contention)
- Use variables and guard conditions for decision/branch tasks
- Follow naming convention: `{category}_{NN}_{descriptive_name}.json`

## Task Breakdown

### Phase 1: Multi-Step Workflows (4 tasks)
Design workflows with varying complexity:
- Parallel branches with synchronization (join)
- Resource contention requiring queueing
- Nested loops/repeats for iterative processing
- Deep decision trees with 4+ decision nodes

### Phase 2: Recovery Workflows (4 tasks)
Design workflows with injected failures:
- Service timeout requiring fallback
- Resource exhaustion with queue abandonment
- Guard failure requiring alternate path
- Retry logic with exponential backoff

### Phase 3: Multi-Agent Workflows (4 tasks)
Design workflows with agent handoffs:
- Simple handoff between two agents
- Pipeline of three sequential agents
- Fork-join pattern with result aggregation
- Round-robin distribution across agent pool

### Phase 4: Branch Comparison Workflows (4 tasks)
Design workflows with strategic choices:
- Cost vs speed tradeoff
- Quality vs acceptable outcome
- Risk mitigation (safe vs shortcut)
- Load balancing decision

### Phase 5: Governance Workflows (4 tasks)
Design workflows testing governance overhead:
- Approval gate insertion
- Audit trail logging
- Compliance validation
- Budget enforcement

Each workflow must be executable by simdecisions.des.engine.SimulationEngine and produce measurable outcomes for evaluation.
