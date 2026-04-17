# TASK-BL-121-C: Canvas Properties Integration Test

## Objective

Create end-to-end integration tests for the full properties panel editing flow: select canvas node → properties panel populates → edit property → canvas node updates.

## Context

Tasks TASK-BL-121-A and TASK-BL-121-B implement the individual pieces:
- **TASK-BL-121-A:** TreeBrowser inline editing UI
- **TASK-BL-121-B:** CanvasApp subscription to property changes

This task verifies the full round-trip works correctly by testing the entire flow in integration.

**Integration flow:**
1. Canvas node is selected → `canvas:node-selected` event published
2. Properties adapter receives event → populates tree-browser with node properties
3. User edits a property in tree-browser → `properties:value-changed` event published
4. CanvasApp receives event → updates node data in ReactFlow state
5. Canvas publishes `canvas:node-updated` event
6. Properties panel re-renders with updated values

**Test scenarios:**
- Select node → properties panel shows correct values
- Edit string property → canvas node updates
- Edit number property → canvas node updates
- Edit nested property (e.g., `config.timing.distribution`) → canvas node updates
- Deselect node → properties panel clears
- Select different node → properties panel switches to new node
- Edit property while another node is selected → only selected node updates

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\TreeBrowser.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\messageBus.ts`

## Deliverables

### 1. Create integration test file

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\canvas-properties-integration.test.tsx`

- [ ] Create new test file
- [ ] Import CanvasApp, TreeBrowser, createPropertiesAdapter, MessageBus
- [ ] Set up test environment with shared MessageBus instance
- [ ] Mock ReactFlowProvider and ReactFlow hooks
- [ ] Create test fixtures for IR nodes

### 2. Test: Select node → properties panel populates

**Scenario:** When a canvas node is selected, the properties panel should display its properties in accordion sections.

- [ ] Render CanvasApp with a test node
- [ ] Render TreeBrowser with propertiesAdapter
- [ ] Simulate node selection in canvas (trigger `canvas:node-selected` event)
- [ ] Wait for TreeBrowser to re-render
- [ ] Assert TreeBrowser displays 4 sections: General, Timing, Operator, Connections
- [ ] Assert General section shows id, type, name

**Test code pattern:**
```typescript
it('shows node properties when canvas node is selected', async () => {
  const mockBus = createMessageBus();
  const testNode = {
    id: 'node-1',
    type: 'human',
    name: 'Review Task',
    config: {
      timing: { distribution: 'lognormal', params: { mean: 3600, std: 600 } },
      operator: { type: 'analyst', count: 2 },
    },
  };

  const { getByText } = render(
    <div>
      <ReactFlowProvider>
        <CanvasApp nodeId="canvas-1" bus={mockBus} />
      </ReactFlowProvider>
      <TreeBrowser
        nodes={[]}
        selectedId={null}
        onSelect={() => {}}
        bus={mockBus}
      />
    </div>
  );

  // Publish canvas:node-selected
  mockBus.publish({
    type: 'canvas:node-selected',
    sourcePane: 'canvas-1',
    target: '*',
    nonce: '123',
    timestamp: new Date().toISOString(),
    data: { node: testNode },
  });

  // Wait for properties to render
  await waitFor(() => {
    expect(getByText('General')).toBeInTheDocument();
    expect(getByText('Review Task')).toBeInTheDocument();
  });
});
```

### 3. Test: Edit property → canvas node updates

**Scenario:** Editing a property in the properties panel should update the canvas node data.

- [ ] Render CanvasApp with a test node
- [ ] Render TreeBrowser with propertiesAdapter
- [ ] Select node (trigger `canvas:node-selected`)
- [ ] Find the editable property row (e.g., "Name")
- [ ] Click to enter edit mode
- [ ] Change the value
- [ ] Blur or press Enter
- [ ] Wait for `properties:value-changed` and `canvas:node-updated` events
- [ ] Assert canvas node data was updated

**Test code pattern:**
```typescript
it('updates canvas node when property is edited', async () => {
  const mockBus = createMessageBus();
  const propertiesAdapter = createPropertiesAdapter({ bus: mockBus });
  const testNode = {
    id: 'node-1',
    type: 'human',
    name: 'Review Task',
  };

  const { getByLabelText, getByText } = render(
    <div>
      <ReactFlowProvider>
        <CanvasApp nodeId="canvas-1" bus={mockBus} />
      </ReactFlowProvider>
      <TreeBrowser
        nodes={[]}
        selectedId={null}
        onSelect={() => {}}
        onPropertyChange={(nodeId, field, value) => {
          propertiesAdapter.updateProperty(nodeId, field, value);
        }}
        bus={mockBus}
      />
    </div>
  );

  // Select node
  mockBus.publish({
    type: 'canvas:node-selected',
    sourcePane: 'canvas-1',
    target: '*',
    nonce: '123',
    timestamp: new Date().toISOString(),
    data: { node: testNode },
  });

  // Edit property
  const nameInput = getByLabelText('Name');
  fireEvent.click(nameInput);
  fireEvent.change(nameInput, { target: { value: 'New Name' } });
  fireEvent.blur(nameInput);

  // Wait for canvas:node-updated
  await waitFor(() => {
    expect(mockBus.publish).toHaveBeenCalledWith(
      expect.objectContaining({
        type: 'canvas:node-updated',
        data: expect.objectContaining({
          node: expect.objectContaining({ name: 'New Name' }),
        }),
      })
    );
  });
});
```

### 4. Test: Nested property edit

**Scenario:** Editing a nested property like `config.timing.distribution` should correctly update the deep object path.

- [ ] Render CanvasApp with a test node that has nested config
- [ ] Select node
- [ ] Find the "Distribution" property row
- [ ] Edit the value
- [ ] Assert canvas node's `config.timing.distribution` was updated

### 5. Test: Deselect node → properties panel clears

**Scenario:** When no node is selected, the properties panel should show empty state.

- [ ] Render CanvasApp and TreeBrowser with propertiesAdapter
- [ ] Select a node (properties populate)
- [ ] Deselect the node (publish `canvas:node-selected` with `node: null` or similar)
- [ ] Wait for TreeBrowser to re-render
- [ ] Assert properties panel shows "Select a node on the canvas" empty state

### 6. Test: Select different node → properties panel switches

**Scenario:** Selecting a different node should clear the old properties and show the new node's properties.

- [ ] Select node-1 (properties populate)
- [ ] Select node-2 (properties update)
- [ ] Assert properties panel shows node-2's data, not node-1's

### 7. Test: Edit property for wrong node is ignored

**Scenario:** If a property change event arrives for a node that doesn't exist on the canvas, it should be ignored gracefully.

- [ ] Render CanvasApp with node-1
- [ ] Publish `properties:value-changed` for non-existent node-999
- [ ] Assert no crash
- [ ] Assert warning logged to console
- [ ] Assert canvas state unchanged

## Test Requirements

**All tests MUST be written FIRST (TDD).**

- [ ] At least 7 integration tests covering the scenarios above
- [ ] All tests use a shared MessageBus instance (not mocked)
- [ ] All tests use real propertiesAdapter (not mocked)
- [ ] All tests wait for async bus events to propagate
- [ ] All tests pass
- [ ] No console errors during test run
- [ ] No hardcoded timeouts (use `waitFor` from @testing-library/react)

### Test file structure:

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, fireEvent, waitFor } from '@testing-library/react';
import { ReactFlowProvider } from '@xyflow/react';
import { CanvasApp } from '../CanvasApp';
import { TreeBrowser } from '../../tree-browser/TreeBrowser';
import { createPropertiesAdapter } from '../../tree-browser/adapters/propertiesAdapter';
import { createMessageBus } from '../../../infrastructure/relay_bus/messageBus';

describe('Canvas Properties Integration', () => {
  let mockBus: MessageBus;
  let propertiesAdapter: ReturnType<typeof createPropertiesAdapter>;

  beforeEach(() => {
    mockBus = createMessageBus();
    propertiesAdapter = createPropertiesAdapter({ bus: mockBus });
  });

  it('shows node properties when canvas node is selected', async () => {
    // ...
  });

  it('updates canvas node when property is edited', async () => {
    // ...
  });

  it('updates nested property correctly', async () => {
    // ...
  });

  it('clears properties panel when node is deselected', async () => {
    // ...
  });

  it('switches properties when different node is selected', async () => {
    // ...
  });

  it('ignores property change for non-existent node', async () => {
    // ...
  });

  it('handles number property edits', async () => {
    // ...
  });
});
```

### Run tests with:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/canvas-properties-integration.test.tsx
```

### Regression test (all canvas tests):

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/
```

### Full integration smoke test:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run
```

## Constraints

- **File must be under 500 lines.** If the test file grows beyond 500 lines, split into multiple test files by scenario group.
- **No stubs.** Use real MessageBus, real adapters. Mock only ReactFlow DOM APIs if needed.
- **TDD.** Tests written FIRST, then ensure TASK-BL-121-A and TASK-BL-121-B implementations pass these tests.
- **No git operations** without Q88N approval.

## Acceptance Criteria

- [ ] Integration test file created with at least 7 test scenarios
- [ ] All tests pass
- [ ] Tests use real MessageBus (not mocked)
- [ ] Tests use real propertiesAdapter (not mocked)
- [ ] Tests verify full round-trip: select → edit → update
- [ ] Deselect scenario works
- [ ] Select different node scenario works
- [ ] Invalid node ID scenario handled gracefully
- [ ] No console errors during test run
- [ ] File is under 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-121-C-RESPONSE.md`

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
