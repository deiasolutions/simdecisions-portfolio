---
egg: canvas
version: 1.0.1
schema_version: 3
displayName: SimDecisions Canvas
description: Visual diagramming and design — palette sidebar, canvas editor, IR generation terminal, properties sidebar. Drag components, edit IR, real-time sync. Mode-specific panels (sim-config-panel, sim-progress-panel, playback-controls) available as shell panes.
author: daaaave-atx
favicon: /icons/canvas.svg
defaultRoute: /canvas
license: MIT
_stub: false
auth: required
---

# SimDecisions Canvas EGG

Visual diagramming and design tool for SimDecisions IR authoring. Drag components from palette, edit on canvas, generate PHASE-IR via LLM terminal, inspect properties.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr).

Terminal IR mode: user types → LLM responds with mixed text + JSON →
chat text routes to text-pane, IR JSON blocks route to canvas.

Mode-specific panes (rendered by FlowDesigner via mode switching, not fixed in layout):
- `sim-config-panel` — Simulation configuration (replications, time horizon, seed, cost estimate). Publishes `sim:config-updated`, `sim:start`, `sim:stop`, `sim:pause`, `sim:resume` events.
- `sim-progress-panel` — Simulation progress, metrics, event log. Subscribes to `sim:progress-updated`, `sim:metrics-updated`, `sim:event`, `sim:results-available` events.
- `playback-controls` — Playback mode controls (play, pause, step, scrub, speed). Publishes `sim:playback-play`, `sim:playback-pause`, `sim:playback-step-forward`, `sim:playback-step-backward`, `sim:playback-reset`, `sim:playback-scrub`, `sim:playback-speed` events.

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": {
        "brand": "egg",
        "showCurrencyChip": true,
        "showKebab": true,
        "showAvatar": true
      }
    },
    {
      "type": "pane",
      "nodeId": "chrome-menu",
      "appType": "menu-bar",
      "label": "Menu",
      "seamless": true,
      "config": {}
    },
    {
      "type": "split",
      "direction": "vertical",
      "ratio": 0.18,
      "children": [
    {
      "type": "pane",
      "nodeId": "canvas-sidebar",
      "appType": "sidebar",
      "label": "Sidebar",
      "chrome": false,
      "minWidth": 48,
      "config": {
        "panels": [
          { "id": "design", "icon": "✏", "label": "Design",
            "action": "sim:mode-change", "actionPayload": { "mode": "design" },
            "appType": "tree-browser",
            "config": { "adapter": "palette", "header": "Components", "searchPlaceholder": "Find component..." } },
          { "id": "configure", "icon": "⚙️", "label": "Configure",
            "action": "sim:mode-change", "actionPayload": { "mode": "configure" } },
          { "id": "simulate", "icon": "▶", "label": "Simulate",
            "action": "sim:mode-change", "actionPayload": { "mode": "simulate" },
            "activeBg": "var(--sd-orange)",
            "appType": "sim-config-panel" },
          { "id": "playback", "icon": "⏮", "label": "Playback",
            "action": "sim:mode-change", "actionPayload": { "mode": "playback" } },
          { "id": "tabletop", "icon": "🎲", "label": "Tabletop",
            "action": "sim:mode-change", "actionPayload": { "mode": "tabletop" },
            "activeBg": "var(--sd-cyan)" },
          { "id": "compare", "icon": "⚖", "label": "Compare",
            "action": "sim:mode-change", "actionPayload": { "mode": "compare" } }
        ],
        "footerPanels": [
          { "id": "properties", "icon": "⚙", "label": "Properties",
            "appType": "tree-browser",
            "config": { "adapter": "properties", "header": "Properties", "searchPlaceholder": "Find property..." } },
          { "id": "branches", "icon": "🔗", "label": "Branches",
            "appType": "tree-browser",
            "config": { "adapter": "branches", "header": "Branches", "searchPlaceholder": "Find branch..." } }
        ],
        "defaultPanel": "design",
        "activityBarWidth": 40,
        "panelWidth": 220
      }
    },
    {
      "type": "split",
      "direction": "vertical",
      "ratio": 0.78,
      "children": [
        {
          "type": "pane",
          "nodeId": "canvas-editor",
          "appType": "sim",
          "label": "Canvas",
          "config": {
            "defaultMode": "design",
            "zoomEnable": true,
            "gridSnap": true,
            "links": {
              "from_palette": "canvas-sidebar",
              "to_properties": "canvas-sidebar"
            }
          }
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.93,
          "seamless": true,
          "secondChildAuto": true,
          "children": [
            {
              "type": "pane",
              "nodeId": "canvas-chat",
              "appType": "text-pane",
              "label": "Chat",
              "chrome": true,
              "chromeCollapsible": true,
              "config": {
                "format": "markdown",
                "readOnly": true,
                "renderMode": "chat"
              }
            },
            {
              "type": "pane",
              "nodeId": "canvas-ir",
              "appType": "terminal",
              "label": "IR Generator",
              "config": {
                "routeTarget": "ir",
                "promptPrefix": "ir>",
                "zone2Position": "hidden",
                "statusBarPosition": "bottom",
                "brandName": "Canvas",
                "statusBarCurrencies": ["clock", "coin", "carbon"],
                "links": {
                  "to_ir": "canvas-editor",
                  "to_text": "canvas-chat"
                }
              }
            }
          ]
        }
      ]
    }
    ]
  }
}
```

```ui
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

```tabs
[
  { "id": "tab-canvas", "eggId": "canvas", "label": "Canvas", "active": true }
]
```

```commands
[
  {
    "id": "canvas.new-diagram",
    "label": "New Diagram",
    "category": "app",
    "defaultShortcut": "Ctrl+N",
    "scope": "egg",
    "icon": "📋",
    "description": "Create a new diagram.",
    "tags": ["diagram", "new", "create"],
    "handler": "canvas.newDiagram"
  },
  {
    "id": "canvas.save",
    "label": "Save Diagram",
    "category": "app",
    "defaultShortcut": "Ctrl+S",
    "scope": "egg",
    "icon": "💾",
    "description": "Save the current diagram to PHASE-IR.",
    "tags": ["save", "diagram", "ir"],
    "handler": "canvas.saveDiagram"
  },
  {
    "id": "canvas.export-ir",
    "label": "Export PHASE-IR",
    "category": "app",
    "defaultShortcut": "Ctrl+E",
    "scope": "egg",
    "icon": "📤",
    "description": "Export current diagram as PHASE-IR JSON.",
    "tags": ["export", "ir", "json"],
    "handler": "canvas.exportIR"
  },
  {
    "id": "canvas.palette",
    "label": "Toggle Palette",
    "category": "view",
    "defaultShortcut": "Ctrl+Shift+P",
    "scope": "egg",
    "icon": "🎨",
    "description": "Show or hide the component palette.",
    "tags": ["palette", "components", "panel"],
    "handler": "canvas.togglePalette"
  },
  {
    "id": "canvas.properties",
    "label": "Toggle Properties",
    "category": "view",
    "defaultShortcut": "Ctrl+Shift+I",
    "scope": "egg",
    "icon": "⚙️",
    "description": "Show or hide the properties panel.",
    "tags": ["properties", "inspector", "panel"],
    "handler": "canvas.toggleProperties"
  },
  {
    "id": "canvas.zoom-fit",
    "label": "Fit to Screen",
    "category": "view",
    "defaultShortcut": "Ctrl+1",
    "scope": "egg",
    "icon": "🔍",
    "description": "Fit entire diagram to screen.",
    "tags": ["zoom", "fit", "view"],
    "handler": "canvas.zoomFit"
  }
]
```

```settings
{
  "gridSize": 20,
  "snapToGrid": true,
  "autoSave": true,
  "autoSaveInterval": 30000,
  "showGrid": true,
  "showGuidelines": true
}
```

```away
{
  "idleThresholdMs": 600000,
  "blackoutDelayMs": 900000,
  "message": "Away from diagram",
  "showFavicon": false,
  "welcomeBack": false
}
```

```startup
{
  "sessionRestore": true,
  "sessionRestoreScope": "perUser",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

```permissions
{
  "storage": { "localStorage": true, "sessionStorage": true },
  "network": { "allowedDomains": ["localhost", "hivenode.railway.app"] },
  "bus_emit": [
    "canvas:node-created",
    "canvas:node-updated",
    "canvas:node-deleted",
    "canvas:node-selected",
    "canvas:node-deselected",
    "canvas:ir-generated",
    "palette:node-drag-start",
    "palette:node-drag-end",
    "palette:node-add",
    "properties:node-edited",
    "properties:value-changed",
    "terminal:ir-deposit",
    "sim:mode-change",
    "sim:mode-updated",
    "sim:branches-updated",
    "sim:branch-select",
    "toolbar:actions-changed",
    "toolbar:action-invoked"
  ],
  "bus_receive": [
    "canvas:node-created",
    "canvas:node-updated",
    "canvas:node-deleted",
    "canvas:node-selected",
    "canvas:node-deselected",
    "canvas:ir-generated",
    "palette:node-drag-start",
    "palette:node-drag-end",
    "palette:node-add",
    "properties:node-edited",
    "properties:value-changed",
    "terminal:ir-deposit",
    "terminal:text-patch",
    "sim:mode-change",
    "sim:mode-updated",
    "sim:branches-updated",
    "sim:branch-select",
    "toolbar:actions-changed",
    "toolbar:action-invoked"
  ]
}
```

```prompt
You are an expert in SimDecisions system architecture and PHASE-IR mutation syntax.

When the user describes a diagram change (e.g., "add a decision node", "connect these two processes"),
generate PHASE-IR mutations and return them in the standard terminal envelope format.

**IMPORTANT: Always respond with a JSON object in this format:**

{
  "to_user": "Brief confirmation message (1-2 sentences)",
  "to_ir": [
    { "type": "insert", "path": "/diagram/nodes/0", "value": { "id": "n1", "type": "Decision", "x": 100, "y": 100 } },
    { "type": "insert", "path": "/diagram/edges/0", "value": { "id": "e1", "from": "n0", "to": "n1" } }
  ]
}

Each mutation in `to_ir` must have: type, path, value (or oldValue/newValue for edits).

If the user asks for clarification on existing diagram state, inspect the canvas app state
via /canvas/state API endpoint before generating mutations.

Always validate that mutations are syntactically correct and semantically sound before sending.
```
