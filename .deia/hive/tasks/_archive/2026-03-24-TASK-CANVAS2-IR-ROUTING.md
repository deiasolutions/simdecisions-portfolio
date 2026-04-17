# TASK-CANVAS2-IR-ROUTING: Fix Canvas2 IR Mutations Not Reaching Canvas

## Objective
Trace and fix the IR mutation routing path from terminal (routeTarget: 'ir') to canvas in the canvas2 EGG. IR mutations from LLM responses are not reaching the canvas pane.

## Context
The canvas2 EGG (`eggs/canvas2.egg.md`) has a terminal pane with `routeTarget: "ir"` that sends user prompts to an LLM. The LLM returns structured JSON with `to_ir` mutations:

```json
{
  "to_user": "Brief confirmation",
  "to_ir": [
    { "action": "add_node", "nodeData": { "id": "n1", "name": "Review", "node_type": "process" } }
  ]
}
```

**Expected flow:**
1. Terminal receives LLM response
2. `routeEnvelope()` parses it, sends `terminal:ir-deposit` to `canvas-editor`
3. FlowDesigner subscribes to `terminal:ir-deposit`, receives mutations
4. `processMutations()` applies them to canvas state

**Current status:**
- Terminal config: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md` (lines 100-117)
- Terminal routing: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 688-715)
- Envelope router: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts` (lines 184-196)
- Canvas handler: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (lines 527-606)
- Mutation processor: `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\irMutationProcessor.ts`

**Likely break points:**
1. paneRegistry construction in useTerminal (lines 688-695) — might not map `to_ir` → `canvas-editor` correctly
2. LLM not returning envelope format (returning plain text or markdown instead)
3. Bus routing: message sent but not received by canvas

## Files to Read First
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\eggs\canvas2.egg.md`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\primitives\terminal\useTerminal.ts` (lines 616-820)
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\services\terminal\terminalResponseRouter.ts`
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\browser\src\apps\sim\components\flow-designer\FlowDesigner.tsx` (lines 527-606)

## Deliverables
- [ ] Integration test: `browser/src/primitives/terminal/__tests__/terminal-canvas2-ir.test.tsx` — full path from LLM response → canvas state update
  - Mock LLM response with `to_ir` array
  - Verify `routeEnvelope` extracts `to_ir` and sends bus message
  - Verify FlowDesigner receives message and applies mutations
  - Verify nodes/edges updated in canvas state
  - Test both mutation array format AND PHASE-IR object format
- [ ] Debug logging added to trace path (remove after verification):
  - Terminal: log paneRegistry, resolveTarget result, bus.send call
  - FlowDesigner: log received message, mutation processing result
- [ ] Fix identified bugs:
  - If paneRegistry mapping wrong: fix construction logic
  - If LLM format wrong: update EGG prompt or add fallback parsing
  - If bus routing broken: fix subscription or send logic
- [ ] Verify existing tests still pass: `npm --prefix browser test terminal` and `npm --prefix browser test flow-designer`

## Test Requirements
- [ ] Tests written FIRST (TDD)
- [ ] All tests pass
- [ ] Edge cases:
  - Empty `to_ir` array (should not crash)
  - Invalid mutation (missing action field) — should log error, not crash
  - LLM returns plain text (no envelope) — should gracefully degrade, show text to user
  - Multiple mutations in one response — all applied
  - Duplicate node IDs — mutation skipped with error logged

## Constraints
- No file over 500 lines
- CSS: `var(--sd-*)` only
- No stubs
- Do NOT modify EGG file unless prompt is provably wrong
- Remove debug logging after verification

## Acceptance Criteria
- [ ] Integration test passes showing full path works
- [ ] Existing terminal tests pass (no regressions)
- [ ] Existing FlowDesigner tests pass (no regressions)
- [ ] Debug logs show exact break point (if any)
- [ ] Bug fix applied (if bug found)
- [ ] All edge cases handled gracefully

## Response Requirements — MANDATORY

When you finish your work, write a response file:
  `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\hive\responses\20260324-TASK-CANVAS2-IR-ROUTING-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** — task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** — every file created/modified/deleted, full paths
3. **What Was Done** — bullet list of concrete changes
4. **Test Results** — test files run, pass/fail counts
5. **Build Verification** — test/build output summary
6. **Acceptance Criteria** — copy from task, mark [x] or [ ]
7. **Clock / Cost / Carbon** — all three, never omit any
8. **Issues / Follow-ups** — edge cases, dependencies, next tasks

DO NOT skip any section.
