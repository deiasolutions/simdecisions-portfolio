# BL-206: Regent Bee Slot Reservation Protocol — Task Breakdown COMPLETE

**Status:** READY FOR Q33NR REVIEW
**Model:** Q33N (Sonnet 4.5)
**Date:** 2026-03-16

---

## Summary

I (Q33N) have read the briefing from Q88NR regarding BL-206 (Regent Bee Slot Reservation Protocol) and broken it down into 4 task files:

1. **TASK-W1-A** — Hivenode slot reservation endpoints (backend, TDD)
2. **TASK-W1-B** — Queue runner slot polling (Python, TDD)
3. **TASK-W1-C** — Regent slot protocol documentation (process doc, no code)
4. **TASK-W1-D** — Integration smoke test (manual script or automated)

All task files are ready for Q33NR review.

---

## Task Files Created

### 1. TASK-W1-A: Hivenode slot reservation endpoints
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-A-PIPELINE-STORE-PROTOCOL.md`

**Objective:** Build 3 new HTTP endpoints in hivenode to manage bee slot reservations.

**Key deliverables:**
- Add slot state to `BuildState` class: `slot_reservations` dict + `total_capacity` int
- 3 new endpoints:
  - `POST /build/slot-reserve` — regent reserves N slots for a spec
  - `POST /build/slot-release` — regent releases N slots as bees complete
  - `GET /build/slot-status` — queue runner polls slot availability
- Persist slot state to `monitor-state.json` (same file as heartbeat state)
- **Tests:** 15+ tests (TDD) in `test_build_monitor_slots.py`
- **Model:** Haiku (straightforward HTTP routes)

**Constraints:**
- No file over 500 lines (extract to `build_slots.py` if needed)
- In-memory slot state (no database, resets on restart)
- Backward compatible (queue runner defaults to 1-slot-per-spec if regent doesn't call `/slot-reserve`)

---

### 2. TASK-W1-B: Queue runner slot polling and gating
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-B-VALIDATION-LEDGER-EVENTS.md`

**Objective:** Modify queue runner to poll hivenode's `/build/slot-status` BEFORE submitting each spec.

**Key deliverables:**
- Add `httpx` dependency + `_poll_slot_status()` helper function
- Modify `_process_queue_pool` to:
  - Poll slot status before backfilling each slot
  - Wait loop if `available < 1` (poll every 10 seconds)
  - Log slot status on each poll
- Graceful fallback if hivenode unreachable (proceed with default 1-slot-per-spec)
- **Tests:** 10+ tests (TDD) in `test_slot_polling.py`
- **Model:** Haiku (straightforward polling logic)

**Constraints:**
- `run_queue.py` is 944 lines, approaching 1,000 hard limit
- Do NOT add more than 100 lines (extract to `slot_poller.py` if needed)

---

### 3. TASK-W1-C: Regent slot protocol documentation
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-C-REGENT-SLOT-PROTOCOL-DOC.md`

**Objective:** Write process doc defining how regent estimates bee count and uses slot endpoints.

**Key deliverables:**
- Process doc: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\processes\P-10-SLOT-RESERVATION.md`
- 6 sections:
  1. Overview (what, who, when)
  2. Bee count estimation (from spec headers or structure)
  3. Slot reservation workflow (step-by-step with curl examples)
  4. Error handling (hivenode unreachable, API errors)
  5. Examples (5-bee spec, 8-bee spec, 12-bee spec with capacity=10)
  6. Integration points (hivenode endpoints, queue runner, Q33N)
- **Tests:** None (documentation task)
- **Model:** Sonnet (requires understanding regent workflow)

**Constraints:**
- ~200-300 lines
- Clear, concise language
- Code examples must be copy-paste ready

---

### 4. TASK-W1-D: Slot reservation integration smoke test
**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-D-SLOT-INTEGRATION-SMOKE-TEST.md`

**Objective:** End-to-end smoke test validating hivenode + queue runner + regent protocol.

**Key deliverables (Option A: manual script, recommended):**
- Bash script: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\smoke\slot-reservation-smoke.sh`
- Test scenario:
  1. Start hivenode
  2. Reserve 8 slots for spec-1
  3. Check status (expect: reserved=8, available=2)
  4. Release 1 slot
  5. Check status (expect: reserved=7, available=3)
  6. Release remaining 7 slots
  7. Check status (expect: reserved=0, available=10)
  8. Kill hivenode
- README explaining how to run
- **Tests:** Manual execution (PASS/FAIL for each step)
- **Model:** Haiku (execute test scenario)

**Alternative Options:**
- Option B: Automated pytest test in `test_slot_integration.py`
- Option C: Queue runner integration with dummy specs (more realistic, longer)

---

## What Changed vs. Briefing

**No changes.** All 4 tasks follow the briefing exactly:
- TASK-A (hivenode endpoints) = Deliverable #1 from briefing
- TASK-B (queue runner polling) = Deliverable #2 from briefing
- TASK-C (regent protocol doc) = Deliverable #3 from briefing
- TASK-D (integration smoke test) = Deliverable #4 from briefing

Model assignments match briefing recommendations.

---

## Checks Performed

### File paths (all absolute):
- ✅ All file paths in tasks are absolute Windows paths
- ✅ Test file paths specified
- ✅ Response file paths specified

### Constraints included:
- ✅ No file over 500 lines (extract logic if needed)
- ✅ TDD (tests first) for TASK-A and TASK-B
- ✅ No stubs
- ✅ In-memory slot state (no DB)
- ✅ Backward compatible (queue runner falls back if hivenode unreachable)

### Response file template:
- ✅ All 4 tasks include mandatory 8-section response template
- ✅ Clock / Cost / Carbon required (all three)

### Model assignments:
- ✅ TASK-W1-A: Haiku (straightforward HTTP routes)
- ✅ TASK-W1-B: Haiku (straightforward polling logic)
- ✅ TASK-W1-C: Sonnet (requires understanding regent workflow, writing clear instructions)
- ✅ TASK-W1-D: Haiku (execute test scenario)

### Test requirements:
- ✅ TASK-W1-A: 15+ tests specified
- ✅ TASK-W1-B: 10+ tests specified
- ✅ TASK-W1-C: No tests (documentation)
- ✅ TASK-W1-D: Smoke test execution (manual PASS/FAIL)

---

## Dependencies

**Task execution order:**
1. **TASK-W1-A** (hivenode endpoints) — NO DEPENDENCIES, can start immediately
2. **TASK-W1-B** (queue runner polling) — DEPENDS ON TASK-W1-A (needs `/build/slot-status` endpoint)
3. **TASK-W1-C** (regent protocol doc) — DEPENDS ON TASK-W1-A (needs to reference endpoint behavior)
4. **TASK-W1-D** (integration smoke test) — DEPENDS ON ALL (A, B, C)

**Recommended dispatch strategy:**
- Dispatch TASK-W1-A first (solo)
- After A completes, dispatch TASK-W1-B and TASK-W1-C in parallel
- After A, B, C complete, dispatch TASK-W1-D (solo)

---

## Next Steps

**Q33NR to review these task files and:**
1. Check for missing deliverables
2. Check for stubs or vague acceptance criteria
3. Verify file paths are correct
4. Verify test requirements are sufficient
5. **If approved:** Tell Q33N to dispatch bees

**If corrections needed:**
- Q33NR tells Q33N what to fix
- Q33N updates task files and returns for re-review

---

## Files Created by Q33N

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-A-PIPELINE-STORE-PROTOCOL.md`
2. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-B-VALIDATION-LEDGER-EVENTS.md`
3. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-C-REGENT-SLOT-PROTOCOL-DOC.md`
4. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-16-TASK-W1-D-SLOT-INTEGRATION-SMOKE-TEST.md`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-BL-206-SLOT-RESERVATION-TASK-BREAKDOWN.md` (this file)

---

## Clock / Cost / Carbon

- **Clock:** ~12 minutes (reading briefing + codebase + writing 4 task files + review)
- **Cost:** ~$0.10 USD (Sonnet 4.5, ~10,000 tokens input, ~8,000 tokens output)
- **Carbon:** ~0.002 kg CO2e (estimated)

---

**Q33N awaits Q33NR review and approval to dispatch bees.**
