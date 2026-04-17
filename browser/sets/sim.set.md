---
egg: sim
version: 1.0.0
schema_version: 3
displayName: SimDecisions Flow Designer
description: Visual BPMN flow designer with DES simulation engine. Design, simulate, playback, tabletop, compare.
author: daaaave-atx
favicon: /icons/sim.svg
defaultRoute: /sim
_stub: false
auth: required
---

# SimDecisions Flow Designer v1

Interactive flow designer for BPMN diagrams with Discrete Event Simulation (DES) capabilities.

Features:
- **Design Mode**: Drag-and-drop node palette, connectors, property panels
- **Simulate Mode**: Run discrete event simulations with configurable parameters
- **Playback Mode**: Step through simulation results frame-by-frame
- **Tabletop Mode**: Collaborative tabletop simulation interface
- **Compare Mode**: Side-by-side comparison of simulation branches

Layout: menu-bar (30px) + sim pane (1fr) + status-bar (24px).

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["30px", "1fr", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-menu",
      "appType": "menu-bar",
      "label": "Menu",
      "seamless": true,
      "config": {}
    },
    {
      "type": "pane",
      "appType": "sim",
      "nodeId": "sim-designer",
      "label": "SimDecisions",
      "chrome": false
    },
    {
      "type": "pane",
      "nodeId": "chrome-status",
      "appType": "status-bar",
      "label": "Status",
      "seamless": true,
      "config": {
        "currencies": ["clock", "coin", "carbon"],
        "showConnection": true
      }
    }
  ]
}
```

```modes
{}
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
  { "id": "tab-sim", "eggId": "sim", "label": "SimDecisions", "icon": "🎬", "active": true }
]
```

```commands
[]
```

```prompt
You are a SimDecisions flow design assistant.
```

```settings
{}
```

```away
{
  "idleThresholdMs": 600000,
  "blackoutDelayMs": 300000,
  "message":         "Flow is safe. Come back when ready.",
  "showFavicon":     true,
  "welcomeBack":     true
}
```

```startup
{
  "sessionRestore": false,
  "defaultDocuments": []
}
```
