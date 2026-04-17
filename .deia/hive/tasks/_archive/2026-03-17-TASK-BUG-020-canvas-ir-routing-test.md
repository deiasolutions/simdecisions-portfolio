# TASK-BUG-020: Canvas IR Mode End-to-End Routing Test

**ID:** TASK-BUG-020
**Type:** Diagnostic Test (Bug Investigation)
**Priority:** P1
**Model:** haiku
**Estimated Time:** 2-3 hours
**Status:** READY FOR DISPATCH
**Created:** 2026-03-17
**Coordinator:** Q33N
**Regent Briefing:** `.deia/hive/coordination/2026-03-17-BRIEFING-BUG-020-canvas-ir-terminal-hides-response.md`

---

## Objective

Create comprehensive integration test to verify Canvas IR mode routing works correctly end-to-end. This will empirically prove whether BUG-020 is a real bug or false report.

**Root Question:** When Canvas terminal is in IR mode and LLM sends mixed `to_user` text + IR JSON:
- Does `to_user` content correctly route to text-pane (canvas-chat)?
- Does terminal correctly show only metrics + terminalMessage?
- Is the text-pane receiving and processing the messages?

---

## Background

### Current Behavior (from code analysis)

**File:** `browser/src/primitives/terminal/useTerminal.ts:749-773`

When IR mode response is parsed:
1. `to_user` content sent to text-pane via `terminal:text-patch` message
2. IR JSON sent to canvas via `terminal:ir-deposit` message
3. Terminal entry created with `metricsOnly: true`

**File:** `browser/src/primitives/terminal/TerminalOutput.tsx:160-162`

Terminal rendering:
- Shows `terminalMessage` (if LLM sends it via `to_terminal` slot)
- Shows `metrics` (cost/time/carbon)
- Hides `to_user` content when `metricsOnly: true`

**This is intentional design** to prevent duplicate content (text-pane shows full content, terminal shows status).

### The Bug Report Claims

"Canvas expanded IR terminal hides to_user response."

**Three possibilities:**
1. **False report:** System working as designed (text-pane shows content, terminal shows metrics)
2. **Real bug:** Text-pane NOT receiving `terminal:text-patch` messages (routing failure)
3. **Feature request:** User wants to_user in BOTH terminal AND text-pane (redundant display)

---

## Deliverables

### 1. Integration Test File

**File:** `browser/src/primitives/terminal/__tests__/canvasIRMode.test.tsx`

**Test Coverage (minimum 8 tests):**

#### Routing Tests
1. **to_user routes to text-pane**
   - User sends command in IR mode
   - LLM responds with to_user text + IR JSON
   - Verify `terminal:text-patch` message sent to correct paneId
   - Verify message contains to_user content

2. **IR JSON routes to canvas**
   - Verify `terminal:ir-deposit` message sent
   - Verify message contains IR JSON payload

3. **Terminal entry has metricsOnly flag**
   - Verify terminal entry created with `metricsOnly: true`
   - Verify entry has metrics object
   - Verify entry has to_user content (but hidden)

#### Terminal Display Tests
4. **Terminal shows metrics**
   - Verify metrics rendered in terminal output
   - Verify format: model name, cost, time, carbon

5. **Terminal shows terminalMessage when present**
   - LLM response includes `to_terminal` slot
   - Verify terminalMessage displayed in terminal
   - Verify styling (terminal-system class)

6. **Terminal hides to_user content**
   - Verify to_user content NOT rendered in terminal
   - Verify ResponseContent component not rendered when metricsOnly: true

#### Text-Pane Integration Tests
7. **Text-pane subscription to terminal:text-patch**
   - Mock text-pane as message bus subscriber
   - Verify text-pane receives `terminal:text-patch` message
   - Verify message data structure

8. **Multi-pane routing isolation**
   - Canvas EGG has terminal + text-pane + canvas
   - Verify to_user only goes to text-pane (not canvas)
   - Verify IR JSON only goes to canvas (not text-pane)

#### Edge Cases
9. **to_user with no IR JSON**
   - Response has only to_user content
   - Verify routing still works
   - Verify terminal shows metrics

10. **IR JSON with no to_user**
    - Response has only IR JSON
    - Verify terminal shows metrics
    - Verify no terminal:text-patch message sent

---

## Test Setup Requirements

### Mock Data

**Canvas EGG layout structure (simplified):**
```typescript
const canvasLayout = {
  type: 'split',
  direction: 'horizontal',
  ratio: 0.18,
  children: [
    {
      type: 'pane',
      app: 'tree-browser',
      id: 'canvas-palette',
      config: { adapter: 'palette' }
    },
    {
      type: 'split',
      direction: 'vertical',
      ratio: 0.82,
      children: [
        { type: 'pane', app: 'canvas', id: 'canvas-editor' },
        {
          type: 'split',
          direction: 'horizontal',
          ratio: 0.65,
          children: [
            {
              type: 'pane',
              app: 'terminal',
              id: 'canvas-terminal',
              config: {
                routeTarget: 'ir',
                linkedPanes: { chat: 'canvas-chat', canvas: 'canvas-editor' }
              }
            },
            {
              type: 'pane',
              app: 'text-pane',
              id: 'canvas-chat',
              config: { renderMode: 'chat' }
            }
          ]
        }
      ]
    }
  ]
};
```

**Mock LLM response with IR:**
```typescript
const mockIRResponse = {
  to_user: "I've created a flow diagram with 3 nodes.",
  ir: {
    format: 'bpmn',
    version: '1.0',
    nodes: [
      { id: 'start', type: 'startEvent', x: 100, y: 100 },
      { id: 'task', type: 'task', label: 'Process', x: 200, y: 100 },
      { id: 'end', type: 'endEvent', x: 300, y: 100 }
    ],
    edges: [
      { from: 'start', to: 'task' },
      { from: 'task', to: 'end' }
    ]
  },
  to_terminal: "Canvas updated with 3 nodes.",
  metrics: {
    model: 'claude-sonnet-4.5',
    input_tokens: 150,
    output_tokens: 75,
    cost_usd: 0.0023,
    duration_ms: 850,
    carbon_g: 0.12
  }
};
```

### Test Helpers

```typescript
function setupCanvasIRMode() {
  const mockBus = {
    send: vi.fn(),
    subscribe: vi.fn()
  };

  const { result } = renderHook(() => useTerminal({
    nodeId: 'canvas-terminal',
    bus: mockBus,
    config: {
      routeTarget: 'ir',
      linkedPanes: { chat: 'canvas-chat', canvas: 'canvas-editor' }
    }
  }));

  return { result, mockBus };
}
```

---

## Acceptance Criteria

### Tests Must Pass
- ✅ All 10+ tests pass
- ✅ No console errors or warnings
- ✅ TypeScript compilation succeeds

### Coverage Verification
- ✅ IR routing logic covered (useTerminal.ts:749-773)
- ✅ Terminal output rendering covered (TerminalOutput.tsx:160-203)
- ✅ Message bus routing verified
- ✅ Text-pane message subscription verified

### Documentation
- ✅ Test file includes inline comments explaining each scenario
- ✅ Mock data clearly labeled
- ✅ Edge cases documented

---

## Success Outcomes

### If All Tests Pass
**Conclusion:** BUG-020 is a **false report**. The system is working as designed:
- Terminal correctly routes to_user to text-pane
- Terminal correctly shows only metrics + terminalMessage
- Text-pane receives and can display the content

**Action:** Q33N closes BUG-020 with status "WORKING_AS_DESIGNED"

### If Text-Pane Routing Tests Fail
**Conclusion:** BUG-020 is a **real bug** in message bus routing or text-pane subscription.

**Action:** Q33N creates follow-up task to fix text-pane message handling.

### If Terminal Display Tests Fail
**Conclusion:** BUG-020 is a **real bug** in terminal rendering logic.

**Action:** Q33N creates follow-up task to fix terminal display.

---

## Files to Read

**Terminal IR mode logic:**
- `browser/src/primitives/terminal/useTerminal.ts:706-793`
- Focus on lines 749-773 (IR response handling)

**Terminal output rendering:**
- `browser/src/primitives/terminal/TerminalOutput.tsx:138-203`
- Focus on lines 160-162 (metricsOnly flag)

**Terminal types:**
- `browser/src/primitives/terminal/types.ts:16-45`
- TerminalEntry response type with metricsOnly field

**Canvas EGG config:**
- `eggs/canvas.egg.md:89-101`
- Terminal config with routeTarget: ir

**Existing terminal tests (for patterns):**
- `browser/src/primitives/terminal/__tests__/terminal-multi-egg-routing.test.tsx`
- `browser/src/primitives/terminal/__tests__/irModeRouting.test.tsx` (if exists)

---

## Test Commands

### Run Tests
```bash
cd browser
npm test -- src/primitives/terminal/__tests__/canvasIRMode.test.tsx
```

### Run with Coverage
```bash
npm test -- --coverage --collectCoverageFrom='src/primitives/terminal/{useTerminal,TerminalOutput}.{ts,tsx}'
```

---

## Notes for Bee

1. **Do NOT modify production code** unless tests reveal an actual bug
2. **Focus on diagnostics first:** What IS the behavior? Is it correct?
3. **Message bus mocking:** Use the patterns from `terminal-multi-egg-routing.test.tsx`
4. **If tests pass:** This confirms working-as-designed. Report back for closure.
5. **If tests fail:** Document WHICH routing is broken (to text-pane or to canvas)

---

## Related Files

**Queue spec:** `.deia/hive/queue/2026-03-17-SPEC-TASK-BUG020-canvas-ir-terminal-hides-response.md`
**Regent briefing:** `.deia/hive/coordination/2026-03-17-BRIEFING-BUG-020-canvas-ir-terminal-hides-response.md`

---

## Q33N Sign-Off

**Status:** READY FOR DISPATCH
**Assigned Model:** haiku
**Expected Completion:** 2-3 hours
**Response File:** `.deia/hive/responses/20260317-TASK-BUG-020-RESPONSE.md`

---

**Q33N** (Queen Coordinator)
2026-03-17
