# TASK-EFEMERA-CONN-04: Refactor Text-Pane Chat Mode

**Priority:** P0
**Depends on:** CONN-02
**Blocks:** CONN-06
**Model:** Sonnet
**Role:** Bee

## Objective

Remove all efemera HTTP code from the text-pane's chat mode. The text-pane should receive efemera data exclusively through `efemera:*` bus events — it never calls fetch() for efemera endpoints.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 5.2
- `browser/src/primitives/text-pane/SDEditor.tsx` — the file being modified
  - Lines 369-398: `channel:selected` handler with HTTP fetch (REMOVE)
  - Lines 401-410: `channel:message-received` handler (REPLACE)
- `browser/src/primitives/efemera-connector/types.ts` — bus event data shapes

## Changes to `browser/src/primitives/text-pane/SDEditor.tsx`

### REMOVE

1. **Lines 369-398** — `channel:selected` handler that fetches messages via HTTP:
   ```typescript
   if (message.type === 'channel:selected' && mode === 'chat') {
     const { channelId, channelName } = message.data || {}
     if (channelId) {
       setLabel(channelName ? `#${channelName}` : 'Messages')
       chatTimestamps.current = new Map()
       chatMessageCount.current = 0
       fetch(`${hivenodeUrl}/efemera/channels/${channelId}/messages`, ...)
       // ... all of this
     }
     return
   }
   ```

2. **Lines 401-410** — `channel:message-received` handler:
   ```typescript
   if (message.type === 'channel:message-received' && mode === 'chat') {
     // ... append message
     return
   }
   ```

### ADD (new bus subscriptions via `subscribeType`)

1. **Subscribe to `efemera:channel-changed`:**
   ```typescript
   // In the bus subscription effect for chat mode
   if (mode === 'chat') {
     const unsub1 = bus.subscribeType('efemera:channel-changed', (msg: any) => {
       const { channelName } = msg.data || {}
       setLabel(channelName ? `#${channelName}` : 'Messages')
       // Reset chat state
       chatTimestamps.current = new Map()
       chatMessageCount.current = 0
       setContent('')  // Clear, show loading state
     })
     // ... return cleanup
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
- The `terminal:text-patch` handler (line 412+) stays — other EGGs (canvas, code) still use it for non-efemera purposes

## Tests

### Update existing text-pane tests or create new ones

- Test: chat mode subscribes to `efemera:channel-changed` (not `channel:selected`)
- Test: `efemera:messages-loaded` replaces content with formatted messages
- Test: `efemera:message-received` appends single message
- Test: `efemera:channel-changed` clears content and resets state
- Test: `efemera:typing` shows "User is typing..." indicator
- Test: `efemera:typing-stop` hides typing indicator
- Test: typing indicator auto-clears after 5 seconds
- Test: no HTTP fetch calls in chat mode

## Constraints

- Do NOT touch file mode, markdown mode, or any non-chat functionality
- Keep the `terminal:text-patch` handler — it's still used by non-efemera EGGs
- The chat rendering format stays the same: `**author:** content\n\n`
- TDD: write tests first
