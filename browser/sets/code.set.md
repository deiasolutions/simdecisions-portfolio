---
egg: code
version: 2.0.0
schema_version: 3
displayName: ShiftCenter Code
description: Browser IDE with Fr@nk AI assistant. Activity Bar, file explorer with git status, editor with tabs and line numbers, Fr@nk terminal. Three Currencies on every session.
author: daaaave-atx
favicon: global-commons://icons/code.png
defaultRoute: /code
license: MIT
_stub: false
auth: required
---

# ShiftCenter Code v2

Default EGG for code.shiftcenter.com. Matches the ShiftCenterCode.jsx mockup.

Layout: top-bar (36px) + menu-bar (30px) + main split (1fr) + status-bar (24px).
Standard chrome frame matching canvas3, chat, efemera, playground.

Content regions (all chrome-suppressed):
- Sidebar (left): Activity Bar icon strip + switchable panels (Explorer, Search, Fr@nk, Settings)
- Editor (center): SDEditor with tab bar, line number gutter, syntax highlighting
- Fr@nk Terminal (right of center): hive> prompt, conversation log

Field names use `id` (shell-native) pending SPEC-EGG-SCHEMA-v1 reconciliation.
v1.3.0 preserved as code-default.v1.egg.md.

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
        "appName": "Code",
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
      "ratio": 0.20,
      "children": [
        {
          "type": "pane",
          "appType": "sidebar",
          "nodeId": "code-sidebar",
          "label": "Sidebar",
          "chrome": false,
          "config": {
            "panels": [
              { "id": "explorer", "icon": "📁", "label": "Explorer",  "appType": "file-explorer" },
              { "id": "search",   "icon": "🔍", "label": "Search",    "appType": "search" },
              { "id": "frank",    "icon": "◐",  "label": "Fr@nk",     "appType": "frank-sidebar" }
            ],
            "footerPanels": [
              { "id": "settings", "icon": "⚙", "label": "Settings" }
            ],
            "defaultPanel": "explorer",
            "activityBarWidth": 48,
            "panelWidth": 240,
            "adapter": "filesystem",
            "showGitStatus": true,
            "showBranchBadge": true
          }
        },
        {
          "type": "split",
          "direction": "horizontal",
          "ratio": 0.70,
          "children": [
            {
              "type": "pane",
              "appType": "text",
              "nodeId": "code-editor",
              "label": "Editor",
              "chrome": false,
              "config": {
                "hideHeader":              true,
                "language":                "auto",
                "theme":                   "dark",
                "minimap":                 true,
                "wordWrap":                "off",
                "lineNumbers":             true,
                "bracketPairColorization": true,
                "formatOnSave":            false,
                "padding":                 { "top": 16, "bottom": 16 },
                "fontSize":                14,
                "lineHeight":              1.5,
                "cursorBlinking":          "blink",
                "cursorStyle":             "block",
                "renderLineHighlight":     "line",
                "scrollBeyondLastLine":    true,
                "overviewRulerLanes":      3,
                "tabBar":                  true,
                "gutter":                  true
              }
            },
            {
              "type": "pane",
              "appType": "terminal",
              "nodeId": "code-frank",
              "label": "Fr@nk",
              "chrome": false,
              "config": {
                "zone2Dock":     "right",
                "welcomeBanner": true,
                "prompt":        "code",
                "collapsed":     false,
                "headerLabel":   "Fr@nk",
                "headerPrompt":  "hive>",
                "showStatus":    true
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

```modes
{
  "zen": {
    "label":       "Zen",
    "icon":        "🧘",
    "shortcut":    "Ctrl+K Z",
    "exitShortcut":"Escape",
    "indicator":   "tab-corner",
    "ui": {
      "hideTopBar":          true,
      "hideMenuBar":         true,
      "hideStatusBar":       true,
      "commandPalette":      true,
      "viewMenu":            false,
      "statusBarCurrencies": []
    },
    "nodes": {
      "code-editor": {
        "minimap":              false,
        "wordWrap":             "on",
        "lineNumbers":          false,
        "padding":              { "top": 48, "bottom": 48 },
        "fontSize":             16,
        "lineHeight":           1.8,
        "cursorBlinking":       "smooth",
        "cursorStyle":          "line",
        "renderLineHighlight":  "none",
        "scrollBeyondLastLine": false,
        "overviewRulerLanes":   0
      },
      "code-frank": {
        "collapsed":     true,
        "welcomeBanner": false,
        "prompt":        "zen"
      },
      "code-sidebar": { "hidden": true }
    },
    "frankBehavior": {
      "silentMode":   true,
      "panelDefault": "collapsed",
      "contextScope": "selection"
    },
    "away": {
      "idleThresholdMs": 900000,
      "blackoutDelayMs": 600000,
      "message":         "Still here. Your work is safe.",
      "welcomeBack":     false
    }
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
  { "id": "tab-code", "eggId": "code", "label": "Code", "icon": "⌨️", "active": true }
]
```

```commands
[
  {
    "id":             "sidebar.toggle",
    "label":          "Toggle Sidebar",
    "category":       "view",
    "defaultShortcut":"Ctrl+B",
    "scope":          "global",
    "icon":           "📁",
    "description":    "Show or hide the sidebar panel.",
    "tags":           ["sidebar", "panel", "explorer", "toggle"],
    "handler":        "applets.sidebar.toggle"
  },
  {
    "id":             "sidebar.explorer",
    "label":          "Show Explorer",
    "category":       "view",
    "defaultShortcut":"Ctrl+Shift+E",
    "scope":          "global",
    "icon":           "📁",
    "description":    "Switch sidebar to the file explorer panel.",
    "tags":           ["explorer", "files", "tree", "sidebar"],
    "handler":        "applets.sidebar.showPanel:explorer"
  },
{
    "id":             "sidebar.search",
    "label":          "Show Search",
    "category":       "view",
    "defaultShortcut":"Ctrl+Shift+F",
    "scope":          "global",
    "icon":           "🔍",
    "description":    "Switch sidebar to the search panel.",
    "tags":           ["search", "find", "sidebar"],
    "handler":        "applets.sidebar.showPanel:search"
  },
  {
    "id":             "sidebar.frank",
    "label":          "Show Fr@nk Panel",
    "category":       "view",
    "defaultShortcut":"Ctrl+Shift+A",
    "scope":          "global",
    "icon":           "◐",
    "description":    "Switch sidebar to the Fr@nk assistant panel.",
    "tags":           ["frank", "assistant", "sidebar"],
    "handler":        "applets.sidebar.showPanel:frank"
  },
  {
    "id":             "code.run",
    "label":          "Run Current File",
    "category":       "app",
    "defaultShortcut":"Ctrl+F5",
    "scope":          "pane",
    "icon":           "▶",
    "description":    "Run the active file in the Fr@nk terminal.",
    "tags":           ["run", "execute", "play", "file"],
    "handler":        "applets.terminal.runActive:code-frank"
  },
  {
    "id":             "code.format",
    "label":          "Format Document",
    "category":       "app",
    "defaultShortcut":"Shift+Alt+F",
    "scope":          "pane",
    "icon":           "≡",
    "description":    "Auto-format the active file via Fr@nk.",
    "tags":           ["format", "prettier", "lint", "tidy"],
    "handler":        "applets.text.formatDocument"
  },
  {
    "id":             "code.frank.explain",
    "label":          "Fr@nk: Explain Selection",
    "category":       "frank",
    "defaultShortcut":"Ctrl+Shift+/",
    "scope":          "pane",
    "icon":           "?",
    "description":    "Ask Fr@nk to explain the currently selected code.",
    "tags":           ["frank", "explain", "help", "understand"],
    "handler":        "frank.explainSelection"
  },
  {
    "id":             "code.frank.refactor",
    "label":          "Fr@nk: Refactor Selection",
    "category":       "frank",
    "defaultShortcut":"Ctrl+Shift+R",
    "scope":          "pane",
    "icon":           "↻",
    "description":    "Ask Fr@nk to refactor the selected code block.",
    "tags":           ["frank", "refactor", "improve", "rewrite"],
    "handler":        "frank.refactorSelection"
  },
  {
    "id":             "code.frank.test",
    "label":          "Fr@nk: Write Tests",
    "category":       "frank",
    "defaultShortcut":"Ctrl+Shift+T",
    "scope":          "pane",
    "icon":           "✓",
    "description":    "Ask Fr@nk to generate tests for the active file or selection.",
    "tags":           ["frank", "test", "jest", "pytest", "unit test"],
    "handler":        "frank.generateTests"
  },
  {
    "id":             "frank.toggle",
    "label":          "Toggle Fr@nk Terminal",
    "category":       "view",
    "defaultShortcut":"Ctrl+`",
    "scope":          "global",
    "icon":           "◐",
    "description":    "Show or hide the Fr@nk terminal pane.",
    "tags":           ["frank", "terminal", "toggle", "hive"],
    "handler":        "applets.terminal.toggle:code-frank"
  },
  {
    "id":             "mode.zen.enter",
    "label":          "Enter Zen Mode",
    "category":       "view",
    "defaultShortcut":"Ctrl+K Z",
    "scope":          "global",
    "icon":           "🧘",
    "description":    "Focus mode — full screen editor, all panels hidden, Fr@nk silent.",
    "tags":           ["zen", "focus", "distraction-free", "full screen", "mode"],
    "handler":        "shell.mode.enter:zen"
  },
  {
    "id":             "mode.zen.exit",
    "label":          "Exit Zen Mode",
    "category":       "view",
    "defaultShortcut":"Escape",
    "scope":          "global",
    "icon":           "⌨️",
    "description":    "Return to full IDE layout.",
    "tags":           ["zen", "exit", "back", "mode"],
    "handler":        "shell.mode.exit"
  }
]
```

```prompt
You are Fr@nk, the AI coding assistant in ShiftCenter Code.

CONTEXT
- You have access to the open file tree (GitHub-backed), the active editor, and the terminal.
- The user may address you by typing in the hive> terminal or via Ctrl+Shift+/ on a selection.
- You can see the active file, selected text, and git status.
- You are aware of the current mode (default or zen). In zen mode, be briefer.

BEHAVIOR — DEFAULT MODE
- When the user asks a code question, answer with working, runnable code.
- When the user selects code and invokes Explain, Refactor, or Write Tests — act on the selection only.
- When the user uses / commands, execute them against the active file or pane.
- Prefer inserting code directly into the editor via to_text. Narrate only when insertion is inappropriate.
- Always state which file you are editing before making changes.
- Ask for clarification before deleting or overwriting more than 20 lines.
- When suggesting a commit message, keep it under 72 characters, imperative mood.

BEHAVIOR — ZEN MODE
- Be brief. One paragraph maximum unless code is requested.
- When explaining: concise, plain English, no headers or bullets.
- When refactoring: show the diff queue only. Do not narrate unless asked.
- Never open the Fr@nk panel unprompted. Never send unsolicited suggestions.
- If the user says nothing, stay silent. Clock runs. You wait.

TOOLS AVAILABLE
- to_text: insert content into the focused editor pane
- to_user: respond in Zone 2 (the response pane)
- git_panel: read branch, diff, and commit history
- run_file: execute the active file in the terminal
- format: auto-format the active file

GOVERNANCE
- REQUIRE_HUMAN before any destructive file operation (delete, overwrite entire file).
- REQUIRE_HUMAN before any git push to main or master.
- Never execute shell commands not explicitly requested by the user.
- Log all file modifications to the Event Ledger with project_tag.
```

```settings
{
  "coAuthorEnabled":        true,
  "acceptEditsOn":          false,
  "embeddingStrategy":      "voyage",
  "rejectFeedbackEnabled":  true,
  "away.idleThresholdMs":   600000,
  "away.blackoutDelayMs":   300000,
  "clock.autoStart":        true,
  "coin.trackPerFile":      true,
  "carbon.trackPerCall":    true,
  "git.confirmBeforePush":  true,
  "git.requireHumanOnMain": true,
  "frank.contextScope":     "file",
  "frank.insertMode":       "diff-queue",
  "defaultMode":            "default"
}
```

```away
{
  "idleThresholdMs": 600000,
  "blackoutDelayMs": 300000,
  "message":         "Code is safe. Come back when you're ready.",
  "showFavicon":     true,
  "faviconPosition": "center",
  "welcomeBack":     true
}
```

```startup
{
  "sessionRestore": true,
  "sessionRestoreScope": "perUser",

  "defaultDocuments": [
    {
      "nodeId":   "code-editor",
      "src":      "global-commons://docs/shiftcenter-code-readme.md",
      "label":    "Welcome to ShiftCenter Code",
      "position": "first",
      "pinned":   false,
      "condition":"firstTabAlways"
    }
  ],

  "restoreOrder": "readmeFirst"
}
```
