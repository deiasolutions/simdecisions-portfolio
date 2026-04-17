# Q33NR APPROVAL: Properties Canvas Wire

**Date:** 2026-03-15
**Q33NR:** REGENT-QUEUE-TEMP-2026-03-15-1558-SPE
**Q33N Report:** `.deia/hive/coordination/2026-03-15-COORDINATION-REPORT-properties-canvas-wire.md`

---

## Status

**APPROVED TO PROCEED** — with required corrections below.

---

## Answers to Q33N's Questions

### 1. Approve Option A (editable tree nodes)?

**APPROVED.** Option A is correct for these reasons:
- Reuses existing primitive (follows DEIA philosophy)
- Smaller surface area
- TDD-friendly
- Consistent with current architecture

### 2. Approve 3-task breakdown?

**APPROVED.** Sequential approach is correct:
- TASK-165: Infrastructure (editable tree nodes)
- TASK-166: Adapter (emit events)
- TASK-167: Consumer (FlowDesigner subscribes)

Good separation of concerns.

### 3. Approve label + description only for first pass?

**APPROVED WITH MODIFICATION.**

Include `label` and `description` in first pass. **EXCLUDE `duration.value`** from first pass because:
- Requires number validation
- Requires unit handling (seconds, minutes, hours)
- Adds complexity to TASK-165 (string-only inputs are simpler)

Defer `duration.value` to a follow-up task.

### 4. Approve inline validation strategy?

**APPROVED.** Restore previous value on invalid input is correct. Do not emit bus events for invalid values.

---

## Required Corrections

Before dispatching bees, Q33N must:

### 1. Write the 3 task files

Task files must be written to `.deia/hive/tasks/` with these names:
- `2026-03-15-TASK-165-editable-tree-nodes.md`
- `2026-03-15-TASK-166-properties-adapter-events.md`
- `2026-03-15-TASK-167-flowdesigner-property-subscription.md`

### 2. Include absolute file paths

All file paths in task files must be absolute Windows paths:
```
C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\types.ts
```

NOT relative paths like `browser/src/primitives/tree-browser/types.ts`

### 3. Include response file template requirement

Each task file must include this section:

```markdown
## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-XXX-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full absolute paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
```

### 4. Include heartbeat requirement

Each task file must include:

```markdown
## Heartbeat

POST to `http://localhost:8420/build/heartbeat` every 3 minutes with JSON:
```json
{
  "task_id": "2026-03-15-TASK-XXX-<name>",
  "status": "running",
  "model": "haiku",
  "message": "working"
}
```
```

### 5. Include file claims requirement

Each task file must include the file claims section from the original spec:

```markdown
## File Claims (IMPORTANT — parallel bees)

Before modifying any file, claim it to prevent conflicts with other bees:
1. POST http://localhost:8420/build/claim with JSON:
   {"task_id": "2026-03-15-TASK-XXX-<name>", "files": ["C:\\...", "C:\\..."]}
2. If response has conflicts (ok=false), you are queued FIFO. Poll GET http://localhost:8420/build/claims every 30s until the file is yours.
3. When done with a file, release it early so other bees can proceed:
   POST http://localhost:8420/build/release with JSON:
   {"task_id": "2026-03-15-TASK-XXX-<name>", "files": ["C:\\..."]}
4. On heartbeat complete/failed, all your claims auto-release. Claims expire after 10 minutes.
```

### 6. Verify file line counts

Before writing task files, check current line counts for all files to be modified:
- `TreeNodeRow.tsx` — check current lines
- `TreeBrowser.tsx` — check current lines
- `FlowDesigner.tsx` — check current lines (likely >500 already)

If FlowDesigner.tsx is already >500 lines, the task must note this and ensure edits don't exceed hard limit of 1,000 lines.

### 7. Update scope: label + description only

Remove `duration.value` from TASK-165 and TASK-166. Only implement:
- `label` (editable text)
- `description` (editable text)

Both are string fields, no validation complexity.

---

## What Q33N Must Do Next

1. Check line counts for files to be modified (TreeNodeRow.tsx, TreeBrowser.tsx, FlowDesigner.tsx, simPropertiesAdapter.ts)
2. Write 3 task files to `.deia/hive/tasks/` with:
   - Absolute file paths
   - Response file template requirement
   - Heartbeat requirement
   - File claims requirement
   - Label + description only (no duration.value)
3. Return task files to Q33NR for final review
4. **DO NOT dispatch bees yet** — wait for Q33NR approval

---

## Approval Summary

**Approach:** ✅ APPROVED
**Task breakdown:** ✅ APPROVED
**Scope:** ✅ APPROVED (label + description only)
**Validation strategy:** ✅ APPROVED
**Task files:** ❌ NOT YET WRITTEN — required before dispatch

---

**Next:** Q33N writes task files, returns for final review.

---

**End of Q33NR Approval**
