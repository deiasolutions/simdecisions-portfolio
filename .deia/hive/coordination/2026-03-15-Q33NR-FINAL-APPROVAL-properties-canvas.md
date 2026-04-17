# Q33NR FINAL APPROVAL: Properties Canvas Wire

**Date:** 2026-03-15
**Time:** 16:35
**Q33NR:** REGENT-QUEUE-TEMP-2026-03-15-1558-SPE
**Spec:** `.deia/hive/queue/2026-03-15-1558-SPEC-w2-03-properties-canvas-wire.md`

---

## Status

**✅ APPROVED TO DISPATCH BEES**

---

## Task Files Reviewed

All 3 task files pass mechanical review:

### TASK-165: Editable Tree Nodes Infrastructure
**File:** `.deia/hive/tasks/2026-03-15-TASK-165-editable-tree-nodes.md`
**Status:** ✅ APPROVED
**Model:** HAIKU
**Tests:** 6 new tests
**Files modified:** 3 (TreeNodeRow.tsx, types.ts, TreeBrowser.tsx)

### TASK-166: Properties Adapter Event Emission
**File:** `.deia/hive/tasks/2026-03-15-TASK-166-properties-adapter-events.md`
**Status:** ✅ APPROVED
**Model:** HAIKU
**Tests:** 6 new tests
**Files modified:** 2 (simPropertiesAdapter.ts, constants.ts)

### TASK-167: FlowDesigner Property Subscription
**File:** `.deia/hive/tasks/2026-03-15-TASK-167-flowdesigner-property-subscription.md`
**Status:** ✅ APPROVED
**Model:** HAIKU
**Tests:** 6 new tests
**Files modified:** 1 (FlowDesigner.tsx)
**Critical:** STOP clause if FlowDesigner.tsx exceeds 1,000 lines

---

## Dispatch Instructions for Q33N

Execute these commands **SEQUENTIALLY** (each task depends on previous):

```bash
# 1. Dispatch TASK-165 (editable tree nodes)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-165-editable-tree-nodes.md --model haiku --role bee --inject-boot

# WAIT for TASK-165 to complete, verify response file

# 2. Dispatch TASK-166 (adapter events)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-166-properties-adapter-events.md --model haiku --role bee --inject-boot

# WAIT for TASK-166 to complete, verify response file

# 3. Dispatch TASK-167 (FlowDesigner subscription)
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-167-flowdesigner-property-subscription.md --model haiku --role bee --inject-boot

# WAIT for TASK-167 to complete, verify response file
```

**DO NOT dispatch all 3 at once.** Tasks have dependencies. Sequential execution required.

---

## Expected Outcomes

After all 3 tasks complete:

### Tests
- **18 new tests** total (6 per task)
- All tests passing
- No regressions on existing tests

### Files Modified
- 6 files modified
- 2 new test files created
- All files under 500 lines (except FlowDesigner.tsx: 921 → ~950, under 1,000 hard limit)

### Functionality
- Clicking canvas node → opens properties in tree panel ✅ (already worked)
- Editing label in properties panel → updates canvas node in real-time ✅ (NEW)
- Editing description in properties panel → updates canvas node in real-time ✅ (NEW)
- Bus events: `canvas:property-updated` emitted and handled ✅ (NEW)

---

## Completion Criteria for Q33N

After all 3 bees complete, Q33N must:

1. **Read all 3 response files**
   - Verify all 8 sections present
   - Check test pass counts match expectations (6 per task)
   - Check file line counts (no file >500, FlowDesigner <1000)

2. **Write completion report**
   - File: `.deia/hive/responses/20260315-DISPATCH-properties-canvas-wire-COMPLETION-REPORT.md`
   - Include: total tests added, files modified, any issues encountered
   - Status: COMPLETE or NEEDS_FIX

3. **Return to Q33NR**
   - If all tests pass: request archival approval
   - If any tests fail: request fix cycle approval

---

## Fix Cycle Rule

Max 2 fix cycles per spec. If bees fail tests:
1. Create P0 fix spec from failures
2. Enter fix spec into queue
3. Process fix spec (counts as 1 fix cycle)
4. Repeat if needed (max 2 cycles total)
5. After 2 failed fix cycles: flag NEEDS_DAVE

---

## Cost Estimate

- **3 HAIKU tasks**
- **Estimated clock:** 45-60 minutes total
- **Estimated cost:** ~$0.15-0.25 (HAIKU pricing)
- **Test count:** 18 new tests

---

## Q33N: Proceed with Dispatch

You are **APPROVED** to:
1. Dispatch TASK-165
2. Wait for completion
3. Dispatch TASK-166
4. Wait for completion
5. Dispatch TASK-167
6. Wait for completion
7. Write completion report
8. Return to Q33NR

**DO NOT skip the wait steps. DO NOT dispatch in parallel.**

---

**End of Final Approval**
