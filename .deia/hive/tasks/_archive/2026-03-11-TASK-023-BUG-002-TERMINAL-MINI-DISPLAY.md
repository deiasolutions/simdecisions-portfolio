# TASK-023: Fix BUG-002 — Terminal Mini-Display Echoing Full Chat Content

**Date:** 2026-03-11
**Priority:** P1
**Component:** terminal
**Assigned to:** BEE (any model)
**Your role:** BEE — Write code, run tests, report results.

---

## Problem Statement

In chat mode (`routeTarget: 'ai'`, used by chat.egg.md), the terminal pane shows:
1. **Full LLM response text** in `<ResponseContent>` blocks (duplicates what's in the text-pane) ❌
2. The `hive> thinking...` spinner during API calls ✅ (this is fine)
3. User input entries are hidden (via `hidden: true` flag) ✅ (this works)

The terminal in chat mode should be a **status display**, not a duplicate chat window. The full response text clutters it.

**Expected behavior in chat mode (`routeTarget === 'ai'`):**
- Terminal shows: spinner while waiting, **metrics only** after response (clock/cost/carbon), system messages, errors
- Terminal does NOT show: full LLM response text (that's in the text-pane)
- User input entries remain hidden (already implemented via `hidden` flag)

**Non-chat mode (`routeTarget === 'shell'`):**
- Behavior unchanged — full response renders in terminal as before

---

## Files to Modify

All paths are absolute:

1. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`**
   Lines 334-356: `handleSubmit()` function, chat mode branch. Modify response entry creation.

2. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`**
   Lines 19-24: `TerminalEntry` union type. May need a new entry type or flag.

3. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\TerminalOutput.tsx`**
   Lines 74-123: `TerminalLine` component. Modify response rendering logic.

4. **`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\TerminalOutput.test.tsx`**
   Add tests for chat-mode vs non-chat-mode rendering.

---

## Constraints

1. **Response entries MUST still store full content** for conversation history building (lines 268-276 of `useTerminal.ts` build LLM context from entries). Only the **rendering** changes, not the data structure.
2. **Do NOT break non-chat mode.** `routeTarget === 'shell'` must continue rendering full responses in terminal.
3. **Reuse existing patterns:** The `hidden` flag pattern (used on input entries) is a good model. Consider adding a `metricsOnly` or `hideContent` flag to response entries in chat mode.

---

## Implementation Guidance

### Step 1: Add a Flag to Response Entries (Option A)

Extend the `TerminalEntry` response type to include an optional flag:

```typescript
// types.ts, line 22
| { type: 'response'; content: string; metrics?: TerminalMetrics; timestamp?: string; metricsOnly?: boolean }
```

### Step 2: Set the Flag in Chat Mode

In `useTerminal.ts`, line 353:

```typescript
// Before:
setEntries((prev) => [...prev, { type: 'response', content: displayContent, metrics, timestamp: responseTimestamp }]);

// After (chat mode only):
setEntries((prev) => [...prev, {
  type: 'response',
  content: displayContent,  // full content stored for history
  metrics,
  timestamp: responseTimestamp,
  metricsOnly: true  // flag to suppress content rendering
}]);
```

**Important:** This change should ONLY apply inside the `if (isChatMode && chatTargetId)` block (line 340). The `else` block (line 354) should NOT set `metricsOnly`, so non-chat mode continues showing full content.

### Step 3: Update TerminalOutput Rendering

In `TerminalOutput.tsx`, line 90-101 (response case):

```typescript
case 'response':
  // In chat mode with metricsOnly flag, skip ResponseContent rendering
  const showContent = !('metricsOnly' in entry && entry.metricsOnly);
  return (
    <div className="terminal-response">
      {showContent && (
        <ResponseContent
          content={entry.content}
          onOpenInDesigner={onOpenInDesigner}
          onCopy={onCopy}
          onDownload={onDownload}
        />
      )}
      {entry.metrics && <div className="terminal-metrics">{formatMetrics(entry.metrics)}</div>}
    </div>
  );
```

### Step 4: Write Tests

Add to `TerminalOutput.test.tsx`:

```typescript
describe('TerminalOutput chat mode rendering', () => {
  it('shows metrics only when metricsOnly flag is true', () => {
    const entries = [
      {
        type: 'response' as const,
        content: 'Full LLM response text here',
        metrics: { clock_ms: 1200, cost_usd: 0.002, carbon_g: 0.0005, input_tokens: 100, output_tokens: 50, model: 'haiku' },
        metricsOnly: true
      }
    ];
    const { container } = render(<TerminalOutput entries={entries} ... />);

    // Metrics should be visible
    expect(container.querySelector('.terminal-metrics')).toBeInTheDocument();

    // Content should NOT be visible
    expect(container.querySelector('.terminal-response-content')).not.toBeInTheDocument();
  });

  it('shows full content when metricsOnly flag is false or missing', () => {
    const entries = [
      { type: 'response' as const, content: 'Full response', metrics: {...}, metricsOnly: false }
    ];
    const { container } = render(<TerminalOutput entries={entries} ... />);

    // Both metrics AND content should be visible
    expect(container.querySelector('.terminal-metrics')).toBeInTheDocument();
    expect(container.querySelector('.terminal-response-content')).toBeInTheDocument();
  });
});
```

---

## Alternative Approach (Option B): New Entry Type

If you prefer, you can create a new entry type instead of a flag:

```typescript
// types.ts
| { type: 'metrics'; metrics: TerminalMetrics; timestamp?: string }
```

Then in `useTerminal.ts`, line 353 (chat mode):

```typescript
setEntries((prev) => [...prev,
  { type: 'response', content: displayContent, metrics, timestamp: responseTimestamp },  // stored for history
  { type: 'metrics', metrics, timestamp: responseTimestamp }  // visual entry
]);
```

But this feels like over-engineering. **Option A (flag) is preferred** because it keeps the entry count 1:1 with API calls.

---

## Acceptance Criteria

Mark each as `[x]` when verified:

- [ ] Chat mode: terminal shows metrics line after LLM response, NOT full response text
- [ ] Chat mode: terminal shows spinner during API call
- [ ] Chat mode: terminal shows system messages and errors
- [ ] Chat mode: conversation history still works (entries still contain content for context building)
- [ ] Non-chat mode: full response renders in terminal (unchanged)
- [ ] Tests cover both chat-mode and non-chat-mode rendering
- [ ] All existing terminal tests still pass (run `cd browser && npx vitest run`)

---

## Test Command

```bash
cd browser && npx vitest run src/primitives/terminal/__tests__/TerminalOutput.test.tsx
```

---

## Verification Steps

1. Run the chat.egg.md product in browser (pane layout: tree-browser | text-pane | terminal)
2. Submit a chat message (e.g., "hello")
3. Verify:
   - Terminal shows spinner during API call
   - Terminal shows metrics line after response (clock, cost, carbon)
   - Terminal does NOT show full response text
   - Text-pane shows full response text
4. Switch to non-chat mode (create a shell.egg.md or use `routeTarget: 'shell'` in terminal config)
5. Verify: Terminal shows full response text as before

---

## Reporting

When done, create:
**`C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260311-TASK-023-RESPONSE.md`**

Follow the 8-section format from `.deia/BOOT.md`:

1. Files Modified
2. What Was Done
3. Test Results
4. Build Verification
5. Acceptance Criteria
6. Clock / Cost / Carbon
7. Issues / Follow-ups
8. Commit (format: `[BEE-XXX] TASK-023: fix terminal mini-display for chat mode`)

---

## Context

- The chat.egg.md uses a 3-pane layout: tree-browser (sidebar), text-pane (center), terminal (right).
- In chat mode, the terminal routes user input to the text-pane via `terminal:text-patch` bus messages.
- The terminal is currently duplicating the LLM response: once in the text-pane (via bus message), once in the terminal (via response entry).
- The terminal in chat mode should act as a **status bar**, showing only system feedback (spinner, metrics, errors).
- The `hidden` flag on input entries (line 21 of types.ts) is a precedent for conditional rendering.

---

## Notes

- Do NOT modify the text-pane component in this task. That's BUG-001.
- Do NOT change the bus message routing. The `terminal:text-patch` system is working correctly.
- The response entry is added in TWO places in `handleSubmit()`: inside the `if (isChatMode)` block (line 353) and in the `else` block (line 355). Make sure your change only affects the chat mode branch.
