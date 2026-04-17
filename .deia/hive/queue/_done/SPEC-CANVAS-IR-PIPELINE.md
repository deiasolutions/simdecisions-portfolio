# SPEC: Canvas IR Pipeline End-to-End Fix

## Objective

Canvas IR pipeline is broken end-to-end. Terminal generates PHASE-IR from NL input but canvas never receives or renders it. This is a REGRESSION -- it was working before. Find the existing working code via git history. Restore it. This was functional before.

Related bugs: BUG-018, BUG-058.

Investigation notes:
- Terminal sends `terminal:ir-deposit` message with target = `links.to_ir`
- Canvas receives by data shape (checks for `nodes` array/object), not message type
- Backend endpoint: `/api/phase/nl-to-ir`
- Possible issue: backend returning wrong structure, or bus message not reaching canvas pane
- Check git log for commits mentioning "to_ir", "ir-deposit", "nl-to-ir" to find last working state

## Files to Read First

- browser/src/primitives/terminal/useTerminal.ts
- browser/src/primitives/terminal/irRouting.ts
- browser/src/primitives/terminal/irExtractor.ts
- browser/src/primitives/canvas/CanvasApp.tsx
- browser/src/services/terminal/terminalResponseRouter.ts
- browser/src/infrastructure/relay_bus/messageBus.ts
- eggs/canvas2.egg.md

## Files to Modify

- browser/src/primitives/terminal/useTerminal.ts
- browser/src/primitives/terminal/irRouting.ts
- browser/src/primitives/terminal/irExtractor.ts
- browser/src/primitives/canvas/CanvasApp.tsx
- browser/src/services/terminal/terminalResponseRouter.ts

## Deliverables

- [ ] Root cause identified via git history
- [ ] IR pipeline restored end-to-end: terminal -> bus -> canvas renders nodes
- [ ] Regression tests covering the full pipeline

## Acceptance Criteria

- [ ] Terminal sends `terminal:ir-deposit` message with correct target paneId when NL input is submitted
- [ ] Canvas bus handler receives `terminal:ir-deposit` message and extracts IR data
- [ ] Canvas calls `loadIRFlow()` with received IR nodes and edges
- [ ] `loadIRFlow()` correctly maps IR nodes to ReactFlow node format
- [ ] Backend `/api/phase/nl-to-ir` endpoint returns correct IR structure
- [ ] End-to-end test: NL input in terminal -> backend generates IR -> canvas renders nodes and edges
- [ ] Regression check: git history reviewed to identify last working commit for this pipeline
- [ ] No stubs: all handler functions fully implemented
- [ ] All tests pass

## Smoke Test

- [ ] cd browser && npx vitest run src/primitives/canvas/__tests__/canvas-ir-deposit.test.tsx -- tests pass
- [ ] cd browser && npx vitest run src/services/terminal/__tests__/terminalResponseRouter.test.ts -- tests pass
- [ ] cd browser && npx vitest run -- no regressions

## Constraints

- CRITICAL: Do NOT rewrite from scratch. Find working code in git history and restore it.
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- TDD -- write tests first, then fix

## Model Assignment

sonnet

## Priority

P0
