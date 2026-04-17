# TASK-BL-121-B: Wire Property Changes to Canvas

## Objective

Subscribe to `properties:value-changed` events in CanvasApp and update node data when properties are edited via the properties panel. Publish `canvas:node-updated` after applying changes.

## Context

The properties adapter already publishes `properties:value-changed` events when a property is edited (via `updateProperty()` method). The CanvasApp needs to subscribe to these events and update the corresponding node's data in the ReactFlow state.

**Current state:**
- ✅ propertiesAdapter publishes `properties:value-changed` with `{ nodeId, field, value }`
- ❌ CanvasApp does NOT subscribe to these events
- ❌ Property changes are published but ignored

**What needs to happen:**
1. CanvasApp subscribes to `properties:value-changed` on its bus
2. On receiving the event, find the node by ID in the ReactFlow nodes array
3. Update the node's data using a helper to handle nested paths (e.g., `"config.timing.distribution"`)
4. Apply the update via `setNodes()` to trigger React re-render
5. Publish `canvas:node-updated` event so other components can react

**Nested property handling:**
- Field paths like `"name"` update directly on the node
- Field paths like `"config.timing.distribution"` require deep object mutation
- Use a helper function `setNestedValue(obj, path, value)` to handle dot-separated paths

## Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\propertiesAdapter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\types\ir.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

## Deliverables

### 1. Add nested value setter helper

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

Create a helper function to set nested object values by dot-separated path:

```typescript
/**
 * Set a nested object value by dot-separated path
 * Example: setNestedValue(obj, 'config.timing.distribution', 'normal')
 */
function setNestedValue(obj: any, path: string, value: any): void {
  const keys = path.split('.');
  const lastKey = keys.pop()!;
  let current = obj;

  for (const key of keys) {
    if (!current[key]) {
      current[key] = {};
    }
    current = current[key];
  }

  current[lastKey] = value;
}
```

- [ ] Add this helper function to CanvasApp.tsx (above the component or in a utils section)
- [ ] Add JSDoc comment explaining the function
- [ ] Add inline examples

### 2. Subscribe to properties:value-changed in CanvasApp

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\CanvasApp.tsx`

In the existing `useEffect` that subscribes to bus events (around line 181), add a handler for `properties:value-changed`:

- [ ] Check if `msg.type === 'properties:value-changed'`
- [ ] Extract `{ nodeId, field, value }` from `msg.data`
- [ ] Find the node by ID: `const nodeIndex = nodes.findIndex(n => n.id === nodeId)`
- [ ] If node not found, log warning and return
- [ ] Clone the node data
- [ ] Use `setNestedValue()` to update the field
- [ ] Call `setNodes()` with the updated nodes array
- [ ] Publish `canvas:node-updated` event

**Example handler:**
```typescript
if (msg.type === 'properties:value-changed') {
  const { nodeId, field, value } = msg.data as { nodeId: string; field: string; value: any };

  setNodes((nds) => {
    const nodeIndex = nds.findIndex((n) => n.id === nodeId);
    if (nodeIndex === -1) {
      console.warn(`[CanvasApp] properties:value-changed: node ${nodeId} not found`);
      return nds;
    }

    const updatedNodes = [...nds];
    const node = { ...updatedNodes[nodeIndex] };
    const nodeData = { ...node.data };

    // Update nested property
    setNestedValue(nodeData, field, value);

    node.data = nodeData;
    updatedNodes[nodeIndex] = node;

    // Publish canvas:node-updated
    bus?.publish({
      type: 'canvas:node-updated',
      sourcePane: nodeId || 'canvas',
      target: '*',
      nonce: `${Date.now()}-${Math.random()}`,
      timestamp: new Date().toISOString(),
      data: { node: nodeData },
    });

    return updatedNodes;
  });

  return;
}
```

- [ ] Add this handler in the bus subscription effect
- [ ] Ensure it runs before other handlers (order matters)
- [ ] Add console.log for debugging (remove before final commit)

### 3. Handle IR node structure vs ReactFlow node structure

**Important:** ReactFlow nodes have `data` property that contains the IR node data. The field paths from properties adapter refer to IR node properties, not ReactFlow properties.

Example ReactFlow node structure:
```typescript
{
  id: 'node-1',
  type: 'task',
  position: { x: 100, y: 100 },
  data: {
    // IR node properties here
    id: 'node-1',
    type: 'human',
    name: 'Review Task',
    config: {
      timing: { distribution: 'lognormal', params: {...} },
      operator: { type: 'analyst', count: 2 }
    }
  }
}
```

The field paths are relative to `node.data`, NOT the top-level ReactFlow node.

- [ ] Apply `setNestedValue()` to `node.data`, not `node`
- [ ] Clone `node.data` before mutation
- [ ] Update `node.data` reference to trigger React re-render

### 4. Update message type definitions

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\infrastructure\relay_bus\types\messages.ts`

Check if `properties:value-changed` and `canvas:node-updated` are defined. If not, add them:

- [ ] Add `'properties:value-changed'` to message type union (if missing)
- [ ] Add `'canvas:node-updated'` to message type union (if missing)
- [ ] Add TypeScript interfaces for the data payloads:

```typescript
export interface PropertiesValueChangedData {
  nodeId: string;
  field: string;
  value: any;
}

export interface CanvasNodeUpdatedData {
  node: IRNode;
}
```

- [ ] Export these interfaces
- [ ] Use them in the CanvasApp handler for type safety

### 5. Handle edge cases

- [ ] If `nodeId` doesn't match any canvas node, log warning and ignore
- [ ] If `field` is empty or undefined, log error and ignore
- [ ] If `value` is undefined, treat as property deletion (set to null or remove key)
- [ ] If nested path doesn't exist, create intermediate objects

## Test Requirements

**All tests MUST be written FIRST (TDD).**

### Test file: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\canvas\__tests__\CanvasApp.propertyUpdates.test.tsx`

Create a new test file specifically for property update integration.

- [ ] Test: setNestedValue() helper sets top-level property
- [ ] Test: setNestedValue() helper sets nested property (2 levels deep)
- [ ] Test: setNestedValue() helper sets deeply nested property (3+ levels)
- [ ] Test: setNestedValue() helper creates intermediate objects if missing
- [ ] Test: CanvasApp subscribes to properties:value-changed
- [ ] Test: Property change updates node data (top-level field like 'name')
- [ ] Test: Property change updates nested field (e.g., 'config.timing.distribution')
- [ ] Test: Property change for non-existent node is ignored
- [ ] Test: canvas:node-updated is published after property update
- [ ] All tests pass

### Test setup pattern:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import { ReactFlowProvider } from '@xyflow/react';
import { CanvasApp } from '../CanvasApp';

describe('CanvasApp - Property Updates', () => {
  let mockBus: any;

  beforeEach(() => {
    mockBus = {
      subscribe: vi.fn(),
      publish: vi.fn(),
      send: vi.fn(),
    };
  });

  it('updates node data when properties:value-changed is received', async () => {
    render(
      <ReactFlowProvider>
        <CanvasApp nodeId="canvas-1" bus={mockBus} />
      </ReactFlowProvider>
    );

    // Get the subscribe handler
    const subscribeCall = mockBus.subscribe.mock.calls.find(
      (call) => call[0] === 'canvas-1'
    );
    expect(subscribeCall).toBeDefined();
    const handler = subscribeCall[1];

    // Simulate properties:value-changed event
    await handler({
      type: 'properties:value-changed',
      sourcePane: 'properties',
      target: '*',
      nonce: '123',
      timestamp: new Date().toISOString(),
      data: { nodeId: 'node-1', field: 'name', value: 'New Name' },
    });

    // Assert that canvas:node-updated was published
    await waitFor(() => {
      expect(mockBus.publish).toHaveBeenCalledWith(
        expect.objectContaining({
          type: 'canvas:node-updated',
          data: expect.objectContaining({ node: expect.any(Object) }),
        })
      );
    });
  });
});
```

### Run tests with:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/__tests__/CanvasApp.propertyUpdates.test.tsx
```

### Regression test:

```bash
cd "C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser" && npx vitest run --reporter=verbose src/primitives/canvas/
```

## Constraints

- **No file over 500 lines.** If CanvasApp grows beyond 500 lines, extract property update logic into a separate hook (e.g., `usePropertyUpdates.ts`).
- **CSS: `var(--sd-*)` only** (if any CSS changes needed).
- **No stubs.** All functionality fully implemented.
- **TDD.** Tests written FIRST, then implementation.
- **No git operations** without Q88N approval.

## Acceptance Criteria

- [ ] CanvasApp subscribes to `properties:value-changed` events
- [ ] Nested property paths are correctly parsed and applied
- [ ] Node data is updated in ReactFlow state via `setNodes()`
- [ ] `canvas:node-updated` event is published after update
- [ ] Invalid node IDs are handled gracefully (log warning, no crash)
- [ ] At least 9 tests pass (one per scenario above)
- [ ] No regressions on existing canvas tests
- [ ] No file exceeds 500 lines

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260318-TASK-BL-121-B-RESPONSE.md`

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
