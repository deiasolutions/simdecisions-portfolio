# BRIEFING: Chat Persistence — Dual-Write + Conversation Navigator

**Date:** 2026-03-14
**Spec:** QUEUE-TEMP-2026-03-14-0402-SPEC-chat-persistence.md
**Model:** sonnet
**Priority:** P1

---

## Objective

Rewrite chat persistence to dual-write to cloud:// and home://. Build tree-browser conversation navigator. This is Wave 4 of SPEC-HIVENODE-E2E-001.

---

## Context

Currently, conversations are not persisted. The terminal's `useTerminal` hook builds history from entries array, but never writes to disk. Sections 7-8 of SPEC-HIVENODE-E2E-001 specify:

1. **Dual-write:** Conversations saved to both cloud:// and home:// simultaneously
2. **Graceful degradation:** If one volume fails, other succeeds
3. **Markdown format:** Human-readable, grep-searchable, with frontmatter
4. **Tree-browser navigator:** Shows chats grouped by date, reads metadata only
5. **Bus integration:** `tree-browser:conversation-selected` published on click
6. **Volume badges:** online, syncing, conflict, offline
7. **Volume preference:** per-conversation (cloud+home, work+cloud, home-only)

---

## Files to Read First

**Spec:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\docs\specs\SPEC-HIVENODE-E2E-001.md` (Sections 7-8)

**Current Chat Flow:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 440-619 show current LLM flow, no persistence)

**Tree-Browser Adapter Pattern:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\treeBrowserAdapter.tsx` (adapter dispatch pattern)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\channelsAdapter.ts` (reference adapter)

**Storage Routes:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\routes\storage.py` (POST /storage/write, POST /storage/read)

**Volume Registry:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\storage\volumes.py` (VolumeRegistry, cloud:// and home:// adapters)

---

## Acceptance Criteria (from spec)

- [ ] Dual-write: conversations saved to both cloud:// and home:// (Promise.all)
- [ ] Graceful degradation: if one volume fails, other succeeds
- [ ] Markdown format with frontmatter (id, title, created, updated, model, volume)
- [ ] Tree-browser conversation navigator shows chats grouped by date
- [ ] Bus integration: `tree-browser:conversation-selected` published on click
- [ ] Volume badges: online, syncing, conflict, offline
- [ ] Volume preference per conversation: cloud+home, work+cloud, home-only
- [ ] 15+ tests
- [ ] No file over 500 lines

---

## Deliverables Breakdown

### 1. Backend: Conversation Write Endpoint
- POST /chat/save endpoint in hivenode
- Accepts: { id, title, messages, model, volumes, actor }
- Writes to specified volumes (dual-write via Promise.all in Python: asyncio.gather)
- Returns: { success: true, written_to: ["cloud://...", "home://..."], failed: [] }
- Graceful degradation: if one volume fails, log error, continue

### 2. Backend: Conversation List Endpoint
- GET /chat/list endpoint
- Scans cloud://chats/ and home://chats/ for .md files
- Returns metadata only (parses frontmatter, NOT full content)
- Grouped by date: { "2026-03-14": [{ id, title, created, updated, model, volume, path }] }

### 3. Backend: Conversation Read Endpoint
- GET /chat/:id endpoint
- Reads from specified volume (or first available if not specified)
- Returns full markdown content

### 4. Frontend: Chat Persistence Service
- `browser/src/services/chat/conversationPersistence.ts`
- `saveConversation(entries, ledger, conversationId, volumes?)` function
- Calls POST /chat/save with dual-write
- Extracts messages from entries array (type: 'input' | 'response')
- Generates title from first user message (truncate to 50 chars)
- Default volumes: ['cloud', 'home']

### 5. Frontend: Integrate Persistence into useTerminal
- Import conversationPersistence service
- After LLM response, call saveConversation() (fire-and-forget, don't block UI)
- Use conversationId from state (already tracked)
- Log errors, don't crash

### 6. Frontend: Tree-Browser Conversation Adapter
- `browser/src/primitives/tree-browser/adapters/conversationAdapter.ts`
- Calls GET /chat/list
- Transforms response to TreeNodeData[] format
- Groups by date (top-level nodes are dates, children are conversations)
- Adds volume badges (meta.badge: 'online' | 'syncing' | 'conflict' | 'offline')

### 7. Frontend: Bus Handler for conversation-selected
- When user clicks conversation in tree-browser, publish `tree-browser:conversation-selected` bus event
- Handler calls GET /chat/:id, pushes content to text-pane via `terminal:text-patch`

### 8. Markdown Format Implementation
- Spec format (from SPEC-HIVENODE-E2E-001 Section 7.2):
  ```markdown
  ---
  id: conversation-<uuid>
  title: "Chat about authentication"
  created: 2026-03-12T09:30:00Z
  updated: 2026-03-12T10:15:00Z
  model: claude-sonnet-4-6
  volume: home://
  ---

  ## You (09:30)
  How does the JWT validation work?

  ## Claude Sonnet 4.6 (09:30)
  The JWT validation flow works like this...
  ```

### 9. Tests
- Backend: 8 tests (save dual-write, save single volume, save failure handling, list conversations, read conversation, metadata parsing, error cases)
- Frontend: 7 tests (conversationPersistence service, adapter transform, bus handler, volume badge logic)
- Minimum: 15 tests

---

## Constraints

- Depends on cloud storage adapter and volume sync being functional (NOTE: cloud storage adapter may NOT be fully wired yet — check if cloud:// volume is functional. If not, stub cloud:// writes to return success without actually writing, and add TODO comment.)
- Tree-browser reads metadata only, NOT full conversation content (parse frontmatter, don't load full markdown into memory)
- Markdown format must be human-readable and grep-searchable
- No file over 500 lines (modularize chat service if needed)
- TDD: tests first
- No stubs in production code (if cloud:// not ready, stub the adapter, not the production code)

---

## Model Assignment

sonnet

---

## Q33N Instructions

1. **Read the spec sections first.** Sections 7-8 of SPEC-HIVENODE-E2E-001 are the source of truth.
2. **Check cloud:// volume status.** Read `hivenode/storage/volumes.py` and check if CloudStorageAdapter is functional. If not, task files must specify how to stub it.
3. **Break into 3-4 task files:**
   - TASK-1: Backend endpoints (POST /chat/save, GET /chat/list, GET /chat/:id)
   - TASK-2: Frontend persistence service + useTerminal integration
   - TASK-3: Tree-browser conversation adapter + bus handler
   - (Optional TASK-4: Volume badge logic if complex)
4. **Every task must specify:**
   - Absolute file paths
   - Test requirements (how many, which scenarios)
   - Edge cases (offline volume, malformed markdown, empty conversations)
   - Response file template (8 sections)
5. **No hardcoded colors.** Use `var(--sd-*)` for any UI changes.
6. **Return task files to Q88NR for review.** Do NOT dispatch bees yet.

---

**End of briefing.**
