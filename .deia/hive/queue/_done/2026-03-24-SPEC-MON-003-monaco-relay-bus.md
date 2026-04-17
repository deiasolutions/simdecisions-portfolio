# SPEC: MON-003 Monaco Relay Bus Integration

## Priority
P1

## Depends On
- SPEC-MON-001-monaco-applet-component

## Objective
Wire Monaco into the relay bus — emit CODE_CHANGED events on content change (debounced 300ms) and accept inbound code:set / code:save bus events from other panes.

## Context
MON-001 exposed getValue() via ref. This task wires Monaco into the relay bus per SPEC-MONACO-BUS-001. This makes Monaco a first-class ShiftCenter citizen: other panes (AI assistant, log-viewer, terminal) can push code into the editor and receive code output via the bus.

## Files to Read First
- browser/src/infrastructure/relay_bus/messageBus.ts
- browser/src/primitives/terminal/useTerminal.ts

## Task File
Full task spec with acceptance criteria and file locations:
.deia/hive/queue/_stage/2026-03-24-TASK-MON-003-monaco-relay-bus.md

Read the task file above — it contains the complete scope, file locations, constraints, and acceptance criteria. Follow it exactly.

## Deliverables
1. browser/src/primitives/code-editor/monacoRelayBus.ts — bus wiring module
2. browser/src/primitives/code-editor/MonacoApplet.tsx — minimal additions (init/dispose calls)
3. browser/src/primitives/code-editor/__tests__/monacoRelayBus.test.ts — TDD tests (min 10)

## Acceptance Criteria
- [ ] CODE_CHANGED emitted after 300ms debounce on content change
- [ ] CODE_CHANGED NOT emitted when content is set programmatically via code:set
- [ ] code:set payload loads content into editor
- [ ] code:save triggers volume save
- [ ] All tests pass (minimum 10 tests)
- [ ] Existing MON-001 tests still pass

## Response File
.deia/hive/responses/20260324-TASK-MON-003-RESPONSE.md
