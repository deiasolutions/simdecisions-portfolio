# SPEC-CANVAS3-CHAT-TERMINAL

Change the canvas3 third pane from text-pane to terminal.

## Priority
P1

## Depends On
None

## Model Assignment
haiku

## Description

The canvas3 set has a 3-column main split: sidebar (20%) | canvas (55%) | chat (25%). The third pane (`canvas-chat`) is currently `appType: "text-pane"` but should be `appType: "terminal"` so users can interact with the AI assistant.

### Current Config (wrong)
```json
{
  "type": "pane",
  "nodeId": "canvas-chat",
  "appType": "text-pane",
  "label": "Chat",
  "chrome": false,
  "config": {
    "format": "markdown",
    "readOnly": true,
    "renderMode": "chat",
    "hideHeader": true
  }
}
```

### Target Config
```json
{
  "type": "pane",
  "nodeId": "canvas-chat",
  "appType": "terminal",
  "label": "Fr@nk",
  "chrome": false,
  "config": {
    "promptPrefix": "canvas>",
    "routeTarget": "ai",
    "brandName": "SimDecisions",
    "welcomeBanner": true,
    "links": {
      "to_text": "canvas-editor"
    }
  }
}
```

### Files

| File | Change |
|------|--------|
| `eggs/canvas3.set.md` | Change canvas-chat pane from text-pane to terminal with proper config |

## Acceptance Criteria
- [ ] Third pane renders the terminal primitive with `canvas>` prompt
- [ ] Terminal routes to AI (`routeTarget: "ai"`)
- [ ] Terminal links `to_text` to the canvas editor pane for IR deposits
- [ ] Welcome banner shows on load

## Smoke Test
1. Load canvas3 set
2. Third column shows terminal with `canvas>` prompt
3. Type a message — it routes to the AI provider
4. AI response with `to_ir` mutations applies to the canvas

## Constraints
- Only change `eggs/canvas3.set.md` — no code changes needed
- Keep `chrome: false` on the pane
- Keep nodeId as `canvas-chat` for backward compat with any bus subscriptions
