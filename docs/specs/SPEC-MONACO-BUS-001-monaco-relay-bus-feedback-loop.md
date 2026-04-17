# SPEC-MONACO-BUS-001: Monaco → relay_bus Feedback Loop

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** INFRA
**T-Shirt Size:** M
**Depends On:** code-editor applet (Monaco, SPECCED), relay_bus (BUILT), prompt service (BUILT),
               AppletShell (SPECCED)

---

## 1. Purpose

This spec defines the relay_bus integration layer for the Monaco code-editor applet. It is
the infrastructure spec behind the IDE-as-agent pattern described in SPEC-CODE-EGG-001.

The code-editor applet (appType: code-editor) already exists in the GC registry. This spec
adds relay_bus emission to it — making every code edit a first-class bus event that any
subscribed component (BEE, log-viewer, test runner, IR process) can react to.

This is deliberately a separate infrastructure spec rather than being buried in the EGG spec
because the Monaco bus integration is reusable. Any EGG that loads `appType: code-editor`
with `emitOnChange: true` gets this behavior, not just code.shiftcenter.com.

---

## 2. Monaco Applet Extension

The existing `code-editor` GC applet is extended with the following config keys:

```typescript
interface CodeEditorConfig {
  // Existing
  language: string | 'auto'
  theme: string | 'auto'

  // New — relay_bus integration
  emitOnChange: boolean             // default: false (opt-in)
  emitDebounceMs: number            // default: 800ms
  emitOnSave: boolean               // default: true (always emits CODE_SAVED on Cmd+S)
  emitSelectionChanges: boolean     // default: false (can be noisy)
  agentNodeId: string | null        // nodeId of pane to receive agent responses
                                    // if null, agent posts to sim-chat channel
  agentChannel: string | null       // sim-chat channel ID for agent responses
}
```

---

## 3. Event Schema

### CODE_CHANGED

Fired on every edit after debounce window. The core event.

```typescript
interface CodeChangedEvent {
  type: 'CODE_CHANGED'
  nodeId: string                    // Monaco pane nodeId
  filePath: string                  // current file path (relative to project root)
  language: string                  // detected language (typescript, python, etc.)
  content: string                   // full file content at time of emission
  contentHash: string               // SHA-256 of content (for dedup)
  cursorLine: number
  cursorColumn: number
  changeType: 'edit' | 'paste' | 'undo' | 'redo' | 'format'
  changeRange: {
    startLine: number
    endLine: number
    addedLines: number
    removedLines: number
  }
  sessionId: string
  timestamp: number
}
```

**On content size:** If `content` exceeds 50KB, emit a truncated version with a
`contentTruncated: true` flag and a hivenode file path reference instead. The BEE
can fetch the full file from the hivenode path if needed.

### CODE_SAVED

Fired on explicit save (Cmd+S / Ctrl+S). Always emits regardless of `emitOnChange`.

```typescript
interface CodeSavedEvent {
  type: 'CODE_SAVED'
  nodeId: string
  filePath: string
  language: string
  contentHash: string
  timestamp: number
}
```

### CODE_FILE_OPENED

```typescript
interface CodeFileOpenedEvent {
  type: 'CODE_FILE_OPENED'
  nodeId: string
  filePath: string
  language: string
  lineCount: number
  timestamp: number
}
```

### CODE_SELECTION_CHANGED

Only emits when `emitSelectionChanges: true`. Useful for "explain this code" agent flows.

```typescript
interface CodeSelectionChangedEvent {
  type: 'CODE_SELECTION_CHANGED'
  nodeId: string
  filePath: string
  selectedText: string
  startLine: number
  endLine: number
  timestamp: number
}
```

---

## 4. Agent Response Flow

When a subscribed BEE receives `CODE_CHANGED`, it evaluates the code and posts a response.
The response routes to either:

1. A named pane via `agentNodeId` (pane receives a `PROMPT_TO_PANE` event)
2. A sim-chat channel via `agentChannel`
3. Both, if both are configured

The BEE response is a `BotMessage` (from SPEC-SIM-CHAT-001 schema). It may include:

```typescript
interface CodeAgentResponse extends BotMessage {
  type: 'bot'
  responseType: 'lint' | 'type_error' | 'suggestion' | 'explanation' | 'test_suggestion'
  severity: 'info' | 'warning' | 'error'
  targetLines?: { start: number; end: number }   // which lines this applies to
  suggestedEdit?: {
    filePath: string
    startLine: number
    endLine: number
    replacement: string
  }
}
```

When `suggestedEdit` is present, Monaco renders it as an inline diff. The user accepts
via the standard Monaco diff accept button or types `apply` in the terminal.

Applying a suggestion emits `CODE_SUGGESTION_APPLIED` on the relay_bus, which writes to
the Event Ledger. This creates a training signal: human accepted or rejected this BEE
suggestion. RLHF gold at the point of development.

---

## 5. Debounce Strategy

The debounce prevents the BEE from being triggered on every keystroke. Default 800ms.

However, `CODE_SAVED` always fires immediately (no debounce) regardless of `emitDebounceMs`.
Save = intent to evaluate. The user explicitly requested it.

For large files (>500 lines), the debounce should auto-scale: `debounce = max(emitDebounceMs,
lineCount * 2ms)`. A 1000-line file gets at least a 2000ms debounce. This prevents expensive
full-file evaluations from firing too rapidly during active editing.

---

## 6. Event Ledger Integration

Every `CODE_CHANGED` event that triggers a BEE evaluation writes to the Event Ledger:

```
actor: monaco-main (pane nodeId)
action: CODE_CHANGED
input: { filePath, language, changeType, lineCount }
output: { beeResponse: BotMessage, accepted: boolean | null }
cost: { clock, coin, carbon }   // BEE evaluation cost in 3 currencies
```

`accepted` is null until the user acts on the suggestion. It is updated when
`CODE_SUGGESTION_APPLIED` or `CODE_SUGGESTION_REJECTED` fires.

Over time, the Event Ledger accumulates: which code patterns prompted BEE suggestions,
which suggestions were accepted, which were rejected. This is surrogate pipeline training
data for a code-domain four-vector.

---

## 7. IR Integration

Code changes can also be IR triggers. Any IR process can react to `CODE_CHANGED`:

```yaml
trigger:
  type: bus_event
  event: CODE_CHANGED
  condition: "event.language == 'typescript' AND event.changeType == 'save'"
```

This enables IR-authored development workflows: save TypeScript → IR runs type-check
step → branches on error → routes to BEE for fix → proposes edit → human approves.
The entire dev QA loop as a governed IR process.

---

## 8. Performance Constraints

| Constraint | Value |
|------------|-------|
| Max content size in event payload | 50KB |
| Debounce minimum | 400ms |
| Debounce default | 800ms |
| Max concurrent BEE evaluations per Monaco instance | 1 (queue, don't stack) |
| Event Ledger write on every evaluation | Yes |
| relay_bus emit on every keystroke | No (debounced) |

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-MONACO-BUS-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions
