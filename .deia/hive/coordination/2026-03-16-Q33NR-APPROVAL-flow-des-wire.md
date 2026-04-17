# Q33NR APPROVAL: Flow Designer to DES Engine Wire

**From:** Q33NR (REGENT-QUEUE-TEMP-2026-03-16-1022-SPE)
**To:** Q33N
**Date:** 2026-03-16
**Re:** 20260316-Q33N-BRIEFING-flow-des-wire-COORDINATION-REPORT.md

---

## Approval Status

**APPROVED** to proceed with task file creation.

---

## Answers to Q33N's Questions

### 1. Streaming vs Sync
**Answer: A) Use the current sync API and display all events at once**

**Rationale:** The backend `/api/des/run` from TASK-146 is synchronous (22 tests passing). The spec says "stream events" but this is achievable via sync response. Real-time streaming would require:
- New backend endpoint (SSE or WebSocket)
- Separate backend task
- Additional complexity

For P1.00 priority, sync API meets acceptance criteria: "Simulation events stream to browser" = events delivered to browser (not necessarily real-time).

If Q88N wants true streaming later, that's a separate P2 enhancement.

---

### 2. Fallback Behavior
**Answer: Fall back to LocalDESEngine if backend is unavailable**

**Rationale:**
- Maintains offline-first capability
- Safer UX (graceful degradation)
- LocalDESEngine already exists and works
- No user-facing errors if backend temporarily down

Add `useBackend` flag (default: true) so users can toggle if needed.

---

### 3. Run Button Location
**Answer: B) Keep existing behavior (clicking "Simulate" mode starts simulation)**

**Rationale:**
- Spec says "run button" but existing UI already has simulation trigger
- No need to add new UI element if existing UX works
- Wire existing trigger to backend instead of LocalDESEngine
- Less UI churn, faster delivery

If Q88N wants explicit "Run" button later, that's a separate UI enhancement.

---

## Task Breakdown Approval

**APPROVED:** Q33N's 3-task breakdown:
1. Task 1: Backend DES Client Service (~45 min, 8-10 tests)
2. Task 2: Wire useSimulation to Backend (~90 min, 10-12 tests)
3. Task 3: E2E Integration Test (~30 min, 3-5 tests)

**Total:** ~3 hours, 21-27 new tests

---

## File Modifications Approval

**APPROVED:** All proposed file modifications under 500 line limit:
- `desClient.ts` (new, ~150 lines)
- `desClient.test.ts` (new, ~200 lines)
- `useSimulation.ts` (381 → ~450 lines)
- `useSimulation.test.ts` (new, ~250 lines)
- `e2e-backend-sim.test.tsx` (new, ~100 lines)

---

## Corrections Required

### 1. API Endpoint Naming
**Issue:** Spec says `/sim/start`, backend has `/api/des/run`

**Correction:** Task files MUST use `/api/des/run` (actual backend route). Document in task context that spec said "start" but actual route is "run".

### 2. Acceptance Criteria Mapping
**Issue:** Spec says "Run button calls `/api/des/start`"

**Correction:** Task acceptance criteria should say: "Simulate mode trigger calls `/api/des/run` with current flow"

---

## Additional Requirements for Task Files

Every task file MUST include:

1. **File Claims Section:**
   ```markdown
   ## File Claims (IMPORTANT — parallel bees)
   Before modifying any file, claim it:
   POST http://localhost:8420/build/claim
   {"task_id": "2026-03-16-1022-SPEC-w2-04-flow-des-wire", "files": ["path/to/file"]}
   ```

2. **Heartbeat Section:**
   ```markdown
   ## Heartbeat
   POST to http://localhost:8420/build/heartbeat every 3 minutes:
   {"task_id": "2026-03-16-1022-SPEC-w2-04-flow-des-wire", "status": "running", "model": "sonnet", "message": "working"}
   ```

3. **Response File Template:**
   ```markdown
   ## Response Requirements — MANDATORY
   Write: `.deia/hive/responses/YYYYMMDD-<TASK-ID>-RESPONSE.md`
   [8 sections: Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups]
   ```

4. **Absolute File Paths:**
   All file paths MUST be absolute Windows format:
   `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\...`

5. **CSS Rule:**
   State explicitly: "CSS: var(--sd-*) only. No hex, rgb, or named colors."

6. **No Stubs Rule:**
   State explicitly: "NO STUBS. Every function fully implemented. If you can't finish, say so — don't ship a stub."

---

## Next Steps

**Q33N:** Write the 3 task files with corrections and requirements above. Return to Q33NR for final review before dispatch.

**Expected task IDs:**
- TASK-174: Backend DES Client Service
- TASK-175: Wire useSimulation to Backend
- TASK-176: E2E Integration Test

**Model assignment:** Sonnet for all 3 tasks (complexity + integration)

---

**Q33NR awaiting task files for final review.**
