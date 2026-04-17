# TASK-166: Wire routeTarget='canvas' in terminal to call NL-to-IR endpoint

## Objective
Extend the terminal's `useTerminal.ts` hook to support `routeTarget='canvas'`, which calls the new `/api/phase/nl-to-ir` backend endpoint and sends the resulting PHASE-IR flow to the canvas via `terminal:ir-deposit` bus event.

## Context
The terminal already supports 4 route targets:
- `'ai'` — sends response to text-pane
- `'shell'` — shows output in terminal
- `'relay'` — sends to efemera channel
- `'ir'` — splits response into chat + IR JSON

We need to add a 5th target: `'canvas'` — sends NL input directly to backend for IR conversion, then routes IR to canvas.

**Key difference from 'ir' mode:**
- `'ir'` mode: LLM call happens in terminal service, response includes chat text + IR blocks
- `'canvas'` mode: Backend handles LLM call, response is pure PHASE-IR flow (no chat text)

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 240-670 for handleSubmit logic)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (terminal types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\irExtractor.ts` (IR extraction logic, for reference)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\constants.ts` (bus event types)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\phase_nl_routes.py` (from TASK-165, if completed)

## Deliverables
- [ ] Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts`
  - Add `routeTarget='canvas'` to UseTerminalOptions type (line 44)
  - Add canvas mode handler in handleSubmit (after line 443)
- [ ] Modify: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts`
  - Update routeTarget type to include 'canvas'
- [ ] Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.canvas.test.ts`
  - New test file specifically for canvas mode

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`)
- [ ] Edge cases:
  - [ ] Valid NL → backend call → IR sent to canvas via bus
  - [ ] Empty input → no backend call
  - [ ] Backend returns 400 → error shown in terminal
  - [ ] Backend returns 500 → error shown in terminal
  - [ ] No canvas link (links.to_ir undefined) → error shown
  - [ ] No bus → graceful fallback
  - [ ] Loading state during backend call
  - [ ] Multiple rapid submissions (debounce/queue)
- [ ] Minimum 8 tests

## Constraints
- No file over 500 lines (useTerminal.ts is currently 770 lines — DO NOT exceed 1000)
- CSS: var(--sd-*) only (N/A for logic)
- No stubs — full implementation required
- Preserve existing routeTarget behavior ('ai', 'shell', 'relay', 'ir')
- Use existing error handling patterns
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes:
  ```json
  {"task_id": "2026-03-15-TASK-166-wire-canvas-route-target", "status": "running", "model": "haiku", "message": "working"}
  ```

## Implementation Guide

### 1. Update Type Definitions

In `types.ts`, update routeTarget union:
```typescript
routeTarget?: 'ai' | 'shell' | 'relay' | 'ir' | 'canvas';
```

### 2. Add Canvas Mode Handler in useTerminal.ts

Insert after relay mode handler (around line 443):

```typescript
// Canvas mode: POST NL to backend /api/phase/nl-to-ir, send IR to canvas
if (routeTarget === 'canvas') {
  if (!links.to_ir) {
    setEntries((prev) => [
      ...prev,
      { type: 'input', content: text, hidden: true },
      { type: 'system', content: 'No canvas pane linked. Check EGG config.' },
    ]);
    return;
  }

  setEntries((prev) => [...prev, { type: 'input', content: text, hidden: true }]);
  setLoading(true);

  try {
    const res = await fetch(`${HIVENODE_URL}/api/phase/nl-to-ir`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, model: currentModel, api_key: apiKey }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(errorData.detail || `Backend error: ${res.status}`);
    }

    const data = await res.json();
    const { flow_data, metadata, validation_result } = data;

    // Send IR flow to canvas via bus
    if (bus && nodeId) {
      bus.send({
        type: 'terminal:ir-deposit',
        sourcePane: nodeId,
        target: links.to_ir,
        nonce: `${Date.now()}-${Math.random()}`,
        timestamp: new Date().toISOString(),
        data: flow_data,
      });
    }

    // Update ledger with LLM metrics
    if (metadata) {
      setLedger((prev) => ({
        total_clock_ms: prev.total_clock_ms + (metadata.clock_ms || 0),
        total_cost_usd: prev.total_cost_usd + (metadata.cost_usd || 0),
        total_carbon_g: prev.total_carbon_g + (metadata.carbon_g || 0),
        total_input_tokens: prev.total_input_tokens + (metadata.input_tokens || 0),
        total_output_tokens: prev.total_output_tokens + (metadata.output_tokens || 0),
        message_count: prev.message_count + 1,
      }));
    }

    // Show success message in terminal
    const nodeCount = flow_data.nodes?.length || 0;
    const edgeCount = flow_data.edges?.length || 0;
    const statusMsg = validation_result?.valid
      ? `✓ Flow sent to canvas (${nodeCount} nodes, ${edgeCount} edges)`
      : `⚠ Flow sent but has validation warnings: ${validation_result?.errors?.join(', ')}`;

    setEntries((prev) => [
      ...prev,
      { type: 'system', content: statusMsg, metrics: metadata },
    ]);
  } catch (error: any) {
    setEntries((prev) => [
      ...prev,
      { type: 'system', content: `Canvas chatbot error: ${error.message}` },
    ]);
  } finally {
    setLoading(false);
  }
  return;
}
```

### 3. Test Structure

Mock fetch for `/api/phase/nl-to-ir` endpoint:
- Test successful flow generation
- Test backend errors (400, 500)
- Test bus message sent correctly
- Test ledger updates
- Test validation warnings displayed

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-166-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
