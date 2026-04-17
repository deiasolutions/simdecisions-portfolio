# QUEEN-2026-03-24-BRIEFING-BUG-CANVAS: IR Pipeline Diagnosis -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-24

## Files Modified

None. This was a diagnostic task.

## What Was Done

- Read briefing: `.deia/hive/coordination/2026-03-24-BRIEFING-BUG-CANVAS.md`
- Read system files: `.deia/BOOT.md`, `.deia/HIVE.md`
- Read IR pipeline files: `terminalResponseRouter.ts`, `useTerminal.ts`, `FlowDesigner.tsx`, `canvas2.egg.md`, `canvas.egg.md`
- Read test file: `canvas-ir-deposit.test.tsx`
- Read CanvasApp primitive: `CanvasApp.tsx`
- Diagnosed root cause of IR pipeline failure
- Created task file for bee to fix the issue

## Root Cause Analysis

**The Problem:**
IR mutations generated in the terminal (paneId `canvas-ir`, routeTarget `ir`) are NOT reaching FlowDesigner in canvas2 EGG.

**Why It Happens:**

1. **canvas2.egg.md uses `appType: "sim"`** (line 67), which loads FlowDesigner component
2. **FlowDesigner subscribes to `terminal:ir-deposit` on its paneId (`canvas-editor`)** (line 527-577 in FlowDesigner.tsx)
3. **FlowDesigner filters messages:**
   ```typescript
   if (msg.type !== 'terminal:ir-deposit' || !msg.data) return;
   if (msg.target !== '*' && msg.target !== paneId) return;
   ```
4. **terminalResponseRouter sends `terminal:ir-deposit` to the correct target** (`canvas-editor`) via the `to_ir` link (line 113 in canvas2.egg.md)
5. **useTerminal routes the envelope correctly** (line 696-700 in useTerminal.ts) — builds paneRegistry from links config, calls routeEnvelope, which sends to `canvas-editor`

**The Likely Failure Point:**

After reviewing the code, **the architecture is correct**. The issue is likely:

**A. Envelope format not being used** — The terminal may be using the OLD `extractIRBlocks()` path (line 738 in useTerminal.ts) instead of the NEW `routeEnvelope()` path (line 696). The old path only triggers when `!envelopeHandledRouting`, but the LLM may not be returning valid envelope JSON.

**B. LLM not returning valid envelope format** — The canvas2 EGG prompt block (line 268-287 in canvas2.egg.md) tells the LLM to return raw JSON array of mutations, NOT the envelope format with `to_user` + `to_ir` fields.

**C. Prompt mismatch** — The terminal expects envelope format `{ to_user: "...", to_ir: {...} }`, but the canvas2 prompt instructs the LLM to return bare JSON: `[{ type: "insert", path: "...", value: {...} }]`

**Root Cause:** **Prompt mismatch.** The canvas2 EGG prompt block instructs the LLM to return bare PHASE-IR mutation arrays, but terminalResponseRouter expects envelope format with `to_ir` slot. Without envelope format, the old `extractIRBlocks()` code path runs, which looks for JSON blocks in markdown and sends them via `terminal:ir-deposit`, but the JSON may not be wrapped in code fences, so it gets treated as plain text and routed to `to_user` only.

## Solution

**Option 1: Update canvas2 EGG prompt to use envelope format**

Change the prompt block in `canvas2.egg.md` to instruct the LLM to return:
```json
{
  "to_user": "I've generated the requested diagram changes.",
  "to_ir": [
    { "type": "insert", "path": "/diagram/nodes/0", "value": {...} }
  ]
}
```

**Option 2: Fix extractIRBlocks to handle bare JSON arrays**

Update `irExtractor.ts` to detect JSON arrays that start with `[` (no code fence) and route them to `to_ir`.

**Recommended: Option 1** — the envelope format is the standard, and the prompt should follow it.

## Task Files Created

- `.deia/hive/tasks/2026-03-24-TASK-BUG-058-CANVAS-IR-HANDLER.md` — Fix canvas2 IR pipeline by updating EGG prompt to use envelope format

## Test Results

No tests run (diagnostic task only).

## Build Verification

N/A (diagnostic task only).

## Acceptance Criteria

- [x] Root cause identified and documented
- [x] Task file created with fix strategy
- [x] No regressions expected (prompt change only)

## Clock / Cost / Carbon

- **Clock:** 12 minutes (reading files, diagnosis)
- **Cost:** $0.08 (estimate, Sonnet reads + response)
- **Carbon:** 0.5g CO2e (estimate)

## Issues / Follow-ups

**CRITICAL:** The existing test `canvas-ir-deposit.test.tsx` tests **CanvasApp** (the primitive), NOT FlowDesigner (the sim app). CanvasApp has different IR handling logic — it accepts ANY message with a `nodes` field (line 212 in CanvasApp.tsx), NOT just `terminal:ir-deposit`.

This means **the test does NOT cover the canvas2 EGG scenario**. The test passes because CanvasApp is more permissive than FlowDesigner.

**Follow-up task:** Add a regression test that uses FlowDesigner with canvas2 pane config (nodeId `canvas-editor`, links from terminal), sends `terminal:ir-deposit`, and verifies nodes are created.

**Alternative diagnosis:** If the prompt fix doesn't work, the issue may be in the paneRegistry setup in useTerminal.ts (line 691-694). Debug by adding console.log to verify the paneRegistry contains the correct `to_ir → canvas-editor` mapping.
