# SPEC-EFEMERA-CONN-04: Refactor Text-Pane Chat Mode

> **Project:** Efemera Connector (12 specs submitted as batch, 2026-03-28)
> Dependencies between specs ensure correct execution order.
> Design doc: `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md`

## Priority
P0

## Depends On
- SPEC-EFEMERA-CONN-02-connector-primitive

## Model Assignment
sonnet

## Objective

Remove all efemera HTTP code from the text-pane's chat mode. The text-pane should receive efemera data exclusively through `efemera:*` bus events — it never calls fetch() for efemera endpoints. Add typing indicator (required).

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 5.2
- `browser/src/primitives/text-pane/SDEditor.tsx` — the file being modified
  - Lines 369-398: `channel:selected` handler with HTTP fetch (REMOVE)
  - Lines 401-410: `channel:message-received` handler (REPLACE)
- `browser/src/primitives/efemera-connector/types.ts` — bus event data shapes

## Changes to `browser/src/primitives/text-pane/SDEditor.tsx`

### REMOVE

1. **Lines 369-398** — `channel:selected` handler that fetches messages via HTTP
2. **Lines 401-410** — `channel:message-received` handler

### ADD (new bus subscriptions via `subscribeType`)

1. **Subscribe to `efemera:channel-changed`:**
   ```typescript
   if (mode === 'chat') {
     const unsub1 = bus.subscribeType('efemera:channel-changed', (msg: any) => {
       const { channelName } = msg.data || {}
       setLabel(channelName ? `#${channelName}` : 'Messages')
       chatTimestamps.current = new Map()
       chatMessageCount.current = 0
       setContent('')
     })
   }
   ```

2. **Subscribe to `efemera:messages-loaded`:**
   ```typescript
   const unsub2 = bus.subscribeType('efemera:messages-loaded', (msg: any) => {
     const { messages } = msg.data || {}
     if (!Array.isArray(messages)) return
     const chatContent = messages.map((m: any) => {
       const ts = m.created_at || new Date().toISOString()
       const count = chatMessageCount.current++
       chatTimestamps.current.set(count, ts)
       return `**${m.author_name || 'Unknown'}:** ${m.content}`
     }).join('\n\n')
     setContent(chatContent ? chatContent + '\n\n' : '')
   })
   ```

3. **Subscribe to `efemera:message-received`:**
   ```typescript
   const unsub3 = bus.subscribeType('efemera:message-received', (msg: any) => {
     const { message: m } = msg.data || {}
     if (!m) return
     const ts = m.created_at || new Date().toISOString()
     const count = chatMessageCount.current++
     chatTimestamps.current.set(count, ts)
     setContent(prev => prev + `**${m.author_name || 'Unknown'}:** ${m.content}\n\n`)
   })
   ```

4. **Subscribe to `efemera:typing` / `efemera:typing-stop` (required):**
   ```typescript
   const unsub4 = bus.subscribeType('efemera:typing', (msg: any) => {
     const { displayName } = msg.data || {}
     if (displayName) setTypingUser(displayName)
   })
   const unsub5 = bus.subscribeType('efemera:typing-stop', () => {
     setTypingUser(null)
   })
   ```
   - Add `const [typingUser, setTypingUser] = useState<string | null>(null)` state
   - Render "User is typing..." indicator at bottom of chat when `typingUser` is non-null
   - Auto-clear after 5 seconds (timeout ref) in case stop event is missed

### Also
- Remove the `HIVENODE_URL` import if no other code in SDEditor uses it (file:selected handler may still use it — check)
- The `terminal:text-patch` handler stays — other EGGs still use it for non-efemera purposes

## Acceptance Criteria
- [ ] Chat mode subscribes to `efemera:channel-changed` (not `channel:selected`)
- [ ] `efemera:messages-loaded` replaces content with formatted messages
- [ ] `efemera:message-received` appends single message
- [ ] `efemera:channel-changed` clears content and resets state
- [ ] `efemera:typing` shows "User is typing..." indicator
- [ ] `efemera:typing-stop` hides typing indicator
- [ ] Typing indicator auto-clears after 5 seconds
- [ ] No HTTP fetch calls in chat mode
- [ ] File mode, markdown mode, and non-chat functionality unchanged
- [ ] terminal:text-patch handler still works for non-efemera EGGs
- [ ] Chat rendering format preserved: `**author:** content\n\n`
- [ ] All tests pass

## Smoke Test
- [ ] `npx vitest run browser/src/primitives/text-pane/` — all pass
- [ ] `npx vite build` — zero errors

## Constraints
- Do NOT touch file mode, markdown mode, or any non-chat functionality
- Keep the `terminal:text-patch` handler — it's still used by non-efemera EGGs
- The chat rendering format stays the same: `**author:** content\n\n`
- TDD: write tests first

## Response File
20260328-EFEMERA-CONN-04-RESPONSE.md
