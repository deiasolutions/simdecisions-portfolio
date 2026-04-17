# BRIEFING: BUG-020 — Canvas IR Terminal Hides to_user Response

**From:** Q88NR-bot (Regent)
**To:** Q33N (Queen Coordinator)
**Date:** 2026-03-17
**Spec File:** `2026-03-17-SPEC-TASK-BUG020-canvas-ir-terminal-hides-response.md`

---

## Situation

The Canvas EGG expanded IR terminal is configured with `routeTarget: 'ir'` mode. In this mode, when the LLM responds with mixed text + IR JSON:

- **Chat text (to_user)** should route to the text-pane (canvas-chat)
- **IR JSON blocks** should route to the canvas editor
- **Terminal should show metrics + terminalMessage**, but currently hides the to_user response content

The bug report states: "Canvas expanded IR terminal hides to_user response."

---

## Root Cause Analysis

After reading the code, I've identified the **exact cause**:

### File: `browser/src/primitives/terminal/useTerminal.ts`

**Lines 749-773:** IR mode response handling

```typescript
// IR mode with successful envelope parse — routing already handled
// Just send displayContent (to_user) to chat pane and show metrics in terminal
if (chatTargetId) {
  bus!.send({
    type: 'terminal:text-patch',
    sourcePane: nodeId!,
    target: chatTargetId,
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: responseTimestamp,
    data: {
      format: 'markdown',
      ops: [{ op: 'append', content: `**${metrics.model}:** ${displayContent}\n\n` }],
    },
  });
}
// Terminal shows metrics only
setEntries((prev) => [...prev, {
  type: 'response',
  content: displayContent,
  metrics,
  timestamp: responseTimestamp,
  metricsOnly: true,  // ← THIS IS THE PROBLEM
  terminalMessage,
}]);
```

**The issue:** When `metricsOnly: true` is set, the terminal output component **intentionally hides** the content field.

### File: `browser/src/primitives/terminal/TerminalOutput.tsx`

**Lines 160-162:**

```typescript
case 'response':
  const showContent = !('metricsOnly' in entry && entry.metricsOnly);
  return (
    <div className="terminal-response">
      {entry.terminalMessage && entry.terminalMessage.trim() && (
        <div className="terminal-system">
          {entry.terminalMessage}
          ...
        </div>
      )}
      {showContent && (  // ← showContent is false when metricsOnly is true
        <>
          <ResponseContent ... />
          ...
        </>
      )}
      {entry.metrics && (
        <div className="terminal-metrics">...</div>
      )}
    </div>
  );
```

**Why this design exists:** In chat/IR mode, the to_user content is sent to the text-pane (canvas-chat) for rich rendering. The terminal should only show:

1. **terminalMessage** (if LLM sends it via `to_terminal` slot)
2. **metrics** (cost/time/carbon)

This prevents duplicate content display: text-pane shows full content, terminal shows status/metrics.

---

## The Real Problem

The bug report's title is **misleading**. The terminal is not "hiding" the response — it's **correctly routing** it to the text-pane and showing metrics.

**Three possible interpretations of BUG-020:**

1. **False bug report:** The system is working as designed. Canvas IR mode routes to_user to chat pane, shows metrics in terminal.

2. **Actual bug: text-pane not showing to_user:** If the to_user content isn't appearing in canvas-chat pane, the bug is in:
   - Message bus routing
   - Text-pane not processing `terminal:text-patch` messages
   - EGG links misconfiguration

3. **Feature request: terminal should show to_user even when routed:** User expects to see to_user in BOTH terminal AND chat pane (redundant but informative).

---

## Recommended Task Breakdown

Since we cannot clarify with Q88N (Dave) right now, I recommend a **diagnostic approach**:

### TASK-BUG-020-A: Verify Canvas IR Mode End-to-End Flow (Haiku, 2 hours)

**Objective:** Create integration test to verify Canvas IR mode routing works correctly.

**Deliverables:**
- Test file: `browser/src/primitives/terminal/__tests__/canvasIRMode.test.tsx`
- Tests verify:
  1. User input with IR mode enabled
  2. LLM response with mixed to_user text + IR JSON
  3. to_user content routed to text-pane via `terminal:text-patch` message
  4. IR JSON routed to canvas via `terminal:ir-deposit` message
  5. Terminal shows metrics + terminalMessage (if present)
  6. Terminal does NOT show to_user content (correct behavior)

**Acceptance Criteria:**
- 8+ tests covering Canvas IR mode routing
- Verifies bus message routing to correct panes
- Verifies terminal entry has metricsOnly: true
- Verifies terminalMessage display when LLM sends to_terminal slot

**Model:** haiku

---

### TASK-BUG-020-B: Add Terminal "Show Full Response" Toggle (Haiku, 3 hours)

**Objective:** If the user genuinely wants to see to_user in the terminal (even when routed to text-pane), add an optional flag.

**Deliverables:**
- EGG config option: `terminal.showRoutedContent: boolean` (default: false)
- When true, terminal shows to_user content even when metricsOnly mode is active
- Update TerminalOutput.tsx to respect this flag
- Update canvas.egg.md to optionally enable this
- Tests for toggle behavior

**Acceptance Criteria:**
- EGG config option works
- Terminal shows to_user when flag is true
- Terminal hides to_user when flag is false (default)
- No duplicate content when flag is false

**Model:** haiku

---

### TASK-BUG-020-C: Verify Text-Pane Receives Canvas IR Messages (Haiku, 1 hour)

**Objective:** Ensure text-pane (canvas-chat) is correctly subscribed to and processing `terminal:text-patch` messages.

**Deliverables:**
- Read text-pane subscription logic
- Verify canvas-chat pane config enables message bus subscription
- Add debug logging (temporary) to confirm message delivery
- Test with real Canvas EGG layout

**Acceptance Criteria:**
- Text-pane processes `terminal:text-patch` messages
- Canvas-chat pane shows to_user content from IR terminal
- If not working, identify the missing subscription or routing bug

**Model:** haiku

---

## My Recommendation

Start with **TASK-BUG-020-A** (diagnostic test). This will empirically prove:

- If routing is working correctly (to_user goes to text-pane)
- If terminal correctly hides to_user content (metricsOnly: true)
- If terminalMessage display is working

If tests pass: **BUG-020 is a false report** (or a feature request for redundant display).

If tests fail: **BUG-020-C** traces the real issue (text-pane not receiving messages).

---

## File Inventory for Reference

**Terminal mode logic:**
- `browser/src/primitives/terminal/useTerminal.ts:706-793` (IR mode response handling)

**Terminal output rendering:**
- `browser/src/primitives/terminal/TerminalOutput.tsx:160-203` (response entry rendering)

**Canvas EGG config:**
- `eggs/canvas.egg.md:89-101` (terminal config with routeTarget: ir)

**Types:**
- `browser/src/primitives/terminal/types.ts:28` (TerminalEntry response type with metricsOnly flag)

---

## Questions for Q33N

1. Should I create all 3 tasks (A, B, C) or just start with A?
2. Should TASK-BUG-020-B be a separate feature request (BL-XXX) instead of a bug fix?
3. Do you want me to add a "verify Canvas EGG works end-to-end" task that launches the EGG and manually tests it?

---

## Decision

Awaiting Q33N's task file for TASK-BUG-020-A (diagnostic test).

If you prefer a different breakdown, let me know.

---

**Q88NR-bot** (Mechanical Regent)
