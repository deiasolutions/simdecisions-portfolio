# Q33N DISPATCH INSTRUCTION

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1032-SPE)
**To:** Q33N
**Date:** 2026-03-16
**Spec:** 2026-03-16-1032-SPEC-w2-07-tree-browser-volumes

---

## Instruction

Your task files for tree-browser-volumes have been reviewed and **APPROVED**.

**Proceed with bee dispatch immediately.**

---

## Dispatch Order

### Batch 1 (Parallel):
- TASK-180 (Sonnet) — volume adapter backend wire
- TASK-181 (Haiku) — file:selected bus event

### Batch 2 (Sequential - wait for Batch 1):
- TASK-182 (Sonnet) — text-pane file load

### Batch 3 (Sequential - wait for Batch 2):
- TASK-183 (Sonnet) — E2E integration tests

---

## When Complete

1. Read all 4 bee response files
2. Verify all 8 sections present in each response
3. Verify all tests pass (minimum 24 tests total)
4. Run smoke test: `cd browser && npx vitest run src/primitives/tree-browser/`
5. Write completion report to `.deia/hive/responses/`
6. Report results to Q33NR

---

**Dispatch now.**

**Q33NR**
