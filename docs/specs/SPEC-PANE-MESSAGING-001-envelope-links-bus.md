# SPEC-PANE-MESSAGING-001: Envelope, Links, and Bus Routing

## Summary

ShiftCenter Stage panes communicate through a relay bus using structured envelopes. The system has three layers:

1. **Envelope** — the LLM's structured response with named slots
2. **Links** — EGG-level config that maps slot names to target pane nodeIds
3. **Bus** — delivers messages point-to-point or broadcast

The key principle: **the sender addresses by slot name, the EGG resolves to a pane, the bus delivers. No pane needs to know another pane's type or implementation.**

## The Envelope

When a terminal pane sends user input to an LLM, the LLM returns a structured JSON envelope:

```json
{
  "to_user": "Here's your process flow.",
  "to_text": [{ "target": "editor", "format": "markdown", "ops": [{ "op": "append", "content": "..." }] }],
  "to_ir": { "id": "flow-1", "nodes": [...], "edges": [...] },
  "to_explorer": { "action": "reveal", "path": "/models" },
  "to_simulator": { "action": "run", "irId": "flow-1" },
  "to_bus": [{ "type": "custom:event", "target": "*", "data": {...} }]
}
```

### Built-in Slots

| Slot | Type | Purpose |
|------|------|---------|
| `to_user` | `string` | **Required.** Displayed to user in terminal Zone 2. |
| `to_terminal` | `string` | Short message for terminal display in chat mode. |
| `to_text` | `TextRouteItem[]` | Text operations (append, replace, etc.) sent to SDEditor panes. Each item has its own `target`. |
| `to_ir` | `object` | PHASE-IR flow data. Sent to the pane linked as `to_ir`. |
| `to_explorer` | `ExplorerRoute` | File explorer commands. Sent to the pane linked as `to_explorer`. |
| `to_simulator` | `SimulatorRoute` | Simulation engine commands. Sent to the pane linked as `to_simulator`. |
| `to_bus` | `BusMessage[]` | **Generic escape hatch.** Egg-defined messages with their own `type` and `target`. The router delivers without interpreting. |

### Rules

- `to_user` is always required. If missing, the router synthesizes a fallback.
- `to_text` items each carry their own `target` field (pane nickname or nodeId).
- `to_ir`, `to_explorer`, `to_simulator` use the **links config** to resolve their target.
- `to_bus` messages carry their own `type` and `target`. The router just delivers.
- **Never add app-specific slots** (no `to_turtle`, `to_chart`, `to_game`). Use `to_bus`.

## Links

Links are EGG-level config on a pane that map slot names to target pane nodeIds. They are the addressing system.

### How Links Are Defined

In the EGG layout, each pane's `config.links` maps slot names to nodeIds:

```json
{
  "type": "pane",
  "nodeId": "canvas-ir",
  "appType": "terminal",
  "label": "IR Generator",
  "config": {
    "routeTarget": "ai",
    "links": {
      "to_ir": "canvas-editor",
      "to_text": "properties-pane"
    }
  }
}
```

This means:
- When the LLM returns a `to_ir` slot, the router sends it to `canvas-editor`
- When the LLM returns a `to_text` slot targeting `"properties-pane"`, it goes there
- If a slot has no link, the router broadcasts to `*`

### How Links Flow Through the Code

```
EGG .egg.md → terminalAdapter.tsx → useTerminal.ts → paneRegistry → routeEnvelope()
     |              |                     |                |                |
  links: {      extracts           passes links       Map<slot,         resolveTarget()
  to_ir:        config.links       to hook            nodeId>           looks up target
  "canvas-1"    from EGG                                                in registry
  }
```

1. **EGG config** defines `links` on the terminal pane
2. **terminalAdapter** extracts `config.links` and passes to `TerminalApp`
3. **useTerminal** builds a `paneRegistry` Map from links: `{ "to_ir" → "canvas-editor" }`
4. **routeEnvelope** parses the LLM response, looks up each slot's target in the registry
5. **bus.send** delivers the message to the resolved nodeId

### Link Key Convention

Link keys should match the envelope slot name they serve:

| Link key | Envelope slot | Description |
|----------|--------------|-------------|
| `to_text` | `to_text` | Text operations to SDEditor panes |
| `to_ir` | `to_ir` | IR flow data to canvas panes |
| `to_explorer` | `to_explorer` | File tree commands |
| `to_simulator` | `to_simulator` | Simulation commands |

Custom names (e.g., `from_palette`, `to_properties`) are for non-envelope pane-to-pane links that apps manage directly.

## The Bus

The relay bus (`MessageBus`) delivers messages between panes.

### Message Envelope

Every bus message is a `MessageEnvelope`:

```typescript
interface MessageEnvelope<T = any> {
  type: string;         // Message type identifier
  sourcePane: string;   // Sender pane's nodeId
  target: string;       // Target nodeId or '*' for broadcast
  nonce: string;        // Replay protection
  timestamp: string;    // ISO timestamp
  data?: T;             // Payload
}
```

### Delivery Modes

- **Point-to-point**: `target: "canvas-editor"` — only that pane receives the message
- **Broadcast**: `target: "*"` — all subscribed panes receive the message

### Subscribing

Panes subscribe by their nodeId. The bus calls the handler for any message targeted at that pane (or broadcast):

```typescript
useEffect(() => {
  if (!bus || !nodeId) return;
  return bus.subscribe(nodeId, (msg: MessageEnvelope) => {
    // Inspect msg.data to decide what to do
    // Do NOT filter on msg.type — the data shape tells you what it is
  });
}, [bus, nodeId]);
```

### Sending

```typescript
bus.send({
  type: 'canvas:node-selected',
  sourcePane: nodeId,
  target: links?.to_properties || '*',
  nonce: `${Date.now()}-${Math.random()}`,
  timestamp: new Date().toISOString(),
  data: { id: node.id, label: node.data.label },
}, nodeId);
```

## Receiving Pattern: Data Shape, Not Message Type

**Panes should inspect the data shape, not filter on message type.**

The message `type` field is a hint for the sender — it describes what the sender thinks it's sending. But the receiver shouldn't depend on it. Instead, check the payload:

```typescript
// WRONG — couples receiver to sender's naming convention
if (msg.type === 'terminal:ir-deposit') {
  loadFlow(msg.data);
}

// RIGHT — receiver decides based on data shape
if (msg.data && Array.isArray(msg.data.nodes)) {
  loadFlow(msg.data);  // It's a flow — render it
} else if (msg.data?.node_id) {
  highlightNode(msg.data.node_id);  // It's a highlight command
}
```

This decoupling means:
- Any pane can send flow data to the canvas, not just terminals
- The canvas doesn't break if the sender changes its message type name
- New senders can be added without modifying the canvas

## Full Pipeline Example: Canvas EGG

### EGG Layout (canvas.egg.md)

```
Terminal (canvas-ir)                Canvas (canvas-editor)
  links:                              links:
    to_ir: "canvas-editor"              from_palette: "canvas-palette"
                                        to_properties: "canvas-properties"
```

### Flow

1. User types "create a 3-step approval flow" in the IR Generator terminal
2. LLM returns:
   ```json
   {
     "to_user": "Created a 3-step approval flow.",
     "to_ir": {
       "id": "flow-1",
       "nodes": [
         { "id": "start", "type": "source", "name": "Start" },
         { "id": "review", "type": "human", "name": "Review" },
         { "id": "approve", "type": "human", "name": "Approve" },
         { "id": "end", "type": "sink", "name": "End" }
       ],
       "edges": [
         { "id": "e1", "from_node": "start", "to_node": "review" },
         { "id": "e2", "from_node": "review", "to_node": "approve" },
         { "id": "e3", "from_node": "approve", "to_node": "end" }
       ]
     }
   }
   ```
3. `routeEnvelope()` parses the envelope
4. Finds `to_ir` slot → looks up `paneRegistry.get('to_ir')` → resolves to `"canvas-editor"`
5. Sends via `bus.send({ target: "canvas-editor", data: flow })`
6. Canvas at `canvas-editor` receives the message
7. Canvas inspects `msg.data` — has `nodes` array → loads as flow
8. ReactFlow renders 4 nodes with dagre layout

### What the canvas does NOT do:
- Filter on `msg.type === 'terminal:ir-deposit'` (it checks data shape)
- Know or care that the sender was a terminal
- Require a specific message type name

## File Locations

| File | Purpose |
|------|---------|
| `browser/src/services/terminal/types.ts` | Envelope types (TerminalEnvelope, TextRouteItem, BusMessage) |
| `browser/src/services/terminal/terminalResponseRouter.ts` | Parses envelopes, dispatches slots via bus |
| `browser/src/infrastructure/relay_bus/messageBus.ts` | MessageBus class (subscribe, send, delivery) |
| `browser/src/infrastructure/relay_bus/types/messages.ts` | MessageEnvelope type definition |
| `browser/src/apps/terminalAdapter.tsx` | Extracts links from EGG config, passes to terminal |
| `browser/src/primitives/terminal/useTerminal.ts` | Builds paneRegistry from links, calls routeEnvelope |
| `eggs/*.egg.md` | EGG layout files with pane links config |
