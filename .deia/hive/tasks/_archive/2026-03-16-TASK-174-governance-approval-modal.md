# TASK-174: Wire GovernanceProxy Approval Modal

## Objective
Create an approval modal system for GovernanceProxy that shows when gate_enforcer returns dispositions requiring human interaction (ESCALATE, HOLD, REQUIRE_HUMAN). User can approve or reject, and the result is propagated back through the gate enforcement flow.

## Context

### Current State
**GovernanceProxy** (`browser/src/infrastructure/relay_bus/GovernanceProxy.tsx`):
- Wraps every applet
- Intercepts MessageBus.send() and MessageBus.subscribe()
- Currently blocks messages not in bus_emit/bus_receive permission lists
- Logs blocks to Event Ledger via LOG_EVENT dispatch action
- Does NOT yet call gate_enforcer.checkAction()

**Gate Enforcer** (`browser/src/infrastructure/gate_enforcer/`):
- Types define 5 dispositions: PASS, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN
- BrowserGateEnforcer.checkAction() returns CheckResult with disposition and reason
- Currently exists but is NOT integrated with GovernanceProxy

**Modal Patterns Available**:
- `NotificationModal.tsx` — simple confirmation modal with backdrop
- `SettingsModal.tsx` — portal-based modal using createPortal to `.hhp-root`

### Disposition Mapping (Spec Clarification)
The spec mentions "warn" and "ask" but gate_enforcer actually defines:
- **PASS** → allow immediately, no modal
- **BLOCK** → block immediately, no modal, log to Event Ledger
- **HOLD** → show modal, user can approve/reject
- **ESCALATE** → show modal, user can approve/reject
- **REQUIRE_HUMAN** → show modal, user MUST approve (no reject allowed via Escape/backdrop)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceProxy.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\enforcer.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\NotificationModal.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\GovernanceProxy.test.tsx`

## Deliverables

### 1. GovernanceApprovalModal Component
**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceApprovalModal.tsx`

**Requirements:**
- Props: `{ disposition: Disposition, reason?: string, matchedRule?: string, onApprove: () => void, onReject: () => void, open: boolean }`
- Portal-based rendering to `.hhp-root` (use createPortal)
- Backdrop (semi-transparent overlay)
- Centered modal card showing:
  - Disposition type (e.g., "Escalation Required", "Human Approval Required")
  - Reason text (from CheckResult.reason)
  - Matched rule (from CheckResult.matchedRule) if present
  - Approve and Reject buttons
- Escape key handling:
  - If REQUIRE_HUMAN → Escape does nothing (must approve)
  - Otherwise → Escape calls onReject
- Backdrop click handling:
  - If REQUIRE_HUMAN → backdrop click does nothing (must approve)
  - Otherwise → backdrop click calls onReject
- CSS: use `var(--sd-*)` only (no hardcoded colors)
- Max 300 lines

### 2. GovernanceProxy Integration
**Modify:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceProxy.tsx`

**Changes needed:**
1. Import BrowserGateEnforcer and create a singleton instance
2. Add modal state: `useState<{ disposition, reason, matchedRule, pendingAction } | null>(null)`
3. In `governedSend()`:
   - BEFORE checking permissions, call `enforcer.checkAction(nodeId, messageType)`
   - Handle disposition:
     - PASS → allow through
     - BLOCK → block and log (existing behavior)
     - HOLD / ESCALATE / REQUIRE_HUMAN → show modal, store pendingAction
   - When modal resolves:
     - If approved → allow message through, log GOVERNANCE_APPROVED event
     - If rejected → block message, log GOVERNANCE_REJECTED event
4. Render `<GovernanceApprovalModal>` component
5. Keep file under 500 lines (modularize if needed)

**Note:** For this first implementation, you may stub the enforcer instance with a simple in-memory ethics config for testing. The full backend integration will come in a later task.

### 3. Event Ledger Integration
Add two new event kinds to Event Ledger logging:

**GOVERNANCE_APPROVED:**
```typescript
{
  kind: 'GOVERNANCE_APPROVED',
  nodeId: string,
  disposition: string,
  reason: string,
  action: string,
  timestamp: string
}
```

**GOVERNANCE_REJECTED:**
```typescript
{
  kind: 'GOVERNANCE_REJECTED',
  nodeId: string,
  disposition: string,
  reason: string,
  action: string,
  timestamp: string
}
```

Keep existing `GOVERNANCE_BLOCKED` events for PASS/BLOCK dispositions.

### 4. State Management
- Add local state to GovernanceProxy for modal visibility and pending action
- Modal interactions are synchronous (user must respond before next action)
- If multiple modal-requiring actions queue up, handle sequentially (show one modal at a time)

## Test Requirements

### GovernanceApprovalModal Tests
**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\GovernanceApprovalModal.test.tsx`

**Minimum 8 tests:**
1. ✅ Renders when open=true
2. ✅ Does not render when open=false
3. ✅ Shows disposition type (ESCALATE, HOLD, REQUIRE_HUMAN)
4. ✅ Shows reason text
5. ✅ Shows matched rule if present
6. ✅ Calls onApprove when Approve button clicked
7. ✅ Calls onReject when Reject button clicked (non-REQUIRE_HUMAN)
8. ✅ Calls onReject on Escape key (non-REQUIRE_HUMAN)
9. ✅ Calls onReject on backdrop click (non-REQUIRE_HUMAN)
10. ✅ Does NOT allow Escape on REQUIRE_HUMAN
11. ✅ Does NOT allow backdrop click on REQUIRE_HUMAN
12. ✅ Portal renders to `.hhp-root`

**Total: 12 tests**

### GovernanceProxy Integration Tests
**Modify:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\GovernanceProxy.test.tsx`

**Add minimum 7 new tests:**
1. ✅ PASS disposition → no modal, message sent
2. ✅ BLOCK disposition → no modal, message blocked, event logged
3. ✅ ESCALATE disposition → modal appears
4. ✅ HOLD disposition → modal appears
5. ✅ REQUIRE_HUMAN disposition → modal appears
6. ✅ User approves ESCALATE → message sent, GOVERNANCE_APPROVED event logged
7. ✅ User rejects ESCALATE → message blocked, GOVERNANCE_REJECTED event logged

**Total: 7 tests**

### TDD Process
1. Write all 19 tests FIRST (12 + 7)
2. All tests should FAIL initially
3. Implement GovernanceApprovalModal component
4. Implement GovernanceProxy integration
5. All tests should PASS

## Constraints
- **Rule 3:** CSS variables only (`var(--sd-*)`)
- **Rule 4:** Max 500 lines per file
- **Rule 5:** TDD — tests first, then implementation
- **Rule 6:** No stubs, no TODOs (except for backend ethics loading, which is out of scope)
- **Absolute paths** in all file references

## Build Monitor Integration

**Heartbeat (every 3 minutes):**
```bash
curl -X POST http://localhost:8420/build/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "status": "running", "model": "haiku", "message": "implementing governance modal"}'
```

**File Claims (before modifying):**
```bash
# Claim files
curl -X POST http://localhost:8420/build/claim \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "files": ["browser/src/infrastructure/relay_bus/GovernanceProxy.tsx"]}'

# Release when done
curl -X POST http://localhost:8420/build/release \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK-174", "files": ["browser/src/infrastructure/relay_bus/GovernanceProxy.tsx"]}'
```

## Smoke Test Commands
```bash
# Run all GovernanceProxy tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/infrastructure/relay_bus/__tests__/GovernanceApprovalModal.test.tsx

# Run all relay_bus tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/infrastructure/relay_bus/

# Run all gate_enforcer tests (should still pass)
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/infrastructure/gate_enforcer/

# Full shell tests
cd C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser
npx vitest run src/shell/
```

## Acceptance Criteria
- [ ] GovernanceApprovalModal component created and tested (12 tests passing)
- [ ] GovernanceProxy calls gate_enforcer.checkAction() before permission checks
- [ ] Modal appears on ESCALATE, HOLD, REQUIRE_HUMAN dispositions
- [ ] User can approve or reject (except REQUIRE_HUMAN blocks reject)
- [ ] Approval → message sent, GOVERNANCE_APPROVED event logged
- [ ] Rejection → message blocked, GOVERNANCE_REJECTED event logged
- [ ] PASS → no modal, message sent
- [ ] BLOCK → no modal, message blocked, GOVERNANCE_BLOCKED logged
- [ ] 19+ tests written and passing (12 modal + 7 integration)
- [ ] All existing GovernanceProxy tests still pass
- [ ] All existing gate_enforcer tests still pass
- [ ] CSS uses `var(--sd-*)` only
- [ ] No file over 500 lines
- [ ] Modal renders via portal to `.hhp-root`
- [ ] Escape key works correctly (rejects non-REQUIRE_HUMAN)
- [ ] Backdrop click works correctly (rejects non-REQUIRE_HUMAN)

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260316-TASK-174-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.

## Notes
- The gate_enforcer ethics config loading from backend is OUT OF SCOPE for this task
- For testing, you can use a mock enforcer with predefined AgentEthics
- Future work will wire the backend /api/ethics endpoints to load real ethics configs
- Keep the modal simple — just disposition type, reason, approve/reject buttons
- Future enhancement: "remember my choice" checkbox (not in this task)
