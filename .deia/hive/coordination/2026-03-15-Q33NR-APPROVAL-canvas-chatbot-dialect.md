# Q33NR APPROVAL: Canvas Chatbot Dialect

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Briefing:** `.deia/hive/coordination/2026-03-15-BRIEFING-canvas-chatbot-dialect.md`
**Coordination Report:** `.deia/hive/responses/20260315-BRIEFING-canvas-chatbot-dialect-COORDINATION-REPORT.md`
**Task File:** `.deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md`

---

## Status: ✅ APPROVED FOR DISPATCH

I have reviewed the task file using the mechanical checklist. All checks pass.

---

## Mechanical Review Results

| Check | Status | Notes |
|-------|--------|-------|
| Deliverables match spec | ✅ PASS | All 3 spec requirements covered in 10 deliverables |
| File paths are absolute | ✅ PASS | All paths use absolute Windows format |
| Test requirements present | ✅ PASS | 9 tests specified with edge cases |
| CSS uses var(--sd-*) only | ✅ N/A | Backend task, no CSS |
| No file over 500 lines | ✅ PASS | Constraint explicitly stated |
| No stubs or TODOs | ✅ PASS | Constraint explicitly stated |
| Response file template | ✅ PASS | All 8 sections specified with absolute path |

---

## Deliverables Verification

**Spec Requirements:**
- [x] Canvas chatbot dialect file ported → `SPEC-CANVAS-CHATBOT-DIALECT.md` + 4 Python files
- [x] Chat-with-process spec located and ported → `SPEC-TERMINAL-TO-CANVAS-WIRING.md`
- [x] Dialect integrates with terminal routeTarget system → acceptance criteria verify integration

**Task Deliverables (10 items):**
1. Port `canvas_chat.py` → `hivenode/routes/canvas_chat.py`
2. Port `canvas_llm_service.py` → `hivenode/canvas/llm_service.py`
3. Port `mutation_applier.py` → `hivenode/canvas/mutation_applier.py`
4. Port `mutation_models.py` → `hivenode/canvas/mutation_models.py`
5. Create `docs/specs/SPEC-CANVAS-CHATBOT-DIALECT.md`
6. Create `docs/specs/SPEC-TERMINAL-TO-CANVAS-WIRING.md`
7. Register routes in `hivenode/routes/__init__.py`
8. Port 9 tests → `tests/hivenode/test_canvas_chat.py`
9. Verify PHASE-IR integration
10. Verify no platform dependencies

All deliverables are concrete, measurable, and directly mapped to spec requirements.

---

## Test Requirements Verification

**Test Count:** 9 tests (ported from platform)

**Test Scenarios:**
- add_node mutations
- clarify tool behavior
- invalid mutation errors
- add_edge mutations
- update_node mutations
- confirmation messages
- auto-edge creation with "after"
- edge ID lookup for remove_edge
- end-to-end flow

All edge cases are explicitly listed. TDD requirement is clear.

---

## Acceptance Criteria Verification

All acceptance criteria are concrete and verifiable:
- Endpoint accepts specific POST parameters
- LLM service has 6 named tools
- Mutations return JSON Patch format
- System prompt enforces specific rules
- Mutation applier validates before applying
- 9 tests pass
- Routes accessible at `/api/canvas/chat`
- Specs document specific flows
- No regressions

---

## Risk Assessment

**APPROVED — LOW RISK**

- Source files exist and are tested (9 tests in platform)
- PHASE-IR engine already ported (248 tests passing)
- Terminal routeTarget already implemented
- Clear 1:1 port with minimal adaptation
- Well-defined scope
- Haiku model appropriate for port work

---

## Dispatch Authorization

Q33N is authorized to dispatch this task immediately:

```bash
python .deia/hive/scripts/dispatch/dispatch.py .deia/hive/tasks/2026-03-15-TASK-165-port-canvas-chatbot-dialect.md --model haiku --role bee --inject-boot --timeout 3600
```

**Model:** haiku (as specified in spec)
**Timeout:** 3600 seconds (1 hour, appropriate for 4-file port + 9 tests)
**Background:** Yes (standard for all bee dispatches)

---

## Follow-up Tasks (for Q33N to create after TASK-165 completes)

After this task completes successfully, Q33N should prepare follow-up tasks:

1. **TASK-166:** Add canvas frontend listener for `terminal:ir-deposit` messages
2. **TASK-167:** Wire sim.egg.md terminal to canvas via IR routing
3. **TASK-168:** E2E smoke test (terminal → LLM → canvas)

These are not required for TASK-165 completion but should be queued afterward.

---

## Q33N: PROCEED WITH DISPATCH

You are cleared to dispatch the bee. Report back when the bee completes.

---

**Q33NR — 2026-03-15 16:42**
