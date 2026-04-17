# Terminal-to-Canvas IR Wiring Specification

**Status:** IMPLEMENTED
**Date:** 2026-03-15
**Version:** 1.0

## Overview

This document specifies how the Terminal pane (natural language interface) communicates with the Canvas pane (visual process designer) to exchange IR mutations.

**Flow:** Terminal `routeTarget: 'ir'` → `/api/canvas/chat` → JSON Patch mutations → Canvas renders

## Architecture

### Communication Pattern

```
┌─────────────────┐         POST /api/canvas/chat      ┌──────────────┐
│   Terminal      │  (flow_id, message, current_ir)    │ Canvas Chat  │
│   (useTerminal) │──────────────────────────────────→│  Endpoint    │
│ routeTarget=ir  │                                     └──────────────┘
│                 │    CanvasChatResponse               │
│                 │    (mutations, changes, message)    │
│                 │←─────────────────────────────────────│
└─────────────────┘                                      │ mutation_applier
                                                         │ llm_service
                  ┌─────────────────────────────────┐   │
                  │       bus.send()                │   │
                  │  terminal:ir-deposit message    │   │
                  └─────────────────────────────────┘
                          │
        ┌───────────────────┼───────────────────┐
        ▼                                       ▼
   ┌──────────┐                         ┌──────────────┐
   │ Text-Pane│                         │ Canvas Pane  │
   │ (chat    │                         │ (renders     │
   │ messages)│                         │  mutations)  │
   └──────────┘                         └──────────────┘
```

### Components

1. **Terminal Pane** (`useTerminal.ts`)
   - User types natural language message
   - Sends message to LLM (via server)
   - In IR mode (`routeTarget: 'ir'`):
     - Calls `/api/canvas/chat` endpoint
     - Publishes mutations to canvas via message bus

2. **Canvas Chat Endpoint** (`hivenode/routes/canvas_chat.py`)
   - Accepts request with: flow_id, message, current_ir
   - Calls LLM with 6 mutation tools
   - Applies mutations to IR graph
   - Returns JSON Patch changes

3. **Canvas Pane** (receives via message bus)
   - Listens for `terminal:ir-deposit` messages
   - Extracts mutations from message data
   - Applies to local IR state
   - Re-renders graph

4. **Text-Pane** (receives via message bus)
   - Listens for `terminal:text-patch` messages
   - Appends chat confirmation text
   - Shows conversation history

## Message Bus Protocol

### Bus Message: terminal:ir-deposit

**Type:** One-way message from terminal to canvas

**Format:**
```typescript
{
  type: 'terminal:ir-deposit',
  sourcePane: string,        // Terminal pane node ID
  target: string,            // Canvas pane node ID
  nonce: string,             // Unique identifier for deduplication
  timestamp: number,         // Unix timestamp (ms)
  data: {
    // Full or partial PHASE-IR state
    nodes: { [id]: {...} },
    edges: [{...}],
    metadata: {...}
  }
}
```

**Example:**
```json
{
  "type": "terminal:ir-deposit",
  "sourcePane": "terminal-pane-123",
  "target": "canvas-pane-456",
  "nonce": "1678902400000-0.456",
  "timestamp": 1678902400000,
  "data": {
    "nodes": {
      "approval_001": {
        "id": "approval_001",
        "type": "task",
        "label": "Approval"
      }
    },
    "edges": [{
      "id": "task_001-approval_001",
      "source": "task_001",
      "target": "approval_001"
    }]
  }
}
```

### Bus Message: terminal:text-patch

**Type:** One-way message from terminal to text-pane

**Format:**
```typescript
{
  type: 'terminal:text-patch',
  sourcePane: string,        // Terminal pane node ID
  target: string,            // Text-Pane node ID
  nonce: string,             // Unique identifier
  timestamp: number,         // Unix timestamp (ms)
  data: {
    format: 'markdown',
    ops: [
      {
        op: 'append',
        content: string        // Text to append (markdown)
      }
    ]
  }
}
```

**Example:**
```json
{
  "type": "terminal:text-patch",
  "sourcePane": "terminal-pane-123",
  "target": "text-pane-789",
  "nonce": "1678902400000-0.789",
  "timestamp": 1678902400000,
  "data": {
    "format": "markdown",
    "ops": [
      {
        "op": "append",
        "content": "**claude-opus-4-6:** Added [approval_001] after [task_001]\n\n"
      }
    ]
  }
}
```

## Endpoint: POST /api/canvas/chat

### Request

**Method:** POST
**Path:** `/api/canvas/chat`
**Content-Type:** `application/json`

**Body Schema:**
```json
{
  "flow_id": "string (required, min length 1)",
  "message": "string (required, min length 1)",
  "current_ir": {
    "nodes": {
      "node_id": {
        "id": "string",
        "type": "task|decision|start|end|subprocess|event",
        "label": "string",
        "...": "any"
      }
    },
    "edges": [
      {
        "id": "string",
        "source": "string",
        "target": "string",
        "...": "any"
      }
    ],
    "...": "any"
  },
  "history": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ]
}
```

### Response

**Status Code:** 200 OK (or 500 for LLM errors)

**Body Schema:**
```json
{
  "message": "string (confirmation or clarification)",
  "mutations": [
    {
      "action": "add_node|add_edge|update_node|remove_node|remove_edge",
      "payload": {
        "...": "action-specific fields"
      }
    }
  ],
  "changes": [
    {
      "op": "add|replace|remove",
      "path": "/nodes/id or /edges/id",
      "value": {
        "...": "any"
      }
    }
  ],
  "errors": ["error message", ...] | null,
  "needs_clarification": boolean,
  "options": ["option1", ...] | null
}
```

## Terminal Implementation (useTerminal.ts)

### IR Mode Detection

```typescript
const isIRMode = settings.routeTarget === 'ir';
const irTargetId = settings.routeTargets?.ir;
const chatTargetId = settings.routeTargets?.chat;
```

### Sending Request to Canvas Chat Endpoint

```typescript
if (isIRMode && irTargetId) {
  const response = await fetch('/api/canvas/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      flow_id: flowId,
      message: userMessage,
      current_ir: canvasState,  // From canvas pane or sessionStorage
      history: conversationHistory
    })
  });

  const result = await response.json() as CanvasChatResponse;

  if (result.needs_clarification) {
    // Show clarification UI
    return showClarificationDialog(result.message, result.options);
  }

  // Handle mutations
  const { chatText, mutations, changes } = result;

  // Send chat text to text-pane
  if (chatText && chatTargetId) {
    bus.send({
      type: 'terminal:text-patch',
      sourcePane: nodeId,
      target: chatTargetId,
      nonce: `${Date.now()}-${Math.random()}`,
      timestamp: Date.now(),
      data: {
        format: 'markdown',
        ops: [{ op: 'append', content: `**${model}:** ${chatText}\n\n` }]
      }
    });
  }

  // Send IR mutations to canvas
  if (changes.length > 0 && irTargetId) {
    bus.send({
      type: 'terminal:ir-deposit',
      sourcePane: nodeId,
      target: irTargetId,
      nonce: `${Date.now()}-${Math.random()}`,
      timestamp: Date.now(),
      data: {
        nodes: applyChanges(currentIR.nodes, changes),
        edges: applyChanges(currentIR.edges, changes)
      }
    });
  }
}
```

## Canvas Implementation (Canvas Component)

### Receiving IR Mutations

```typescript
// Listen for IR deposits from terminal
bus.subscribe('terminal:ir-deposit', (message) => {
  if (message.target === currentPaneId) {
    const { nodes, edges } = message.data;

    // Update local IR state
    graphStore.updateNodes(nodes);
    graphStore.updateEdges(edges);

    // Re-render canvas
    refresh();

    // Optionally: show confirmation toast
    toast.success(`Updated from terminal`);
  }
});
```

## Data Flow Walkthrough

### Scenario: User adds a node via terminal

```
1. User types in terminal: "Add an approval step after the review"
   └─ Terminal mode: routeTarget = 'ir'

2. Terminal sends request to /api/canvas/chat:
   ├─ flow_id: "flow-123"
   ├─ message: "Add an approval step after the review"
   ├─ current_ir: { nodes: {...}, edges: [...] }
   └─ history: [...]

3. Canvas Chat Endpoint:
   ├─ Call LLM with tools
   ├─ LLM returns tool call: add_node(id="approval_001", after="review_001")
   ├─ Apply mutation via mutation_applier
   ├─ Auto-detect "after" and create edge mutation
   ├─ Generate JSON Patch changes
   └─ Return: { mutations, changes, message: "Added [approval_001]..." }

4. Terminal receives response:
   ├─ Extract message: "Added [approval_001]..."
   ├─ Send to text-pane: terminal:text-patch
   │  └─ Appends confirmation message
   └─ Send to canvas: terminal:ir-deposit
      └─ Contains updated nodes/edges

5. Canvas receives terminal:ir-deposit:
   ├─ Extract nodes and edges
   ├─ Apply to local IR state
   └─ Re-render graph (new node visible, connected)

6. Text-pane receives terminal:text-patch:
   ├─ Extract message
   └─ Append to chat history
```

## Clarification Flow

```
1. User types: "Update the step"
   └─ Ambiguous (multiple nodes with "step" in label)

2. Terminal sends to /api/canvas/chat
   └─ No mutations applied yet

3. Canvas Chat Endpoint:
   ├─ LLM determines ambiguity
   ├─ Calls clarify tool:
   │  ├─ question: "Which step would you like to update?"
   │  └─ options: ["task_001 (Review)", "task_002 (Approval)"]
   └─ Returns: { needs_clarification: true, message, options }

4. Terminal receives response:
   ├─ Detects needs_clarification = true
   ├─ Shows clarification dialog with options
   └─ Waits for user selection

5. User selects option: "task_001 (Review)"
   └─ Terminal re-sends request with clarified message

6. Second request proceeds normally
   └─ Mutation applied, canvas updated
```

## Error Handling

### API Errors (5xx)

If LLM service fails or API key is missing:
```json
{
  "detail": "LLM call failed: ANTHROPIC_API_KEY not set"
}
```

Terminal shows error toast and does NOT send mutations to canvas.

### Validation Errors

If mutation violates constraints (e.g., cycle, orphan, duplicate):
```json
{
  "message": "⚠️ Some operations failed:\n• Cannot remove node 'start_001': has incoming edges",
  "errors": ["remove_node failed: Cannot remove node 'start_001': has incoming edges (orphan detection)"]
}
```

Terminal appends error to text-pane but does NOT send mutations to canvas (no changes).

## Configuration

### Terminal Settings (in EGG or localStorage)

```typescript
{
  routeTarget: 'ir',                  // Target 'ir' for canvas chat
  routeTargets: {
    ir: 'canvas-pane-456',            // Canvas pane ID to send IR to
    chat: 'text-pane-789'             // Text-pane ID for confirmation
  }
}
```

### Environment Variables

- `ANTHROPIC_API_KEY` — API key for Claude (required on server)

## Testing

### Test Cases

1. **Single node addition** — Terminal sends request, canvas renders new node
2. **Auto-edge creation** — Terminal sends add_node with "after", canvas shows edge
3. **Clarification** — Terminal receives clarification response, shows dialog
4. **Error handling** — Terminal receives error, does NOT update canvas
5. **Multi-turn conversation** — Terminal preserves history across requests
6. **Concurrent messages** — Multiple message.send() calls don't conflict (nonce deduplication)

### Manual Testing

1. Start dev server: `npm run dev`
2. Navigate to shell with terminal and canvas panes
3. In terminal, switch to IR mode
4. Type: "Create a workflow with start, review, approval, and end steps"
5. Verify:
   - Canvas shows 4 new nodes
   - Edges connect them in sequence
   - Text-pane shows confirmation message
6. Type: "Update the review label to QA Review"
7. Verify:
   - Canvas node label updates
   - Text-pane confirms change

## Backwards Compatibility

- Terminal defaults to `routeTarget: 'text'` (chat mode, no canvas)
- Canvas defaults to NOT listening for IR mutations
- Existing terminal functionality unaffected
- No breaking changes to Canvas component

## Future Enhancements

1. **Bulk mutations** — Multiple mutations in single request
2. **Conditional branches** — Decision nodes with branches
3. **Visual suggestions** — LLM suggests node positions, colors
4. **Undo/Redo** — Store mutation history, allow rollback
5. **Real-time sync** — WebSocket instead of POST (for large flows)
6. **Version control** — Track changes, show diffs
7. **Collaboration** — Multiple users editing same flow
