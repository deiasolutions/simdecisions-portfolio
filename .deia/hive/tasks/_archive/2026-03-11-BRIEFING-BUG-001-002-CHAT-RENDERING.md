# Briefing: BUG-001 + BUG-002 — Chat Rendering Fixes

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-11
**Priority:** P1

---

## Objective

Fix two bugs in the Chat EGG's rendering pipeline. The terminal-to-text-pane chat flow has wiring in place but both ends produce wrong output.

---

## BUG-001: Text-pane renders raw text instead of formatted markdown

**Component:** SDEditor (text-pane primitive)
**Primary file:** `browser/src/primitives/text-pane/SDEditor.tsx`

### What happens

The text-pane receives AI responses correctly via `terminal:text-patch` bus messages. The content arrives with `format: 'markdown'` and the SDEditor sets its format state accordingly. The `renderMarkdown()` function (SDEditor.tsx lines 43-134) is called.

The problem: `renderMarkdown()` only handles **block-level** elements — headings, lists, blockquotes, code block markers, blank lines, paragraphs. It does NOT parse **inline** formatting within those blocks.

Result: content like `**You:** Hello` and `**claude-sonnet-4-5:** Here is my answer` renders with literal `**` asterisks visible. No bold, no italic, no inline code, no links.

### What should happen

Inline formatting must be parsed and rendered within each block element:
- `**bold**` → `<strong>`
- `*italic*` → `<em>`
- `` `code` `` → `<code>`
- `[text](url)` → `<a href>`

### Fix location

The `renderMarkdown()` function currently outputs raw text strings inside JSX `<div>` elements. Each line's text content needs to pass through an inline formatter that returns JSX with `<strong>`, `<em>`, `<code>`, and `<a>` elements.

### File size constraint

SDEditor.tsx is currently **564 lines — already over the 500-line limit**. The bee MUST extract `renderMarkdown()` (and the new inline parser) into a separate module, e.g. `browser/src/primitives/text-pane/services/markdownRenderer.tsx`, to bring SDEditor.tsx back under 500 lines.

### CSS

Any new inline element classes must use `var(--sd-*)` variables only.

---

## BUG-002: Terminal mini-display shows prompt echo + full LLM response

**Component:** Terminal primitive
**Primary files:**
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/terminal/TerminalOutput.tsx`
- `browser/src/services/terminal/types.ts` (TerminalEnvelope)
- `browser/src/services/terminal/terminalResponseRouter.ts`
- `browser/src/services/terminal/terminalService.ts` (formatMetrics)

### What happens

In chat mode (Chat EGG: `routeTarget: "ai"`, `links.to_text: "chat-output"`), the terminal currently shows:
1. The user's prompt (echo) — should NOT appear
2. The full LLM response content — should NOT appear

### What should happen

In chat mode, the terminal should show ONLY:
1. **The LLM's `to_terminal` message** (if the envelope includes one) — a short status or acknowledgment the LLM optionally sends to the terminal
2. **Status metrics** — one line with token count, cost, and 3Cs

The user's prompt does not echo. The full LLM response goes exclusively to the text-pane via `to_text` bus messages.

### Root cause analysis

The code has `isChatMode` logic (useTerminal.ts line 246):
```
const isChatMode = routeTarget === 'ai' && bus && nodeId && links.to_text;
```

When true:
- Line 268: user input entry gets `hidden: true`
- Line 353: response entry gets `metricsOnly: true`

TerminalOutput.tsx checks both flags (line 43 for hidden, line 91 for metricsOnly).

**The bee must investigate why this isn't working at runtime.** Possible causes:
1. `isChatMode` evaluates false (one of the four conditions failing — trace it)
2. The flags are set but the rendering path doesn't respect them
3. A timing/state issue where entries render before flags are applied

### New: `to_terminal` envelope slot

The `TerminalEnvelope` type (services/terminal/types.ts line 52) currently has no `to_terminal` slot. Add it:

```typescript
to_terminal?: string;  // Optional short message for terminal display in chat mode
```

The envelope router (terminalResponseRouter.ts) does NOT need to route this — the terminal reads it directly from the parsed envelope in useTerminal.ts.

In chat mode, when `to_terminal` is present, display it as a system-style line in the terminal above the metrics.

### Metrics format change

When `metricsOnly` is active, the current format is:
```
clock: 1.2s | cost: $0.0034 | carbon: 0.0023g
```

For chat mode, use a format that includes token count:
```
Response received, 847 tokens, $0.003 | clock: 1.2s | carbon: 0.0023g
```

This may mean a `formatChatMetrics()` variant in terminalService.ts, or a parameter on the existing `formatMetrics()`.

---

## Files Q33N Must Read Before Writing Tasks

| File | Why |
|------|-----|
| `browser/src/primitives/text-pane/SDEditor.tsx` | BUG-001: renderMarkdown() is the fix target |
| `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx` | BUG-001: existing tests |
| `browser/src/primitives/text-pane/sd-editor.css` | BUG-001: CSS classes for inline elements |
| `browser/src/primitives/terminal/useTerminal.ts` | BUG-002: chat mode flow, isChatMode, hidden/metricsOnly |
| `browser/src/primitives/terminal/TerminalOutput.tsx` | BUG-002: rendering checks for hidden/metricsOnly |
| `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx` | BUG-002: existing metricsOnly tests (lines 239-305) |
| `browser/src/primitives/terminal/types.ts` | BUG-002: TerminalEntry type |
| `browser/src/services/terminal/types.ts` | BUG-002: TerminalEnvelope type (add to_terminal) |
| `browser/src/services/terminal/terminalResponseRouter.ts` | BUG-002: envelope parsing |
| `browser/src/services/terminal/terminalService.ts` | BUG-002: formatMetrics() |
| `browser/src/apps/terminalAdapter.tsx` | BUG-002: EGG config → useTerminal prop wiring |
| `browser/src/primitives/terminal/TerminalApp.tsx` | BUG-002: eggConfig → useTerminal prop passing |
| `eggs/chat.egg.md` | Both: Chat EGG layout and config |

## Task Breakdown Guidance

Two independent bugs → two task files, dispatchable in parallel:

1. **TASK for BUG-001**: Markdown inline rendering + extract to module. Assign **sonnet** — needs careful regex work and JSX output.
2. **TASK for BUG-002**: Debug isChatMode, add to_terminal slot, fix chat-mode display + metrics format. Assign **sonnet** — investigation + multi-file changes.

## Constraints (apply to both tasks)

- CSS: `var(--sd-*)` only. No hex, no rgb(), no named colors.
- No file over 500 lines.
- TDD: tests first.
- No stubs.
- No third-party markdown library for BUG-001 — extend the existing hand-rolled renderer.
