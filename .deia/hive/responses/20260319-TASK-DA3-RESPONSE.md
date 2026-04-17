# TASK-DA3: Design Mode + EGG Save/Write Audit -- COMPLETE

**Status:** COMPLETE
**Model:** Sonnet
**Date:** 2026-03-19

## Files Modified
None (research only, no code changes)

## What Was Done
Comprehensive audit of platform repo and shiftcenter repo to determine the gap between the Product Session spec (§7-8: Visual EGG Builder and Draft/Release Model) and actual implementation.

Findings:
1. **Design Mode**: Canvas has local design mode (sim-specific), but NO scene_system design stage exists
2. **EGG Writer**: NOT implemented — no serialization back to .egg.md
3. **Register Block**: NOT implemented — no draft change tracking
4. **Property Editor Terminal**: Partial (canvas has property panel, but NOT as inspector terminal)
5. **ELEMENT_SELECTED Bus Event**: NOT implemented globally
6. **Workspace Persistence**: Platform has SAVE_WORKSPACE action, but NOT EGG format

**Key Gap**: Product Session §7-8 describes a universal design mode where ANY pane in ANY EGG can be visually edited and written back to .egg.md. Nothing in this vision exists yet. Canvas has a local "design vs simulate" mode, but this is canvas-internal editing of IR nodes, NOT editing the EGG layout itself.

---

## Research Findings (Atomic)

### FINDING 1: scene_system Design Stage — NOT IMPLEMENTED

---
bee: BEE-DA3
type: RESEARCH
finding: 1
source: platform/simdecisions-2/src/components/shell/shell.reducer.js + browser/src/*
shift: false
---

**Product Session §7.1** specifies: `scene_system gains a new stage mode: design. In design mode, the entire input model shifts from 'use the app' to 'edit the app': Clicks select elements instead of interacting with them. Hovers highlight elements. Bus emits ELEMENT_SELECTED.`

**Platform Repo**: No scene_system service exists. Searched for:
- `scene_system` — not found
- `ELEMENT_SELECTED` bus event — not found
- Design stage mode — not found

**Canvas has local design mode** (see browser/src/apps/sim/components/flow-designer/modes/DesignMode.tsx), but this is canvas-internal: editing IR nodes on the canvas, NOT editing the EGG layout itself. This is sim mode switching (design vs simulate vs tabletop), NOT scene_system stage mode.

**Shiftcenter Repo (commit 850317c, March 15)**: Same. Canvas design mode exists for IR editing. No global scene_system or inspector mode.

DIVERGENCE: Complete gap. spec describes universal design mode for all panes; reality has zero implementation.

P0: none

BACKLOG: Implement scene_system as infrastructure service per §7.1 spec. Stage modes: normal, emergency, away, design. Design mode: click-to-select, hover-to-highlight, ELEMENT_SELECTED bus event. {source_bee: BEE-DA3, task_context: "Product Session §7.1", file: none}

---

### FINDING 2: egg_writer / EGG Serialization — NOT IMPLEMENTED

---
bee: BEE-DA3
type: RESEARCH
finding: 2
source: platform/simdecisions-2/src/eggs/eggInflater.ts + shiftcenter browser/src/
shift: false
---

**Product Session §7** states: "The EGG is not written after the design — the EGG IS the live document that updates as you design. Every edit writes directly to the .egg.md file."

**Product Session §9.4** clarifies: "egg_writer: Not separate infrastructure. Just text-pane pointed at the .egg.md file. SC already renders from the EGG; edits to the text are edits to the app."

**Platform Repo**: Only `eggInflater.ts` exists (reads .egg.md → EGG IR). No reverse direction (EGG IR → .egg.md). No egg_writer, eggDeflater, eggSerializer. Searched:
- `egg.*writ`, `write.*egg`, `serialize.*egg` — only one test hit (unrelated)
- `eggDeflater`, `eggWriter` — not found

**Shiftcenter Repo**: Same. Only egg inflater, no writer.

**Workspace Persistence**: `shell.reducer.js` (platform) has `SAVE_WORKSPACE` action at L432-444. This serializes the shell tree to JSON and writes to `volumeStorage` (localStorage or filesystem). Format: `{ id, name, tree: JSON, focusedPaneId, savedAt }`. This is NOT .egg.md format. This is runtime state snapshot, not EGG spec.

DIVERGENCE: Complete gap. Workspace save exists, but NOT as .egg.md. No reverse serialization from shell tree → .egg.md layout block.

P0: none

BACKLOG: Implement EGG serialization: shell tree → .egg.md layout block. Design: text-pane with live two-way binding OR dedicated eggWriter service. Integrate with design mode: every layout change writes to .egg.md immediately. {source_bee: BEE-DA3, task_context: "Product Session §7-8", file: none}

---

### FINDING 3: Register Block / Draft Change Tracking — NOT IMPLEMENTED

---
bee: BEE-DA3
type: RESEARCH
finding: 3
source: platform/simdecisions-2/src/eggs/*.egg.md + browser/src/eggs/eggInflater.ts
shift: false
---

**Product Session §8.1** specifies: "The .egg.md file is a wrapper containing two logical sections: the live spec (what SC Stage renders) and the register (draft change history). egg_loader only parses the live spec blocks; the register block is explicitly skipped during inflate."

Example from spec:
```
\`\`\`register
[
  { "seq": 1, "author": "daaaave-atx", "ts": "...",
    "block": "layout", "path": "children[0].config.ratio",
    "from": 0.25, "to": 0.30, "note": "wider sidebar" }
]
\`\`\`
```

**Platform Repo**: Searched all .egg.md files for `register:` block. NOT FOUND. No EGG files contain register blocks.

**eggInflater.ts** (platform): Parses frontmatter + fenced blocks (layout, modes, ui, tabs, commands, prompt, settings, away, startup, permissions). No mention of `register`. No skip logic for unknown blocks.

**Shiftcenter Repo**: Same. No register blocks in any EGG file.

DIVERGENCE: Complete gap. Register block not implemented in .egg.md format, not parsed by inflater, not generated by any service.

P0: none

BACKLOG: Implement register block per §8.1 spec. Update .egg.md schema to include optional \`\`\`register block. Update eggInflater to skip register during parse (already ignores unknown blocks). Implement register writer: every design mode change appends entry to register. On release: strip register, bump version, flip status DRAFT→RELEASED. {source_bee: BEE-DA3, task_context: "Product Session §8.1-8.3", file: platform/simdecisions-2/src/eggs/eggInflater.ts}

---

### FINDING 4: Property Editor Terminal — PARTIAL IMPLEMENTATION

---
bee: BEE-DA3
type: RESEARCH
finding: 4
source: platform/simdecisions-2/src/components/panels/properties/PropertiesPanelContent.tsx
shift: false
---

**Product Session §7.1** specifies: "A floating terminal (property editor) listens for ELEMENT_SELECTED and loads context-appropriate input primitives: color-picker for colors, slider for dimensions, toggle for booleans."

**Platform Repo**: Properties panel EXISTS at `src/components/panels/properties/PropertiesPanelContent.tsx`. This is a React component panel (not a terminal primitive) with sections: GeneralSection, TimingSection, ActionsSection, OutputsSection, BadgesSection, OperatorSection, QueueSection, EdgePropertiesSection, DesignPropertiesSection.

Reads from: `useGraphStore` (nodes/edges) and `useSelectionStore` (selectedNodeIds/selectedEdgeIds). When a node is selected, shows property forms. Has Reset/Apply buttons.

**Divergence from spec**:
- This is a dedicated properties panel component, NOT a terminal with routeTarget: 'inspector'
- Listens to Zustand stores, NOT relay_bus ELEMENT_SELECTED events
- Canvas-specific (sim canvas), NOT universal for all panes
- No color-picker primitive, no slider primitive (uses HTML inputs)

**Shiftcenter Repo**: No properties panel ported. Canvas has inline property editing (see useNodeEditing.ts), but no floating property inspector.

DIVERGENCE: Partial. Canvas property editor exists in platform, but architecture differs from spec. Spec wants universal terminal-based inspector; reality has canvas-specific React panel.

P0: none

BACKLOG: Refactor properties panel to use terminal primitive per §7.1 spec. Terminal config: routeTarget: 'inspector', displayMode: 'float'. Listen to relay_bus ELEMENT_SELECTED events. Load primitives dynamically: color-picker, slider, toggle, text-input based on property type. Make universal for all primitives, not canvas-specific. {source_bee: BEE-DA3, task_context: "Product Session §7.1", file: platform/simdecisions-2/src/components/panels/properties/PropertiesPanelContent.tsx}

---

### FINDING 5: Workspace Persistence Format

---
bee: BEE-DA3
type: RESEARCH
finding: 5
source: platform/simdecisions-2/src/components/shell/shell.reducer.js:L432-444
shift: false
---

**shell.reducer.js SAVE_WORKSPACE action**:
```js
case 'SAVE_WORKSPACE': {
  const ws = {
    id: uid(),
    name: action.name,
    tree: JSON.parse(JSON.stringify(state.root)),
    focusedPaneId: state.focusedPaneId,
    savedAt: new Date().toISOString()
  }
  const nextWorkspaces = [...state.workspaces.filter(w=>w.name!==action.name), ws]

  // Persist to volume
  try {
    writeVolume('local://shell/workspaces', nextWorkspaces)
  } catch (e) {
    console.warn('[shell.reducer] Failed to save workspaces:', e)
  }

  return { ...state, workspaces: nextWorkspaces }
}
```

**Format**: JSON array of workspace objects. Each workspace: `{ id, name, tree, focusedPaneId, savedAt }`. Tree is full shell tree (branches with layout/float/pinned/spotlight).

**Storage**: `volumeStorage` service (imported from `src/services/storage/volumeStorage`). Key: `'local://shell/workspaces'`. This is localStorage or filesystem depending on environment.

**NOT .egg.md format**: This is runtime state snapshot, not EGG spec. Tree includes runtime fields (loadState, appState, notification, etc) not in .egg.md schema.

DIVERGENCE: Platform has workspace save, but not as .egg.md. Shiftcenter has no workspace save yet.

P0: none

BACKLOG: none (workspace persistence works, just different format than .egg.md)

---

### FINDING 6: Design-io Services Are NOT EGG Writers

---
bee: BEE-DA3
type: RESEARCH
finding: 6
source: platform/simdecisions-2/src/services/design-io/designExport.ts + designImport.ts
shift: false
---

**Platform has design-io services**: `src/services/design-io/` with:
- `designExport.ts`: Serializes Design + DesignNode[] + DesignEdge[] to JSON
- `designImport.ts`: Deserializes JSON back to Design objects
- Validation, round-trip tests

**Format**: Design JSON export format for canvas IR (sim canvas flows). NOT .egg.md format. This is canvas content (IR nodes/edges), NOT EGG layout.

Example: `{ exportVersion: "1.0", design: {...}, nodes: [...], edges: [...] }`

**NOT related to EGG writer**: These services export/import canvas content (what's INSIDE a canvas pane), not the EGG layout itself (which panes exist, how they're arranged).

DIVERGENCE: None. These services do what they're supposed to do (canvas content persistence). They are NOT a gap for EGG writer.

P0: none

BACKLOG: none

---

### FINDING 7: Shell Utils Serialize/Deserialize — Simple JSON

---
bee: BEE-DA3
type: RESEARCH
finding: 7
source: platform/simdecisions-2/src/components/shell/shell.utils.js:L253-254
shift: false
---

**shell.utils.js L253-254**:
```js
export const serializeTree   = root => JSON.stringify(root)
export const deserializeTree = json => JSON.parse(json)
```

Simple JSON stringify/parse. No .egg.md format generation. Used by SAVE_WORKSPACE (stringify the tree before writing to volumeStorage).

DIVERGENCE: None. This is exactly what it claims to be: JSON serialization for runtime persistence.

P0: none

BACKLOG: none

---

## Summary of Gaps

| Spec (Product Session §7-8) | Platform Repo | Shiftcenter Repo | Gap |
|------------------------------|---------------|------------------|-----|
| scene_system design stage | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| ELEMENT_SELECTED bus event | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| Click-to-select, hover-to-highlight | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| Property editor terminal (universal) | Partial (canvas-only React panel) | NOT IMPLEMENTED | ARCHITECTURE GAP |
| EGG writer (shell tree → .egg.md) | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| Register block (draft change tracking) | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| Dirty indicator on applet_shell | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |
| Release command (strip register, bump version) | NOT IMPLEMENTED | NOT IMPLEMENTED | FULL GAP |

**Bottom Line**: The Visual EGG Builder (Product Session §7) and Draft/Release Model (§8) are 0% implemented. Canvas has a local design mode for editing IR nodes, but this is NOT the universal scene_system design stage described in the spec.

**Workspace Persistence**: Works in platform (JSON to volumeStorage), but NOT in .egg.md format. This is runtime state, not EGG spec.

---

## Recommended Next Steps

1. **Implement scene_system infrastructure service** per Product Session §4 (infrastructure table, row 8): "CSS scene engine. Modes: normal, emergency, away, design (inspector). Design mode: clicks select elements instead of interacting, hovers highlight, emits ELEMENT_SELECTED to bus."

2. **Implement EGG serialization** (shell tree → .egg.md layout block). Decision: dedicated eggWriter service OR text-pane with live binding to .egg.md file (as §9.4 suggests).

3. **Implement register block** in .egg.md format. Update eggInflater to skip register during parse. Implement register writer: append change entries on every design mode edit.

4. **Refactor properties panel** from canvas-specific React component to universal terminal-based inspector. Use relay_bus ELEMENT_SELECTED events. Load primitives dynamically (color-picker, slider, toggle).

5. **Add primitives from §2**: color-picker (P-24), slider (P-23), toggle (P-26) if not already implemented.

6. **Implement release command** in command_registry: strip register, bump version, flip status DRAFT→RELEASED, archive register to Event Ledger.

---

## Files Audited

**Platform Repo** (`C:\Users\davee\OneDrive\Documents\GitHub\platform\simdecisions-2\`):
- `src/components/shell/shell.reducer.js` (665 lines) — workspace save, no .egg.md
- `src/components/shell/shell.utils.js` (436 lines) — serializeTree = JSON.stringify
- `src/services/design-io/designExport.ts` (94 lines) — canvas IR export, NOT EGG
- `src/services/design-io/designImport.ts` (150 lines) — canvas IR import, NOT EGG
- `src/components/panels/properties/PropertiesPanelContent.tsx` (100+ lines) — canvas property panel (React)
- `src/eggs/eggInflater.ts` (first 100 lines read) — only inflater, no writer
- Searched: ELEMENT_SELECTED, scene_system, design mode, egg_writer, register block — NOT FOUND

**Product Session Doc** (`C:\Users\davee\Downloads\2026-03-10-PRODUCT-SESSION-CANONICAL.docx`):
- Extracted full text (§1-§10)
- §7: Visual EGG Builder
- §8: EGG Draft/Release Model
- §9.4: egg_writer clarification

**Shiftcenter Repo** (commit 850317c, March 15):
- Canvas design mode: `browser/src/apps/sim/components/flow-designer/modes/DesignMode.tsx`
- No scene_system, no ELEMENT_SELECTED, no EGG writer
- No register blocks in any .egg.md files

---

## NVWR Review

No NVWR items. All code reviewed is correct for its intended purpose. The gap is missing features, not buggy code.
