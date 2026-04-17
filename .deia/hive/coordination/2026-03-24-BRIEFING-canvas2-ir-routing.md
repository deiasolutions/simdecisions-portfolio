# BRIEFING: Canvas2 IR Mutations Not Reaching Canvas

**Date:** 2026-03-24
**From:** Q33NR
**Priority:** P1
**Bug:** LLM commands from terminal are NOT getting to the canvas on canvas2

## Problem

In the canvas2 EGG (`eggs/canvas2.egg.md`), the terminal pane (nodeId: `canvas-ir`, appType: `terminal`, routeTarget: `ir`) sends user prompts to the LLM. The LLM returns structured JSON:

```json
{
  "to_user": "Brief confirmation",
  "to_ir": [
    { "action": "add_node", "nodeData": { "id": "n1", "name": "Review", "node_type": "process" } }
  ]
}
```

The `to_ir` mutations are supposed to reach the canvas pane (nodeId: `canvas-editor`, appType: `sim`) and render as nodes/edges. **They are not arriving.**

## EGG Config (key parts)

Terminal pane config:
```json
{
  "routeTarget": "ir",
  "links": {
    "to_ir": "canvas-editor",
    "to_text": "canvas-chat"
  }
}
```

Bus permissions include `terminal:ir-deposit` for both emit and receive.

## What Q33N Must Do

1. **Trace the full code path** from terminal LLM response → bus emission → canvas reception:
   - `browser/src/primitives/terminal/` — how does routeTarget "ir" handle LLM responses? Does it parse `to_ir` and emit `terminal:ir-deposit`?
   - `browser/src/apps/sim/` — does the sim/FlowDesigner component subscribe to `terminal:ir-deposit`? Does it process the mutations array?
   - `browser/src/infrastructure/relay_bus/` — is the bus correctly routing between these panes?

2. **Identify the break point.** Find exactly where the chain stops.

3. **Write a task file** for a bee to fix it. The fix must include tests.

4. A previous bee attempt (commit `272955f`) claimed to fix this but made NO actual code changes — only config/logs. Do not repeat that mistake. Look at the SOURCE CODE.

## Constraints

- Do NOT modify the EGG file — the config is correct.
- The fix is in the TypeScript source code (browser/).
- Tests must verify the full path: terminal response → bus event → canvas mutation applied.
