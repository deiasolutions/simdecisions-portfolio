# Canvas Chatbot Dialect Specification

**Status:** IMPLEMENTED
**Date:** 2026-03-15
**Version:** 1.0

## Overview

The Canvas Chatbot Dialect is a natural language interface for building and modifying PHASE-IR process flows. Users type natural language descriptions of process workflows, and the system translates them into structured mutations that update the PHASE-IR graph.

**Flow:** User Message → Claude LLM (with tools) → IR Mutations → JSON Patch → Canvas Renders

## System Architecture

### Components

1. **Canvas Chat Endpoint** (`hivenode/routes/canvas_chat.py`)
   - FastAPI POST route at `/api/canvas/chat`
   - Accepts: flow_id, message, current_ir, optional history
   - Returns: mutations, JSON Patch changes, confirmation message

2. **LLM Service** (`hivenode/canvas/llm_service.py`)
   - Formats current IR state for LLM context
   - Calls Claude Opus 4.6 with 6 tool definitions
   - Parses tool calls from response

3. **Mutation Applier** (`hivenode/canvas/mutation_applier.py`)
   - Applies mutations to IR graphs
   - Validates nodes/edges exist before mutations
   - Detects cycles and orphan nodes
   - Generates RFC 6902 JSON Patch diffs

4. **Mutation Models** (`hivenode/canvas/mutation_models.py`)
   - Pydantic model: `MutationResult` (success, changes, error)

## LLM Tools (6 mutation actions)

### 1. add_node

Add a new node to the process flow.

**Input Schema:**
```json
{
  "id": "string (snake_case, required)",
  "type": "string (task|decision|start|end|subprocess|event, required)",
  "label": "string (human-readable, required)",
  "after": "string (optional node ID to connect from)"
}
```

**Behavior:**
- Creates new node with given ID, type, label
- If `after` is provided, automatically creates edge from that node
- Fails if node ID already exists

**Example:**
```
User: "Add an approval step"
→ LLM calls add_node(id="approval_001", type="task", label="Approval")
→ Mutation returned
```

### 2. add_edge

Add a connection between two nodes.

**Input Schema:**
```json
{
  "source": "string (source node ID, required)",
  "target": "string (target node ID, required)",
  "label": "string (optional edge label)",
  "condition": "string (optional condition for branches)"
}
```

**Behavior:**
- Creates edge from source to target
- Detects cycles (rejects if edge would create cycle)
- Detects duplicates (rejects duplicate source→target edges)
- Auto-generates edge ID: `{source}-{target}` if not provided

**Example:**
```
User: "Connect review to approval"
→ LLM calls add_edge(source="review_001", target="approval_001")
```

### 3. update_node

Modify properties of an existing node.

**Input Schema:**
```json
{
  "id": "string (node ID, required)",
  "properties": {
    "label": "string (optional)",
    "type": "string (optional)",
    "...": "any other properties"
  }
}
```

**Behavior:**
- Updates specified properties on existing node
- Fails if node doesn't exist
- Supports any property (label, type, custom attributes)

**Example:**
```
User: "Change the review step label to QA Review"
→ LLM calls update_node(id="review_001", properties={"label": "QA Review"})
```

### 4. remove_node

Remove a node from the flow.

**Input Schema:**
```json
{
  "id": "string (node ID, required)"
}
```

**Behavior:**
- Removes node from graph
- **Orphan Protection:** Fails if node has incoming edges
- Fails if node doesn't exist

**Example:**
```
User: "Remove the obsolete step"
→ LLM calls remove_node(id="obsolete_001")
```

### 5. remove_edge

Remove a connection between nodes.

**Input Schema:**
```json
{
  "source": "string (source node ID, required)",
  "target": "string (target node ID, required)"
}
```

**Behavior:**
- Canvas chat endpoint looks up edge ID from source/target
- Removes edge from graph
- Returns error if edge not found

**Example:**
```
User: "Remove the connection from start to task"
→ LLM returns source="start_001", target="task_001"
→ Canvas endpoint finds edge ID, calls remove_edge
```

### 6. clarify

Ask user for clarification when request is ambiguous.

**Input Schema:**
```json
{
  "question": "string (question to ask, required)",
  "options": ["string (optional choices)"]
}
```

**Behavior:**
- Immediately returns to user without applying any mutations
- Response includes `needs_clarification=true`
- Frontend should prompt user with question and options

**Example:**
```
User: "Add an approval step" (but multiple nodes match)
→ LLM calls clarify(
    question="Where should I add the approval step?",
    options=["After review", "After intake", "At the end"]
)
→ Response: needs_clarification=true, message=question, options=[...]
```

## System Prompt Rules

The LLM is instructed to:

1. **Use snake_case IDs** consistently (e.g., `review_001`, `approval_002`)
2. **Handle "after" parameter** when user says "add X after Y"
3. **Create decision branches** by adding edges with conditions
4. **Use clarify tool** when ambiguous (multiple nodes match)
5. **Confirm actions** in responses with `[node_id]` format

**System Prompt Template:**
```
You are a process design assistant. Translate natural language into process flow mutations.

Current flow state:
{flow_json}

Rules:
1. Use snake_case IDs (e.g., review_001, approval_002)
2. When user says "after X", set after=X in add_node payload
3. For decisions, create edges for each branch with conditions
4. If ambiguous (multiple nodes match), use clarify tool
5. If node not found, suggest closest matches in the question

Always confirm what you did using [node_id] format for references.
Example: "Added [review_001] after [intake_001]"

When adding multiple nodes in sequence, use the "after" parameter to chain them automatically.
```

## Request/Response Format

### Request: POST /api/canvas/chat

```json
{
  "flow_id": "string (flow identifier)",
  "message": "string (natural language message)",
  "current_ir": {
    "nodes": {
      "node_id": {
        "id": "node_id",
        "type": "task|decision|...",
        "label": "Human Label",
        ...other properties
      }
    },
    "edges": [
      {
        "id": "edge_id",
        "source": "node_id",
        "target": "node_id",
        ...other properties
      }
    ]
  },
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

### Response: CanvasChatResponse

```json
{
  "message": "string (confirmation or clarification question)",
  "mutations": [
    {
      "action": "add_node|add_edge|update_node|remove_node|remove_edge",
      "payload": {...tool input...}
    }
  ],
  "changes": [
    {
      "op": "add|replace|remove",
      "path": "/nodes/node_id or /edges/edge_id",
      "value": {...}
    }
  ],
  "errors": ["error message", ...],
  "needs_clarification": false,
  "options": null
}
```

### Clarification Response

```json
{
  "message": "Where should I add the approval step?",
  "mutations": [],
  "changes": [],
  "errors": null,
  "needs_clarification": true,
  "options": ["After review", "After start", "At the end"]
}
```

## Validation & Error Handling

### Validation Rules

1. **Node ID uniqueness:** Cannot add node with existing ID
2. **Node existence:** Must reference existing nodes in add_edge, update_node
3. **Cycle detection:** add_edge fails if would create cycle
4. **Duplicate edges:** Cannot create multiple edges with same source→target
5. **Orphan protection:** Cannot remove node with incoming edges
6. **Edge ID lookup:** remove_edge requires looking up edge ID from source/target

### Error Responses

All errors are returned in the `errors` array with descriptive messages:

```json
{
  "errors": [
    "Node 'review_001' already exists",
    "Cannot remove node 'start_001': has incoming edges (orphan detection)",
    "Adding edge would create a cycle"
  ]
}
```

## Mutation Application & Patch Generation

### Application Process

1. LLM returns tool calls
2. For each tool call:
   - Convert to mutation format: `{action, payload}`
   - Apply via `apply_mutation(ir, mutation)`
   - If successful:
     - Add to mutations list
     - Collect changes (JSON Patch operations)
     - Update current_ir for next mutation
     - Check if `after` parameter exists (auto-create edge)
   - If failed:
     - Add error message to errors list
     - Skip mutation, continue with next

### JSON Patch Format (RFC 6902)

Changes are returned as RFC 6902 JSON Patch operations:

```json
[
  {
    "op": "add",
    "path": "/nodes/approval_001",
    "value": {
      "id": "approval_001",
      "type": "task",
      "label": "Approval"
    }
  },
  {
    "op": "add",
    "path": "/edges/task_001-approval_001",
    "value": {
      "id": "task_001-approval_001",
      "source": "task_001",
      "target": "approval_001"
    }
  }
]
```

Supported operations:
- `op: "add"` — add node or edge
- `op: "replace"` — update node properties
- `op: "remove"` — remove node or edge

## Integration with Terminal

### Message Flow

1. User types in terminal pane (in `routeTarget: 'ir'` mode)
2. Terminal calls `/api/canvas/chat` endpoint
3. Response includes:
   - `message` → sent to text-pane (if linked)
   - `changes` → sent to canvas as mutations
   - Canvas renders updated graph

### Bus Message: terminal:ir-deposit

Terminal sends mutations to canvas via bus message:

```typescript
bus.send({
  type: 'terminal:ir-deposit',
  sourcePane: 'terminal-node-id',
  target: 'canvas-node-id',
  nonce: '...',
  timestamp: Date.now(),
  data: {
    // Each IR block from LLM response
    nodes: {...},
    edges: [...]
  }
});
```

## Example Usage

### Scenario 1: Add a Single Node

```
User: "Add an approval step after the review"

System Prompt Context:
  Nodes: start_001 (start), review_001 (task)
  Edges: start_001 → review_001

LLM Response:
  Tool: add_node(
    id="approval_001",
    type="task",
    label="Approval",
    after="review_001"
  )

Canvas Chat Response:
{
  "message": "Added [approval_001] after [review_001]",
  "mutations": [
    {"action": "add_node", "payload": {...}},
    {"action": "add_edge", "payload": {"source": "review_001", "target": "approval_001"}}
  ],
  "changes": [
    {"op": "add", "path": "/nodes/approval_001", "value": {...}},
    {"op": "add", "path": "/edges/review_001-approval_001", "value": {...}}
  ]
}
```

### Scenario 2: Clarification

```
User: "Update the review step"
(Multiple nodes contain "review" in label)

LLM Response:
  Tool: clarify(
    question="Which step would you like to update?",
    options=["review_001 (Review)", "review_assessment_001 (Review Assessment)"]
  )

Canvas Chat Response:
{
  "message": "Which step would you like to update?",
  "needs_clarification": true,
  "options": ["review_001 (Review)", "review_assessment_001 (Review Assessment)"]
}
```

### Scenario 3: Invalid Mutation

```
User: "Remove the start node"

LLM Response:
  Tool: remove_node(id="start_001")

Canvas Chat Response:
{
  "message": "⚠️ Some operations failed: Cannot remove node 'start_001': has incoming edges",
  "errors": ["remove_node failed: Cannot remove node 'start_001': has incoming edges (orphan detection)"]
}
```

## Implementation Details

### File Structure

```
hivenode/canvas/
  __init__.py
  mutation_models.py      # MutationResult dataclass
  mutation_applier.py     # apply_mutation(), add_node(), etc.
  llm_service.py          # call_llm(), generate_confirmation_message()

hivenode/routes/
  canvas_chat.py          # canvas_chat() endpoint
```

### Dependencies

- **FastAPI:** Web framework
- **Pydantic:** Request/response models
- **httpx:** Async HTTP client for Anthropic API
- **jsonpatch:** JSON Patch (RFC 6902) utilities

### Model

- **Claude Opus 4.6** (latest, most capable) for natural language understanding
- Fallback to **Claude Haiku 4.5** if server key (cost control)

## Testing

### Test Coverage (9 tests)

1. `test_add_node_mutation` — add node with tool call
2. `test_clarify_tool_returns_clarification` — clarify tool behavior
3. `test_invalid_mutation_returns_error` — error handling
4. `test_add_edge_mutation` — add edge tool call
5. `test_update_node_mutation` — update node tool call
6. `test_confirmation_message_generation_when_no_text` — auto-confirmation
7. `test_add_node_with_after_creates_edge` — auto-edge creation
8. `test_remove_edge_finds_edge_id` — edge lookup
9. Additional edge cases as needed

### Running Tests

```bash
pytest tests/hivenode/test_canvas_chat.py -v
```

## Acceptance Criteria

- [x] Endpoint accepts POST with flow_id, message, current_ir
- [x] LLM service has 6 tools with clear schemas
- [x] Mutations return JSON Patch (RFC 6902)
- [x] System prompt enforces snake_case IDs, "after" chaining, decision branches
- [x] Mutation applier validates before applying
- [x] All 9 tests passing
- [x] Routes registered at /api/canvas/chat
- [x] Dialect spec documents NL → LLM → IR → render flow
- [x] No regressions in existing tests

## Future Enhancements

1. **Conversation memory** — Multi-turn dialog with history preservation
2. **Bulk operations** — User requests multiple changes at once
3. **Visualization suggestions** — LLM suggests node positions/colors
4. **Decision trees** — Specialized syntax for complex branching
5. **Rollback** — Undo mechanism for mutations
6. **Rate limiting** — Per-user API rate limits
