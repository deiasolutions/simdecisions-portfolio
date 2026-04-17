# BRIEFING: Dispatch Bees for BUG-019

**From:** Q33NR (REGENT-QUEUE-TEMP-SPEC-BUG-019)
**To:** Q33N
**Date:** 2026-03-25
**Model Assignment:** sonnet
**Priority:** P0

---

## Objective

Dispatch 3 bees to execute TASK-BUG-019-A, TASK-BUG-019-B, and TASK-BUG-019-C. Tasks A and B are independent and should be dispatched in parallel. Task C depends on both A and B and must be dispatched after both complete.

---

## Context

Task files have been reviewed and approved by Q33NR. All mechanical checks passed. Ready for bee execution.

**Task Files:**
1. `.deia/hive/tasks/2026-03-25-TASK-BUG-019-A-PALETTE-TREENODE-MARKER.md`
2. `.deia/hive/tasks/2026-03-25-TASK-BUG-019-B-SHELL-EARLY-RETURN.md`
3. `.deia/hive/tasks/2026-03-25-TASK-BUG-019-C-RUNTIME-TESTS.md`

---

## Dispatch Instructions

### Phase 1: Parallel Dispatch (A and B)

Dispatch A and B simultaneously (independent tasks):

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-25-TASK-BUG-019-A-PALETTE-TREENODE-MARKER.md --model haiku --role bee --inject-boot &

python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-25-TASK-BUG-019-B-SHELL-EARLY-RETURN.md --model haiku --role bee --inject-boot &
```

### Phase 2: Wait for Completion

Monitor response files:
- `.deia/hive/responses/*TASK-BUG-019-A*`
- `.deia/hive/responses/*TASK-BUG-019-B*`

Both must complete before Phase 3.

### Phase 3: Sequential Dispatch (C)

After A and B complete:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-25-TASK-BUG-019-C-RUNTIME-TESTS.md --model haiku --role bee --inject-boot
```

---

## Expected Outcomes

- **TASK-BUG-019-A:** paletteAdapter + TreeNodeRow changes, 7+ tests passing
- **TASK-BUG-019-B:** ShellNodeRenderer changes, 5+ tests passing
- **TASK-BUG-019-C:** canvasDragIsolation.test.tsx replaced, 8+ tests passing
- **Total:** 20+ tests passing, all acceptance criteria met

---

## Instructions for Q33N

1. **Execute Phase 1 dispatches** (A and B in parallel)
2. **Wait for both A and B to complete** (monitor response files)
3. **Read A and B response files** — verify all 8 sections present, tests passing
4. **Execute Phase 3 dispatch** (C after A and B complete)
5. **Read C response file** — verify all 8 sections present, tests passing
6. **Write completion report** to Q33NR with summary of all 3 bee results
7. **Report back to Q33NR** — do NOT archive yet (Q33NR will instruct)

---

**Q33N: Proceed with dispatch as instructed above.**
