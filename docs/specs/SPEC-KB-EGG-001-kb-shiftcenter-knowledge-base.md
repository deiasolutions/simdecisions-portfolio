# SPEC-KB-EGG-001: kb.shiftcenter.com — Knowledge Base EGG

**Date:** 2026-03-13
**Author:** Q88N (Dave) × Claude (Anthropic)
**Status:** SPEC — LOCKED
**Area:** EGG
**T-Shirt Size:** M
**Depends On:** EGG system (BUILT), text-pane / SDEditor (BUILT), tree-browser (BUILT),
               ADR-GC-APPLET-001 (draw.io applet), relay_bus (BUILT), prompt service (BUILT)

---

## 1. Purpose

`kb.shiftcenter.com` is the knowledge base EGG. It is a documentation workspace where
prose documents and diagrams coexist as first-class content — not diagrams embedded in
docs, not docs linked from diagrams, but both in the same pane tree, navigated from the
same tree-browser, and searchable together.

It is also the first EGG to use `appType: drawio` in production, making it the proof-of-
concept for the GC third-party applet model established in ADR-GC-APPLET-001.

---

## 2. Domain

**Primary subdomain:** `kb.shiftcenter.com`

Also embeddable as a pane composite in any EGG where documentation is needed alongside
tooling — code.shiftcenter.com has a kb pane, meeting room EGG has an agenda pane, etc.

---

## 3. Content Model

The KB stores two first-class content types:

| Type | Extension | Opens In |
|------|-----------|----------|
| Document | `.md` | SDEditor (text-pane, markdown mode) |
| Diagram | `.drawio` | draw.io applet (freeform mode) |

Both types live in the same file tree. The tree-browser treats them as peers. No separate
"diagrams section" — a diagram is just a file that happens to open in a different pane.

Future content types (`.ir.yaml`, `.egg.md`) are supported by the same model — the
tree-browser uses file extension to route to the correct applet. This is the decomposition
principle applied to content: the tree-browser is the navigator, the pane is the renderer,
the file is the data.

---

## 4. EGG Layout

```
┌──────────────┬─────────────────────────────┐
│              │                             │
│  tree-browser│     Content Pane            │
│  (file tree) │  (SDEditor or draw.io       │
│              │   depending on file type)   │
│              │                             │
│              ├─────────────────────────────┤
│              │  terminal (agent / search)  │
└──────────────┴─────────────────────────────┘
```

```yaml
layout:
  type: split
  direction: horizontal
  children:
    - type: app
      appType: file-explorer
      nodeId: kb-tree
      config:
        rootPath: ./kb
        showHidden: false
        adapter: local
        fileTypeIcons: true
        supportedTypes: [md, drawio, ir.yaml, egg.md]

    - type: split
      direction: vertical
      ratio: 0.80
      children:
        - type: app
          appType: text                     # default; swapped to drawio for .drawio files
          nodeId: kb-content
          config:
            format: markdown
            label: Document
            acceptEditsOn: true
            coAuthor: true

        - type: app
          appType: terminal
          nodeId: kb-terminal
          config:
            welcomeBanner: "kb.shiftcenter.com — hive>"
            zone2Dock: right
```

### Dynamic Pane Switching

When the user opens a `.drawio` file from the tree-browser, the content pane switches
from `text` to `drawio` applet. This is handled by the EGG loader's pane-swap mechanism
(EGG swap continuity via AppletShell `appState`).

The swap is seamless — the pane chrome stays the same, the applet inside changes. The
user never navigates away; the content area adapts to the file type.

```yaml
# In EGG config — file-type routing rules
contentPane:
  nodeId: kb-content
  fileTypeRouting:
    md: text
    drawio: drawio
    ir.yaml: text                   # IR files open in SDEditor (raw YAML)
    egg.md: text                    # EGG files open in SDEditor
```

---

## 5. Draw.io Integration (First Production Use)

The KB EGG is the first EGG to use `appType: drawio` from ADR-GC-APPLET-001 in a real
product context. Configuration:

```yaml
# draw.io applet config when a .drawio file is opened
appType: drawio
config:
  mode: freeform                    # no IR shape constraints in KB
  toolbar: full
  theme: auto
  saveTarget: kb-tree               # saves back to the file in the tree
  autoSave: true
  autoSaveDebounceMs: 2000
  exportFormats: [svg, png, xml]    # available from draw.io toolbar
```

No IR constraint mode in the KB — diagrams here are documentation artifacts, not
executable processes. Architecture sketches, org charts, ERDs, system diagrams,
wireframes — all freeform.

---

## 6. Agent / Search Interface

The terminal pane serves two purposes:

### 6.1 Knowledge Search

```
hive> search authentication flow
hive> find all diagrams mentioning "relay_bus"
hive> show me docs about EGG format
hive> what did we decide about calendar adapter?
```

Search uses the embedding_protocol infrastructure service (semantic search over the KB
content). Results posted to the terminal Zone 2 response pane as a ranked list with
excerpts. Clicking a result opens the file in the content pane.

### 6.2 Content Generation

```
hive> write a doc about the presence service
hive> create a diagram for the IR trigger flow
hive> summarize this document
hive> generate a glossary from all docs in this folder
```

For `create a diagram` commands: the BEE generates a draw.io XML file, saves it to the
KB tree, and opens it in the content pane. The user sees a draw.io diagram appear from
a natural language command. This is the "AI diagramming" pattern from the landscape
analysis in UNIFIED-COMPONENT-REGISTRY.md — same as Eraser's model.

---

## 7. Publishing

KB documents can be published to a static docs site at a subdomain (e.g.
`docs.shiftcenter.com` or a customer's domain). The publish flow:

```
hive> publish docs
```

1. BEE collects all `.md` files in the KB tree
2. Generates a static site (text-pane `readOnly` EGG configuration)
3. Deploys to Vercel or hivenode static server
4. Diagrams are exported as SVG and embedded in the published docs

The published docs site is a read-only EGG: `text-pane (md, readOnly) + tree-browser
(page hierarchy, sidebar nav)` — exactly the "Docs Site" composite from the landscape
analysis.

---

## 8. EGG Config (Full)

```yaml
---
egg: kb
version: 1.0.0
displayName: Knowledge Base
description: Documentation workspace. Prose and diagrams as first-class content.
favicon: global-commons://icons/kb.png
---

content:
  rootPath: ./kb
  defaultView: tree               # tree | recent | search

contentPane:
  nodeId: kb-content
  fileTypeRouting:
    md: text
    drawio: drawio
    ir.yaml: text
    egg.md: text

search:
  provider: embedding_protocol    # semantic search
  indexOnSave: true               # re-index when file saved
  indexedTypes: [md, drawio]      # drawio indexed by shape labels

agent:
  model: auto
  coAuthor: true                  # SDEditor Co-Author mode on by default
  diagramGeneration: true         # "create a diagram" commands enabled
  requireHumanOnPublish: true

publish:
  target: vercel                  # vercel | hivenode-static | none
  outputPath: ./kb-dist
  includeDiagrams: true
  diagramFormat: svg
```

---

## 9. Relationship to Other EGGs

The KB EGG is designed to be embedded as a sub-pane in other EGGs, not just run
standalone. Common patterns:

| Host EGG | KB Usage | Pane Location |
|----------|----------|---------------|
| code.shiftcenter.com | API docs, architecture notes | Right panel, tabbed with agent response |
| Meeting room EGG | Meeting notes, decision log | Scaffold region, lower-right |
| SimDecisions | Domain documentation, process notes | Side panel |
| design.shiftcenter.com | Design system docs | Left panel |

When embedded, the KB pane uses a minimal layout (tree-browser hidden, content pane
full-width, terminal suppressed). The host EGG controls what file is shown via
`PANE_LOAD_FILE` bus event.

---

## 10. Open Items — PARTIALLY RESOLVED

| # | Question | Decision (Q88N, 2026-03-13) |
|---|----------|-----------------------------|
| 1 | Should draw.io diagrams be semantically indexed (by shape labels) for search? | Still open — no decision recorded. |
| 2 | Publishing: Vercel as default or hivenode static server? | Still open — no decision recorded. |
| 3 | Co-authoring in KB docs: draw.io collaboratively editable or single-user for v1? | Still open — no decision recorded. |
| 4 | `docs.shiftcenter.com` as a published KB subdomain — confirm domain intent? | **Yes. `docs.shiftcenter.com` confirmed.** Docs is docs. |

---

*Signed,*
**Q88N (Dave) × Claude (Anthropic)**
SPEC-KB-EGG-001 — LOCKED 2026-03-13
License: CC BY 4.0 | Copyright: © 2026 DEIA Solutions
