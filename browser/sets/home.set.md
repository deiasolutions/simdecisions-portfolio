---
egg: home
version: 0.1.0
schema_version: 3
displayName: ShiftCenter
description: Default home layout.
defaultRoute: /home
_stub: true
auth: public
---

# Home EGG

Default home landing page. Stub — applet not yet implemented (BL-106).

Layout: top-bar (36px) + menu-bar (30px) + home pane (1fr).

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
      "type": "pane",
      "appType": "home",
      "nodeId": "home-main",
      "label": "Home",
      "config": {}
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
[]
```

```commands
[]
```
