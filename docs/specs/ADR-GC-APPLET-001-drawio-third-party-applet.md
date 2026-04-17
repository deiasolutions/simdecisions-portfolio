# ADR-GC-APPLET-001: Global Commons Third-Party Applet Model
## Draw.io / maxGraph as Reference Implementation

**Date:** 2026-03-13  
**Author:** Q88N (Dave) × Claude (Anthropic)  
**Status:** SPEC — LOCKED  
**Registry ID:** ADR-GC-APPLET-001  
**Supersedes:** n/a — first ADR in GC applet series  

---

## 1. Context

ShiftCenter's canvas primitive is an IR execution surface. It renders PHASE-IR nodes as visual
objects; diagrams that can run. This is the moat. But it is not a drawing tool.

Two gaps exist that the canvas primitive does not address:

1. **Freeform drawing for non-IR work.** Whiteboarding, architecture sketches, org charts,
   wireframes, ERDs — none of these are IR. Users need a capable freeform drawing tool on day 1.
   Building one from scratch is out of scope and out of sequence.

2. **No proof that the Global Commons applet model accepts third-party open source components.**
   The SDK specifies that any applet wrapping AppletShell and registering in the GC can be
   referenced by any EGG. This has not been demonstrated with a real external library. Without a
   reference implementation, the GC applet model is theoretical.

Draw.io — specifically the `maxGraph` fork (MIT licensed, actively maintained) — resolves both
gaps simultaneously: it is a battle-tested freeform drawing library that becomes the first
externally-sourced GC applet.

---

## 2. Decision

**Draw.io (maxGraph) is adopted as `appType: drawio` in the Global Commons applet registry.**

It serves three distinct roles, in priority order:

1. **Proof of GC third-party applet model.** The first open source library to implement
   AppletShell's wrapper contract and register in the GC. This establishes the pattern for
   all future third-party applets — Monaco, Quill, vis.js, p5.js, others.

2. **Freeform drawing surface for non-IR work.** Whiteboarding, diagrams, sketches — anything
   that does not need to execute. File saved as `.drawio` format via tree-browser adapter.

3. **IR-constrained authoring surface (opt-in).** When `shapeConstraint: "phase-ir-v2"` is set
   in EGG config, the shape palette filters to PHASE-IR-valid node types only. User draws
   in familiar tooling; output is valid IR. This is a third authoring path alongside the
   SC canvas primitive and terminal (prompt-driven IR generation).

**Draw.io does NOT replace the canvas primitive.** The canvas primitive remains the
authoritative IR execution surface. Draw.io is a peer applet for different use cases.

---

## 3. Rejected Alternatives

| Alternative | Reason Rejected |
|-------------|-----------------|
| Build a freeform drawing tool from scratch | Out of scope, duplicates solved problem |
| Use the canvas primitive for freeform drawing | Canvas is an IR surface; repurposing it conflates authoring with execution |
| Use draw.io as an iframe embed | iframe embeds bypass AppletShell — no 3Cs reporting, no relay_bus, no governance. Violates the wrapper contract. |
| Use Excalidraw instead of draw.io | Excalidraw is MIT licensed and valid. Not rejected permanently — can be a second GC applet. Draw.io chosen first because shape library depth and enterprise familiarity are stronger for the IR-constraint use case. |
| Keep GC applets DEIA-only | Kills the ecosystem thesis. The GC must accept external contributions to be a marketplace, not a walled garden. |

---

## 4. Architecture

### 4.1 The AppletShell Wrapper Contract

Any third-party library entering the GC must satisfy the wrapper contract. Draw.io's
implementation is the reference. Future applets follow the same pattern.

**Required interface (all third-party applets must implement):**

```typescript
interface GCAppletWrapper {
  // Identity
  appType: string               // registered name in GC applet registry
  gcVersion: string             // semver of the GC-wrapped build
  sourceLibrary: string         // upstream library name + version
  sourceLicense: string         // must be OSI-approved open source license

  // AppletShell hooks (called by the shell, not the applet author)
  onMount(shell: AppletShellHandle): void
  onUnmount(): void
  onAwayMode(entering: boolean): void
  onSceneChange(scene: SceneMode): void

  // 3Cs reporting (called on every meaningful user action)
  reportMetrics(): ThreeCurrencyReport

  // Feature registry (for command palette + Fr@nk addressing)
  listFeatures(): FeatureRegistryEntry[]

  // relay_bus integration
  emitEvent(type: string, payload: Record<string, unknown>): void
  onBusEvent(type: string, handler: (payload: unknown) => void): void

  // Persistence
  getState(): SerializableState       // for EGG swap continuity
  setState(state: SerializableState): void
}
```

Draw.io wraps maxGraph's editor API and exposes this interface. The shell never calls
maxGraph directly — it calls the wrapper.

### 4.2 Bus Events

Draw.io emits the following events on the relay_bus:

| Event | Payload | When |
|-------|---------|------|
| `DRAWIO_DIAGRAM_CHANGED` | `{ nodeId, changeType, elementCount }` | Any edit to diagram |
| `DRAWIO_SELECTION_CHANGED` | `{ nodeId, selectedIds, selectedTypes }` | Selection changes |
| `DRAWIO_EXPORT_REQUESTED` | `{ nodeId, format: 'svg'\|'png'\|'xml'\|'ir' }` | Export triggered |
| `DRAWIO_IR_EMITTED` | `{ nodeId, ir: PhaseIRv2 }` | When `shapeConstraint` set and diagram is valid IR |
| `DRAWIO_SAVE` | `{ nodeId, filePath, format }` | Diagram saved to tree-browser |

Draw.io consumes:

| Event | Source | Effect |
|-------|--------|--------|
| `PROMPT_TO_PANE` | terminal / Fr@nk | If payload targets this nodeId, attempts to apply AI layout or generate shapes |
| `PANE_CLEAR` | layout manager | Resets to empty diagram |
| `SCENE_SET` | scene_system | Applies dark/light theme to draw.io canvas |

### 4.3 EGG Configuration

**Freeform mode (no IR constraint):**

```yaml
layout:
  type: split
  direction: horizontal
  children:
    - type: app
      appType: file-explorer
      nodeId: file-tree
      config:
        rootPath: ./diagrams
        adapter: local

    - type: app
      appType: drawio
      nodeId: diagram-canvas
      config:
        mode: freeform
        defaultFormat: drawio
        theme: auto
        toolbar: full
        saveTarget: file-tree
```

**IR-constrained mode:**

```yaml
- type: app
  appType: drawio
  nodeId: ir-author
  config:
    mode: constrained
    shapeConstraint: phase-ir-v2
    shapeLibrary: global-commons://shape-libraries/phase-ir-v2.xml
    emitIROnSave: true
    irTarget: sim-runner        # nodeId of the pane that receives IR output
    toolbar: constrained        # only shows IR-valid shapes
```

**Whiteboard mode (minimal chrome):**

```yaml
- type: app
  appType: drawio
  nodeId: whiteboard
  config:
    mode: freeform
    toolbar: minimal
    hideGrid: false
    autoSave: true
    saveTarget: file-tree
```

### 4.4 Shape Library for IR Constraint

When `shapeConstraint: "phase-ir-v2"` is active, the GC ships a draw.io-compatible XML shape
library at `global-commons://shape-libraries/phase-ir-v2.xml`. This library contains:

| Shape Name | Maps to IR Primitive | Visual |
|------------|----------------------|--------|
| `ir.task` | `TASK` node | Rounded rectangle |
| `ir.gateway` | `GATEWAY` node | Diamond |
| `ir.event.start` | `EVENT` (type: start) | Circle, thin border |
| `ir.event.end` | `EVENT` (type: end) | Circle, thick border |
| `ir.subprocess` | `SUBPROCESS` node | Rectangle with + icon |
| `ir.datastore` | `DATA_STORE` node | Cylinder |
| `ir.agent` | `AGENT` assignment | Person silhouette |
| `ir.branch` | `BRANCH` (Alterverse) | Hexagon |
| `ir.merge` | `MERGE` node | Inverted diamond |
| `ir.annotation` | `ANNOTATION` | Bracket notation |

When `emitIROnSave: true`, the wrapper compiles the constrained diagram to PHASE-IR v2.0 JSON
and emits `DRAWIO_IR_EMITTED` on the bus. Invalid diagrams (missing required connections,
unknown shapes) emit a validation error to the terminal pane if one is present.

### 4.5 GC Registration

The draw.io applet is registered in the Global Commons applet registry as:

```json
{
  "appType": "drawio",
  "displayName": "Draw.io",
  "description": "Freeform diagram and whiteboard tool. Optionally constrained to PHASE-IR v2 shapes for IR authoring.",
  "gcVersion": "1.0.0",
  "sourceLibrary": "maxGraph",
  "sourceLibraryVersion": "0.13.0",
  "sourceLicense": "Apache-2.0",
  "gcPath": "global-commons://applets/drawio/",
  "author": "deiasolutions",
  "trustTier": 1,
  "capabilities": ["freeform", "ir-constrained", "export-svg", "export-png", "export-xml"],
  "consumes": ["relay_bus", "ledger_writer", "gate_enforcer", "scene_system", "dnd_service"],
  "emits": ["DRAWIO_DIAGRAM_CHANGED", "DRAWIO_SELECTION_CHANGED", "DRAWIO_EXPORT_REQUESTED", "DRAWIO_IR_EMITTED", "DRAWIO_SAVE"]
}
```

---

## 5. Trust & Governance

Third-party applets entering the GC are assigned a trust tier following AGT-003 (Skill
Certification Tiers). Draw.io enters at **Tier 1** (security audit passed, standard capabilities)
by default because:

- maxGraph is Apache-2.0 licensed with a clean provenance chain
- No network calls; operates entirely on local/session data
- No shell access; no filesystem access outside the tree-browser adapter contract
- Source is auditable; GC build is pinned to a specific maxGraph release

Trust tier governs what AppletShell capabilities the wrapper can exercise:

| Capability | Tier -1 | Tier 0 | Tier 1 (Draw.io) | Tier 2 | Tier 3 |
|------------|---------|--------|-----------------|--------|--------|
| relay_bus read/write | No | Read only | Yes | Yes | Yes |
| ledger_writer | No | No | Yes | Yes | Yes |
| File system (via tree-browser) | No | No | Yes | Yes | Yes |
| gate_enforcer access | No | No | Read | Read/Write | Full |
| Network (declared endpoints) | No | No | No | Yes | Yes |

Draw.io at Tier 1 cannot make outbound network calls. Export to external services (Confluence,
Notion, etc.) is deferred to a Tier 2 certified extension, not the base applet.

---

## 6. Composite EGGs That Use Draw.io

### 6.1 `kb.shiftcenter.com` — Knowledge Base

```
text-pane (md, readOnly) + drawio (freeform) + tree-browser (page hierarchy)
```

Documentation workspace where diagrams live alongside prose. The tree-browser shows both `.md`
and `.drawio` files as first-class content. Opening a `.drawio` file inflates the drawio applet
in the adjacent pane.

### 6.2 `design.shiftcenter.com` — Visual EGG Builder (addendum)

The Visual EGG Builder EGG gains draw.io as an optional pane alongside the scene_system
inspector. Used for mocking layout concepts before encoding them in the EGG's `layout` block.
Not IR-constrained here — purely freeform for visual planning.

### 6.3 Whiteboard EGG

```
drawio (mode: freeform, toolbar: full) full-pane, no chrome
```

A standalone whiteboard at `board.shiftcenter.com` or as a float pane in any EGG. No tree-browser
required unless the user saves. Closest analog: Excalidraw or Miro lite.

### 6.4 IR Authoring via Draw.io (constrained)

```
drawio (mode: constrained, shapeConstraint: phase-ir-v2) + sim-runner + terminal
```

Three-pane layout: draw the process in draw.io → save emits IR → sim-runner executes it →
terminal shows output. Alternative IR authoring path for users who think visually rather than
through the SC canvas primitive or prompt-to-IR.

---

## 7. What This Proves

ADR-GC-APPLET-001's significance is not draw.io. It is the pattern.

Once maxGraph wraps AppletShell and registers in the GC:

- **Monaco** can register as `appType: code-editor` from its own GC-wrapped build
- **Quill / ProseMirror** as alternative `appType: rich-text`
- **vis.js / Cytoscape** as `appType: network-graph`
- **p5.js** as `appType: processing-canvas` (SPEC-PROCESSING-ADAPTER-001)
- **Any OSI-licensed library** that a developer wraps and certifies

The Global Commons becomes a real marketplace; not because DEIA Solutions built every applet,
but because the wrapper contract is clear enough for external contributors to follow.

The EGG format is already CC BY 4.0 on the Global Commons. This ADR extends that openness to
the applet layer. Together they mean: any developer can build an EGG-native app using
GC-registered applets, publish the EGG to the Commons, and have it run in any ShiftCenter
instance without a deployment step.

> "Apps don't live on the server. They live as EGGs in memory. Applets don't come from a
> proprietary registry. They come from the Commons."

---

## 8. Open Items — PARTIALLY RESOLVED

| # | Question | Decision (Q88N, 2026-03-13) |
|---|----------|-----------------------------|
| 1 | Trust tier upgrade path: who reviews Tier 1 → Tier 2 promotion? | Still open — no decision recorded. |
| 2 | GC build pipeline: DEIA Solutions or community maintains maxGraph wrapper? | Still open — no decision recorded. |
| 3 | `board.shiftcenter.com` as standalone whiteboard product? | Still open — no decision recorded. |
| 4 | Excalidraw as a second GC applet alongside draw.io? | Still open — no decision recorded. |
| 5 | PHASE-IR v2 shape library — bee task or Dave's hand? | **Dave defines it.** Use SPEC-CANVAS-APP-001 §5.1 palette as the starting point. Shapes map to IR node types (task, decision, resource, fork, join, start, end). |

---

## 9. Implementation Notes for Mr. Code

The wrapper is a TypeScript class, not a React component. It instantiates maxGraph's `Graph`
class internally and exposes only the `GCAppletWrapper` interface to AppletShell. The React
component that renders in the pane is a thin mount point that calls `wrapper.onMount(shell)`.

Recommended build approach:
1. Install `@maxgraph/core` as a dependency in the GC applet package (separate from the
   monorepo — GC applets are independently versioned)
2. Implement `DrawioAppletWrapper implements GCAppletWrapper`
3. Write the XML shape library for `phase-ir-v2` constraint mode
4. Register in the GC applet registry JSON
5. Write a reference EGG (`whiteboard.egg.md`) that loads `appType: drawio` in freeform mode
6. Write a reference EGG (`ir-draw.egg.md`) that loads `appType: drawio` in constrained mode
7. Smoke test: emit `DRAWIO_IR_EMITTED` → confirm sim-runner receives valid PHASE-IR

The wrapper must pass the GC applet test suite before registration:
- AppletShell hooks fire correctly on mount/unmount
- `reportMetrics()` returns valid ThreeCurrencyReport (CLOCK, COIN, CARBON)
- relay_bus events emit with correct payloads
- `getState()` / `setState()` round-trips cleanly (EGG swap continuity)
- Trust Tier 1 capabilities respected (no network calls attempted)

---

*Signed,*  
**Q88N (Dave) × Claude (Anthropic)**  
ADR-GC-APPLET-001 — LOCKED 2026-03-13
License: CC BY 4.0 International
Copyright: © 2026 DEIA Solutions / Global Commons

---

## IMPLEMENTATION ADDENDUM — Bus Event Routing (Q33NR, 2026-03-13)

> *This section is an implementation note appended after spec lock. It does not modify the spec.*

Draw.io is a **self-contained applet** — its bus events are consumed by its own wrapper and by external systems that opt in.

**Emitted events → consumed by:**

| Event | Consumers | Handler Location |
|-------|-----------|-----------------|
| `DRAWIO_DIAGRAM_CHANGED` | Event Ledger (if tracking), autosave timer | `DrawioAppletWrapper` internal, `ledger_writer` |
| `DRAWIO_SELECTION_CHANGED` | Command palette (contextual actions) | `AppletShell` feature registry |
| `DRAWIO_EXPORT_REQUESTED` | Tree-browser (file save) | Tree-browser adapter `onBusEvent` |
| `DRAWIO_IR_EMITTED` | sim-runner (IR execution), IR engine | sim-runner pane adapter |
| `DRAWIO_SAVE` | Tree-browser (file write) | Tree-browser adapter |

**Consumed events:**

| Event | Source | Effect |
|-------|--------|--------|
| `PROMPT_TO_PANE` | Terminal / Fr@nk | AI-assisted layout or shape generation |
| `PANE_CLEAR` | Layout manager | Reset to empty diagram |
| `SCENE_SET` | scene_system | Apply dark/light theme to draw.io canvas |

**Isolation:** Draw.io at Trust Tier 1 has no knowledge of presence, sim-chat, or scaffold events. It communicates only through its declared bus events. AppletShell mediates everything else.
