# SPEC-CALENDAR-EGG-001: Calendar Scheduling Agent EGG

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** EGG
**T-Shirt Size:** L
**Depends On:** relay_bus (BUILT), EGG system (BUILT), calendar primitive (SPECCED),
               SPEC-IR-PRESENCE-TRIGGER-001, timeline primitive (SPECCED), prompt service (BUILT)

---

## 1. Purpose

The Calendar EGG turns ShiftCenter into a scheduling agent. It is not a passive calendar
viewer — it is an IR-driven process that reacts to calendar events, proposes actions, and
executes governed responses.

The thesis: a calendar event is an IR trigger. "Meeting at 2pm" compiles to a PHASE-IR
process with a `trigger: timer` at 14:00 that dispatches a BEE, sends a sim-chat
notification, prepares an agenda, and opens the meeting room EGG. None of this requires
hardcoded platform logic — it is all IR authored from natural language.

---

## 2. Domain

**Primary subdomain:** `calendar.shiftcenter.com`

The EGG runs on its own subdomain. It is also embeddable as a pane inside any other EGG
via `appType: calendar-agent` (GC-registered composite applet).

---

## 3. Data Sources

The Calendar EGG ingests events from external calendar systems via adapters. Adapters are
declared in the EGG config. Multiple adapters can run simultaneously.

### Supported Adapters (v1)

| Adapter | Protocol | Auth |
|---------|----------|------|
| `google-calendar` | Google Calendar API v3 | OAuth2 via ra96it connector |
| `icloud` | CalDAV | ra96it credential store |
| `outlook` | Microsoft Graph API | OAuth2 via ra96it connector |
| `caldav-generic` | RFC 4791 CalDAV | URL + credentials |
| `ics-url` | iCalendar feed (read-only) | URL |

Adapters are GC-registered infrastructure services, not EGG-level connectors. They run
on the hivenode and push events to the relay_bus as `CALENDAR_EVENT_*` bus events.

### #NOKINGS on Calendar Data

Calendar data never leaves the hivenode except to the declared external calendar system.
DEIA Solutions does not receive calendar data. The adapter runs locally. The EGG config
declares which adapters to load. The user owns their schedule.

---

## 4. EGG Layout

Three-pane layout:

```yaml
layout:
  type: split
  direction: horizontal
  children:
    - type: app
      appType: tree-browser
      nodeId: calendar-tree
      config:
        adapter: calendar-agent
        showCalendars: true
        showAgendaItems: true

    - type: split
      direction: vertical
      children:
        - type: app
          appType: timeline
          nodeId: calendar-view
          config:
            datePickerMode: true
            view: week                  # day | week | month | agenda
            adapter: calendar-agent
            showIRStatus: true          # shows IR execution status on events

        - type: app
          appType: terminal
          nodeId: agent-terminal
          config:
            welcomeBanner: "Calendar agent ready. hive>"
            zone2Dock: right
```

The terminal pane is the scheduling agent interface. The user types natural language
scheduling instructions; the agent parses them to IR and executes.

---

## 5. Calendar Adapter Bus Events

The calendar adapter emits the following events on the relay_bus:

| Event | Payload | When |
|-------|---------|------|
| `CALENDAR_EVENT_CREATED` | `{ eventId, title, start, end, attendees, calendarId }` | New event detected |
| `CALENDAR_EVENT_UPDATED` | `{ eventId, changes }` | Existing event modified |
| `CALENDAR_EVENT_DELETED` | `{ eventId }` | Event removed |
| `CALENDAR_EVENT_STARTING` | `{ eventId, minutesUntil }` | Configurable lead time (default 5min) |
| `CALENDAR_EVENT_STARTED` | `{ eventId }` | Event start time reached |
| `CALENDAR_EVENT_ENDED` | `{ eventId, duration }` | Event end time reached |
| `CALENDAR_SYNC_COMPLETE` | `{ calendarId, eventCount }` | Full sync finished |

These events are first-class IR triggers. See SPEC-IR-CALENDAR-TRIGGER-001 (implied
by this spec — small addendum to IR trigger types, same pattern as SPEC-IR-PRESENCE-TRIGGER-001).

---

## 6. IR Trigger: calendar

Following the pattern established in SPEC-IR-PRESENCE-TRIGGER-001, calendar events become
IR trigger conditions:

```yaml
trigger:
  type: calendar
  event: CALENDAR_EVENT_STARTING
  condition: "event.minutesUntil <= 5"
  calendarFilter: "work"            # optional: filter by calendar name
  titleFilter: "standup"            # optional: filter by event title (substring)
```

```yaml
trigger:
  type: calendar
  event: CALENDAR_EVENT_CREATED
  condition: "event.attendees.length >= 3"
```

This is the mechanism for "react to things happening on the list." The calendar adapter
emits; the IR process listens and responds.

---

## 7. Sample IR Processes (Meeting Prep Pattern)

The canonical use case: when a meeting is starting soon, prepare the room.

```yaml
# meeting-prep.ir.yaml
name: Meeting Preparation
version: 1.0.0

- type: EVENT
  id: start
  trigger:
    type: calendar
    event: CALENDAR_EVENT_STARTING
    condition: "event.minutesUntil <= 10 AND event.attendees.length >= 2"

- type: TASK
  id: generate-agenda
  label: Generate Agenda
  agent: BEE-001
  prompt: |
    Meeting: {{event.title}}
    Attendees: {{event.attendees | join(', ')}}
    Duration: {{event.duration}} minutes
    Generate a structured agenda for this meeting.
  output: agenda_text
  next: open-meeting-room

- type: TASK
  id: open-meeting-room
  label: Open Meeting Room EGG
  actions:
    - type: bus_emit
      event: EGG_OPEN
      payload:
        eggId: meeting-room
        sessionTitle: "{{event.title}}"
        agenda: "{{agenda_text}}"
        attendees: "{{event.attendees}}"
    - type: emit
      channel: sim-chat
      message: "Meeting room ready for {{event.title}}. Agenda prepared."
      source: { type: bot, botLabel: Calendar Agent }
  next: end

- type: EVENT
  id: end
  trigger:
    type: calendar
    event: CALENDAR_EVENT_ENDED
```

This entire workflow — detect meeting, generate agenda, open room — is IR. No platform code.

---

## 8. Scheduling Agent — Natural Language Interface

The terminal pane runs the scheduling agent. Users issue natural language commands:

```
hive> schedule a standup with Sarah tomorrow at 9am for 30 minutes
hive> move my 3pm to Thursday same time
hive> find a free 1-hour slot this week for Dave and Sarah
hive> what's on my calendar Friday?
hive> cancel the 2pm and notify attendees
```

The agent:
1. Parses the command to an IR intent
2. Shows a round-trip confirmation ("Here's what I'll do: ...") — REQUIRE_HUMAN by default
3. Executes via the calendar adapter on approval
4. Posts confirmation to sim-chat

REQUIRE_HUMAN is on by default for all write operations (create, update, delete, notify).
Read operations (query, "what's on my calendar") are auto-approved.

---

## 9. "React to Things on the List" — Automation Patterns

The Calendar EGG ships with a library of pre-authored IR process templates:

| Template | Trigger | Action |
|----------|---------|--------|
| `meeting-prep` | Event starting in 10min | Generate agenda, open meeting room |
| `daily-brief` | Every day at configured time | Summarize today's calendar, post to sim-chat |
| `overdue-checker` | Event ended with no notes | Prompt for meeting notes |
| `conflict-detector` | Event created overlapping existing | Alert, suggest resolution |
| `attendee-notifier` | Event updated | Notify attendees via Efemera |
| `focus-block` | Focus time event starting | Set presence to DESKTOP_IDLE, suppress notifications |

Each template is a `.ir.yaml` file in the GC. Users activate them via the terminal:

```
hive> activate meeting-prep template
hive> show active automations
hive> deactivate daily-brief
```

---

## 10. EGG Config (Full)

```yaml
---
egg: calendar-agent
version: 1.0.0
displayName: Calendar
description: Scheduling agent. Reacts to calendar events via IR-driven automations.
favicon: global-commons://icons/calendar.png
---

adapters:
  - type: google-calendar
    calendarIds: [primary]
    syncIntervalMs: 60000
    leadTimeMinutes: 10

  - type: caldav-generic
    url: "{{secrets.caldav_url}}"
    credentials: "{{secrets.caldav_creds}}"

agent:
  model: auto                       # routes via LLM Router
  requireHumanOnWrite: true
  confirmationStyle: round-trip     # shows English before executing

automations:
  active:
    - global-commons://ir/calendar/meeting-prep.ir.yaml
    - global-commons://ir/calendar/daily-brief.ir.yaml

simChat:
  channelId: calendar-agent-chat
  nodeVerbosity: summary
```

---

## 11. Open Items — RESOLVED

| # | Question | Decision (Q88N, 2026-03-13) |
|---|----------|-----------------------------|
| 1 | Domain confirmed as `calendar.shiftcenter.com`? Or `schedule.shiftcenter.com`? | **`calendar.shiftcenter.com`**. ShiftCenter's original meaning was scheduling. Honor that. |
| 2 | Should calendar adapter be a GC infrastructure service (reusable by any EGG) or calendar-agent-specific? | GC infrastructure service — other EGGs will want calendar data. *(Q33NR recommendation accepted.)* |
| 3 | v1 adapter priority: Google Calendar first, then CalDAV? | **Google Calendar first.** Largest user base. Microsoft/Outlook second. |
| 4 | Should `CALENDAR_EVENT_*` triggers be a formal PHASE-IR addendum spec or folded into SPEC-IR-PRESENCE-TRIGGER-001? | Still open — no decision recorded. |

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-CALENDAR-EGG-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions
