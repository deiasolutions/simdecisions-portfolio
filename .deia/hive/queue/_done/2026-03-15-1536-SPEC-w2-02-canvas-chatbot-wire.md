# SPEC: Wire canvas chatbot terminal NL to LLM to to_ir to canvas renders

## Priority
P0.90

## Model Assignment
sonnet

## Objective
Wire the canvas chatbot flow: user types natural language in terminal, LLM converts to PHASE-IR, canvas renders nodes. Connect terminal routeTarget=canvas to LLM adapter, parse response into IR, send to canvas via bus events.

## Acceptance Criteria
- [ ] Terminal NL input reaches LLM
- [ ] LLM response parsed into PHASE-IR flow
- [ ] Canvas receives and renders flow
- [ ] End-to-end demo works
- [ ] Tests written and passing

## Constraints
- Max 500 lines per file
- TDD: tests first
- No stubs
- CSS: var(--sd-*) only
- POST heartbeats to http://localhost:8420/build/heartbeat every 3 minutes with JSON:
  {"task_id": "2026-03-15-1536-SPEC-w2-02-canvas-chatbot-wire", "status": "running", "model": "sonnet", "message": "working"}

## Smoke Test
- [ ] cd browser && npx vitest run src/apps/sim/
- [ ] No new test failures
