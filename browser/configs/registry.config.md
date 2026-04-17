---
schema_version: 3
type: config
eggId: registry.config
name: Applet Registry
description: Central registry of all known appTypes with metadata, trust tiers, and loader paths.
author: ShiftCenter Platform Team
version: 1.0.0
---

# Applet Registry

This config EGG replaces the hardcoded APP_REGISTRY in shell.constants.js.
Adding a new platform applet = ship a new registry.config.egg. Zero shell code changes.

Field definitions:
- **appType**: Unique ID matching the node's appType field in app EGGs
- **label**: Display name shown in UI
- **icon**: Single emoji or unicode icon
- **accepts**: Array of MIME-like strings (file/*, url, text/plain, etc.)
- **trustTier**: "platform" (bundled, signed by SC) | "gc" (Global Commons, sandboxed) | "external" (third-party)
- **loaderPath**: Loader routing string. Format: "platform:{name}" for bundled, "gc://applets/{id}" for GC
- **description**: Human-readable summary
- **category**: Group label for UI organization
- **allowMultiple**: Whether multiple instances can exist simultaneously

```registry
[
  {
    "appType": "terminal",
    "label": "Terminal",
    "icon": ">_",
    "color": "var(--sd-green)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["file/*", "url", "text/plain"],
    "trustTier": "platform",
    "loaderPath": "platform:terminal",
    "description": "Integrated terminal with LLM assistance"
  },
  {
    "appType": "text-pane",
    "label": "Text Pane",
    "icon": "T",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["text/plain", "file/*.md", "file/*.txt"],
    "trustTier": "platform",
    "loaderPath": "platform:text-pane",
    "description": "Markdown and plain text renderer"
  },
  {
    "appType": "text-editor",
    "label": "Text Editor",
    "icon": "E",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["text/plain", "file/*.md", "file/*.txt"],
    "trustTier": "platform",
    "loaderPath": "platform:text-pane",
    "description": "Alias for text-pane (backward compat)"
  },
  {
    "appType": "text",
    "label": "Text",
    "icon": "T",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["text/plain", "file/*.md", "file/*.txt"],
    "trustTier": "platform",
    "loaderPath": "platform:text-pane",
    "description": "Alias for text-pane (code.egg.md uses 'text')"
  },
  {
    "appType": "tree-browser",
    "label": "Tree Browser",
    "icon": "T",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["file/*"],
    "trustTier": "platform",
    "loaderPath": "platform:tree-browser",
    "description": "Hierarchical tree view for navigation"
  },
  {
    "appType": "drawing-canvas",
    "label": "Drawing Canvas",
    "icon": "D",
    "color": "var(--sd-green)",
    "category": "Education",
    "allowMultiple": true,
    "accepts": ["text"],
    "trustTier": "platform",
    "loaderPath": "platform:drawing-canvas",
    "description": "Turtle graphics drawing surface"
  },
  {
    "appType": "canvas",
    "label": "Canvas",
    "icon": "C",
    "color": "var(--sd-purple)",
    "category": "SimDecisions",
    "allowMultiple": true,
    "accepts": ["file/ir.json", "file/bpmn", "event-ledger-entry", "url"],
    "trustTier": "platform",
    "loaderPath": "platform:canvas",
    "description": "PHASE-IR canvas for process design"
  },
  {
    "appType": "kanban",
    "label": "Kanban",
    "icon": "K",
    "color": "var(--sd-orange)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:kanban",
    "description": "Kanban board for task management"
  },
  {
    "appType": "progress",
    "label": "Progress",
    "icon": "P",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:progress",
    "description": "Progress tracking display"
  },
  {
    "appType": "build-monitor",
    "label": "Build Monitor",
    "icon": "B",
    "color": "var(--sd-orange)",
    "category": "DevOps",
    "allowMultiple": true,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:build-monitor",
    "description": "CI/CD build status monitor"
  },
  {
    "appType": "build-data-service",
    "label": "Build Data Service",
    "icon": "D",
    "color": "var(--sd-orange)",
    "category": "DevOps",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:build-data-service",
    "description": "Background service for build data fetching"
  },
  {
    "appType": "apps-home",
    "label": "Apps Home",
    "icon": "H",
    "color": "var(--sd-purple)",
    "category": "Core",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:apps-home",
    "description": "Application launcher and home screen"
  },
  {
    "appType": "sidebar",
    "label": "Sidebar",
    "icon": "S",
    "color": "var(--sd-purple)",
    "category": "Core",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:sidebar",
    "description": "Activity bar with switchable panels"
  },
  {
    "appType": "git-panel",
    "label": "Git Panel",
    "icon": "G",
    "color": "var(--sd-green)",
    "category": "DevOps",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:git-panel",
    "description": "Git version control integration"
  },
  {
    "appType": "auth",
    "label": "Auth",
    "icon": "A",
    "color": "var(--sd-red)",
    "category": "Core",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:auth",
    "description": "Authentication and login adapter"
  },
  {
    "appType": "sim",
    "label": "Sim",
    "icon": "S",
    "color": "var(--sd-purple)",
    "category": "SimDecisions",
    "allowMultiple": true,
    "accepts": ["file/ir.json", "file/bpmn"],
    "trustTier": "platform",
    "loaderPath": "platform:sim",
    "description": "SimDecisions simulation runner"
  },
  {
    "appType": "settings",
    "label": "Settings",
    "icon": "S",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": false,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:settings",
    "description": "User settings panel"
  },
  {
    "appType": "efemera",
    "label": "Efemera Chat",
    "icon": "E",
    "color": "var(--sd-cyan)",
    "category": "Communication",
    "allowMultiple": true,
    "accepts": ["file/*", "url", "text/plain", "image/*"],
    "trustTier": "platform",
    "loaderPath": "platform:efemera",
    "description": "Conversational AI with memory and context"
  },
  {
    "appType": "governance-dashboard",
    "label": "Governance",
    "icon": "G",
    "color": "var(--sd-red)",
    "category": "Governance",
    "allowMultiple": true,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:governance-dashboard",
    "description": "Governance proxy status and controls"
  },
  {
    "appType": "event-ledger",
    "label": "Event Ledger",
    "icon": "L",
    "color": "var(--sd-purple)",
    "category": "Governance",
    "allowMultiple": true,
    "accepts": ["event-ledger-entry"],
    "trustTier": "platform",
    "loaderPath": "platform:event-ledger",
    "description": "System event log and audit trail"
  },
  {
    "appType": "four-vector",
    "label": "Four-Vector",
    "icon": "4",
    "color": "var(--sd-cyan)",
    "category": "Governance",
    "allowMultiple": true,
    "accepts": [],
    "trustTier": "platform",
    "loaderPath": "platform:four-vector",
    "description": "Clock, Cost, Carbon, Capability tracking"
  },
  {
    "appType": "webpage",
    "label": "Web Page",
    "icon": "W",
    "color": "var(--sd-cyan)",
    "category": "Core",
    "allowMultiple": true,
    "accepts": ["url"],
    "trustTier": "platform",
    "loaderPath": "platform:webpage",
    "description": "Embedded web browser pane"
  }
]
```
