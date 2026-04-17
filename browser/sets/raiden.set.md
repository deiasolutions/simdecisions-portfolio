---
egg: raiden
version: 1.0.0
schema_version: 3
displayName: Raiden
description: Raiden shmup arcade game. Mobile-first, full-viewport.
defaultRoute: /raiden
_stub: false
auth: public
---

# Raiden Game Set

Mobile-first arcade shooter game. Full-viewport, no chrome, no shell UI.

Layout: Single pane, iframe wrapper, no top-bar, no menu-bar. The game handles its own UI, viewport, and touch controls.

```layout
{
  "type": "pane",
  "nodeId": "raiden-game",
  "appType": "iframe-pane",
  "label": "Raiden",
  "chrome": false,
  "seamless": true,
  "config": {
    "src": "/games/raiden-v1-20260413.html",
    "sandbox": "allow-scripts allow-same-origin",
    "allow": "autoplay"
  }
}
```

```ui
{
  "chromeMode": "none",
  "commandPalette": false,
  "akk": false
}
```

```tabs
[]
```

```commands
[]
```

```settings
{}
```
