# TASK-167: E2E test for terminal → LLM → canvas chatbot flow

## Objective
Write an end-to-end integration test that verifies the complete canvas chatbot flow: user types natural language in terminal with `routeTarget='canvas'`, backend converts to PHASE-IR, and canvas receives and renders nodes via bus events.

## Context
This test validates the full wiring from TASK-165 (backend endpoint) and TASK-166 (frontend routing). It ensures:
1. Terminal calls `/api/phase/nl-to-ir` with NL text
2. Backend returns valid PHASE-IR flow
3. Terminal sends IR to canvas via bus
4. Canvas renders nodes correctly

**Dependencies:** This task can ONLY run after TASK-165 and TASK-166 are complete and their tests pass.

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.canvas.test.ts` (from TASK-166)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\tests\hivenode\test_phase_nl_routes.py` (from TASK-165)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas.integration.test.tsx` (existing canvas integration tests)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\useTerminal.test.ts` (existing terminal tests)

## Deliverables
- [ ] New test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\__tests__\terminal-canvas-e2e.test.tsx`
- [ ] Test: Full flow with mocked backend
- [ ] Test: Bus message verification
- [ ] Test: Canvas state update verification
- [ ] Test: Error handling (backend failure)
- [ ] Test: Validation warnings displayed correctly

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass (`cd browser && npx vitest run src/primitives/terminal/__tests__/terminal-canvas-e2e.test.tsx`)
- [ ] Edge cases:
  - [ ] Simple flow (2-3 nodes) → canvas renders all nodes
  - [ ] Complex flow (8+ nodes, branching) → canvas renders correctly
  - [ ] Backend returns validation warnings → terminal shows warnings
  - [ ] Backend times out → terminal shows timeout error
  - [ ] No canvas link → terminal shows error, no bus message sent
  - [ ] Bus message format matches canvas expectations
- [ ] Minimum 6 e2e tests

## Constraints
- No file over 500 lines
- CSS: var(--sd-*) only (N/A for tests)
- No stubs — full integration test with mocks
- Use vitest + React Testing Library
- Mock fetch for `/api/phase/nl-to-ir`
- Mock MessageBus for event verification
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes:
  ```json
  {"task_id": "2026-03-15-TASK-167-canvas-chatbot-e2e-test", "status": "running", "model": "haiku", "message": "working"}
  ```

## Test Structure

### Test 1: Simple Flow E2E
```typescript
test('terminal NL → backend → canvas: simple flow', async () => {
  // 1. Mock backend /api/phase/nl-to-ir response
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      flow_data: {
        id: 'flow-test',
        name: 'Simple Flow',
        nodes: [
          { id: 'start', type: 'start', name: 'Start', position: { x: 0, y: 0 } },
          { id: 'task1', type: 'task', name: 'Do Something', position: { x: 200, y: 0 } },
          { id: 'end', type: 'end', name: 'End', position: { x: 400, y: 0 } },
        ],
        edges: [
          { id: 'e1', source: 'start', target: 'task1' },
          { id: 'e2', source: 'task1', target: 'end' },
        ],
      },
      metadata: { model: 'claude-sonnet-4-5', input_tokens: 50, output_tokens: 100, cost_usd: 0.001, clock_ms: 800 },
      validation_result: { valid: true, errors: [] },
    }),
  });

  // 2. Setup terminal with routeTarget='canvas'
  const mockBus = createMockBus();
  const { result } = renderHook(() =>
    useTerminal({
      routeTarget: 'canvas',
      bus: mockBus,
      nodeId: 'terminal-1',
      links: { to_ir: 'canvas-1' },
      apiKey: 'test-key',
    })
  );

  // 3. Submit natural language input
  act(() => {
    result.current.setInput('Create a simple flow with start, task, and end');
  });
  await act(async () => {
    await result.current.handleSubmit();
  });

  // 4. Verify backend called with correct payload
  expect(fetch).toHaveBeenCalledWith(
    expect.stringContaining('/api/phase/nl-to-ir'),
    expect.objectContaining({
      method: 'POST',
      body: expect.stringContaining('Create a simple flow'),
    })
  );

  // 5. Verify bus message sent to canvas
  expect(mockBus.send).toHaveBeenCalledWith(
    expect.objectContaining({
      type: 'terminal:ir-deposit',
      sourcePane: 'terminal-1',
      target: 'canvas-1',
      data: expect.objectContaining({
        nodes: expect.arrayContaining([
          expect.objectContaining({ id: 'start', type: 'start' }),
          expect.objectContaining({ id: 'task1', type: 'task' }),
          expect.objectContaining({ id: 'end', type: 'end' }),
        ]),
      }),
    })
  );

  // 6. Verify ledger updated
  expect(result.current.ledger.total_cost_usd).toBeGreaterThan(0);
  expect(result.current.ledger.message_count).toBe(1);

  // 7. Verify terminal shows success message
  const lastEntry = result.current.entries[result.current.entries.length - 1];
  expect(lastEntry.type).toBe('system');
  expect(lastEntry.content).toContain('3 nodes');
  expect(lastEntry.content).toContain('2 edges');
});
```

### Test 2: Backend Error Handling
```typescript
test('terminal handles backend error gracefully', async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: false,
    status: 400,
    json: async () => ({ detail: 'Invalid input: no nodes found' }),
  });

  const mockBus = createMockBus();
  const { result } = renderHook(() =>
    useTerminal({
      routeTarget: 'canvas',
      bus: mockBus,
      nodeId: 'terminal-1',
      links: { to_ir: 'canvas-1' },
      apiKey: 'test-key',
    })
  );

  act(() => {
    result.current.setInput('garbage input');
  });
  await act(async () => {
    await result.current.handleSubmit();
  });

  // Verify no bus message sent
  expect(mockBus.send).not.toHaveBeenCalled();

  // Verify error shown in terminal
  const lastEntry = result.current.entries[result.current.entries.length - 1];
  expect(lastEntry.type).toBe('system');
  expect(lastEntry.content).toContain('error');
  expect(lastEntry.content).toContain('Invalid input');
});
```

### Test 3: Validation Warnings
```typescript
test('terminal shows validation warnings when flow has issues', async () => {
  global.fetch = vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      flow_data: {
        id: 'flow-test',
        nodes: [{ id: 'orphan', type: 'task', name: 'Orphan Task' }],
        edges: [],
      },
      metadata: { model: 'claude-sonnet-4-5', cost_usd: 0.001 },
      validation_result: {
        valid: false,
        errors: ['No start node found', 'Node orphan has no connections'],
      },
    }),
  });

  const mockBus = createMockBus();
  const { result } = renderHook(() =>
    useTerminal({
      routeTarget: 'canvas',
      bus: mockBus,
      nodeId: 'terminal-1',
      links: { to_ir: 'canvas-1' },
      apiKey: 'test-key',
    })
  );

  act(() => {
    result.current.setInput('Create an orphan task');
  });
  await act(async () => {
    await result.current.handleSubmit();
  });

  // Verify flow still sent to canvas (best-effort)
  expect(mockBus.send).toHaveBeenCalled();

  // Verify warnings shown
  const lastEntry = result.current.entries[result.current.entries.length - 1];
  expect(lastEntry.content).toContain('validation warnings');
  expect(lastEntry.content).toContain('No start node');
});
```

### Test 4: No Canvas Link Error
```typescript
test('terminal shows error when no canvas link configured', async () => {
  const mockBus = createMockBus();
  const { result } = renderHook(() =>
    useTerminal({
      routeTarget: 'canvas',
      bus: mockBus,
      nodeId: 'terminal-1',
      links: {}, // No to_ir link
      apiKey: 'test-key',
    })
  );

  act(() => {
    result.current.setInput('Create a flow');
  });
  await act(async () => {
    await result.current.handleSubmit();
  });

  // Verify no backend call
  expect(fetch).not.toHaveBeenCalled();

  // Verify error message
  const lastEntry = result.current.entries[result.current.entries.length - 1];
  expect(lastEntry.type).toBe('system');
  expect(lastEntry.content).toContain('No canvas pane linked');
});
```

## Helper Utilities

Create `createMockBus()` helper:
```typescript
function createMockBus(): MessageBus {
  return {
    send: vi.fn(),
    subscribe: vi.fn(() => () => {}),
    nodeId: 'mock-bus',
  } as any;
}
```

## Smoke Test
After all tests pass, run full terminal test suite to ensure no regressions:
```bash
cd browser && npx vitest run src/primitives/terminal/__tests__/
```

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260315-TASK-167-RESPONSE.md`

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
