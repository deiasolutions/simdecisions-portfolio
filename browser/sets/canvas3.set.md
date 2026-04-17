---
egg: canvas3
version: 0.1.0
schema_version: 3
displayName: SimDecisions Canvas 3
description: Visual diagramming and design — new chrome layout with top-bar, menu-bar, status-bar. Triple-split main: palette+properties | canvas | chat.
author: daaaave-atx
favicon: /icons/canvas.svg
defaultRoute: /canvas3
license: MIT
_stub: false
auth: required
---

# SimDecisions Canvas 3

New chrome layout with top-bar (36px) + menu-bar (30px) + status-bar (24px) + main split (1fr).
Main split: sidebar with palette+properties (20%) | canvas sim (55%) | chat output + terminal input (25%).

```layout
{
  "type": "split",
  "direction": "horizontal",
  "ratio": ["36px", "30px", "1fr", "24px"],
  "children": [
    {
      "type": "pane",
      "nodeId": "chrome-top",
      "appType": "top-bar",
      "label": "Top",
      "seamless": true,
      "config": {
        "appName": "Canvas",
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
      "ratio": [0.20, 0.55, 0.25],
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
              {
                "id": "design",
                "icon": "\u270f",
                "label": "Components",
                "appType": "tree-browser",
                "config": {
                  "adapter": "palette",
                  "header": "Components",
                  "searchPlaceholder": "Find component..."
                }
              },
              {
                "id": "properties",
                "icon": "\u2699",
                "label": "Properties",
                "appType": "tree-browser",
                "config": {
                  "adapter": "properties",
                  "header": "Properties"
                }
              }
            ],
            "footerPanels": [],
            "defaultPanel": "design",
            "activityBarWidth": 48,
            "panelWidth": 240,
            "hideHeader": true,
            "hideActivityBar": true
          }
        },
        {
          "type": "pane",
          "nodeId": "canvas-editor",
          "appType": "sim",
          "label": "Canvas",
          "chrome": false,
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
          "ratio": [0.85, 0.15],
          "children": [
            {
              "type": "pane",
              "nodeId": "canvas-output",
              "appType": "text-pane",
              "label": "Fr@nk",
              "chrome": false,
              "config": {
                "format": "markdown",
                "readOnly": true,
                "renderMode": "chat"
              }
            },
            {
              "type": "pane",
              "nodeId": "canvas-chat",
              "appType": "terminal",
              "label": "Input",
              "chrome": false,
              "config": {
                "promptPrefix": "canvas>",
                "routeTarget": "ai",
                "brandName": "SimDecisions",
                "welcomeBanner": false,
                "displayMode": "minimal",
                "links": {
                  "to_text": "canvas-output",
                  "to_ir": "canvas-editor"
                }
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
  ],
  "slideover": [
    {
      "type": "pane",
      "nodeId": "settings-panel",
      "appType": "settings",
      "label": "Settings",
      "chrome": false,
      "config": {},
      "slideoverMeta": {
        "edge": "left",
        "width": "400px",
        "trigger": "settings",
        "dockable": false,
        "defaultDocked": false,
        "minDockWidth": 768
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

```commands
[
  {
    "id": "canvas.new-diagram",
    "label": "New Diagram",
    "category": "app",
    "defaultShortcut": "Ctrl+N",
    "scope": "egg",
    "icon": "\ud83d\udccb",
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
    "icon": "\ud83d\udcbe",
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
    "icon": "\ud83d\udce4",
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
    "icon": "\ud83c\udfa8",
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
    "icon": "\u2699\ufe0f",
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
    "icon": "\ud83d\udd0d",
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
    "canvas:node-created", "canvas:node-updated", "canvas:node-deleted",
    "canvas:node-selected", "canvas:node-deselected", "canvas:ir-generated",
    "palette:node-drag-start", "palette:node-drag-end", "palette:node-add",
    "palette:tool-select", "palette:action",
    "properties:node-edited", "properties:value-changed",
    "terminal:ir-deposit", "sim:mode-change", "sim:mode-updated",
    "sim:branches-updated", "sim:branch-select",
    "toolbar:actions-changed", "toolbar:action-invoked"
  ],
  "bus_receive": [
    "canvas:node-created", "canvas:node-updated", "canvas:node-deleted",
    "canvas:node-selected", "canvas:node-deselected", "canvas:ir-generated",
    "palette:node-drag-start", "palette:node-drag-end", "palette:node-add",
    "palette:tool-select", "palette:action",
    "properties:node-edited", "properties:value-changed",
    "terminal:ir-deposit", "terminal:text-patch",
    "sim:mode-change", "sim:mode-updated",
    "sim:branches-updated", "sim:branch-select",
    "toolbar:actions-changed", "toolbar:action-invoked"
  ]
}
```

```prompt
You are a canvas assistant for SimDecisions. You control a visual flow diagram.

HARD RULE: Your ENTIRE response must be a single JSON object. No text before it. No text after it. No markdown fences. Just the JSON object. Every single response, no exceptions.

The JSON object always has "to_user" (required string). It optionally has "to_ir" (array of mutations).

OVERRIDE: The envelope dialect's to_ir format does NOT apply here. In this EGG, to_ir is ALWAYS a mutation array, never a PHASE-IR v2.0 object.

## When the user wants diagram changes

Return to_ir with an array of mutations:

{"to_user":"Added Review node and connected it to Start.","to_ir":[{"action":"add_node","nodeData":{"id":"n1","name":"Review Application","node_type":"process","description":"Review the submitted application","pos":{"x":300,"y":200}}},{"action":"add_edge","source":"start","target":"n1","label":"submit"}]}

## When the user asks a question (no diagram changes needed)

Return only to_user:

{"to_user":"Process nodes represent work activities. They have timing, resources, and guard conditions."}

## When you don't know how to handle the request

Return an unsupported mutation so we can see what was requested:

{"to_user":"I don't have a canvas action for that yet.","to_ir":[{"action":"unsupported","description":"User asked to: clear the canvas. No clear_all action exists.","original_request":"clear the canvas"}]}

## Mutation actions

- add_node — nodeData: {id, name, node_type, pos:{x,y}, description?, icon?, timing?, resources?, guards?, actions?, oracle?}
- add_edge — source, target, label?, condition?, edge_type? (default|conditional|exception|timeout)
- update_node — nodeId, updates (partial fields to merge)
- delete_node — nodeId
- delete_edge — edgeId
- unsupported — description, original_request (for requests you can't map to an action)

Valid node_type: process, decision, checkpoint, resource, start, end, split, join, queue, group, annotation.

## Examples

User: "add a review step"
{"to_user":"Added Review step.","to_ir":[{"action":"add_node","nodeData":{"id":"review-1","name":"Review","node_type":"process","pos":{"x":300,"y":200}}}]}

User: "connect review to approval"
{"to_user":"Connected Review to Approval.","to_ir":[{"action":"add_edge","source":"review-1","target":"approval-1"}]}

User: "what is a checkpoint?"
{"to_user":"A checkpoint node marks a milestone in the process. Tokens pause there until a condition is met or a manual release occurs."}

User: "undo the last change"
{"to_user":"I don't have a canvas action for undo yet.","to_ir":[{"action":"unsupported","description":"User wants to undo last mutation. No undo action exists in the mutation protocol.","original_request":"undo the last change"}]}

User: "clear everything"
{"to_user":"I don't have a clear-all action yet.","to_ir":[{"action":"unsupported","description":"User wants to clear all nodes and edges. No clear_all action exists.","original_request":"clear everything"}]}
```
