# Q33N RESTART DISPATCH INSTRUCTION

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1032-SPE) — RESTART ATTEMPT 1/2
**To:** Q33N
**Date:** 2026-03-16
**Spec:** 2026-03-16-1032-SPEC-w2-07-tree-browser-volumes

---

## Context

Previous Q33NR timed out after dispatching TASK-180 and TASK-181. Those tasks have completed successfully:

✅ **TASK-180:** Volume adapter backend wire — COMPLETE (filesystemAdapter.ts updated, 9 tests passing)
✅ **TASK-181:** File:selected bus event — COMPLETE (treeBrowserAdapter.tsx updated, 6 tests passing)

❌ **TASK-182:** Text-pane file load — NOT STARTED (no bee response found)
❌ **TASK-183:** E2E integration tests — NOT STARTED (no bee response found)

---

## Instruction

**Dispatch remaining tasks immediately:**

### Batch 1 (Sequential - TASK-182 first):
- TASK-182 (Sonnet) — text-pane file load via /storage/read

### Batch 2 (Sequential - wait for TASK-182):
- TASK-183 (Sonnet) — E2E integration tests

---

## Task Files Ready

- `.deia/hive/tasks/2026-03-16-TASK-182-text-pane-file-load.md`
- `.deia/hive/tasks/2026-03-16-TASK-183-volume-integration-e2e-test.md`

---

## When Complete

1. Read both bee response files
2. Verify all 8 sections present
3. Verify all tests pass
4. Run smoke test: `cd browser && npx vitest run src/primitives/tree-browser/`
5. Write completion report to `.deia/hive/responses/20260316-Q33N-TASK-FILES-READY-tree-browser-volumes.md`
6. Report results to Q33NR

---

**Dispatch now. No delay.**

**Q33NR**
