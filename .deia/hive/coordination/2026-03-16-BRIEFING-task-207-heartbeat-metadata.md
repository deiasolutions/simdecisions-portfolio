# Briefing: TASK-207 Heartbeat Metadata Verification

**From:** Q33NR (Regent)
**To:** Q33N (Coordinator)
**Date:** 2026-03-16
**Model:** Sonnet

---

## Objective

Review TASK-207 task file and dispatch a bee to implement heartbeat metadata verification + build monitor display of real cumulative cost.

---

## Context

**What exists:**
- TASK-207 file already written: `.deia/hive/tasks/2026-03-16-TASK-207-heartbeat-metadata-verify.md`
- Task was created by queue runner as follow-up to TASK-204 (CLI token capture fix)
- Dependency: TASK-204 must be complete before this task (ProcessResult.usage now contains non-zero tokens)

**What needs to happen:**
1. You (Q33N) review TASK-207 task file for completeness using mechanical checklist
2. If issues found: correct the task file
3. If clean: dispatch a BEE (model: haiku) to execute TASK-207
4. When BEE completes: review response file, verify all 8 sections present
5. Report results back to me (Q33NR)

---

## Mechanical Review Checklist

Before dispatching, verify TASK-207 has:

- [ ] **Deliverables match objective.** Every acceptance criterion has a corresponding deliverable.
- [ ] **File paths are absolute.** No relative paths.
- [ ] **Test requirements present.** Task specifies test count, scenarios, test file path.
- [ ] **CSS uses var(--sd-*)** only (if applicable). No hex, no rgb(), no named colors.
- [ ] **No file over 500 lines.** Check modularization.
- [ ] **No stubs or TODOs.** Every function is fully implemented or task explicitly says "cannot finish — reason."
- [ ] **Response file template present.** Task includes 8-section response file requirement.

---

## Task File Location

`.deia/hive/tasks/2026-03-16-TASK-207-heartbeat-metadata-verify.md`

---

## Dispatch Command (after your review)

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-16-TASK-207-heartbeat-metadata-verify.md --model haiku --role bee --inject-boot --timeout 1800
```

---

## Expected BEE Deliverables

1. Heartbeat callback in ClaudeCodeProcess sends model, input_tokens, output_tokens, cost_usd
2. Dispatch script heartbeat callback forwards tokens to build monitor
3. Build monitor /status endpoint returns non-zero total_cost after dispatch
4. CCCMetadata.model_for_cost populated with actual model ID (not empty)
5. 3+ tests pass (test_heartbeat_metadata.py)
6. Integration test confirms real dispatch results in non-zero total_cost

---

## Constraints

- No file over 500 lines
- No stubs — all functions fully implemented
- TDD: tests first, then implementation
- Heartbeat callback must not crash dispatch on failure (try/except)

---

## What You Do Next

1. Read TASK-207 task file
2. Run mechanical checklist
3. If corrections needed: fix task file, report what you fixed
4. If clean: dispatch BEE with command above
5. When BEE completes: read response file, verify all 8 sections
6. Report back to me (Q33NR) with summary

---

## What You Do NOT Do

- Write code yourself (unless I explicitly approve it for this task)
- Skip the mechanical review
- Dispatch without reporting task file status first
- Modify files outside task scope

---

**Q33N: Review TASK-207 and report status. If clean, dispatch BEE. If issues, report corrections needed.**
