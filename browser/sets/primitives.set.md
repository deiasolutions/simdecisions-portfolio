---
egg: primitives
version: 1.0.0
schema_version: 3
displayName: Primitives Catalog
description: Showcases every primitive in the system. Tree browser with live CSS-scaled frame previews, full-size preview pane, and compose terminal.
author: daaaave-atx
favicon: /icons/primitives.svg
defaultRoute: /primitives
license: MIT
_stub: false
auth: required
---

# Primitives Catalog EGG

Browse every primitive, applet, and app in the system. The tree on the left shows each component with a live CSS-scaled mini frame. Click to see a full-size live instance in the preview pane. Compose terminal at the bottom for interaction.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr).

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
      "ratio": 0.35,
      "children": [
        {
          "type": "pane",
          "appType": "tree-browser",
          "nodeId": "prim-nav",
          "label": "Primitives",
          "chrome": false,
          "config": {
            "adapter": "primitives",
            "renderMode": "frames",
            "header": "Primitives",
            "searchPlaceholder": "Find primitive..."
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
              "appType": "primitive-preview",
              "nodeId": "prim-detail",
              "label": "Preview",
              "chrome": false,
              "config": {}
            },
            {
              "type": "pane",
              "appType": "terminal",
              "nodeId": "prim-compose",
              "label": "Compose",
              "chrome": false,
              "config": {
                "routeTarget": "shell",
                "promptPrefix": "demo>",
                "zone2Position": "hidden",
                "statusBarPosition": "bottom",
                "brandName": "Primitives",
                "links": {
                  "to_preview": "prim-detail"
                }
              }
            }
          ]
        }
      ]
    }
  ]
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
  { "id": "tab-primitives", "eggId": "primitives", "label": "Primitives", "active": true }
]
```

```commands
[
  {
    "id": "primitives.search",
    "label": "Search Primitives",
    "category": "view",
    "defaultShortcut": "Ctrl+K",
    "scope": "egg",
    "icon": "\uD83D\uDD0D",
    "description": "Focus the primitive search input.",
    "tags": ["search", "find", "primitive"],
    "handler": "primitives.focusSearch"
  }
]
```

```settings
{
  "showFramePreviews": true,
  "defaultCategory": "primitive"
}
```

```away
{
  "idleThresholdMs": 600000,
  "blackoutDelayMs": 900000,
  "message": "Away from catalog",
  "showFavicon": false,
  "welcomeBack": false
}
```

```permissions
{
  "storage": { "localStorage": true, "sessionStorage": true },
  "network": { "allowedDomains": ["localhost", "hivenode.railway.app"] },
  "bus_emit": [
    "primitive:selected",
    "primitive:deselected",
    "primitive:preview-mounted"
  ],
  "bus_receive": [
    "primitive:selected",
    "primitive:deselected",
    "primitive:preview-mounted"
  ]
}
```
