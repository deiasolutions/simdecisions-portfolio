# BRIEFING: MessageBus API Sweep

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-24
**Priority:** P0 — Runtime crashes

---

## Objective

Find and fix ALL incorrect MessageBus API calls across the entire `browser/src/` directory. The MessageBus class only has two public methods:
- `send(message, sourcePane?)` — send a message
- `subscribe(paneId, handler)` — subscribe to messages, returns unsubscribe function

Bees have introduced calls to non-existent methods that cause runtime crashes:
- `bus.emit()` — DOES NOT EXIST, use `bus.send()`
- `bus.on()` — DOES NOT EXIST, use `bus.subscribe()`
- `bus.off()` — DOES NOT EXIST, `subscribe()` returns an unsubscribe function

## Task

1. Search all `.ts` and `.tsx` files under `browser/src/` for:
   - `bus.emit(`
   - `bus.on(`
   - `bus.off(`
   - Any other method call on bus that is not `.send(` or `.subscribe(`

2. For each violation found, fix it:
   - `bus.emit(eventName, data)` → `bus.send({ type: eventName, sourcePane: paneId, target: '*', nonce: Math.random().toString(36).slice(2, 11), timestamp: new Date().toISOString(), data }, paneId)`
   - `bus.on(event, handler)` → `bus.subscribe(paneId, handler)` (handler must filter by msg.type)
   - `bus.off(event, handler)` → use the unsubscribe function returned by `bus.subscribe()`

3. Run the affected test files to verify no regressions.

## MessageBus Reference

File: `browser/src/infrastructure/relay_bus/messageBus.ts`

```typescript
subscribe(paneId: string, handler: (msg: MessageEnvelope) => void): () => void
send(message: Partial<MessageEnvelope>, sourcePane?: string): string | null
```

MessageEnvelope shape:
```typescript
{
  type: string
  sourcePane: string
  target: string | '*'
  nonce: string
  timestamp: string
  data?: unknown
}
```

## Rules

- Read `.deia/BOOT.md` first.
- TDD: write a test for each fix if one doesn't exist.
- No files over 500 lines.
- CSS: `var(--sd-*)` only.
