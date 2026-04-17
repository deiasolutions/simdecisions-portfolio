# SPEC: Port canvas chatbot dialect + chat-with-process spec

## Priority
P0.75

## Model Assignment
haiku

## Objective
Port the canvas chatbot dialect .md file from platform and find/port the chat-with-process spec. The dialect defines how the terminal talks to the canvas (NL to LLM to to_ir to render). Source: platform/dialects/. Target: eggs/ or docs/specs/.

## Acceptance Criteria
- [ ] Canvas chatbot dialect file ported
- [ ] Chat-with-process spec located and ported
- [ ] Dialect integrates with terminal routeTarget system

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1519-SPEC-w1-15-canvas-chatbot-dialect", "status": "running", "model": "haiku", "message": "working"}

## Smoke Test
- [ ] File exists and is valid markdown
- [ ] No new test failures
