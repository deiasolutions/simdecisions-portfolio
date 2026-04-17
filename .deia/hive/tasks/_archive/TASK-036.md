# TASK-036: Chat Persistence Rewrite

**Assigned to:** BEE
**Model:** Sonnet
**Parent:** SPEC-HIVENODE-E2E-001 (Wave 3)
**Date:** 2026-03-12
**Depends on:** None

---

## Objective

Rewrite chat persistence to use markdown format and dual-write to `home://` + `cloud://`. Changes both browser (TypeScript) and backend (Python). This enables:
1. Human-readable conversation archives (markdown format)
2. Dual-write to local and cloud storage for redundancy
3. Per-conversation volume choice (`home-only`, `cloud-only`, `both`)

---

## What Already Exists

- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts` (221 lines) — stores conversations as JSON to `home://chat/` via hivenode, localStorage fallback
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts` — Conversation, Message types
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts` — loads conversations, groups by date

---

## What to Build

### 1. Markdown Format

**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts`

**Markdown structure:**
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

**File paths:**
- Conversations: `{volume}://chats/{date}/conversation-{uuid}.md`
  - Example: `home://chats/2026-03-12/conversation-abc123.md`
- Index: `{volume}://chats/index.json` (lightweight: id, title, date, path, resume_code)

**Functions:**
- `serializeConversation(conversation: ConversationWithMessages): string` — to markdown
- `parseConversation(markdown: string): ConversationWithMessages` — from markdown
- Handle frontmatter (YAML between `---` fences) — use library like `gray-matter`
- Handle message blocks (`## Role (timestamp)`)

---

### 2. Dual-Write Logic

**Update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`

**Changes:**
1. **Storage format:** JSON → markdown
2. **Dual-write:** write to BOTH `home://` and `cloud://` simultaneously
   - Use `Promise.all()` for parallel writes
   - If either write fails, the successful one is source of truth
   - Log errors but do not block
3. **Volume choice:** add `volume_preference` field to Conversation
   - `home-only` — write to `home://` only
   - `cloud-only` — write to `cloud://` only
   - `both` — write to both (default)
4. **Index files:** maintain separate index files for each volume
   - `home://chats/index.json`
   - `cloud://chats/index.json`
5. **Read logic:** try `home://` first, fallback to `cloud://` if not found
6. **Backward compatibility:** existing JSON conversations should still load (add migration path)

**New functions:**
- `writeConversationToVolume(volume: string, conversation: ConversationWithMessages): Promise<void>` — write markdown to single volume
- `writeConversationDual(conversation: ConversationWithMessages): Promise<void>` — write to both volumes

**Updated functions:**
- `createConversation(title?: string, volumePreference?: 'home-only' | 'cloud-only' | 'both'): Promise<Conversation>`
- `addMessage(conversationId: string, message: Omit<Message, 'id' | 'created_at'>): Promise<Message>` — dual-write

---

### 3. Update Types

**Update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts`

**Add fields to Conversation:**
```typescript
export interface Conversation {
  id: string;
  title: string | null;
  resume_code?: string | null;
  created_at: string;
  updated_at: string;
  message_count?: number;
  volume_preference?: 'home-only' | 'cloud-only' | 'both';  // NEW
  volume?: string;  // NEW — where it's actually stored
}
```

---

### 4. Update Chat History Adapter

**Update:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`

**Changes:**
1. Handle markdown format (use `chatMarkdown.ts` to parse)
2. Show volume info in tree node metadata
3. Merge conversations from both volumes (dedupe by ID)

**New function:**
- `loadChatHistoryFromVolume(volume: string): Promise<TreeNodeData[]>` — load from single volume
- Update `loadChatHistory()` to merge results from both volumes

---

## Tests

**New file:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatMarkdown.test.ts`

**Test coverage (~12 tests):**
1. `serializeConversation()` — full conversation to markdown
2. `parseConversation()` — markdown to full conversation
3. Frontmatter parsing (id, title, created, updated, model, volume)
4. Message block parsing (role, timestamp, content)
5. Dual-write success (both volumes written)
6. Dual-write partial failure (one volume fails, other succeeds)
7. Volume choice `home-only` (only writes to home)
8. Volume choice `cloud-only` (only writes to cloud)
9. Volume choice `both` (writes to both)
10. Read fallback (home → cloud)
11. Index merging (dedupe by ID)
12. Backward compatibility (existing JSON conversations still load)

**Update existing tests:**
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatApi.test.ts` — update to handle markdown format + dual-write
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\chatHistoryAdapter.test.ts` — update to handle markdown format + volume info

---

## Constraints

- No file over 500 lines
- TDD — tests first
- No stubs — all functions fully implemented
- Backward compatibility: existing chatApi consumers must still work during transition
- Dual-write must be non-blocking (errors logged but not thrown)
- Markdown format must be human-readable and valid YAML frontmatter

---

## Dependencies

**npm libraries:**
- `gray-matter` — YAML frontmatter parser (add to `package.json`)

---

## Deliverables

1. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatMarkdown.ts`
2. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\chatApi.ts`
3. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\types.ts`
4. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\adapters\chatHistoryAdapter.ts`
5. `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatMarkdown.test.ts`
6. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\__tests__\chatApi.test.ts`
7. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\tree-browser\__tests__\chatHistoryAdapter.test.ts`
8. Update `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\package.json` to add `gray-matter` dependency

---

**End of TASK-036**
