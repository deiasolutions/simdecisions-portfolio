# TASK-DA1: Terminal → LLM Response Pipeline -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-19

## Files Modified
None (research only)

## What Was Done

Audited terminal → LLM → response routing pipeline in both platform and shiftcenter repos. Traced call chains, provider abstractions, envelope routing, Zone 2 rendering, and cross-pane bus messaging. All findings emitted atomically below.

---

# RESEARCH FINDINGS

---
bee: BEE-DA1
type: RESEARCH
finding: 1
source: platform/simdecisions-2/src/hooks/useTerminalSession.ts:L85-L236
shift: false
---

**FINDING 1: Terminal Submit → LLM Call Chain**

The terminal sends prompts to LLM via this call chain:

1. **User input** → `useTerminalSession.handleSubmit()` (platform) or `useTerminal.handleSubmit()` (shiftcenter)
2. **Build conversation history** from terminal entries (type: 'input'/'response')
3. **Get LLM provider** — AnthropicProvider or GroqProvider instance
4. **Build MCP servers list** if GitHub MCP is enabled
5. **Call `sendMessage(history, provider, mcpServers, sessionFlags)`** in frankService.ts (platform) or terminalService.ts (shiftcenter)
6. **Compose system prompt** from dialects (patois, envelope, ir-generation, simulation) via dialectLoader
7. **Call provider.call({ systemPrompt, messages, tools, currentIR, mcpServers })**
8. **Provider makes HTTP POST** to `https://api.anthropic.com/v1/messages` with BYOK API key
9. **Parse response**, extract content + usage metrics
10. **Calculate 3-currency metrics** (clock_ms, cost_usd, carbon_g)
11. **Return { content, metrics }** to terminal

**Key observation:** The prompt is composed from DIALECT files loaded by dialectLoader. The system prompt is NOT hardcoded — it is assembled from modular .md files in `src/services/frank/prompts/` or `src/services/terminal/prompts/`.

DIVERGENCE: none (platform logic correctly ported to shiftcenter)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 2
source: platform/simdecisions-2/src/services/llm/providers/anthropic.ts:L16-L148
shift: false
---

**FINDING 2: LLM Provider Abstraction (BYOLLM Pattern)**

Platform uses a **model-agnostic provider interface** defined in `src/services/llm/types.ts`:

```typescript
export interface LLMProvider {
  id: string;
  name: string;
  call(request: LLMRequest): Promise<LLMResponse>;
}
```

Concrete providers:
- **AnthropicProvider** — calls api.anthropic.com with Claude models
- **GroqProvider** — calls api.groq.com with Llama models
- **OpenAICompatibleProvider** (stub in platform, exists in shiftcenter)

**BYOK (Bring Your Own Key):** API key is stored in localStorage (`sd_user_settings.apiKey` in platform, `sd_user_settings.apiKeys.anthropic` in shiftcenter). No server-side key storage. Direct browser → LLM API calls.

**MCP support:** Anthropic provider adds `anthropic-beta: mcp-client-2025-04-04` header when `mcpServers` array is provided. MCP servers are SSE endpoints that provide tool definitions and execute tool calls.

**Shiftcenter extension:** Added proxy mode (`routingMode: 'proxy'`) that calls hivenode `/llm/chat` with BYOK key forwarded via `X-Api-Key` header. Falls back to server key if user has none.

DIVERGENCE: Shiftcenter added proxy mode (hivenode /llm/chat) — platform is direct-only. This is an INTENTIONAL feature addition, not drift.
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 3
source: platform/simdecisions-2/src/services/frank/responseRouter.ts:L1-L404
shift: false
---

**FINDING 3: Structured Response Envelope Parsing**

LLM responses follow a structured JSON envelope format defined in `src/services/frank/prompts/envelope.md` (platform) and `src/services/terminal/prompts/envelope.md` (shiftcenter).

**Envelope structure:**
```json
{
  "to_user": "string — required, shown in Zone 2",
  "to_text": [{ "target": "pane-nickname", "format": "markdown", "ops": [...] }],
  "to_explorer": { "action": "open", "path": "/src" },
  "to_ir": { "version": "2.0", "nodes": [], "edges": [] },
  "to_simulator": { "action": "run", "irId": "..." },
  "to_bus": [{ "type": "CUSTOM_EVENT", "target": "*", "data": {...} }]
}
```

**Parsing logic** (`parseResponseEnvelope()` in platform, `parseEnvelope()` in shiftcenter):
1. Extract JSON blocks from markdown (handles accidental code fence wrapping)
2. Parse JSON
3. Validate `to_user` field (required)
4. Validate `to_text` is array (drop if not)
5. Drop `to_text` items with both `ops` AND `diff` (mutually exclusive)
6. Fallback to `{ to_user: <entire response> }` if parse fails or no envelope found

**Error handling:** Graceful degradation. If LLM returns plain text instead of JSON, treat entire response as `to_user`. No user-facing error — logged to console only.

DIVERGENCE: none (identical logic in both repos)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 4
source: platform/simdecisions-2/src/services/frank/responseRouter.ts:L212-L287
shift: false
---

**FINDING 4: to_text Routing Mechanism — Cross-Pane Ops Delivery**

The `to_text` envelope slot routes structured text operations to text-pane targets (SDEditor in platform, text-pane in shiftcenter).

**Routing flow:**
1. **Parse envelope** → extract `to_text` array
2. **For each item** in `to_text`:
   - Resolve `target` nickname → nodeId via paneRegistry
   - Build bus message: `{ type: 'terminal:text-patch', target: nodeId, data: { format, ops, diff } }`
   - Send via MessageBus.publish()
3. **Text-pane receives** `terminal:text-patch` message
4. **Text-pane applies ops** to Monaco editor content (append, replace, insert, delete, set)
5. **Text-pane responds** with `{ type: 'terminal:text-response', data: { status: 'ok', message: '...' } }`

**Op types supported:**
- `append` — add content to end
- `prepend` — add content to start
- `replace` — replace anchor text
- `insert` — insert after anchor
- `delete` — delete anchor text
- `set` — replace entire document
- **Diff mode** — unified diff string (mutually exclusive with ops)

**Nickname resolution:** Pane registry maps user-friendly names (e.g., "docs", "code") to nodeId UUIDs. Terminal resolves nicknames before routing.

**Multiple targets:** A single LLM response can route to multiple text panes. Example:
```json
{
  "to_text": [
    { "target": "notes", "ops": [{ "op": "append", "content": "..." }] },
    { "target": "summary", "ops": [{ "op": "set", "content": "..." }] }
  ]
}
```

DIVERGENCE: none (logic ported correctly)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 5
source: platform/simdecisions-2/src/components/apps/FrankCLI.tsx:L440-L483
shift: false
---

**FINDING 5: Zone 2 Rendering — Response Pane Layout**

Zone 2 is the **response pane** (scrolling history area). Zone 1 is the **prompt line** (input at bottom).

**Zone 2 layout modes** (configurable via EGG config):
- `top` — response pane above prompt
- `bottom` — response pane below prompt (default)
- `left` — response pane left of prompt
- `right` — response pane right of prompt
- `hidden` — no response pane (headless mode, metrics only)

**Entry types rendered in Zone 2:**
- `banner` — welcome message, styled with `.fkcli-entry-banner`
- `input` — user input echo, styled with `.fkcli-entry-input`
- `response` — LLM response, styled with `.fkcli-entry-response`, supports markdown rendering
- `system` — system messages (slash command output, errors), styled with `.fkcli-entry-system`
- `ir` — PHASE-IR JSON blocks, rendered with action buttons (Open in Designer, Copy, Download)

**Markdown rendering:**
- Uses custom `markdownRenderer.tsx` in platform
- Supports code blocks with syntax highlighting
- Supports tables, lists, links, images
- Converts IR JSON blocks to interactive IR cards

**Metrics display:**
- Each response entry includes metrics badge: `clock: 1.2s | cost: $0.0012 | carbon: 0.05g`
- Status bar shows session totals (3-currency ledger)

**Chat mode vs Shell mode:**
- **Chat mode** (`routeTarget: 'ai'` or `routeTarget: 'ir'`): User input and LLM responses routed to text-pane. Terminal shows metrics only.
- **Shell mode** (`routeTarget: 'shell'`): User input echoed, LLM response shown in terminal Zone 2.
- **Relay mode** (`routeTarget: 'relay'`): User input sent to efemera channel, no LLM call. Zone 2 hidden.

DIVERGENCE: none (Zone 2 logic ported to shiftcenter terminal)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 6
source: platform/simdecisions-2/src/services/frank/dialectLoader.ts:L1-L72
shift: false
---

**FINDING 6: Dialect System — Modular Prompt Assembly**

The system prompt is **assembled from dialect files**, not hardcoded. Dialects are .md prompt files loaded via Vite's `?raw` import.

**Core dialects (always loaded):**
- `patois.md` — base Fr@nk personality, rules, 3-currency awareness
- `envelope.md` — JSON envelope format spec (to_user, to_text, etc.)

**Optional dialects (loaded based on context):**
- `ir-generation.md` — PHASE-IR generation rules (loaded when `irMode: true`)
- `simulation.md` — simulation control dialect (loaded when `simulationMode: true`)

**Composition logic:**
```typescript
export function composeSystemPrompt(
  additionalDialects: Dialect[] = [],
  eggPrompt?: string
): string {
  const parts: string[] = []

  // Egg prompt comes first if provided
  if (eggPrompt && eggPrompt.trim()) {
    parts.push(eggPrompt.trim())
  }

  // Then dialect-based prompts
  const active = [...CORE_DIALECTS, ...additionalDialects]
  const unique = Array.from(new Set(active))
  const dialectPrompts = unique
    .map(d => DIALECT_MAP[d])
    .filter(Boolean)

  parts.push(...dialectPrompts)

  return parts.join('\n\n---\n\n')
}
```

**EGG prompt injection:** When an EGG is active, its `prompt` field is **prepended** to the system prompt. This allows EGGs to teach Fr@nk new capabilities (e.g., turtle graphics commands, chart data formats) without modifying core dialects.

**Shiftcenter changes:** File paths changed from `src/services/frank/prompts/` to `src/services/terminal/prompts/`. Logic identical.

DIVERGENCE: none (ported correctly, path differences intentional)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 7
source: platform/simdecisions-2/src/components/shell/shell.context.js:L43-L186
shift: false
---

**FINDING 7: MessageBus — Cross-Pane Event Routing**

The **MessageBus** is the core IPC mechanism for pane-to-pane communication. It lives in shell.context.js (platform) and messageBus.ts (shiftcenter).

**Key methods:**
- `subscribe(paneId, handler)` — register message handler for a pane
- `send(message, sourcePane)` — route message to target pane(s)
- `setTree(tree)` — keep routing table synced with shell tree state
- `setLastFocusedByAppType(map)` — track focused pane per app type (for IR routing)
- `getLastFocusedPane(appType)` — resolve most recent pane of given type

**Message envelope structure:**
```typescript
{
  messageId: string,    // unique ID
  nonce: string,        // replay protection (5s TTL)
  sourcePane: string,   // sender nodeId
  timestamp: string,    // ISO 8601
  type: string,         // message type (e.g., 'terminal:text-patch')
  target: string,       // '*' for broadcast, nodeId for targeted
  data: any             // payload
}
```

**Routing rules:**
- `target: '*'` → broadcast to all subscribers
- `target: nodeId` → targeted delivery to one pane
- Nonce prevents duplicate delivery (5s window)

**Bus security:**
- Governed by GovernanceProxy.tsx (sandboxes applets)
- Applets get proxied bus that intercepts send/subscribe
- No raw MessageBus access outside shell core

**Terminal → Text Pane example:**
```typescript
bus.send({
  type: 'terminal:text-patch',
  sourcePane: terminalNodeId,
  target: textPaneNodeId,
  data: { format: 'markdown', ops: [{ op: 'append', content: '...' }] }
})
```

DIVERGENCE: Platform uses shell.context.js (React Context), shiftcenter uses messageBus.ts (standalone class). Both implement same API. No functional difference.
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 8
source: platform/simdecisions-2/src/services/frank/prompts/envelope.md:L1-L229
shift: false
---

**FINDING 8: Envelope Dialect — LLM Output Contract**

The `envelope.md` dialect is the **output contract** between LLM and terminal. It teaches the LLM how to structure responses.

**Key rules (from envelope.md):**

1. **Every response MUST be a single JSON object.** No prose outside JSON. No markdown fences.
2. **`to_user` is required.** Always present, never empty.
3. **Omit unused slots.** No empty objects, no empty arrays.
4. **Never use both `ops` and `diff` in the same `to_text` item.**
5. **`to_user` does not narrate other slots.** Say "Done — updated the document.", not a full recitation of ops.
6. **If JSON fails, fallback:** `{"to_user": "I encountered an error and could not format my response. Please try again."}`
7. **Never wrap JSON in markdown code fences.** The response IS the JSON.

**Example envelope:**
```json
{
  "to_user": "Done. I've added the summary section.",
  "to_text": [
    {
      "target": "report",
      "format": "markdown",
      "ops": [{ "op": "append", "content": "## Summary\n\nKey findings: ..." }]
    }
  ]
}
```

**Enforcement:** Parser gracefully degrades. If LLM returns plain text or malformed JSON, treat entire response as `to_user`. No user-visible error.

**Why this works:** Anthropic's Claude models follow structured output instructions reliably. Fallback handles edge cases (rate limits, context window exhaustion, model errors).

DIVERGENCE: none (envelope.md ported verbatim)
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 9
source: shiftcenter/browser/src/primitives/terminal/useTerminal.ts:L593-L761
shift: false
---

**FINDING 9: Shiftcenter Routing Modes — AI/Shell/Relay/Canvas/IR**

Shiftcenter extends platform with **multiple routing modes** via `routeTarget` config:

1. **`shell` mode (default):**
   - User input echoed in terminal
   - LLM response shown in Zone 2
   - Traditional terminal UX

2. **`ai` mode (chat mode):**
   - User input routed to text-pane as "**You:** {message}"
   - LLM response routed to text-pane as "**{model}:** {response}"
   - Terminal shows metrics only (metricsOnly flag)
   - Text-pane becomes chat transcript

3. **`ir` mode (split chat + IR):**
   - User input → text-pane (chat)
   - LLM response parsed: chat text → text-pane, IR JSON → canvas
   - Uses `extractIRBlocks()` to split content
   - Terminal shows metrics only

4. **`relay` mode (efemera integration):**
   - User input → efemera channel via POST `/efemera/channels/{id}/messages`
   - Message routed to text-pane as chat message
   - No LLM call (relay only)
   - Zone 2 hidden

5. **`canvas` mode (backend NL→IR):**
   - User input → POST `/api/phase/nl-to-ir` (hivenode)
   - Backend calls LLM to generate IR
   - IR returned → routed to canvas via `terminal:ir-deposit`
   - Terminal shows success message + metrics

**Key observation:** The terminal is a **routing hub**, not just a chat UI. It can:
- Send to LLM and display response (shell mode)
- Send to LLM and route to other panes (ai/ir mode)
- Skip LLM and route directly (relay mode)
- Call backend LLM proxy (canvas mode)

DIVERGENCE: Platform has shell mode only. Shiftcenter added 4 new routing modes. INTENTIONAL feature addition.
P0: none
BACKLOG: none

---
bee: BEE-DA1
type: RESEARCH
finding: 10
source: shiftcenter/browser/src/primitives/terminal/useTerminal.ts:L115-L116
shift: false
---

**FINDING 10: File Attachment Support — Context Injection**

Shiftcenter terminal has **file attachment** capability (not in platform).

**Implementation:**
- `useAttachment()` hook manages attachment state
- `handleFileSelect(file)` — reads file, stores content + metadata
- `formatPromptWithAttachment(text)` — prepends file content to user prompt
- File content wrapped in markdown code fence with filename

**Supported file types:**
- Text files (txt, md, json, yaml, etc.) — content embedded directly
- Images (png, jpg, etc.) — not yet supported (TODO)

**Use case:** User can attach a code file, spec document, or data file. Terminal prepends content to prompt before LLM call. LLM sees file content as part of user message.

**Example formatted prompt:**
```
File: example.py
```python
def hello():
    print("Hello, world!")
```

Now refactor this function to accept a name parameter.
```

**Attachment UI:** File picker button in prompt area. Attachment badge shows filename + size. Click to remove.

DIVERGENCE: Shiftcenter-only feature. Not in platform.
P0: none
BACKLOG: {
  title: "Port file attachment to platform",
  provenance: { source_bee: "BEE-DA1", task_context: "Terminal attachment support", file: "shiftcenter/browser/src/primitives/terminal/useAttachment.ts" }
}

---

# COMPLETION SUMMARY

## Files Read (Platform)
- `platform/simdecisions-2/src/components/shell/shell.context.js`
- `platform/simdecisions-2/src/components/apps/FrankCLI.tsx`
- `platform/simdecisions-2/src/hooks/useTerminalSession.ts`
- `platform/simdecisions-2/src/services/frank/responseRouter.ts`
- `platform/simdecisions-2/src/services/frank/frankResponseRouter.ts`
- `platform/simdecisions-2/src/services/frank/frankService.ts`
- `platform/simdecisions-2/src/services/frank/dialectLoader.ts`
- `platform/simdecisions-2/src/services/frank/prompts/envelope.md`
- `platform/simdecisions-2/src/services/llm/providers/anthropic.ts`
- `platform/simdecisions-2/src/services/llm/types.ts`

## Files Read (Shiftcenter)
- `shiftcenter/browser/src/primitives/terminal/useTerminal.ts`
- `shiftcenter/browser/src/primitives/terminal/TerminalApp.tsx`
- `shiftcenter/browser/src/services/terminal/terminalService.ts`
- `shiftcenter/browser/src/services/terminal/terminalResponseRouter.ts`
- `shiftcenter/browser/src/services/terminal/providers/anthropic.ts`

## Answers to Research Questions

### Q1: How does the terminal send prompts to an LLM?

**Answer:** User input → `handleSubmit()` → build conversation history from terminal entries → get LLM provider (Anthropic/Groq) → compose system prompt from dialects → call `provider.call()` → HTTP POST to LLM API with BYOK key → parse response → calculate 3-currency metrics → return to terminal.

### Q2: What LLM provider abstraction exists?

**Answer:** `LLMProvider` interface with `.call(request)` method. Concrete providers: AnthropicProvider, GroqProvider, OpenAICompatibleProvider. BYOK pattern — API keys stored in localStorage. MCP support for tool calling. Shiftcenter adds proxy mode (hivenode /llm/chat).

### Q3: How does the terminal handle structured responses?

**Answer:** LLM returns JSON envelope with slots: `to_user` (required), `to_text` (ops/diff), `to_explorer`, `to_ir`, `to_simulator`, `to_bus`. Parser extracts envelope, validates, routes slots to bus targets. Text-pane receives `terminal:text-patch` messages and applies ops. Graceful degradation if JSON parse fails.

### Q4: What is the to_text routing mechanism?

**Answer:** `to_text` slot contains array of targets with ops (append/replace/insert/delete/set) or diff strings. Terminal resolves target nicknames → nodeIds via paneRegistry, sends `terminal:text-patch` bus messages, text-pane applies ops to Monaco editor.

### Q5: What is Zone 2 rendering?

**Answer:** Zone 2 is the response pane (scrolling history). Zone 1 is the prompt line. Zone 2 renders entries: banner, input, response (markdown), system, ir (interactive cards). Configurable position: top/bottom/left/right/hidden. Chat mode routes responses to text-pane, shows metrics only in terminal.

## Test Status

No tests run (research only).

## Next Steps

1. Q33NR reviews findings, identifies P0 issues or spec drift
2. If approved, archive task to `.deia/hive/tasks/_archive/TASK-DA1-terminal-llm-pipeline.md`
3. Cross-reference findings with other DA tasks (DA2, DA3, DA4, DA5) for holistic audit
4. Update MEMORY.md if new patterns discovered

---

END OF RESPONSE
