# Q33NR Directive: Dispatch Properties Canvas Wire Tasks

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1501-SPE)
**To:** Q33N Coordinator
**Date:** 2026-03-16
**Spec ID:** 2026-03-16-1501-SPEC-w2-03-properties-canvas-wire

---

## Directive

Your task files have been reviewed and approved. Proceed with sequential dispatch of all 5 tasks.

---

## Tasks to Dispatch (Sequential Order)

1. **TASK-186:** flow-designer-bus-integration
2. **TASK-187:** property-panel-bus-listener
3. **TASK-188:** property-panel-emit-changes
4. **TASK-189:** flow-designer-listen-property-changes
5. **TASK-190:** integration-test-properties-bus

---

## Execution Instructions

### Model: haiku (all 5 tasks per spec requirement)
### Mode: Sequential (wait for each to complete before next)
### Timeout: 1200 seconds (20 minutes) per task

**Dispatch sequence:**

```bash
# Step 1: TASK-186
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-186-flow-designer-bus-integration.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for completion, verify response file

# Step 2: TASK-187
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-187-property-panel-bus-listener.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for completion, verify response file

# Step 3: TASK-188
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-188-property-panel-emit-changes.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for completion, verify response file

# Step 4: TASK-189
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-189-flow-designer-listen-property-changes.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for completion, verify response file

# Step 5: TASK-190
python .deia/hive/scripts/dispatch/dispatch.py \
  .deia/hive/tasks/2026-03-16-TASK-190-integration-test-properties-bus.md \
  --model haiku --role bee --inject-boot --timeout 1200

# Wait for completion, verify response file
```

---

## Monitoring Requirements

After each task completes:

1. **Check response file exists:** `.deia/hive/responses/20260316-TASK-XXX-RESPONSE.md`
2. **Verify all 8 sections present**
3. **Check test results:** Did tests pass?
4. **Check for stubs:** Were any stubs shipped?
5. **Check acceptance criteria:** All marked [x]?

If any task fails:
- Create fix spec immediately
- Do NOT proceed to next task until fix completes

---

## Final Verification

After all 5 tasks complete successfully:

```bash
# Run smoke test
cd browser && npx vitest run src/apps/sim/components/flow-designer/
```

Expected: All existing tests + new tests from TASK-186 to TASK-190 pass.

---

## Completion Report Required

When all 5 tasks complete, write completion report to:
`.deia/hive/responses/20260316-properties-canvas-wire-COMPLETION-REPORT.md`

Include:
- Total tests added (across all 5 tasks)
- All tests passing? (Y/N)
- Smoke test output (last 10 lines)
- Any issues or follow-ups
- Recommendation: READY_FOR_COMMIT or NEEDS_FIX

---

## Budget Tracking

Track cumulative cost across all 5 tasks. Report in completion report.

---

**Q33NR awaits your completion report.**
