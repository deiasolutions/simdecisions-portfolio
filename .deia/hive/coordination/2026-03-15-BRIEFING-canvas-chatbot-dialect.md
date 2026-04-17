# BRIEFING: Port Canvas Chatbot Dialect

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-15
**Model Assignment:** haiku
**Source Spec:** `.deia/hive/queue/2026-03-15-1519-SPEC-w1-15-canvas-chatbot-dialect.md`

---

## Objective

Port the canvas chatbot dialect .md file from the platform repo and find/port the chat-with-process spec. The dialect defines how the terminal talks to the canvas (NL → LLM → to_ir → render).

---

## Context from Q88N

This is a P0.75 spec from the queue. The canvas chatbot dialect is a key integration piece that connects the terminal's natural language input to the canvas rendering system. The flow is:

1. User types in terminal
2. LLM processes natural language
3. Converts to IR (intermediate representation)
4. Canvas renders the IR

The dialect file should be in `platform/dialects/` and needs to be ported to either `eggs/` or `docs/specs/`.

There's also a chat-with-process spec that needs to be located and ported.

---

## Source Files to Check

From the platform repo (`platform/` directory):
- `platform/dialects/` — look for canvas chatbot dialect
- Search for chat-with-process spec (could be in specs/, dialects/, or docs/)

Target locations in shiftcenter:
- `eggs/` — if it's an EGG config
- `docs/specs/` — if it's a spec document

---

## Constraints

- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: `var(--sd-*)` only
- Heartbeat required: POST to `http://localhost:8420/build/heartbeat` every 3 minutes with:
  ```json
  {
    "task_id": "2026-03-15-1519-SPEC-w1-15-canvas-chatbot-dialect",
    "status": "running",
    "model": "haiku",
    "message": "working"
  }
  ```

---

## Acceptance Criteria (from spec)

- [ ] Canvas chatbot dialect file ported
- [ ] Chat-with-process spec located and ported
- [ ] Dialect integrates with terminal routeTarget system

---

## Smoke Test

- [ ] File exists and is valid markdown
- [ ] No new test failures

---

## What Q33N Must Do

1. **Search the platform repo** for the canvas chatbot dialect file
2. **Search the platform repo** for the chat-with-process spec
3. **Write a task file** for a bee to:
   - Port the dialect file
   - Port the chat-with-process spec
   - Verify integration with terminal routeTarget system
   - Add tests if needed (per TDD)
4. **Return task file(s) to Q33NR** for review before dispatching

---

## Notes

- The terminal routeTarget system is already implemented (per MEMORY.md: "Terminal `routeTarget: 'relay'` added")
- The dialect should define the contract between terminal and canvas
- The chat-with-process spec should define how the process communicates with the canvas
- Both files are documentation/specs, so they may not need tests (but Q33N should verify)

---

## Q33N: Read These Files First

Before writing task files, read:
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (routeTarget implementation)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\sim.egg.md` (example EGG with canvas)
- Search platform repo for source files

---

**Q33NR approval required before dispatch.**
