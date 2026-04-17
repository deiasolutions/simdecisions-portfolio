# SPEC-FACTORY-101: Fr4nk Factory System Prompt

**MODE: EXECUTE**

**Spec ID:** SPEC-FACTORY-101
**Created:** 2026-04-09
**Author:** Q88N
**Type:** CONFIG
**Status:** READY
**Phase:** P1 (after P0 complete)

---

## Priority
P1

## Depends On
None

## Reference
- P0 build (FACTORY-001 through 008) already complete
- MCP tools already exist (per telemetry survey)

## Model Assignment
sonnet

## Purpose

Give Fr4nk access to factory MCP tools and a system prompt that positions him as the factory operator's assistant. This transforms the existing terminal into a factory command interface. No new primitives — just prompt configuration.

**Deliverable:** System prompt file + tool manifest (~150 lines total)

---

## Current State

Per Mr. Code's research:
- Fr4nk exists as a service (`browser/src/services/frank/`)
- Currently scoped to "efemera greeter"
- Terminal already supports BYOK, voice, slash commands
- MCP server has 14 tools including queue/task/briefing/response CRUD

Fr4nk just needs:
1. Factory-specific system prompt
2. Tool manifest declaring available MCP tools
3. Context mode switch in terminal

---

## System Prompt

### browser/src/services/frank/prompts/factory.md

```markdown
# Fr4nk — Factory Operations Assistant

You are Fr4nk, the AI factory operations assistant for DEIA Solutions. You help Q88N (Dave) manage the AI bee factory — monitoring queue status, reviewing responses, approving gates, and submitting new specs.

## Your Role

You are the voice interface to the factory. When Q88N speaks or types, you:
1. Understand what they need
2. Call the appropriate MCP tools
3. Summarize results conversationally
4. Offer relevant follow-up actions

## Available Tools

You have access to these MCP tools:

### Queue Management
- `queue_list` — List tasks by status (pending, claimed, blocked, complete, failed)
- `queue_status` — Get current queue summary (counts by status)
- `queue_wake` — Wake the queue runner if idle

### Task Operations
- `task_read` — Read a specific task file
- `task_create` — Create a new task/spec in backlog
- `task_archive` — Archive a completed task

### Response Operations
- `response_list` — List bee response files
- `response_read` — Read a specific response file

### Briefing Operations
- `briefing_list` — List coordination briefings
- `briefing_read` — Read a specific briefing
- `briefing_write` — Write a new briefing

### Telemetry
- `heartbeat` — Send liveness heartbeat
- `status_report` — Get factory status summary
- `cost_summary` — Get CLOCK/COIN/CARBON totals

### Governance
- `approval_list` — List pending REQUIRE_HUMAN gates
- `approval_resolve` — Approve or reject a gate

### Dispatch
- `dispatch_bee` — Dispatch a task to a specific model

## Response Style

- Be concise. Q88N is busy.
- Lead with the answer, then offer details.
- When showing lists, summarize first: "3 tasks pending, 1 blocked."
- Offer actionable follow-ups: "Want me to show the blocked one?"
- Use inline primitives when helpful: [EMBED:queue-pane] to show the queue.

## Examples

**User:** "What's blocking?"
**You:** "BEE-003 is blocked on TASK-127 — waiting for REQUIRE_HUMAN approval on a deploy action. [Approve] [Reject] [Show details]"

**User:** "Status"
**You:** "Factory running. 2 bees active (sonnet, haiku). 5 tasks queued, 1 blocked, 12 completed today. $14.27 spent. Want the breakdown?"

**User:** "Write a spec for fixing the reconnect bug"
**You:** "Got it. What type — bug fix, feature, or refactor? And which model should handle it?"

**User:** "Bug, sonnet"
**You:** "Creating SPEC-BUG-SSE-RECONNECT-001. Priority P1 okay? [Submit] [Edit first]"

## Inline Primitives

When your response would benefit from showing a UI component, use:

```
[EMBED:queue-pane filter="blocked"]
[EMBED:approval-cards]
[EMBED:response-browser limit="5"]
[EMBED:dashboard metrics="clock,coin,carbon"]
```

The chat renderer will instantiate these inline.

## Constraints

- Never fabricate data. If you don't know, call a tool.
- Never approve gates without explicit user confirmation.
- Always confirm before destructive actions (archive, dispatch).
- Keep responses under 100 words unless showing details.

## Context

Current user: Q88N (Dave Eichler, Human Sovereign)
Current time: {timestamp}
Factory location: Austin, TX
```

---

## Tool Manifest

### browser/src/services/frank/toolManifests/factory.ts

```typescript
/**
 * Fr4nk Factory Tool Manifest
 * 
 * Declares MCP tools available in factory context.
 * Tools are called via hivenode MCP server at localhost:8421.
 */

export const FACTORY_TOOLS = {
  // Queue Management
  queue_list: {
    name: 'queue_list',
    description: 'List tasks by status',
    parameters: {
      status: { type: 'string', enum: ['all', 'pending', 'claimed', 'blocked', 'complete', 'failed'], default: 'all' },
      limit: { type: 'number', default: 20 },
    },
  },
  queue_status: {
    name: 'queue_status',
    description: 'Get queue summary with counts by status',
    parameters: {},
  },
  queue_wake: {
    name: 'queue_wake',
    description: 'Wake the queue runner if idle',
    parameters: {},
  },

  // Task Operations
  task_read: {
    name: 'task_read',
    description: 'Read a specific task file',
    parameters: {
      taskId: { type: 'string', required: true },
    },
  },
  task_create: {
    name: 'task_create',
    description: 'Create a new task/spec in backlog',
    parameters: {
      title: { type: 'string', required: true },
      type: { type: 'string', enum: ['bug', 'feature', 'refactor', 'research', 'test'], required: true },
      priority: { type: 'string', enum: ['P0', 'P1', 'P2'], required: true },
      model: { type: 'string', enum: ['haiku', 'sonnet', 'opus'], required: true },
      description: { type: 'string', required: true },
      dependsOn: { type: 'array', items: { type: 'string' }, default: [] },
    },
  },
  task_archive: {
    name: 'task_archive',
    description: 'Archive a completed task',
    parameters: {
      taskId: { type: 'string', required: true },
      responseId: { type: 'string' },
    },
  },

  // Response Operations
  response_list: {
    name: 'response_list',
    description: 'List bee response files',
    parameters: {
      status: { type: 'string', enum: ['all', 'pending', 'reviewed', 'archived'], default: 'all' },
      limit: { type: 'number', default: 10 },
    },
  },
  response_read: {
    name: 'response_read',
    description: 'Read a specific response file',
    parameters: {
      responseId: { type: 'string', required: true },
    },
  },

  // Telemetry
  status_report: {
    name: 'status_report',
    description: 'Get factory status summary',
    parameters: {},
  },
  cost_summary: {
    name: 'cost_summary',
    description: 'Get CLOCK/COIN/CARBON totals for current session',
    parameters: {
      period: { type: 'string', enum: ['today', 'week', 'month', 'all'], default: 'today' },
    },
  },

  // Governance
  approval_list: {
    name: 'approval_list',
    description: 'List pending REQUIRE_HUMAN gates',
    parameters: {},
  },
  approval_resolve: {
    name: 'approval_resolve',
    description: 'Approve or reject a gate',
    parameters: {
      gateId: { type: 'string', required: true },
      disposition: { type: 'string', enum: ['approved', 'rejected'], required: true },
      note: { type: 'string' },
    },
  },

  // Dispatch
  dispatch_bee: {
    name: 'dispatch_bee',
    description: 'Dispatch a task to a specific model',
    parameters: {
      taskId: { type: 'string', required: true },
      model: { type: 'string', enum: ['haiku', 'sonnet', 'opus'], required: true },
    },
  },
};

export type FactoryToolName = keyof typeof FACTORY_TOOLS;
```

---

## Terminal Mode Switch

### Update: browser/src/primitives/terminal/terminalModes.ts

Add `factory` mode:

```typescript
export const TERMINAL_MODES = {
  standalone: { /* existing */ },
  pane: { /* existing */ },
  bus: { /* existing */ },
  factory: {
    label: 'Factory',
    agent: 'fr4nk',
    context: 'factory',
    systemPrompt: '/prompts/factory.md',
    tools: FACTORY_TOOLS,
    mcpEndpoint: 'http://localhost:8421',
    voiceEnabled: true,
    autoRead: true,  // TTS responses on mobile
  },
};
```

---

## File Targets

| File | Action | Lines |
|------|--------|-------|
| `browser/src/services/frank/prompts/factory.md` | CREATE | ~100 |
| `browser/src/services/frank/toolManifests/factory.ts` | CREATE | ~100 |
| `browser/src/primitives/terminal/terminalModes.ts` | MODIFY | +15 |

---

## Reference Files

Read before implementation:
- `browser/src/services/frank/` — existing Fr4nk service
- `browser/src/primitives/terminal/` — terminal implementation
- `hivenode/hive_mcp/local_server.py` — MCP tool definitions
- `browser/src/primitives/terminal/terminalModes.ts` — if exists

---

## Acceptance Criteria

- [ ] Factory system prompt exists at `prompts/factory.md`
- [ ] Tool manifest exports `FACTORY_TOOLS`
- [ ] Terminal mode `factory` added
- [ ] Fr4nk responds to "status" with factory summary
- [ ] Fr4nk calls MCP tools correctly
- [ ] Voice input works in factory mode
- [ ] Responses are concise (<100 words default)

## Smoke Test

```bash
# Files exist
test -f browser/src/services/frank/prompts/factory.md && echo "Prompt exists" || echo "MISSING"
test -f browser/src/services/frank/toolManifests/factory.ts && echo "Manifest exists" || echo "MISSING"

# Manual test:
# 1. Open terminal with ?mode=factory
# 2. Type "status"
# 3. Verify Fr4nk calls status_report tool
# 4. Verify concise response
```

## Constraints

- System prompt under 150 lines
- No changes to Fr4nk core service
- Tools call existing MCP endpoints
- Voice response via existing TTS

## Response File

`.deia/hive/responses/20260409-FACTORY-101-RESPONSE.md`

---

*SPEC-FACTORY-101 — Q88N — 2026-04-09*
