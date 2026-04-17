# SPEC-IR-PRESENCE-TRIGGER-001: Presence Events as IR-Triggerable Conditions

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** IR
**T-Shirt Size:** S
**Depends On:** PHASE-IR v2.0, SPEC-PRESENCE-001, relay_bus (BUILT)

---

## 1. Purpose

This spec adds `trigger: presence` as a first-class trigger type in PHASE-IR v2.0. It is an
addendum to the existing IR trigger system, which already supports `timer`, `human_input`,
and `bus_event`.

With this addition, meeting agenda IR can react to participant events — host drop, mobile
bridge handoff, participant join/leave — without hardcoded platform logic. The meeting bot
executes the process; presence events are just another input stream.

This is a small change with large implications: it is the mechanism by which an IR-authored
meeting agenda governs its own logistics.

---

## 2. Existing Trigger Types (Reference)

```yaml
# Timer trigger
trigger:
  type: timer
  duration: PT5M              # ISO 8601 duration

# Human input trigger
trigger:
  type: human_input
  promptText: "Approve to continue?"
  tier_required: 5            # HOST tier minimum

# Bus event trigger
trigger:
  type: bus_event
  event: SOME_BUS_EVENT
  condition: "payload.value > 10"
```

---

## 3. New Trigger Type: presence

```yaml
trigger:
  type: presence
  event: PRESENCE_EVENT_NAME        # required — which presence event to listen for
  condition: string                  # optional — CEL expression evaluated against event payload
  timeout: ISO8601Duration           # optional — if event not received within timeout, take timeout branch
  participantFilter: string          # optional — filter to specific participant ID or role
```

### Supported Presence Events

All events from SPEC-PRESENCE-001 `§7 Bus Events` are available as IR triggers:

| Event | Typical Use in IR |
|-------|-------------------|
| `PRESENCE_JOINED` | Start timer when minimum participants are present |
| `PRESENCE_LEFT` | Handle participant drop gracefully |
| `PRESENCE_STATE_CHANGED` | React to mobile bridge, idle, reconnect |
| `HOST_CHANGED` | Announce new host, update agenda display |
| `SESSION_LEADERLESS` | Pause agenda, wait for host |
| `MOBILE_BRIDGE_ENTERED` | Switch to TTS-friendly node output summaries |
| `VIEWPORT_SYNC` | (consumed, not triggered by) |

---

## 4. Examples

### 4.1 Host Drop → Survivor Election

```yaml
- type: GATEWAY
  id: host-drop-check
  label: Host Connected?
  trigger:
    type: presence
    event: HOST_CHANGED
    condition: "event.reason == 'disconnect'"
    timeout: PT30S
  branches:
    - condition: "event.newHost != null"
      label: Survivor took over
      next: announce-new-host
    - condition: "event.newHost == null"
      label: No survivor available
      next: leaderless-state-handler
    - condition: timeout
      label: Grace period expired with no change
      next: leaderless-state-handler

- type: TASK
  id: announce-new-host
  label: Announce New Host
  actions:
    - type: emit
      channel: sim-chat
      message: "{{event.newHost.displayName}} is now hosting."
      source: { type: bot, botLabel: Meeting Bot }
  next: resume-agenda

- type: TASK
  id: leaderless-state-handler
  label: Room Leaderless
  actions:
    - type: emit
      channel: sim-chat
      message: "The room has no active host. Canvas is read-only. First person to reconnect will lead."
      source: { type: system }
    - type: bus_emit
      event: CANVAS_READONLY
      payload: { reason: leaderless }
  trigger:
    type: presence
    event: HOST_CHANGED
    condition: "event.newHost != null"
  next: announce-new-host
```

### 4.2 Start Meeting When Quorum Reached

```yaml
- type: TASK
  id: wait-for-quorum
  label: Waiting for Participants
  actions:
    - type: emit
      channel: sim-chat
      message: "Waiting for at least 3 participants before we begin..."
      source: { type: bot, botLabel: Meeting Bot }
  trigger:
    type: presence
    event: PRESENCE_JOINED
    condition: "session.participantCount >= 3"
    timeout: PT10M
  branches:
    - condition: "session.participantCount >= 3"
      next: welcome-and-begin
    - condition: timeout
      next: begin-anyway
```

### 4.3 Mobile Bridge — Switch to Audio-Friendly Mode

```yaml
- type: GATEWAY
  id: host-bridge-check
  label: Host on Mobile?
  trigger:
    type: presence
    event: MOBILE_BRIDGE_ENTERED
    participantFilter: role:HOST
  branches:
    - condition: "event.participantId == session.hostId"
      next: enable-tts-mode
    - condition: default
      next: continue-normally

- type: TASK
  id: enable-tts-mode
  label: Enable TTS Mode
  actions:
    - type: bus_emit
      event: SIM_CHAT_TTS_MODE
      payload: { enabled: true, targetParticipantId: "{{event.participantId}}" }
    - type: emit
      channel: sim-chat
      message: "Host has joined from mobile. Voice bridge active."
      source: { type: system }
```

### 4.4 "Continue Without Me" — Host Hands Off

```yaml
- type: TASK
  id: continue-without-host
  label: Host Delegating
  trigger:
    type: human_input
    promptText: "Continue without me?"
    tier_required: 5
  actions:
    - type: bus_emit
      event: TIER_GRANT
      payload:
        participantId: "{{session.designeeList[0]}}"
        tier: 5
    - type: emit
      channel: sim-chat
      message: "{{session.host.displayName}} has handed off. {{session.designeeList[0].displayName}} is now host."
      source: { type: bot, botLabel: Meeting Bot }
  next: resume-agenda
```

---

## 5. CEL Expression Context

When evaluating `condition` expressions on presence triggers, the following variables are
available:

| Variable | Type | Description |
|----------|------|-------------|
| `event` | PresenceEvent | The triggering event payload (from SPEC-PRESENCE-001 §7) |
| `session` | SessionState | Current session metadata |
| `session.participantCount` | number | Current connected participant count |
| `session.hostId` | string | Current host's participant ID |
| `session.designeeList` | Participant[] | Ordered survivor list |
| `session.ownerId` | string | Session owner's participant ID |

---

## 6. PHASE-IR Schema Change

This spec adds one entry to the `TriggerType` enum in the PHASE-IR v2.0 schema:

```typescript
// Before
type TriggerType = 'timer' | 'human_input' | 'bus_event';

// After (this spec)
type TriggerType = 'timer' | 'human_input' | 'bus_event' | 'presence';
```

And adds the `PresenceTrigger` interface to the trigger union:

```typescript
interface PresenceTrigger {
  type: 'presence';
  event: PresenceEventName;          // keyof PresenceEventMap from SPEC-PRESENCE-001
  condition?: string;                // CEL expression
  timeout?: string;                  // ISO 8601 duration
  participantFilter?: string;        // participantId | 'role:HOST' | 'role:OWNER'
}
```

The IR engine subscribes to relay_bus presence events and evaluates trigger conditions on
each incoming event. No new engine subsystem required — presence triggers use the same
condition evaluation pipeline as `bus_event` triggers. The only new code is the
`PresenceTrigger` type guard and the relay_bus subscription for presence event types.

---

## 7. Round-Trip Fidelity

Presence trigger conditions must survive the English→IR→English round-trip. The following
English phrases should compile to predictable IR:

| English | Expected IR |
|---------|-------------|
| "If the host disconnects" | `trigger: presence, event: HOST_CHANGED, condition: "event.reason == 'disconnect'"` |
| "When at least 5 people have joined" | `trigger: presence, event: PRESENCE_JOINED, condition: "session.participantCount >= 5"` |
| "If the host goes to their phone" | `trigger: presence, event: MOBILE_BRIDGE_ENTERED, participantFilter: "role:HOST"` |
| "Wait up to 10 minutes for everyone to arrive" | `trigger: presence, event: PRESENCE_JOINED, condition: "...", timeout: PT10M` |

These phrases should be validated in the English→IR compiler test suite.

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-IR-PRESENCE-TRIGGER-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

IR presence triggers are **consumers** of presence events. The IR engine subscribes to relay_bus presence events and evaluates trigger conditions.

**Handler location:** `services/ir/triggerEvaluator.ts` — the existing bus_event trigger evaluation pipeline. Presence triggers reuse the same condition evaluation logic; the only new code is the `PresenceTrigger` type guard and relay_bus subscriptions for presence event types.

**Events consumed by IR engine for presence triggers:**

| Event | Trigger Use |
|-------|-------------|
| `HOST_CHANGED` | Host drop → survivor election IR branch |
| `PRESENCE_JOINED` | Quorum checks, meeting start conditions |
| `PRESENCE_LEFT` | Graceful participant drop handling |
| `MOBILE_BRIDGE_ENTERED` | Host→mobile handoff, TTS mode activation |
| `SESSION_LEADERLESS` | Pause agenda, wait for host |
| `PRESENCE_STATE_CHANGED` | General state-change conditions (idle, reconnect) |

**Events emitted by IR engine (in response to presence triggers):**

| Event | Target |
|-------|--------|
| `SIM_CHAT_TTS_MODE` | sim-chat pane adapter |
| `CANVAS_READONLY` | canvas_surface |
| `TIER_GRANT` | Presence service |
| sim-chat `emit` actions | sim-chat channel (bot/system messages) |
