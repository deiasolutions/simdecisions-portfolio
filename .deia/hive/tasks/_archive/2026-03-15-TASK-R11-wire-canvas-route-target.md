# TASK-R11: Wire Canvas Route Target in Terminal (Rebuild)

## Objective
Restore the terminal's `routeTarget='canvas'` functionality that was lost during git reset. Re-apply the modifications to types.ts and useTerminal.ts so the canvas mode handler can POST NL text to `/api/phase/nl-to-ir` and send IR flows to the canvas pane.

## Context
This is a rebuild of TASK-166, which was fully completed but lost during the git reset incident. The test file (`useTerminal.canvas.test.ts`) survived and shows the expected behavior. This task restores only the tracked-file modifications that were documented in the response files.

**What happened:**
- TASK-166 added 'canvas' as a route target type and implemented a 73-line handler in `handleSubmit()`
- The test file was created and survived the reset (10 tests, all passing)
- The source file modifications (types.ts, useTerminal.ts) were lost

**What this bee must do:**
Re-apply the exact modifications documented in the TASK-166 response file.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\types.ts` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (current state)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.canvas.test.ts` (surviving test file — shows expected behavior)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-166-RESPONSE.md` (exact changes documented)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-1650-BEE-HAIKU-2026-03-15-TASK-166-WIRE-CANVAS-ROUTE-TARGET-RAW.txt` (bee's full output)

## Deliverables

### 1. Modify `browser/src/primitives/terminal/types.ts`
- [ ] Add `metrics?: TerminalMetrics` to the system entry type in `TerminalEntry` union (around line 29)
- [ ] Change `routeTarget` type from `'ai' | 'shell' | 'relay' | 'ir'` to `'ai' | 'shell' | 'relay' | 'ir' | 'canvas'` in BOTH `UseTerminalOptions` (line ~43) and `TerminalEggConfig` (line ~115)
- [ ] Update JSDoc comments to document canvas mode behavior

### 2. Modify `browser/src/primitives/terminal/useTerminal.ts`
- [ ] Update `UseTerminalOptions.routeTarget` type union to include `'canvas'` (around lines 43-44)
- [ ] Insert canvas mode handler block in `handleSubmit()` function (approximately 73 lines of code)
  - Insert **after** relay mode handler (~line 443), **before** API key check (~line 520)
  - Handler must:
    - Validate canvas link exists (`links.to_ir`)
    - Show error if no canvas link configured
    - Add hidden input entry (user won't see echo in terminal)
    - Set loading state
    - POST to `${HIVENODE_URL}/api/phase/nl-to-ir` with `{ text, model: currentModel, api_key: apiKey }`
    - Handle non-OK response (extract error detail, throw with message)
    - Parse response: `{ flow_data, metadata, validation_result }`
    - Send `terminal:ir-deposit` bus event to `links.to_ir` with flow_data payload
    - Include nonce (`${Date.now()}-${Math.random()}`) and timestamp
    - Update ledger with metadata (clock_ms, cost_usd, carbon_g, input_tokens, output_tokens, message_count)
    - Display success message: `✓ Flow sent to canvas (N nodes, M edges)` or warning with validation errors
    - Catch errors and display `Canvas chatbot error: ${error.message}`
    - Clear loading state in finally block
    - Return after handling (don't fall through to LLM mode)

**Exact code block to insert** (based on TASK-166 response):
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

### 3. Verify Tests Pass
- [ ] Run canvas mode tests: `cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.canvas.test.ts`
- [ ] All 10 canvas tests must pass
- [ ] No regressions in other terminal tests

## Test Requirements
- [ ] Tests ALREADY EXIST (TDD was followed in original task)
- [ ] All 10 canvas tests pass
- [ ] Edge cases covered:
  - No canvas link configured → error message
  - Valid flow → success with node/edge count
  - Invalid flow → warning with validation errors
  - Backend 400 error → error message
  - Backend 500 error → error message
  - Network error → error message
  - Ledger updated with metadata
  - Empty input → no-op
  - Bus message sent with correct payload
  - Loading state managed correctly

## Constraints
- No file over 500 lines (useTerminal.ts will be ~850 lines after insertion)
- No stubs — full implementation with all error handling
- Match the original implementation exactly (use response files as reference)
- Test file already exists — DO NOT modify it

## Acceptance Criteria
- [ ] `types.ts` updated: metrics field added to system entry, 'canvas' added to both routeTarget type unions
- [ ] `useTerminal.ts` updated: canvas handler block inserted in correct location (after relay, before API key check)
- [ ] Canvas handler validates link, POSTs to backend, sends bus message, updates ledger, displays status
- [ ] All error paths handled (no link, 400, 500, network)
- [ ] 10 canvas tests pass (no modifications to test file needed)
- [ ] No regressions in existing terminal tests
- [ ] Loading state set/cleared correctly
- [ ] Response file written to `.deia/hive/responses/` with all 8 sections

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/20260315-TASK-R11-RESPONSE.md`

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
