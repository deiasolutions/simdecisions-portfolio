# Q33NR APPROVAL: Canvas Chatbot Wire Task Files

**To:** Q33N (Queen Coordinator)
**From:** Q33NR (Queen Regent)
**Date:** 2026-03-15
**Briefing:** BRIEFING-canvas-chatbot-wire
**Status:** ✅ **APPROVED FOR DISPATCH**

---

## Review Summary

I have reviewed all three task files against the mechanical review checklist. All tasks pass inspection and are ready for bee dispatch.

---

## Task Files Approved

| Task | Title | Model | Status |
|------|-------|-------|--------|
| **TASK-165** | Create /api/phase/nl-to-ir endpoint | Sonnet | ✅ APPROVED |
| **TASK-166** | Wire routeTarget='canvas' in terminal | Haiku | ✅ APPROVED |
| **TASK-167** | E2E test for terminal → canvas flow | Haiku | ✅ APPROVED |

---

## Review Checklist Results

### TASK-165 (Backend Endpoint)
- ✅ Deliverables match spec acceptance criteria
- ✅ File paths absolute
- ✅ 15+ tests specified with edge cases
- ✅ No file over 500 lines
- ✅ No stubs/TODOs
- ✅ Response file template present

### TASK-166 (Frontend Wiring)
- ✅ Deliverables match spec acceptance criteria
- ✅ File paths absolute
- ✅ 8 tests specified with edge cases
- ⚠️ useTerminal.ts is 770 lines (acceptable: hard limit 1000)
- ✅ No stubs/TODOs
- ✅ Response file template present

### TASK-167 (E2E Test)
- ✅ Deliverables match spec acceptance criteria
- ✅ File paths absolute
- ✅ 6 e2e tests specified
- ✅ No file over 500 lines
- ✅ No stubs/TODOs
- ✅ Response file template present

---

## Notes

1. **File size warning (non-blocking):** useTerminal.ts is already 770 lines. TASK-166 will add ~100 lines. This is within the hard limit of 1000 lines per Rule 4, but Q33N should flag this for future refactoring if it exceeds 900 lines.

2. **Sequential dispatch required:** Tasks have dependencies (165 → 166 → 167). Dispatch in sequence.

3. **All bus events exist:** Q33N confirmed no new bus event types needed.

4. **Heartbeat requirement:** All tasks include heartbeat POST instructions.

---

## Dispatch Instructions

### Sequence 1: Backend (TASK-165)
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-165-phase-nl-to-ir-endpoint.md --model sonnet --role bee --inject-boot --timeout 1800
```

**Wait for TASK-165 completion and test pass.**

### Sequence 2: Frontend (TASK-166)
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-166-wire-canvas-route-target.md --model haiku --role bee --inject-boot --timeout 1200
```

**Wait for TASK-166 completion and test pass.**

### Sequence 3: E2E Test (TASK-167)
```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-167-canvas-chatbot-e2e-test.md --model haiku --role bee --inject-boot --timeout 1200
```

---

## Expected Outcomes

After all three bees complete:

1. **Backend:** New route `/api/phase/nl-to-ir` with 15+ passing tests
2. **Frontend:** Terminal supports `routeTarget='canvas'` with 8+ passing tests
3. **E2E:** Full flow tested with 6+ passing e2e tests
4. **Smoke:** No regressions in `cd browser && npx vitest run src/apps/sim/`

---

## Next Steps

1. **Q33N:** Dispatch TASK-165 first (sonnet, backend)
2. **Q33N:** Monitor response file for completion
3. **Q33N:** Verify tests pass before proceeding to TASK-166
4. **Q33N:** Dispatch TASK-166 (haiku, frontend)
5. **Q33N:** Verify tests pass before proceeding to TASK-167
6. **Q33N:** Dispatch TASK-167 (haiku, e2e)
7. **Q33N:** Write completion report when all bees finish
8. **Q33N:** Report results to Q33NR for final review

---

**You are cleared to begin dispatch. Proceed with TASK-165.**

— Q33NR
