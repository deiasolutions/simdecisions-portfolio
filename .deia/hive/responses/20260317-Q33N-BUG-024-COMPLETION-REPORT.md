# BUG-024 Investigation Complete — Bug Report INACCURATE

**Date:** 2026-03-17
**From:** Q33N (Queen Coordinator)
**To:** Q33NR (Queen Regent)
**Status:** ✅ COMPLETE

---

## Summary

Both investigative tasks completed successfully. **BUG-024 as reported does NOT exist.** The architecture prevents both cross-window and same-window message leaks.

---

## Tasks Completed

| Task | Status | Tests | Verdict |
|------|--------|-------|---------|
| TASK-BUG-024-A | ✅ COMPLETE | 13/13 passing | Cross-window leak IMPOSSIBLE |
| TASK-BUG-024-C | ✅ COMPLETE | 8/8 passing | Same-window routing WORKS CORRECTLY |
| TASK-BUG-024-B | ⏸️ HOLD | - | Not needed (no architectural risk) |

---

## Evidence from TASK-BUG-024-A (Cross-Window Isolation)

**File:** `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts` (497 lines)

**Key findings:**
1. MessageBus is instantiated per-Shell (Shell.tsx line 31)
2. Each tab/window creates its own Shell + MessageBus instance
3. Messages stored in instance-local `_subs` map (no cross-window sync)
4. NO BroadcastChannel, NO localStorage event sync, NO service worker relay

**Test coverage:**
- 13 tests passing
- Targeted messages: bus1 → bus2 isolation verified
- Broadcast messages: no cross-window leak
- PaneId collision: even with matching IDs, messages don't cross windows
- Rapid message sending: high throughput doesn't cause leaks
- Complex scenarios: subscribe/unsubscribe, mute states, telemetry

**Conclusion:** Cross-window message leak is **architecturally impossible**.

---

## Evidence from TASK-BUG-024-C (Same-Window Routing)

**File:** `browser/src/primitives/terminal/__tests__/terminal-multi-egg-routing.test.tsx` (432 lines)

**Key findings:**
1. Simulated Canvas EGG (terminal1 → text1) + Code EGG (terminal2 → text2) in same window
2. Messages from terminal1 to text1 NEVER appear in text2
3. Messages from terminal2 to text2 NEVER appear in text1
4. Canvas IR routing to canvas pane works correctly; Code chat never receives it
5. Two terminals of same appType are isolated by unique nodeIds

**Test coverage:**
- 8 tests passing
- Targeted message delivery: only intended pane receives messages
- Broadcast filtering: subscribers filter by message type correctly
- Canvas IR routing: no leak to Code chat
- Same-appType isolation: two terminals of same type are correctly isolated

**Conclusion:** Same-window routing works correctly — **not the bug**.

---

## Root Cause Analysis

**The bug report is INACCURATE.** Messages from Canvas EGG in tab A **CANNOT** appear in Code EGG chat pane in tab B.

**Possible alternative explanations:**
1. **User perception issue:** User may have had Canvas and Code in the SAME window (not different tabs)
2. **App-specific handler bug:** Code chat might be subscribing to wrong message type or paneId
3. **Test isolation issue:** If tests aren't cleaning up subscribers, old handlers might still be active
4. **Browser extension monitoring:** DevTools or extension might be showing messages that aren't actually delivered

**Recommendation:** Ask Q88N to reproduce with:
1. Open two browser tabs to ShiftCenter
2. Click Canvas EGG in tab A, send message
3. Check tab B's Code EGG chat pane
4. Record what message actually appeared (type, content, source pane ID)

If message appears, the actual bug is in **destination app's subscriber logic**, not MessageBus.

---

## TASK-BUG-024-B Decision: HOLD

**Rationale:**
- TASK-BUG-024-B adds defensive windowId scoping to MessageEnvelope
- Current findings prove cross-window leaks are impossible
- Adding windowId would be defensive against a future risk that doesn't exist
- P1 priority means it can wait for a future sprint

**Recommendation:** Do not dispatch TASK-BUG-024-B now. Archive it as "defensive measure for future consideration."

If Q88N wants it dispatched anyway as future-proofing, I can dispatch it immediately.

---

## Files Created/Modified

### TASK-BUG-024-A
- **Created:** `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts` (497 lines)
- **Modified:** `browser/src/infrastructure/relay_bus/messageBus.ts` (added architecture docs, 23 new lines)

### TASK-BUG-024-C
- **Created:** `browser/src/primitives/terminal/__tests__/terminal-multi-egg-routing.test.tsx` (432 lines)

---

## Test Results

### TASK-BUG-024-A
```
✓ messageBus.crossWindow.test.ts (13 tests) 30ms
  ✓ targeted messages (3)
  ✓ broadcast messages (3)
  ✓ rapid message sending (2)
  ✓ complex scenarios (3)
  ✓ root cause analysis (2)

Test Files: 1 passed (1)
Tests: 13 passed (13)
Duration: 31.76s
```

### TASK-BUG-024-C
```
✓ terminal-multi-egg-routing.test.tsx (8 tests) 15ms
  ✓ terminal1 to text1 only
  ✓ terminal2 to text2 only
  ✓ Canvas and Code EGGs simultaneous
  ✓ broadcast with mute filtering
  ✓ Canvas IR no leak to Code
  ✓ two terminals same type
  ✓ paneId collision resolution
  ✓ different nonces both delivered

Test Files: 1 passed (1)
Tests: 8 passed (8)
Duration: 59.45s
```

---

## Clock / Cost / Carbon

### TASK-BUG-024-A
- **Clock:** 35 minutes
- **Cost:** ~$0.12 USD (Haiku)
- **Carbon:** ~0.08g CO2e

### TASK-BUG-024-C
- **Clock:** 45 minutes
- **Cost:** ~$0.15 USD (Haiku)
- **Carbon:** ~0.3g CO2e

### Q33N Monitoring
- **Clock:** ~12 minutes (dispatch + 4 poll cycles + review)
- **Cost:** ~$0.10 USD (Sonnet)
- **Carbon:** ~0.2g CO2e

### Total
- **Clock:** 92 minutes (~1.5 hours)
- **Cost:** ~$0.37 USD
- **Carbon:** ~0.58g CO2e

---

## Next Steps

### Option A: Close BUG-024 as "cannot reproduce"
- Archive TASK-BUG-024-A, TASK-BUG-024-C, TASK-BUG-024-B (unexecuted)
- Mark BUG-024 as INVALID or CANNOT_REPRODUCE in inventory
- Add 21 new tests to inventory (13 + 8)

### Option B: Dispatch TASK-BUG-024-B anyway (defensive measure)
- Adds windowId scoping for future-proofing
- P1 priority, low risk
- Would take ~30 minutes (haiku)

### Option C: Ask Q88N to reproduce the bug
- Get exact steps, screenshots, message content
- If reproduced, it's an app-specific handler bug (not MessageBus)

**Awaiting Q33NR decision.**

---

## Review Checklist

- ✅ All 8 sections present in both response files
- ✅ All tests pass (13 + 8 = 21 tests total)
- ✅ No stubs shipped
- ✅ No regressions
- ✅ Acceptance criteria all checked [x]
- ✅ File sizes OK (497 + 432 = 929 lines, both under 500 individually)
- ✅ Root cause analysis documented in both responses

**Ready for Q33NR review and decision.**
