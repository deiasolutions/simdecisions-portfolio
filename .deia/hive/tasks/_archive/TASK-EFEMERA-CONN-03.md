# TASK-EFEMERA-CONN-03: Refactor Terminal Relay Mode

**Priority:** P0
**Depends on:** CONN-02
**Blocks:** CONN-06
**Model:** Sonnet
**Role:** Bee

## Objective

Remove all efemera HTTP code from the terminal's relay mode. The terminal should only communicate with efemera through `efemera:*` bus events — it never calls fetch() for efemera endpoints.

## Read First

- `.deia/BOOT.md` — hard rules
- `.deia/hive/responses/20260328-EFEMERA-CONNECTOR-DESIGN.md` — section 5.1
- `browser/src/primitives/terminal/useTerminal.ts` — the file being modified
  - Lines 182-194: `channel:selected` bus subscription (REMOVE)
  - Lines 468-535: Relay mode HTTP POST + bus emissions (REMOVE)
- `browser/src/primitives/efemera-connector/types.ts` — bus event data shapes

## Changes to `browser/src/primitives/terminal/useTerminal.ts`

### REMOVE

1. **Lines 182-194** — `channel:selected` subscription effect:
   ```typescript
   // Listen for channel:selected bus messages (relay mode)
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus || !nodeId) return;
     const unsubscribe = bus.subscribe(nodeId, (message: any) => {
       if (message.type === 'channel:selected' && message.data) {
         setActiveChannelId(message.data.channelId);
         setActiveChannelName(message.data.channelName);
         setEntries(prev => prev.filter(e => e.type !== 'system'));
       }
     });
     return unsubscribe;
   }, [routeTarget, bus, nodeId]);
   ```

2. **Lines 468-535** — Relay mode block in `handleSubmit`:
   ```typescript
   // Relay mode: POST message to efemera channel, no LLM
   if (routeTarget === 'relay') {
     // ... all of this HTTP + bus code
   }
   ```

### ADD

1. **New effect — subscribe to `efemera:channel-changed`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:channel-changed', (msg: any) => {
       setActiveChannelId(msg.data.channelId);
       setActiveChannelName(msg.data.channelName);
       setEntries(prev => prev.filter(e => e.type !== 'system'));
     });
   }, [routeTarget, bus]);
   ```

2. **New effect — subscribe to `efemera:message-sent`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:message-sent', () => {
       setLoading(false);  // Delivery confirmed
     });
   }, [routeTarget, bus]);
   ```

3. **New effect — subscribe to `efemera:error`:**
   ```typescript
   useEffect(() => {
     if (routeTarget !== 'relay' || !bus) return;
     return bus.subscribeType('efemera:error', (msg: any) => {
       setLoading(false);  // Stop loading on error
       const { message: errMsg, context } = msg.data || {};
       setEntries(prev => [...prev, {
         type: 'system',
         content: `Error: ${errMsg || 'Unknown error'}`,
         level: 'error',
       }]);
     });
   }, [routeTarget, bus]);
   ```

4. **Replace relay mode block in `handleSubmit`:**
   ```typescript
   if (routeTarget === 'relay') {
     if (!activeChannelId) {
       setEntries(prev => [...prev,
         { type: 'input', content: text, hidden: true },
         { type: 'system', content: 'Select a channel first.' },
       ]);
       return;
     }
     // Hide input (chat bubbles handle display)
     setEntries(prev => [...prev, { type: 'input', content: text, hidden: true }]);
     // Emit to connector — it handles the HTTP/WS
     setLoading(true);
     if (bus && nodeId) {
       bus.send({
         type: 'efemera:message-send',
         sourcePane: nodeId,
         target: '*',
         nonce: `${Date.now()}-${Math.random()}`,
         timestamp: new Date().toISOString(),
         data: { content: text },
       });
     }
     return;
   }
   ```

### Also remove

- The `HIVENODE_URL` import if no other code in useTerminal uses it (check first — IR mode and canvas mode may still use it)
- The `channel:message-sent` bus event emission (connector handles this now)
- The `terminal:text-patch` emission for relay mode (connector emits `efemera:message-received` to text-pane directly)

## Tests

### Update `browser/src/primitives/terminal/__tests__/` as needed

- Test: relay mode emits `efemera:message-send` on Enter (not HTTP POST)
- Test: relay mode sets loading=true when sending, loading=false on `efemera:message-sent`
- Test: relay mode sets loading=false on `efemera:error`
- Test: relay mode subscribes to `efemera:channel-changed` (not `channel:selected`)
- Test: relay mode shows error from `efemera:error` bus event
- Test: relay mode without active channel shows "Select a channel first"

## Constraints

- Do NOT touch IR mode, canvas mode, or standard LLM mode — only relay mode
- Keep `activeChannelId` and `activeChannelName` state — they're still used for prompt display
- The terminal still needs `bus.send()` — just the event types change
- TDD: verify existing relay tests still pass or update them
