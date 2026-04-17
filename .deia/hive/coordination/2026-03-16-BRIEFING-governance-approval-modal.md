# BRIEFING: Wire GovernanceProxy Approval Modal

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-16
**Spec:** `.deia/hive/queue/2026-03-16-1007-SPEC-w2-10-governance-visual.md`
**Priority:** P1.30
**Model Assignment:** haiku

---

## Objective

Wire GovernanceProxy to show an approval modal when gate_enforcer returns dispositions that require user interaction. User can approve or reject. Result propagated back to gate_enforcer.

---

## Context

### Current State

**GovernanceProxy** exists at `browser/src/infrastructure/relay_bus/GovernanceProxy.tsx`. It currently:
- Wraps every applet
- Intercepts `MessageBus.send()` and `MessageBus.subscribe()`
- Blocks messages not in `bus_emit` / `bus_receive` permission lists
- Logs blocks to Event Ledger via `LOG_EVENT` dispatch action

**Gate Enforcer** exists at `browser/src/infrastructure/gate_enforcer/`. It has:
- **Types** (`types.ts`): 5 dispositions (PASS, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN)
- **Enforcer** (`enforcer.ts`): `BrowserGateEnforcer` class with `checkAction()` method
- **CheckResult** interface: `{ disposition, violationType?, matchedRule?, reason? }`

**Modal patterns** already exist:
- `browser/src/shell/components/NotificationModal.tsx` — simple confirmation modal
- `browser/src/primitives/settings/SettingsModal.tsx` — portal-based modal with backdrop

### Spec Ambiguity — CRITICAL

The spec says:
> "when gate_enforcer returns warn or ask disposition, show approval modal"

However, the actual gate_enforcer types define **5 dispositions**:
1. PASS
2. BLOCK
3. HOLD
4. ESCALATE
5. REQUIRE_HUMAN

There is **NO "WARN" or "ASK" disposition** in the codebase.

**Q33N: Please interpret as follows (unless Q88N corrects):**
- **"warn"** → ESCALATE (show warning, user can approve or reject)
- **"ask"** → REQUIRE_HUMAN (requires explicit human approval)
- HOLD may also need a modal (unclear — assume yes for now)
- PASS → no modal (allowed)
- BLOCK → no modal (silently blocked, already logged)

If this interpretation is wrong, Q88N will correct during task review.

---

## Files to Read First

**GovernanceProxy:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\GovernanceProxy.tsx`

**Gate Enforcer:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\enforcer.ts`

**Modal patterns:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\shell\components\NotificationModal.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\settings\SettingsModal.tsx`

**Tests (reference for test patterns):**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\__tests__\GovernanceProxy.test.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\gate_enforcer\__tests__\enforcer.test.ts`

---

## Deliverables (Task File Requirements)

Q33N must write task file(s) that include:

### 1. GovernanceApprovalModal Component
- New file: `browser/src/infrastructure/relay_bus/GovernanceApprovalModal.tsx`
- Props: `{ disposition, reason, onApprove, onReject, open }`
- Portal-based (render to `.hhp-root`)
- Backdrop (click to reject, unless REQUIRE_HUMAN)
- Escape key handling (reject, unless REQUIRE_HUMAN)
- CSS: var(--sd-*) only
- Max 300 lines

### 2. GovernanceProxy Integration
- Modify `GovernanceProxy.tsx` to:
  - Call `gate_enforcer.checkAction()` BEFORE blocking a message
  - If disposition is ESCALATE, HOLD, or REQUIRE_HUMAN → show modal
  - Wait for user response (approve/reject)
  - If approved → allow message through
  - If rejected → block message and log to Event Ledger
  - If disposition is PASS → allow message through (no modal)
  - If disposition is BLOCK → block message and log (no modal)
- Keep under 500 lines (modularize if needed)

### 3. State Management
- Add modal state to GovernanceProxy (local useState)
- Track pending action while modal is open
- Queue multiple modal requests if needed (or show sequentially)

### 4. Event Ledger Integration
- Log approval events: `GOVERNANCE_APPROVED` (disposition, reason, action, timestamp)
- Log rejection events: `GOVERNANCE_REJECTED` (disposition, reason, action, timestamp)
- Keep existing `GOVERNANCE_BLOCKED` logs

### 5. Tests (TDD)
**GovernanceApprovalModal tests:**
- Renders when open=true
- Shows disposition reason
- Calls onApprove when user clicks Approve
- Calls onReject when user clicks Reject
- Calls onReject on Escape (unless REQUIRE_HUMAN)
- Calls onReject on backdrop click (unless REQUIRE_HUMAN)
- Does NOT allow reject on REQUIRE_HUMAN (only Approve button)
- Uses CSS variables only
- Min 8 tests

**GovernanceProxy integration tests:**
- ESCALATE disposition → modal appears
- REQUIRE_HUMAN disposition → modal appears
- HOLD disposition → modal appears
- User approves → message sent, event logged
- User rejects → message blocked, event logged
- PASS disposition → no modal, message sent
- BLOCK disposition → no modal, message blocked
- Min 7 tests

**Total test requirement: 15+ tests**

### 6. Smoke Test
- All existing GovernanceProxy tests still pass
- All existing gate_enforcer tests still pass
- No new test failures in `browser/src/shell/`

---

## Constraints

- **Rule 3:** CSS variables only (`var(--sd-*)`)
- **Rule 4:** Max 500 lines per file (modularize if needed)
- **Rule 5:** TDD — tests first, then implementation
- **Rule 6:** No stubs, no TODOs
- **Absolute paths** in task files
- **Model:** haiku (fast, good for wiring tasks)

---

## Build Monitor Integration

Task must include heartbeat and file claim instructions:
- POST heartbeats every 3 minutes to `http://localhost:8420/build/heartbeat`
- Claim files before modifying (FIFO queue if conflicts)
- Release files early when done

---

## Acceptance Criteria (Copy to Task File)

- [ ] GovernanceApprovalModal component created
- [ ] GovernanceProxy calls gate_enforcer.checkAction()
- [ ] Modal appears on ESCALATE, HOLD, REQUIRE_HUMAN
- [ ] User can approve or reject
- [ ] Approval → message sent, event logged
- [ ] Rejection → message blocked, event logged
- [ ] PASS → no modal, message sent
- [ ] BLOCK → no modal, message blocked
- [ ] 15+ tests written and passing
- [ ] All existing tests still pass
- [ ] CSS uses var(--sd-*) only
- [ ] No file over 500 lines

---

## Q33N Next Steps

1. Read the files listed above
2. Write task file(s) to `.deia/hive/tasks/`
3. Return to Q33NR for review (DO NOT dispatch bees yet)
4. Include absolute paths, test requirements, smoke test command
5. Include 8-section response file template requirement

---

## Notes

- If the disposition mapping (warn→ESCALATE, ask→REQUIRE_HUMAN) is wrong, Q88N will correct during review
- If gate_enforcer integration is more complex than expected, Q33N may split into 2 tasks (modal component, then integration)
- Keep modal simple — just approve/reject buttons, reason text, and disposition type
- Future work: may add "remember my choice" checkbox (not in this spec)
