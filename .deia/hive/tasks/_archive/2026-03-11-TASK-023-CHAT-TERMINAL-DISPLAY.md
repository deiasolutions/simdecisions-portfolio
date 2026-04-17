# TASK-023: Fix Chat Mode Terminal Display

**Assigned to:** BEE-SONNET
**Priority:** P1
**Created:** 2026-03-11
**Dependencies:** None

---

## Objective

Fix BUG-002: In chat mode (Chat EGG: `routeTarget: "ai"`, `links.to_text: "chat-output"`), the terminal currently shows:
1. The user's prompt (echo) — should NOT appear
2. The full LLM response content — should NOT appear

The terminal should show ONLY:
1. The LLM's optional `to_terminal` message (short status or acknowledgment)
2. Status metrics (one line with token count, cost, clock, carbon)

---

## Context

The Chat EGG uses a terminal primitive in `routeTarget: "ai"` mode. User input and AI responses go to the text-pane (`chat-output`) via bus messages. The terminal should show only a lightweight status display, not full conversation echoes.

The code has `isChatMode` logic (useTerminal.ts:246) that sets `hidden: true` on input entries and `metricsOnly: true` on response entries. TerminalOutput.tsx checks these flags (line 43 for hidden, line 91 for metricsOnly).

**The bug:** At runtime, either `isChatMode` evaluates false (one of the four conditions failing) OR the rendering path doesn't respect the flags.

---

## Root Cause Investigation

### Step 1: Trace `isChatMode` Evaluation

File: `browser/src/primitives/terminal/useTerminal.ts:246`

```typescript
const isChatMode = routeTarget === 'ai' && bus && nodeId && links.to_text;
```

Verify at runtime:
1. `routeTarget` is `'ai'` (from EGG config)
2. `bus` is truthy (passed from TerminalAdapter)
3. `nodeId` is truthy (paneId from AppFrame)
4. `links.to_text` is truthy (from EGG config `links: { to_text: "chat-output" }`)

**Hypothesis:** One of these conditions may be falsy at the moment the input/response entries are created.

**Debug task:** Add temporary `console.log` inside `handleSubmit` (line 246) to verify all four values:
```typescript
console.log('[useTerminal] isChatMode check:', { routeTarget, bus: !!bus, nodeId, links_to_text: links.to_text, isChatMode });
```

If `isChatMode` is `false`, identify which condition is failing.

### Step 2: Verify Flag Application

If `isChatMode` is `true`, verify the flags are set correctly:

**Input entry (line 268):**
```typescript
setEntries((prev) => [...prev, { type: 'input', content: text, timestamp: now, hidden: true }]);
```

**Response entry (line 353):**
```typescript
setEntries((prev) => [...prev, { type: 'response', content: displayContent, metrics, timestamp: responseTimestamp, metricsOnly: true }]);
```

Verify these lines execute when `isChatMode` is `true`.

### Step 3: Verify Rendering Checks

File: `browser/src/primitives/terminal/TerminalOutput.tsx`

**Line 43:** Check `hidden` flag
```typescript
if ('hidden' in entry && entry.hidden) return null;
```

**Line 91:** Check `metricsOnly` flag
```typescript
const showContent = !('metricsOnly' in entry && entry.metricsOnly);
```

Verify these checks are executed and respected.

**Debug task:** Add temporary `console.log` in TerminalOutput to trace rendering:
```typescript
// Line 42
{entries.map((entry, idx) => {
  console.log('[TerminalOutput] rendering entry:', entry.type, { hidden: entry.hidden, metricsOnly: entry.metricsOnly });
  if ('hidden' in entry && entry.hidden) return null;
  // ...
```

---

## New Feature: `to_terminal` Envelope Slot

The `TerminalEnvelope` type currently has no `to_terminal` slot. Add it:

**File:** `browser/src/services/terminal/types.ts:52`

**Current:**
```typescript
export interface TerminalEnvelope {
  to_user: string;
  to_text?: TextRouteItem[];
  to_explorer?: ExplorerRoute;
  to_ir?: Record<string, unknown>;
  to_simulator?: SimulatorRoute;
  to_bus?: BusMessage[];
}
```

**Add:**
```typescript
export interface TerminalEnvelope {
  to_user: string;
  to_terminal?: string;  // Optional short message for terminal display in chat mode
  to_text?: TextRouteItem[];
  to_explorer?: ExplorerRoute;
  to_ir?: Record<string, unknown>;
  to_simulator?: SimulatorRoute;
  to_bus?: BusMessage[];
}
```

### Rendering `to_terminal`

The envelope router (terminalResponseRouter.ts) does NOT need to route `to_terminal` — the terminal reads it directly from the parsed envelope in useTerminal.ts.

**File:** `browser/src/primitives/terminal/useTerminal.ts`

**After parsing envelope (around line 309):**
```typescript
const { envelope, parseError } = routeEnvelope(rawContent, {
  bus,
  fromPaneId: nodeId,
  paneRegistry,
});
if (parseError) {
  console.warn('[useTerminal] Envelope parse issue:', parseError);
}
displayContent = envelope.to_user;
```

**Add:**
```typescript
// Extract to_terminal for chat mode
const terminalMessage = envelope.to_terminal || null;
```

**When creating response entry (line 353):**
```typescript
if (isChatMode && chatTargetId) {
  // Send to_user to text-pane
  bus.send({
    type: 'terminal:text-patch',
    sourcePane: nodeId,
    target: chatTargetId,
    nonce: `${Date.now()}-${Math.random()}`,
    timestamp: responseTimestamp,
    data: {
      format: 'markdown',
      ops: [{ op: 'append', content: `**${metrics.model}:** ${displayContent}\n\n` }],
    },
  });

  // Terminal shows to_terminal message (if present) + metrics
  setEntries((prev) => [
    ...prev,
    {
      type: 'response',
      content: displayContent,
      metrics,
      timestamp: responseTimestamp,
      metricsOnly: true,
      terminalMessage  // NEW: store to_terminal for display
    }
  ]);
} else {
  // Non-chat mode: show full response
  setEntries((prev) => [...prev, { type: 'response', content: displayContent, metrics, timestamp: responseTimestamp }]);
}
```

**Update TerminalEntry type (browser/src/primitives/terminal/types.ts:22):**

**Current:**
```typescript
| { type: 'response'; content: string; metrics?: TerminalMetrics; timestamp?: string; metricsOnly?: boolean }
```

**Add `terminalMessage`:**
```typescript
| { type: 'response'; content: string; metrics?: TerminalMetrics; timestamp?: string; metricsOnly?: boolean; terminalMessage?: string | null }
```

**Rendering in TerminalOutput.tsx (line 90):**

**Current:**
```typescript
case 'response':
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

**Add:**
```typescript
case 'response':
  const showContent = !('metricsOnly' in entry && entry.metricsOnly);
  return (
    <div className="terminal-response">
      {entry.terminalMessage && (
        <div className="terminal-system">{entry.terminalMessage}</div>
      )}
      {showContent && (
        <ResponseContent
          content={entry.content}
          onOpenInDesigner={onOpenInDesigner}
          onCopy={onCopy}
          onDownload={onDownload}
        />
      )}
      {entry.metrics && <div className="terminal-metrics">{formatChatMetrics(entry.metrics, entry.metricsOnly)}</div>}
    </div>
  );
```

---

## Metrics Format Change for Chat Mode

**Current format (terminalService.ts:80):**
```typescript
export function formatMetrics(m: TerminalMetrics): string {
  const clock = m.clock_ms < 1000 ? `${m.clock_ms}ms` : `${(m.clock_ms / 1000).toFixed(1)}s`;
  const cost = `$${m.cost_usd.toFixed(4)}`;
  const carbon = m.carbon_g < 1 ? `${m.carbon_g.toFixed(4)}g` : `${m.carbon_g.toFixed(2)}g`;
  return `clock: ${clock} | cost: ${cost} | carbon: ${carbon}`;
}
```

**Output:** `clock: 1.2s | cost: $0.0034 | carbon: 0.0023g`

**For chat mode, add token count:**

**New function (add to terminalService.ts):**
```typescript
export function formatChatMetrics(m: TerminalMetrics, chatMode: boolean = false): string {
  if (!chatMode) {
    return formatMetrics(m); // Use existing format for non-chat mode
  }

  const totalTokens = m.input_tokens + m.output_tokens;
  const clock = m.clock_ms < 1000 ? `${m.clock_ms}ms` : `${(m.clock_ms / 1000).toFixed(1)}s`;
  const cost = `$${m.cost_usd.toFixed(4)}`;
  const carbon = m.carbon_g < 1 ? `${m.carbon_g.toFixed(4)}g` : `${m.carbon_g.toFixed(2)}g`;

  return `Response received, ${totalTokens} tokens, ${cost} | clock: ${clock} | carbon: ${carbon}`;
}
```

**Output:** `Response received, 847 tokens, $0.003 | clock: 1.2s | carbon: 0.0023g`

**Update TerminalOutput.tsx line 102:**

**Current:**
```typescript
{entry.metrics && <div className="terminal-metrics">{formatMetrics(entry.metrics)}</div>}
```

**New:**
```typescript
{entry.metrics && <div className="terminal-metrics">{formatChatMetrics(entry.metrics, entry.metricsOnly || false)}</div>}
```

**Import at top of TerminalOutput.tsx:**
```typescript
import { extractJsonBlocks, isValidIR, formatMetrics, formatChatMetrics } from '../../services/terminal';
```

---

## Files to Modify

| File | Action | Changes |
|------|--------|---------|
| `browser/src/services/terminal/types.ts` | **EDIT** | Add `to_terminal?: string` to TerminalEnvelope (line 52) |
| `browser/src/primitives/terminal/types.ts` | **EDIT** | Add `terminalMessage?: string \| null` to response TerminalEntry (line 22) |
| `browser/src/primitives/terminal/useTerminal.ts` | **EDIT** | Extract `to_terminal` from envelope, pass to response entry (line 309+) |
| `browser/src/primitives/terminal/TerminalOutput.tsx` | **EDIT** | Render `terminalMessage` if present (line 90), use `formatChatMetrics` |
| `browser/src/services/terminal/terminalService.ts` | **EDIT** | Add `formatChatMetrics()` function, export it |
| `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx` | **EDIT** | Add test for `to_terminal` display, update metrics tests |

---

## Test Requirements (TDD — Write Tests First)

### New Tests

Add to `TerminalOutput.test.tsx`:

1. **`to_terminal` message display (chat mode)**:
   ```typescript
   it('displays to_terminal message when present in chat mode', () => {
     const entries: TerminalEntry[] = [
       {
         type: 'response',
         content: 'Full response',
         metrics: {
           clock_ms: 1200,
           cost_usd: 0.002,
           carbon_g: 0.0005,
           input_tokens: 100,
           output_tokens: 50,
           model: 'haiku',
         },
         metricsOnly: true,
         terminalMessage: 'Working on it...',
       },
     ];

     render(
       <TerminalOutput
         entries={entries}
         loading={false}
         onOpenInDesigner={mockOnOpenInDesigner}
         onCopy={mockOnCopy}
         onDownload={mockOnDownload}
       />
     );

     // to_terminal message should be visible
     expect(screen.getByText('Working on it...')).toBeInTheDocument();

     // Full content should NOT be visible (metricsOnly mode)
     expect(screen.queryByText('Full response')).not.toBeInTheDocument();
   });
   ```

2. **Chat mode metrics format includes token count**:
   ```typescript
   it('formats metrics with token count in chat mode', () => {
     const entries: TerminalEntry[] = [
       {
         type: 'response',
         content: 'Response',
         metrics: {
           clock_ms: 1500,
           cost_usd: 0.003,
           carbon_g: 0.0008,
           input_tokens: 500,
           output_tokens: 347,
           model: 'haiku',
         },
         metricsOnly: true,
       },
     ];

     render(
       <TerminalOutput
         entries={entries}
         loading={false}
         onOpenInDesigner={mockOnOpenInDesigner}
         onCopy={mockOnCopy}
         onDownload={mockOnDownload}
       />
     );

     // Should show token count + cost + clock + carbon
     expect(screen.getByText(/Response received, 847 tokens/)).toBeInTheDocument();
     expect(screen.getByText(/\$0\.003/)).toBeInTheDocument();
   });
   ```

3. **Non-chat mode still uses old metrics format**:
   ```typescript
   it('uses standard metrics format in non-chat mode', () => {
     const entries: TerminalEntry[] = [
       {
         type: 'response',
         content: 'Response',
         metrics: {
           clock_ms: 1200,
           cost_usd: 0.002,
           carbon_g: 0.0005,
           input_tokens: 100,
           output_tokens: 50,
           model: 'haiku',
         },
         metricsOnly: false,
       },
     ];

     render(
       <TerminalOutput
         entries={entries}
         loading={false}
         onOpenInDesigner={mockOnOpenInDesigner}
         onCopy={mockOnCopy}
         onDownload={mockOnDownload}
       />
     );

     // Should use old format (no token count)
     expect(screen.getByText(/clock: 1200ms | cost: \$0\.0020 | carbon:/)).toBeInTheDocument();
   });
   ```

4. **Hidden input entries do not render**:
   ```typescript
   it('does not render input entry when hidden flag is true', () => {
     const entries: TerminalEntry[] = [
       { type: 'input', content: 'Hidden user input', hidden: true },
     ];

     const { container } = render(
       <TerminalOutput
         entries={entries}
         loading={false}
         onOpenInDesigner={mockOnOpenInDesigner}
         onCopy={mockOnCopy}
         onDownload={mockOnDownload}
       />
     );

     expect(screen.queryByText('Hidden user input')).not.toBeInTheDocument();
   });
   ```

### Existing Tests

All existing TerminalOutput tests must pass:
- Lines 239-334: `metricsOnly` flag tests (already exist and should pass)
- Other rendering tests

---

## Debug Plan (Step-by-Step)

Since the root cause is unknown, follow this sequence:

### Phase 1: Diagnose `isChatMode` Evaluation

1. Add temporary debug logs to `useTerminal.ts:246`:
   ```typescript
   console.log('[useTerminal] isChatMode check:', {
     routeTarget,
     bus: !!bus,
     nodeId,
     links_to_text: links.to_text,
     isChatMode
   });
   ```

2. Run the Chat EGG in dev mode
3. Submit a test message
4. Check browser console — is `isChatMode` true or false?

**If `isChatMode` is false:**
- Identify which condition failed
- Check EGG config wiring in `terminalAdapter.tsx` and `TerminalApp.tsx`
- Fix the wiring issue

**If `isChatMode` is true:**
- Proceed to Phase 2

### Phase 2: Verify Flag Application

1. Add temporary debug logs to `useTerminal.ts:268` and `useTerminal.ts:353`:
   ```typescript
   // Line 268 (input entry)
   console.log('[useTerminal] Adding input entry, isChatMode:', isChatMode, 'hidden:', isChatMode);

   // Line 353 (response entry)
   console.log('[useTerminal] Adding response entry, isChatMode:', isChatMode, 'metricsOnly:', isChatMode);
   ```

2. Submit a test message
3. Check console — are the flags set correctly?

**If flags are set correctly:**
- Proceed to Phase 3

**If flags are NOT set:**
- Fix the conditional logic in `handleSubmit`

### Phase 3: Verify Rendering Checks

1. Add temporary debug logs to `TerminalOutput.tsx:42` and `TerminalOutput.tsx:91`:
   ```typescript
   // Line 42
   {entries.map((entry, idx) => {
     console.log('[TerminalOutput] entry:', entry.type, {
       hidden: 'hidden' in entry ? entry.hidden : 'N/A',
       metricsOnly: 'metricsOnly' in entry ? entry.metricsOnly : 'N/A'
     });
     if ('hidden' in entry && entry.hidden) return null;
     // ...
   })}

   // Line 91
   const showContent = !('metricsOnly' in entry && entry.metricsOnly);
   console.log('[TerminalOutput] response entry, metricsOnly:', entry.metricsOnly, 'showContent:', showContent);
   ```

2. Submit a test message
3. Check console — are the flags respected during rendering?

**If flags are respected:**
- The bug is elsewhere (state update timing issue?)

**If flags are NOT respected:**
- Fix the rendering checks

### Phase 4: Clean Up Debug Logs

After identifying and fixing the root cause, remove all temporary `console.log` statements.

---

## Constraints (Hard Rules)

1. **No file over 500 lines.**
2. **TDD**: Write tests first, then implementation.
3. **No stubs**: Every function fully implemented.
4. **CSS variables only**: No hardcoded colors in any CSS changes.

---

## Verification Checklist

After implementation, verify:

- [ ] `isChatMode` evaluates correctly in Chat EGG
- [ ] Input entries have `hidden: true` in chat mode
- [ ] Response entries have `metricsOnly: true` in chat mode
- [ ] Hidden input entries do NOT render
- [ ] Response entries in chat mode show only metrics (no full content)
- [ ] `to_terminal` message displays if present
- [ ] Chat mode metrics include token count
- [ ] Non-chat mode metrics use old format
- [ ] All existing tests pass
- [ ] New tests pass (at least 4 new test cases)
- [ ] No console errors or warnings
- [ ] Manual test in Chat EGG: user input goes to text-pane, terminal shows only metrics

---

## Definition of Done

1. `TerminalEnvelope` has `to_terminal?: string` field
2. `TerminalEntry` response type has `terminalMessage?: string | null` field
3. `formatChatMetrics()` function added to terminalService.ts
4. Chat mode (`isChatMode`) correctly evaluates at runtime
5. Input entries hidden in chat mode
6. Response entries show only metrics (and optional `to_terminal` message) in chat mode
7. Metrics in chat mode include token count
8. All tests pass (existing + new)
9. No stubs, no TODOs
10. Manually verified in Chat EGG: terminal shows lightweight status, text-pane shows full conversation

---

## Q&A

**Q: What if `to_terminal` is an empty string?**
A: Treat as falsy — don't render an empty system line. Check `if (entry.terminalMessage && entry.terminalMessage.trim())`.

**Q: Should `to_terminal` support markdown?**
A: No. It's a short status message (1-2 sentences). Render as plain text in `.terminal-system` class.

**Q: What if the LLM doesn't include `to_terminal` in the envelope?**
A: That's fine. The field is optional. In chat mode, show only metrics if `to_terminal` is absent.

**Q: Should we update the LLM prompt to teach it about `to_terminal`?**
A: Not in this task. This task is purely browser-side wiring. Prompt updates are a separate task.

---

**END OF TASK-023 SPEC**
