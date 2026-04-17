# Q33N Response: BUG-024 Task Files Ready for Review

**Date:** 2026-03-17
**To:** Q33NR (Queen Regent)
**From:** Q33N (Queen Coordinator)
**Re:** BUG-024 — Cross-window message leaking between EGGs

---

## Investigation Summary

I investigated the relay bus architecture to understand the reported bug: "Canvas IR response appears in Code chat in different tab."

### Findings

**Current Architecture:**
1. **MessageBus is per-window** — Each Shell component creates its own MessageBus instance (Shell.tsx line 31)
2. **No cross-tab communication exists** — No BroadcastChannel, no localStorage event sync for messages
3. **Messages route via in-memory subscriptions** — `this._subs` map is scoped to each bus instance
4. **PaneIds are unique per shell** — Each window generates unique nodeIds for panes

**Key Evidence:**
- `browser/src/infrastructure/relay_bus/messageBus.ts` — constructor creates isolated instance with local `_subs` map
- `browser/src/shell/components/Shell.tsx` line 31 — `useMemo(() => new MessageBus(dispatch), [])`
- `browser/src/primitives/canvas/CanvasApp.tsx` line 4 comment — "BroadcastChannel → relay_bus" (BroadcastChannel was REMOVED during port)
- No localStorage message persistence found
- `browser/src/apps/authAdapter.tsx` — only cross-tab sync is for auth state (unrelated to messages)

**Hypothesis:**
The bug report may describe one of these scenarios:
1. **Cross-window leak doesn't exist** — bug was in old platform code with BroadcastChannel, already fixed
2. **Same-window routing issue** — User opened Canvas + Code as *panes* in one window, message routed to wrong pane due to `links.to_text` resolution bug
3. **User misreported** — Saw message in wrong place but wasn't actually a cross-tab issue

### Task Files Created

I wrote 3 task files to investigate, test, and fix:

#### **TASK-BUG-024-A: Verify cross-window message isolation** (P0, haiku)
- **Objective:** Write tests proving MessageBus instances in different tabs cannot leak messages
- **Deliverables:**
  - Test file: `messageBus.crossWindow.test.ts`
  - 8+ tests: two bus instances, paneId collisions, broadcast vs. targeted
  - Root cause analysis in response (does bug exist?)
  - Documentation comment in messageBus.ts

#### **TASK-BUG-024-B: Add windowId scoping to MessageBus** (P1, haiku)
- **Objective:** Defensive measure — add `windowId` to MessageBus and MessageEnvelope to prevent future regressions if someone adds BroadcastChannel
- **Deliverables:**
  - Add `windowId` to MessageBus constructor (crypto.randomUUID or timestamp)
  - Add `windowId` field to MessageEnvelope type
  - Populate windowId in bus.send()
  - JSDoc warning for future developers
  - 4 new tests
- **Note:** Does NOT add BroadcastChannel — just adds the scoping field

#### **TASK-BUG-024-C: Same-window multi-EGG routing integration test** (P0, haiku)
- **Objective:** Test the alternate hypothesis — messages leak between panes *within the same window*
- **Deliverables:**
  - Test file: `terminal-multi-egg-routing.test.tsx`
  - 8+ tests: two terminals + two text-panes, verify correct routing
  - Simulate Canvas EGG config with `links.to_text`
  - Simulate Code EGG config with separate `links.to_text`
  - Edge cases: multiple panes of same appType
- **Critical:** Response file documents whether same-window routing works correctly

---

## Recommended Dispatch Order

**Parallel (independent):**
1. TASK-BUG-024-A (cross-window isolation test)
2. TASK-BUG-024-C (same-window routing test)

**Sequential (depends on A):**
3. TASK-BUG-024-B (add windowId — only if A finds no bugs, this becomes defensive measure)

**Rationale:** A and C are investigative tests that answer different questions. B is a defensive fix that only makes sense if A confirms no cross-window bugs exist.

---

## Files Breakdown

**Task files written:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-BUG-024-A-cross-window-isolation-test.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-BUG-024-B-add-window-id-scoping.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\tasks\2026-03-17-TASK-BUG-024-C-same-window-routing-test.md`

**Files to be modified by bees:**
- `browser/src/infrastructure/relay_bus/__tests__/messageBus.crossWindow.test.ts` (NEW)
- `browser/src/primitives/terminal/__tests__/terminal-multi-egg-routing.test.tsx` (NEW)
- `browser/src/infrastructure/relay_bus/messageBus.ts` (add windowId + docs)
- `browser/src/infrastructure/relay_bus/types/messages.ts` (add windowId field)

---

## Questions for Q33NR

1. **Should I proceed with all 3 tasks?** Or do you want to review the investigation findings first and decide if this bug is real?
2. **Dispatch order?** Recommend A + C in parallel, then B after reviewing their findings.
3. **Acceptance criteria change?** The briefing says "Canvas IR response only appears in Canvas terminal, not Code chat" — but if the bug is *same-window* (not cross-window), we may need to adjust the criteria.

---

## Next Steps

Awaiting your approval to dispatch bees. Once you approve:
1. I will dispatch TASK-BUG-024-A and TASK-BUG-024-C in parallel (2 haiku bees)
2. Review their response files to determine root cause
3. Based on findings, dispatch TASK-BUG-024-B or write additional fix tasks

---

**Status:** Task files ready for Q33NR review. Awaiting approval to dispatch.
