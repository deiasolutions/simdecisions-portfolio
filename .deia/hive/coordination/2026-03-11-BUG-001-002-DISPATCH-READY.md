# BUG-001 & BUG-002 Dispatch Package — Ready for Q88N Approval

**Date:** 2026-03-11
**Status:** READY FOR DISPATCH
**Prepared by:** Q33N
**Dispatch mode:** PARALLEL (2 independent tasks)

---

## Summary

Two P1 bugs in the chat.egg.md product have been broken down into parallel bee tasks:

1. **TASK-022 (BUG-001):** Text-pane not rendering inline markdown (`**bold**`, `*italic*`, etc.)
2. **TASK-023 (BUG-002):** Terminal mini-display echoing full chat content instead of metrics-only status

Both tasks are **fully independent** — no shared files, no dependencies. Can be dispatched in parallel.

---

## Task Files Created

### TASK-022: Fix Text-Pane Inline Markdown Rendering
**Path:** `.deia/hive/tasks/2026-03-11-TASK-022-BUG-001-TEXT-PANE-INLINE-MARKDOWN.md`

**Scope:**
- Modify `renderMarkdown()` in `SDEditor.tsx` to parse inline formatting (bold, italic, code, links)
- Add helper function `parseInlineMarkdown(text: string): (string | JSX.Element)[]`
- Update CSS classes in `sd-editor.css`
- Write tests in `SDEditor.test.tsx`

**Constraints:**
- No third-party library
- Custom renderer stays under 150 lines
- Fault-tolerant (malformed markdown renders as plain text)
- CSS variables only (`var(--sd-*)`)

**Files touched:** 3
- `browser/src/primitives/text-pane/SDEditor.tsx`
- `browser/src/primitives/text-pane/sd-editor.css`
- `browser/src/primitives/text-pane/__tests__/SDEditor.test.tsx`

---

### TASK-023: Fix Terminal Mini-Display for Chat Mode
**Path:** `.deia/hive/tasks/2026-03-11-TASK-023-BUG-002-TERMINAL-MINI-DISPLAY.md`

**Scope:**
- Add `metricsOnly: boolean` flag to `TerminalEntry` response type
- Set flag in `useTerminal.ts` chat mode branch (line 353)
- Update `TerminalOutput.tsx` to conditionally render content based on flag
- Write tests for chat-mode vs non-chat-mode rendering

**Constraints:**
- Response entries MUST still store full content (for conversation history building)
- Do NOT break non-chat mode (`routeTarget === 'shell'`)
- Reuse existing `hidden` flag pattern

**Files touched:** 4
- `browser/src/primitives/terminal/useTerminal.ts`
- `browser/src/primitives/terminal/types.ts`
- `browser/src/primitives/terminal/TerminalOutput.tsx`
- `browser/src/primitives/terminal/__tests__/TerminalOutput.test.tsx`

---

## Dispatch Script

**Path:** `_outbox/dispatch_bug_001_002.py`

Launches both tasks in parallel via `ThreadPoolExecutor`. Each task uses:
- Model: `haiku`
- Role: `bee`
- Timeout: 1200s
- Boot injection: enabled

### Run Command

```bash
python _outbox/dispatch_bug_001_002.py
```

---

## Estimated Costs

| Task | Model | Est. Clock | Est. Cost | Est. Carbon |
|------|-------|------------|-----------|-------------|
| TASK-022 | Haiku | 5-8 min | $0.05-$0.10 | 0.01g CO2e |
| TASK-023 | Haiku | 4-6 min | $0.04-$0.08 | 0.01g CO2e |
| **Total** | | **9-14 min** | **$0.09-$0.18** | **0.02g CO2e** |

---

## Pre-Dispatch Checklist

- [x] Task files validated (all in `.deia/hive/tasks/`)
- [x] File paths absolute
- [x] Constraints documented
- [x] Acceptance criteria explicit
- [x] Test commands provided
- [x] Response format template included
- [x] BOOT.md rules referenced
- [x] Dispatch script tested (syntax only, not executed)

---

## Expected Outputs

After dispatch, expect:

1. **Response files:**
   - `.deia/hive/responses/20260311-XXXX-BEE-HAIKU-TASK-022-RAW.txt`
   - `.deia/hive/responses/20260311-XXXX-BEE-HAIKU-TASK-023-RAW.txt`

2. **Formatted responses:**
   - `.deia/hive/responses/20260311-TASK-022-RESPONSE.md`
   - `.deia/hive/responses/20260311-TASK-023-RESPONSE.md`

3. **Commits:**
   - `[BEE-HAIKU] TASK-022: add inline markdown rendering to text-pane`
   - `[BEE-HAIKU] TASK-023: fix terminal mini-display for chat mode`

4. **Test results:**
   - TASK-022: new tests in `SDEditor.test.tsx` + all existing text-pane tests passing
   - TASK-023: new tests in `TerminalOutput.test.tsx` + all existing terminal tests passing

---

## Q88N Approval Required

**Before dispatching, confirm:**

1. ✅ Task scope is clear and bounded?
2. ✅ Parallel dispatch is safe (no shared files)?
3. ✅ Cost/time estimates acceptable?
4. ✅ Response format requirements clear?

If approved, run:

```bash
python _outbox/dispatch_bug_001_002.py
```

If changes needed, update task files and re-submit for approval.

---

**Q33N standing by for Q88N approval.**
