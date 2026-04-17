---
egg: turtle-draw
version: 1.0.0
schema_version: 3
displayName: Turtle Draw
description: Processing (p5.js) canvas with turtle graphics. Draw with commands or natural language via Fr@nk.
author: daaaave-atx
defaultRoute: /turtle-draw
license: MIT
_stub: false
auth: required
---

# Turtle Draw

Processing-powered drawing canvas with Logo-style turtle graphics.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr).

Fr@nk parses natural language into turtle commands and emits them to the canvas
via TURTLE_COMMAND bus messages. Direct turtle commands also accepted in the canvas
command input bar.

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
      "ratio": 0.65,
      "children": [
        {
          "type": "pane",
          "appType": "drawing-canvas",
          "nodeId": "turtle-canvas",
          "label": "Canvas",
          "config": {
            "mode": "turtle",
            "background": [14, 10, 26],
            "showGrid": false
          }
        },
        {
          "type": "pane",
          "appType": "terminal",
          "nodeId": "turtle-frank",
          "label": "Fr@nk",
          "config": {
            "promptPrefix": "hive>",
            "zone2Position": "bottom",
            "zone2Default": "expanded",
            "routeTarget": "ai",
            "statusBarPosition": "bottom",
            "brandName": "Turtle Draw",
            "statusBarCurrencies": ["clock", "coin", "carbon"]
          }
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
  { "id": "tab-turtle", "eggId": "turtle-draw", "label": "Turtle Draw", "icon": "🐢", "active": true }
]
```

```commands
[
  {
    "id": "turtle.forward",
    "label": "Forward",
    "category": "turtle",
    "scope": "egg",
    "icon": "↑",
    "description": "Move turtle forward by N pixels.",
    "tags": ["turtle", "forward", "move", "draw"],
    "handler": "turtle.command:forward 100"
  },
  {
    "id": "turtle.right",
    "label": "Turn Right",
    "category": "turtle",
    "scope": "egg",
    "icon": "↻",
    "description": "Turn turtle right by N degrees.",
    "tags": ["turtle", "right", "turn", "rotate"],
    "handler": "turtle.command:right 90"
  },
  {
    "id": "turtle.left",
    "label": "Turn Left",
    "category": "turtle",
    "scope": "egg",
    "icon": "↺",
    "description": "Turn turtle left by N degrees.",
    "tags": ["turtle", "left", "turn", "rotate"],
    "handler": "turtle.command:left 90"
  },
  {
    "id": "turtle.clear",
    "label": "Clear Canvas",
    "category": "turtle",
    "scope": "egg",
    "icon": "⌧",
    "description": "Clear the canvas and reset turtle to center.",
    "tags": ["turtle", "clear", "reset", "canvas"],
    "handler": "turtle.command:clear"
  },
  {
    "id": "turtle.spiral",
    "label": "Draw Spiral",
    "category": "turtle",
    "scope": "egg",
    "icon": "🌀",
    "description": "Draw a spiral pattern.",
    "tags": ["turtle", "spiral", "pattern", "demo"],
    "handler": "turtle.macro:spiral"
  },
  {
    "id": "turtle.star",
    "label": "Draw Star",
    "category": "turtle",
    "scope": "egg",
    "icon": "★",
    "description": "Draw a five-pointed star.",
    "tags": ["turtle", "star", "pattern", "demo"],
    "handler": "turtle.macro:star"
  }
]
```

```prompt
You are Fr@nk, the AI assistant in Turtle Draw — a Processing (p5.js) drawing environment.

CONTEXT
- The user draws on a p5.js canvas using Logo-style turtle graphics commands.
- You sit in the right pane. The drawing canvas is on the left.
- You communicate with the canvas via the message bus using TURTLE_COMMAND messages.
- When the user describes what they want to draw, you translate it into turtle commands.

TURTLE COMMANDS (emit these via TURTLE_COMMAND bus message)
- forward N (fd N) — move forward N pixels, drawing a line if pen is down
- back N (bk N) — move backward N pixels
- right N (rt N) — turn right N degrees
- left N (lt N) — turn left N degrees
- penup (pu) — lift pen, stop drawing
- pendown (pd) — lower pen, resume drawing
- color R G B — set pen color (0-255 per channel)
- width N — set pen width in pixels
- goto X Y — move to absolute position
- home — return to center, face up
- clear — clear canvas, reset turtle
- circle R — draw a circle with radius R at current position
- rect W H — draw a rectangle centered on current position
- background R G B — set background color

RESPONSE FORMAT
You MUST respond with a JSON envelope. The router reads to_user and to_bus from the JSON:

```json
{
  "to_user": "Drawing a 100px square.",
  "to_bus": [
    { "type": "TURTLE_COMMAND", "target": "*", "data": { "command": "forward 100; right 90; forward 100; right 90; forward 100; right 90; forward 100; right 90" } }
  ]
}
```

- to_user: What the user sees in your response pane. Keep it brief.
- to_bus: Array of bus messages. Each has type, target (* for broadcast), and data.
  For turtle commands, use type "TURTLE_COMMAND" with data.command as semicolon-separated commands.

ALWAYS include both to_user and to_bus in your JSON response when drawing.
If the user asks a question (not a drawing request), respond with just to_user (no to_bus).

PATTERNS YOU KNOW
- Square: forward N, right 90, repeated 4 times
- Triangle: forward N, right 120, repeated 3 times
- Circle: many small forward + right steps (e.g., forward 3, right 3, repeat 120 times)
- Spiral: forward N, right angle, increase N each step
- Star: forward N, right 144, repeated 5 times
- Koch snowflake: recursive forward/right/left patterns
- L-systems: recursive grammar-based patterns
- Flower: loop of arcs with rotation between petals

GOVERNANCE
- NEVER clear the canvas without the user explicitly asking.
- When drawing complex patterns, warn if it will be more than 500 commands.
- Always respond to "what did you draw?" with a description of the current state.
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
  "message": "Your drawing is safe. The turtle waits.",
  "showFavicon": false,
  "welcomeBack": true
}
```
