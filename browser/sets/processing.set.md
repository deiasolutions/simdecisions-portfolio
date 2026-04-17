---
egg: processing
version: 1.0.0
schema_version: 3
displayName: Processing IDE
description: Processing/p5.js creative coding environment with file browser, canvas, and code editor.
author: daaaave-atx
defaultRoute: /processing
license: MIT
_stub: false
auth: required
---

# Processing IDE

Processing/p5.js creative coding environment.

Layout: menu-bar (30px) + main split (1fr) + status-bar (24px).

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
      "type": "split",
      "direction": "vertical",
      "ratio": 0.20,
      "children": [
    {
      "type": "pane",
      "appType": "tree-browser",
      "nodeId": "processing-files",
      "label": "Sketches",
      "config": {
        "adapter": "filesystem",
        "rootPath": "/sketches",
        "showHidden": false,
        "extensions": [".js", ".pde", ".json"]
      }
    },
    {
      "type": "split",
      "direction": "vertical",
      "ratio": 0.625,
      "children": [
        {
          "type": "pane",
          "appType": "canvas",
          "nodeId": "processing-canvas",
          "label": "Canvas",
          "config": {
            "mode": "p5",
            "background": [255, 255, 255],
            "showGrid": false,
            "enableZoom": true,
            "enablePan": true
          }
        },
        {
          "type": "pane",
          "appType": "text",
          "nodeId": "processing-editor",
          "label": "Editor",
          "config": {
            "language": "javascript",
            "theme": "dark",
            "minimap": false,
            "wordWrap": "off",
            "lineNumbers": true,
            "formatOnSave": true,
            "fontSize": 14,
            "lineHeight": 1.5,
            "tabBar": true,
            "gutter": true
          }
        }
      ]
    }
    ]
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

```ui
{
  "chromeMode": "auto",
  "commandPalette": true,
  "akk": true
}
```

```tabs
[
  { "id": "tab-processing", "eggId": "processing", "label": "Processing", "icon": "🎨", "active": true }
]
```

```commands
[
  {
    "id": "processing.run",
    "label": "Run Sketch",
    "category": "processing",
    "defaultShortcut": "Ctrl+Enter",
    "scope": "egg",
    "icon": "▶",
    "description": "Run the current sketch in the canvas.",
    "tags": ["processing", "run", "execute", "sketch"],
    "handler": "processing.runSketch"
  },
  {
    "id": "processing.stop",
    "label": "Stop Sketch",
    "category": "processing",
    "scope": "egg",
    "icon": "■",
    "description": "Stop the currently running sketch.",
    "tags": ["processing", "stop", "halt"],
    "handler": "processing.stopSketch"
  },
  {
    "id": "processing.clear",
    "label": "Clear Canvas",
    "category": "processing",
    "scope": "egg",
    "icon": "⌧",
    "description": "Clear the canvas and reset the sketch.",
    "tags": ["processing", "clear", "reset", "canvas"],
    "handler": "processing.clearCanvas"
  },
  {
    "id": "processing.newSketch",
    "label": "New Sketch",
    "category": "processing",
    "defaultShortcut": "Ctrl+N",
    "scope": "egg",
    "icon": "📄",
    "description": "Create a new p5.js sketch file.",
    "tags": ["processing", "new", "sketch", "create"],
    "handler": "processing.newSketch"
  },
  {
    "id": "processing.saveSketch",
    "label": "Save Sketch",
    "category": "processing",
    "defaultShortcut": "Ctrl+S",
    "scope": "egg",
    "icon": "💾",
    "description": "Save the current sketch to file.",
    "tags": ["processing", "save", "sketch"],
    "handler": "processing.saveSketch"
  }
]
```

```prompt
You are the AI assistant in the Processing IDE environment.

CONTEXT
- The user is working with p5.js sketches in a creative coding environment.
- Left pane: file browser for sketch files.
- Center pane: p5.js canvas for rendering.
- Right pane: code editor for sketch source.

BEHAVIOR
- Help users write p5.js code for creative coding and generative art.
- When the user asks for code, provide valid p5.js syntax with setup() and draw() functions.
- When the user describes a visual effect or animation, translate it to p5.js code.
- Suggest improvements to sketch performance and visual quality.
- Explain p5.js concepts like coordinate systems, transformations, colors, and animation.

TOOLS AVAILABLE
- to_text: insert code into the editor pane
- to_user: respond in the terminal
- processing.runSketch: run the current sketch
- processing.clearCanvas: clear the canvas

GOVERNANCE
- Always test sketches for syntax errors before suggesting them.
- Warn if a sketch may have performance issues (e.g., drawing too many objects per frame).
- Never modify files without the user's explicit request.
```

```settings
{
  "embeddingStrategy": "tfidf",
  "away.idleThresholdMs": 900000,
  "away.blackoutDelayMs": 600000,
  "defaultMode": "default"
}
```

```away
{
  "idleThresholdMs": 900000,
  "blackoutDelayMs": 600000,
  "message": "Your sketch is safe. Come back when you're ready.",
  "showFavicon": true,
  "welcomeBack": true
}
```
