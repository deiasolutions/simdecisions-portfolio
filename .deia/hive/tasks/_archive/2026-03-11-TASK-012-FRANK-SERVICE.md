# TASK-012: Frank Service + Envelope Router — Port to browser/src/services/frank/

## Objective

Port the Fr@nk service layer from simdecisions-2 to `browser/src/services/frank/`. This is the LLM interaction service: message sending with 3-currency metrics, structured response envelope parsing with slot routing (to_user, to_text, to_ir, to_simulator, to_bus), dialect-based system prompt composition, chat conversation persistence API, and the dialect .md prompt files. All files port to TypeScript.

## Dependencies

- **TASK-004 (LLM Router)** — needed for **proxy mode only** (future enhancement). Not required for MVP direct mode.
- **TASK-005 (Relay Bus)** — must be complete. `routeEnvelope()` dispatches `to_bus` messages via the relay bus. Bus message types: `terminal:text-patch`, `frank:explorer-command`, `frank:ir-deposit`, `frank:simulator-command`.
- **TASK-010 (SDEditor)** — must be complete. `to_text` slot routes text operations (append, prepend, replace, insert, delete, set) and unified diffs to SDEditor panes. The router dispatches `terminal:text-patch` bus messages that SDEditor subscribes to.

## LLM Routing — Dual Mode Architecture

The frank service supports **two LLM routing modes**. The user chooses which mode via settings.

### Mode 1: Direct Mode (MVP — build this)

Browser calls the LLM API directly using the user's own API key (BYOK). The key **never leaves the browser** — no backend hop, no governance, no PII scan, no sensitivity gate. This is the privacy-first path.

```
Browser (frankService.ts)
  → Anthropic/OpenAI/Groq API directly
  → Response back to browser
  → Metrics calculated locally (3-currency)
  → Envelope parsed + routed locally
```

**Implementation:**
- Import LLM provider classes (Anthropic SDK, etc.) in the browser
- API key stored in browser localStorage or in-memory only
- `sendMessage()` calls provider directly with system prompt + user message
- All token counting, cost calculation, and carbon estimation done locally
- No backend involvement — works fully offline from our servers

### Mode 2: Proxy Mode (future enhancement — DO NOT build yet)

Browser calls our backend API, which runs the full governance pipeline before calling the LLM:

```
Browser (frankService.ts)
  → POST /api/llm/chat (our backend)
  → Sensitivity Gate (TASK-004)
  → PII Scan (privacy module)
  → LLM Router → Provider API
  → Ledger logging (3C tracking)
  → Response back to browser
```

**For this task:** Add a `routingMode: 'direct' | 'proxy'` field to the service config and a `TODO: proxy mode` branch in `sendMessage()` that throws `'Proxy mode not yet implemented'`. The direct mode path must be fully functional.

### Provider Support (Direct Mode)

Port the existing provider classes from simdecisions-2. Check:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\providers\anthropic.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\providers\groq.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\types.ts`

Port these into `browser/src/services/frank/providers/`:
- `providers/types.ts` — `LLMProvider` interface, `ChatMessage`, `LLMResponse`, `McpServerConfig`
- `providers/anthropic.ts` — Anthropic SDK wrapper
- `providers/groq.ts` — Groq SDK wrapper
- `providers/index.ts` — Provider registry: `getProvider(model: string): LLMProvider`

The provider abstraction lets `sendMessage()` call `provider.call()` without knowing which vendor.

## Source Files

Port from simdecisions-2:

| Source Path | Lines | Dest Path | What It Does |
|-------------|-------|-----------|-------------|
| `services/frank/frankService.ts` | 121 | `frankService.ts` | sendMessage(), calculateMetrics(), formatMetrics(), extractJsonBlocks(), isValidIR() |
| `services/frank/frankResponseRouter.ts` | 271 | `frankResponseRouter.ts` | parseEnvelope(), routeEnvelope(), FrankEnvelope types |
| `services/frank/dialectLoader.ts` | 72 | `dialectLoader.ts` | composeSystemPrompt(), resolveDialects(), DIALECT_MAP |
| `services/frank/chatApi.ts` | 130 | `chatApi.ts` | Conversation CRUD: create, list, resume, addMessage, delete |
| `services/frank/prompts/envelope.md` | 229 | `prompts/envelope.md` | Response envelope format specification |
| `services/frank/prompts/patois.md` | ? | `prompts/patois.md` | Core personality dialect |
| `services/frank/prompts/ir-generation.md` | ? | `prompts/ir-generation.md` | IR generation dialect (conditional) |
| `services/frank/prompts/simulation.md` | ? | `prompts/simulation.md` | Simulation dialect (conditional) |
| `services/llm/types.ts` | ? | `providers/types.ts` | LLMProvider interface, ChatMessage, LLMResponse |
| `services/llm/providers/anthropic.ts` | ? | `providers/anthropic.ts` | Anthropic SDK wrapper (direct mode) |
| `services/llm/providers/groq.ts` | ? | `providers/groq.ts` | Groq SDK wrapper (direct mode) |

**All source paths relative to:** `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\`

**Total source: ~800+ lines code + ~300+ lines prompts.**

## Port Rules

### 1. File Organization

```
browser/src/services/frank/
├── index.ts                    -- Public exports
├── types.ts                    -- FrankMetrics, FrankEnvelope, TextOp, TextRouteItem, etc.
├── frankService.ts             -- sendMessage, calculateMetrics, formatMetrics, extractJsonBlocks
├── frankResponseRouter.ts      -- parseEnvelope, routeEnvelope, slot dispatching
├── dialectLoader.ts            -- composeSystemPrompt, resolveDialects
├── chatApi.ts                  -- Conversation CRUD API client
├── prompts/
│   ├── envelope.md             -- Response envelope format spec
│   ├── patois.md               -- Core personality dialect
│   ├── ir-generation.md        -- IR generation dialect
│   └── simulation.md           -- Simulation dialect
└── __tests__/
    ├── frankService.test.ts
    ├── frankResponseRouter.test.ts
    ├── dialectLoader.test.ts
    └── chatApi.test.ts
```

### 2. Extract Types to types.ts

Create `types.ts` as the canonical type source:

```typescript
/** 3-currency metrics from a single LLM interaction. */
export interface FrankMetrics {
  clock_ms: number;
  cost_usd: number;
  carbon_g: number;
  input_tokens: number;
  output_tokens: number;
  model: string;
}

/** Text operation for to_text slot. */
export interface TextOp {
  op: 'append' | 'prepend' | 'replace' | 'insert' | 'delete' | 'set';
  content?: string;
  position?: number;
  length?: number;
}

/** Single text routing item. */
export interface TextRouteItem {
  target: string;
  format: 'markdown' | 'plaintext' | 'html';
  ops?: TextOp[];
  diff?: string;
}

/** File explorer route. */
export interface ExplorerRoute {
  action: 'open' | 'reveal' | 'refresh';
  path: string;
}

/** Simulation engine route. */
export interface SimulatorRoute {
  action: 'run' | 'pause' | 'reset' | 'branch';
  irId?: string;
}

/** Generic bus message for egg-specific protocols. */
export interface BusMessage {
  type: string;
  target?: string;  // default: '*' (broadcast)
  data?: Record<string, unknown>;
}

/** Fr@nk structured response envelope. */
export interface FrankEnvelope {
  to_user: string;              // Required — always present
  to_text?: TextRouteItem[];    // Route text ops to SDEditor panes
  to_explorer?: ExplorerRoute;  // Route file explorer commands
  to_ir?: Record<string, unknown>;  // Deposit PHASE-IR v2.0
  to_simulator?: SimulatorRoute;    // Command simulation engine
  to_bus?: BusMessage[];        // Generic egg-specific messages
}

/** Parse result with optional error. */
export interface RouteResult {
  envelope: FrankEnvelope;
  parseError: string | null;
}

/** Dialect type — modular system prompt components. */
export type Dialect = 'patois' | 'envelope' | 'ir-generation' | 'simulation';

/** Session flags that control dialect composition and routing. */
export interface SessionFlags {
  irMode?: boolean;
  simulationMode?: boolean;
  eggPrompt?: string;
  routingMode?: 'direct' | 'proxy';  // default: 'direct'
}

/** Chat conversation. */
export interface Conversation {
  id: string;
  title: string | null;
  resume_code: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

/** Chat message within a conversation. */
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  metrics?: FrankMetrics;
  created_at: string;
}

/** Conversation with full message history. */
export interface ConversationWithMessages extends Conversation {
  messages: Message[];
}
```

### 3. frankService.ts — LLM Interaction + Metrics

Port with these changes:

- **Token rates:** Keep the model-aware pricing map. Update to current models:
  ```typescript
  export const TOKEN_RATES: Record<string, { input: number; output: number }> = {
    'claude-sonnet-4-5': { input: 3e-6, output: 15e-6 },
    'claude-haiku-4-5': { input: 0.25e-6, output: 1.25e-6 },
    'claude-opus-4-6': { input: 15e-6, output: 75e-6 },
    'llama-3.3-70b': { input: 0.1e-6, output: 0.1e-6 },
  };
  ```
- **Carbon rate:** `0.0001` g CO2 per token (industry average).
- **sendMessage():** Takes prompt, system prompt (from dialectLoader), session flags, and optional MCP server configs. In **direct mode** (MVP), calls the LLM provider directly in the browser using the user's API key. Import providers from `./providers/`. In **proxy mode** (future), would POST to backend `/api/llm/chat`. Add a routing mode check at the top of `sendMessage()`:
  ```typescript
  export async function sendMessage(
    prompt: string,
    options: SendMessageOptions,
  ): Promise<{ content: string; metrics: FrankMetrics }> {
    if (options.routingMode === 'proxy') {
      throw new Error('Proxy mode not yet implemented — use direct mode with BYOK');
    }
    const provider = getProvider(options.model);
    // ... direct call to provider.call()
  }
  ```
- **extractJsonBlocks():** Regex-based JSON extraction from markdown code blocks.
- **isValidIR():** Validates that an object has a `nodes` property.
- **calculateMetrics():** Returns `FrankMetrics` from usage data.
- **formatMetrics():** Returns human-readable string: `"clock: Xs | cost: $Y | carbon: Zg"`

### 4. frankResponseRouter.ts — Envelope Parsing + Bus Dispatch

Port with these changes:

- **parseEnvelope():** Parse raw LLM response string → `RouteResult`. Strip code fences if present. Validate `to_user` is present. Fallback: treat entire response as `to_user` if JSON parse fails.
- **routeEnvelope():** Dispatch each slot to the appropriate bus target:
  - `to_text` → dispatch `terminal:text-patch` messages to target panes
  - `to_explorer` → dispatch `frank:explorer-command`
  - `to_ir` → dispatch `frank:ir-deposit`
  - `to_simulator` → dispatch `frank:simulator-command`
  - `to_bus` → dispatch each message as-is (generic egg protocol)
- **resolveTarget():** Map pane nickname → nodeId. This uses the relay bus's pane registry. Import from `../../infrastructure/relay_bus`.
- **Validation:** Drop malformed items (e.g., `to_text` item with both `ops` and `diff`). Log to console, don't throw.
- **No hardcoded slots beyond the 5 platform primitives.** The `to_bus` slot handles all egg-specific communication generically.

### 5. dialectLoader.ts — System Prompt Composition

Port with these changes:

- **Dialect .md files:** Import via Vite `?raw` loader:
  ```typescript
  import patoisRaw from './prompts/patois.md?raw';
  import envelopeRaw from './prompts/envelope.md?raw';
  import irGenRaw from './prompts/ir-generation.md?raw';
  import simulationRaw from './prompts/simulation.md?raw';
  ```
- **CORE_DIALECTS:** `['patois', 'envelope']` — always loaded, cannot be removed.
- **composeSystemPrompt():** Compose from: `[eggPrompt?] + core dialects + conditional dialects`. Join with `'\n\n---\n\n'`.
- **resolveDialects():** Return active dialect list based on session flags.
- **Deduplication:** Use `Set` before mapping dialects to content.

### 6. chatApi.ts — Conversation Persistence

Port with these changes:

- **API_URL:** Read from `import.meta.env.VITE_API_URL` with fallback.
- **Auth:** Bearer token from `localStorage.getItem('sd:token')`.
- **Functions:** `createConversation()`, `listConversations()`, `getConversation()`, `addMessage()`, `deleteConversation()`, `resumeConversation()`.
- **Resume codes:** Alphanumeric codes (e.g., `FRK-7A3X-9B2M`). Server-generated.
- **Error handling:** Return `null` on 404 for `resumeConversation()`. Throw on other HTTP errors.

### 7. Prompt Files — Copy As-Is

Copy the dialect .md files to `browser/src/services/frank/prompts/` without modification. These are static prompt templates consumed by `dialectLoader.ts` via Vite `?raw` imports. Do not modify their content.

Read all 4 prompt files from the old repo:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\patois.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\envelope.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\ir-generation.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\simulation.md`

If additional prompt files exist in that directory (e.g., `coauthor.md`), copy those too and add to the dialect map.

## Test Requirements

### Port Existing Tests

| Old Test File | Lines | New Test File | What It Tests |
|---------------|-------|---------------|---------------|
| `chatApi.test.ts` | 126 | `chatApi.test.ts` | CRUD operations, resume codes, auth header |
| `dialectLoader.egg-prompt.test.ts` | 62 | `dialectLoader.test.ts` | Prompt composition, egg prompt prepend, separators |
| `frankService.egg-prompt.test.ts` | 70 | `frankService.test.ts` | sendMessage with egg prompt, metrics calculation |

### New Tests

**frankResponseRouter.test.ts** (new — comprehensive):
- [ ] parseEnvelope with valid JSON returns envelope
- [ ] parseEnvelope strips code fences before parsing
- [ ] parseEnvelope with invalid JSON falls back to to_user
- [ ] parseEnvelope rejects missing to_user field
- [ ] parseEnvelope handles empty to_user string
- [ ] routeEnvelope dispatches to_text as terminal:text-patch
- [ ] routeEnvelope dispatches to_explorer as frank:explorer-command
- [ ] routeEnvelope dispatches to_ir as frank:ir-deposit
- [ ] routeEnvelope dispatches to_simulator as frank:simulator-command
- [ ] routeEnvelope dispatches to_bus messages as-is
- [ ] routeEnvelope skips empty optional slots
- [ ] Validation drops to_text item with both ops and diff
- [ ] resolveTarget maps nickname to nodeId via bus
- [ ] resolveTarget defaults to broadcast (*) when target unknown

**frankService.test.ts** (extend existing):
- [ ] calculateMetrics computes clock_ms correctly
- [ ] calculateMetrics computes cost_usd with correct token rates
- [ ] calculateMetrics computes carbon_g at 0.0001 per token
- [ ] formatMetrics returns human-readable string
- [ ] extractJsonBlocks extracts from markdown code blocks
- [ ] extractJsonBlocks handles multiple blocks
- [ ] extractJsonBlocks returns empty array on no blocks
- [ ] isValidIR validates nodes property exists
- [ ] isValidIR rejects objects without nodes
- [ ] TOKEN_RATES has entries for all supported models

**dialectLoader.test.ts** (extend existing):
- [ ] composeSystemPrompt includes core dialects
- [ ] composeSystemPrompt prepends egg prompt when provided
- [ ] composeSystemPrompt adds ir-generation when irMode true
- [ ] composeSystemPrompt adds simulation when simulationMode true
- [ ] composeSystemPrompt deduplicates dialects
- [ ] resolveDialects returns core only by default
- [ ] resolveDialects adds conditional dialects based on flags
- [ ] Dialect separator is '\n\n---\n\n'

**chatApi.test.ts** (extend existing):
- [ ] createConversation POSTs with auth header
- [ ] listConversations GETs with auth header
- [ ] resumeConversation returns null on 404
- [ ] resumeConversation returns conversation on success
- [ ] addMessage POSTs message with metrics
- [ ] deleteConversation sends DELETE
- [ ] API_URL falls back to default when env var missing

**providers.test.ts** (new):
- [ ] getProvider returns AnthropicProvider for claude models
- [ ] getProvider returns GroqProvider for llama models
- [ ] getProvider throws on unknown model
- [ ] AnthropicProvider.call sends correct request shape
- [ ] AnthropicProvider.call returns content + usage
- [ ] GroqProvider.call sends correct request shape
- [ ] GroqProvider.call returns content + usage
- [ ] Provider uses API key from options (never from env/backend)
- [ ] sendMessage in direct mode calls provider directly
- [ ] sendMessage in proxy mode throws not-implemented error

**Minimum: 65+ tests.**

## Source Files to Read First

Service files:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\frankService.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\frankResponseRouter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\dialectLoader.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\chatApi.ts`

Provider files (for direct mode):
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\types.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\providers\anthropic.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\llm\providers\groq.ts`

Prompt files:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\envelope.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\patois.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\ir-generation.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\prompts\simulation.md`

Test files to port:
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\__tests__\chatApi.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\__tests__\dialectLoader.egg-prompt.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\__tests__\frankService.egg-prompt.test.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\src\services\frank\frankResponseRouter.test.ts`

Also check TASK-005 output for:
- `MessageBus` import path and dispatch API
- Pane registry / nickname resolution

Also check TASK-010 output for:
- SDEditor bus message subscription types (what `terminal:text-patch` should contain)

## What NOT to Build

- No terminal UI components (TASK-011)
- No useTerminal hook (TASK-011)
- No slash commands (TASK-011)
- No RAG EGG loader (future task)
- No Efemera sync (future task)
- No backend LLM router changes (TASK-004, already complete)
- No new prompt dialects — copy existing ones as-is

## Constraints

- TypeScript strict mode
- All files under 500 lines
- No stubs — every function fully implemented
- All CSS uses `var(--sd-*)` (N/A for this task — no CSS)
- Test with vitest
- Prompt .md files copied verbatim — no content changes

## Deliverables

### Source Files
- [ ] `browser/src/services/frank/index.ts`
- [ ] `browser/src/services/frank/types.ts`
- [ ] `browser/src/services/frank/frankService.ts`
- [ ] `browser/src/services/frank/frankResponseRouter.ts`
- [ ] `browser/src/services/frank/dialectLoader.ts`
- [ ] `browser/src/services/frank/chatApi.ts`
- [ ] `browser/src/services/frank/providers/types.ts`
- [ ] `browser/src/services/frank/providers/anthropic.ts`
- [ ] `browser/src/services/frank/providers/groq.ts`
- [ ] `browser/src/services/frank/providers/index.ts`
- [ ] `browser/src/services/frank/prompts/envelope.md`
- [ ] `browser/src/services/frank/prompts/patois.md`
- [ ] `browser/src/services/frank/prompts/ir-generation.md`
- [ ] `browser/src/services/frank/prompts/simulation.md`

### Test Files
- [ ] `browser/src/services/frank/__tests__/frankService.test.ts`
- [ ] `browser/src/services/frank/__tests__/frankResponseRouter.test.ts`
- [ ] `browser/src/services/frank/__tests__/dialectLoader.test.ts`
- [ ] `browser/src/services/frank/__tests__/chatApi.test.ts`
- [ ] `browser/src/services/frank/__tests__/providers.test.ts`

**19 deliverables total (14 source + 5 test).**

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-012-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
