# SPEC-SIM-CHAT-001: Simulation Chat Channel

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** EPH
**T-Shirt Size:** M
**Depends On:** relay_bus (BUILT), ledger_writer (BUILT), SPEC-PRESENCE-001, Efemera (BUILT)

---

## 1. Purpose

The sim-chat channel is a unified message stream that interleaves human participant messages
and IR node execution events in a single chronological thread. It makes the simulation a
first-class participant in any conversation — not a separate log to check, but a voice in
the room.

This is new. No competitor product has simulation execution events and human messages in the
same thread. The effect in a meeting: participants can comment on what the IR just did,
ask the bot questions mid-execution, and see the process and the conversation as one narrative.

---

## 2. Message Schema

All messages in the sim-chat channel share a base schema with a `source` discriminator:

```typescript
interface SimChatMessage {
  id: string                    // UUID
  channelId: string             // session-scoped channel ID
  timestamp: number             // Unix ms
  source: MessageSource         // discriminates the union
  content: string               // rendered display text (markdown supported)
  metadata: Record<string, unknown>
}

type MessageSource =
  | HumanMessage
  | NodeExecutionMessage
  | SystemMessage
  | BotMessage
```

### Human Message

```typescript
interface HumanMessage {
  type: 'human'
  participantId: string         // ra96it UUID
  displayName: string
  avatarColor: string           // hex
  inputMethod: 'keyboard' | 'voice' | 'paste'
  tier: number                  // participant permission tier at time of message
}
```

### Node Execution Message

```typescript
interface NodeExecutionMessage {
  type: 'node_execution'
  nodeId: string                // IR node ID
  nodeType: string              // TASK | GATEWAY | EVENT | SUBPROCESS | etc.
  nodeLabel: string             // human-readable node name
  executionStatus: 'started' | 'completed' | 'failed' | 'branched'
  durationMs?: number
  cost?: ThreeCurrencyReport    // CLOCK, COIN, CARBON
  branchTaken?: string          // for GATEWAY nodes
  outputSummary?: string        // LLM-generated one-liner summary of what happened
  irRunId: string               // links back to the Event Ledger run record
}
```

### System Message

```typescript
interface SystemMessage {
  type: 'system'
  event: string                 // e.g. 'HOST_CHANGED', 'PARTICIPANT_JOINED', 'SESSION_LEADERLESS'
  displayText: string           // pre-rendered human-readable description
  severity: 'info' | 'warning' | 'critical'
}
```

### Bot Message

```typescript
interface BotMessage {
  type: 'bot'
  botId: string                 // which bee or agent sent this
  botLabel: string              // display name e.g. "Meeting Bot", "Q33N"
  replyToId?: string            // if this is a reply to a human message
  confidence?: number           // 0-1, shown as subtle indicator
}
```

---

## 3. Visual Rendering

The sim-chat pane renders all message types in a single scrolling thread. Visual
differentiation by source type:

| Source | Left gutter | Background | Name treatment |
|--------|-------------|------------|----------------|
| Human | Colored avatar circle | None (chat bubble) | Display name bold |
| Node execution | IR node type icon | Subtle tinted bg (`--sd-purple-dim`) | Node label + type badge |
| System | System icon | Amber tint for warning, red for critical | Italic, centered |
| Bot | Bot avatar | Subtle green tint | Bot label + model badge |

Node execution messages are visually lighter than human messages — they should not dominate
the thread. Configurable verbosity:

```yaml
simChat:
  nodeVerbosity: summary        # summary | detailed | silent
  # summary: show node name, status, duration only
  # detailed: show full metadata including costs and output
  # silent: node events suppressed (not recommended for governed sessions)
```

---

## 4. Channel Routing

The sim-chat channel is a named relay_bus channel. Any component that can emit to or
subscribe from the relay_bus can participate.

**Channel ID:** `sim-chat:{sessionId}`

### Who Can Post

| Source | How | Gate |
|--------|-----|------|
| Human participant | Chat input in sim-chat pane | Requires tier ≥ 1 (PARTICIPANT) |
| IR node | `emit` step in IR with `channel: sim-chat` | gate_enforcer checks IR signature |
| Meeting bot (BEE) | relay_bus emit with `type: bot` | gate_enforcer checks bot identity |
| System | Automatic on presence events | No gate — system always posts |

### IR Emit Step

Any IR node can post to sim-chat as a process step:

```yaml
- type: TASK
  id: notify-team
  label: Notify Team
  actions:
    - type: emit
      channel: sim-chat
      message: "Step 3 complete. Sarah, please review the output above."
      source:
        type: bot
        botLabel: Meeting Bot
```

This is the mechanism that makes the simulation a meeting participant. The IR author writes
the messages. The bot delivers them at the right moment in the process.

---

## 5. MCP Exposure

The sim-chat channel is exposed via the Hive Chat MCP server. External agents (including
Claude in a separate Claude Code session) can:

- **Read** the sim-chat history as context
- **Post** bot messages (with appropriate credentials)
- **Subscribe** to new messages (streaming)

This enables scenarios where an external agent joins the sim-chat as an observer or
contributor — attending the meeting as a peer, not just watching logs.

```
MCP tool: sim_chat_read(sessionId, since?: timestamp, limit?: number)
MCP tool: sim_chat_post(sessionId, message: BotMessage)
MCP tool: sim_chat_subscribe(sessionId) → stream
```

---

## 6. Mobile Bridge (Efemera STT/TTS)

When a participant is in `MOBILE_BRIDGE` presence state:

- Their voice is transcribed via STT (stt-engine primitive)
- Transcribed text posts to sim-chat as a human message with `inputMethod: 'voice'`
- Incoming sim-chat messages are read aloud via TTS (tts-engine primitive)
- The participant hears the full meeting stream including node execution summaries
- Node execution messages use `outputSummary` field for TTS (full metadata is not read aloud)

The STT/TTS bridge runs on the Efemera mobile client. The sim-chat channel is the shared
medium — mobile and desktop participants are in the same thread.

---

## 7. Persistence

Sim-chat messages are persisted in two places:

1. **Y.js shared document** — real-time sync across all participants, session-scoped
2. **Event Ledger** — append-only audit trail, permanent record

On session end, the full sim-chat log is included in the meeting summary artifact. The
summary is generated by a BEE that reads the log and produces a structured markdown document:

- Key decisions made
- IR execution summary (nodes run, costs incurred in 3 currencies)
- Action items extracted from human messages
- Participant attendance record

---

## 8. Meeting Agenda IR Integration

The sim-chat channel is aware of the meeting agenda IR. When an IR process is running in
the session, the sim-chat pane can optionally show a subtle "process tracker" above the
message thread — the current IR node highlighted, with a progress indicator.

This is display-only. The IR execution happens in the IR engine. The sim-chat channel
just listens and renders.

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-SIM-CHAT-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

sim-chat is primarily a **consumer** — it renders messages from multiple sources into one thread.

**Events consumed by sim-chat pane adapter:**

| Event | Source | Effect |
|-------|--------|--------|
| `PRESENCE_JOINED` | Presence service | System message: "X joined" |
| `PRESENCE_LEFT` | Presence service | System message: "X left" |
| `HOST_CHANGED` | Presence service | Bot message: "X is now hosting" (if IR running) |
| `MOBILE_BRIDGE_ENTERED` | Presence service | System message + enable TTS output mode |
| `SESSION_LEADERLESS` | Presence service | System message: "Room has no active host" |
| `SIM_CHAT_TTS_MODE` | IR engine (via presence trigger) | Switch rendering to outputSummary for TTS |
| IR node execution events | IR engine | Interleaved node_execution messages in thread |

**Events emitted by sim-chat:**

| Event | When | Consumers |
|-------|------|-----------|
| `SIM_CHAT_MESSAGE_POSTED` | Human types a message | Event Ledger (permanent record), Y.js (session sync) |
| `SESSION_END` | Host ends session | Presence service teardown, meeting summary generation |

**Channel naming:** `sim-chat:{sessionId}` — sim-chat adapter subscribes to this channel on mount.

**Distinct from chat bubbles (BL-010, BUILT):** BL-010 is a text-pane markdown renderer for bot-style output. sim-chat is a multi-participant real-time channel with mixed human + IR messages. Different pane, different purpose.
