---
egg: flappy
version: 1.0.0
schema_version: 3
displayName: "Flappy Bird AI"
description: "Flappy Bird with NEAT neural network AI — evolution-based gameplay."
author: "DEIA Solutions"
favicon: /icons/hodeia.svg
defaultRoute: /flappy
auth: public
---

# Flappy Bird AI EGG

Full-screen Flappy Bird game with NEAT (NeuroEvolution of Augmenting Topologies) AI. Watch neural networks evolve to play Flappy Bird, or play manually. Mobile-responsive with touch controls.

## Layout

```layout
{
  "type": "pane",
  "nodeId": "flappy-game",
  "appType": "iframe-pane",
  "label": "Flappy Bird AI",
  "config": {
    "src": "/games/flappy-bird-ai-v2-20260407.html"
  }
}
```

## UI

```ui
{
  "chromeMode": "hidden",
  "commandPalette": false,
  "akk": false
}
```

## Startup

```startup
{
  "sessionRestore": false,
  "sessionRestoreScope": "none",
  "restoreOrder": "sessionFirst",
  "defaultDocuments": []
}
```

## Permissions

```permissions
{
  "storage": { "localStorage": true, "sessionStorage": false },
  "network": { "allowedDomains": [] }
}
```
