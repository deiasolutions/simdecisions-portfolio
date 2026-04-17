# Ship Feed Manifest

Feed items for the ship plan queue feeder. Each `###` block is one spec to feed. The feeder reads this file and creates queue specs in order.

## Pre-existing (already in queue, P0.005-P0.025)
- WAVE0-02: Fix engine import paths (P0.005, haiku)
- BL-126: Kanban backlog DB (P0.010, sonnet)
- ra96it SSO federation (P0.015, haiku)
- WAVE0-07: Fix SpotlightOverlay tests (P0.020, haiku)
- WAVE0-08: Fix CloudAPIClient mock (P0.025, haiku)

---

## Wave 1: Finish the Ports

### w1-01-properties-panel
- model: sonnet
- big: true
- title: Port Properties Panel (16 files, 6 accordion sections)
- objective: Port the Properties Panel from platform/efemera to shiftcenter. 16 files, 6 accordion sections (General, Data, Rules, Connections, Resources, Advanced). Full node property editor. Source: platform/efemera/src/efemera/components/properties/. Target: browser/src/apps/sim/components/properties/.
- acceptance: All 16 properties panel files ported | 6 accordion sections render correctly | Node property editing works | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/components/properties/

### w1-02-phase-ir-cli
- model: sonnet
- big: true
- title: Port PHASE-IR CLI toolchain (13 subcommands) + domain vocab YAMLs
- objective: Port the PHASE-IR CLI from platform. 13 subcommands for flow management, validation, compilation, and analysis. Include domain vocabulary YAML files. Source: platform/efemera/src/efemera/phase_ir/cli.py (578 lines). Target: engine/phase_ir/cli.py. Also port domain vocab YAMLs to engine/phase_ir/vocabularies/.
- acceptance: CLI module ported with all 13 subcommands | Domain vocabulary YAMLs copied | python -m engine.phase_ir --help works | Tests for CLI commands written and passing
- smoke_test: python -m pytest tests/engine/phase_ir/test_cli.py -v

### w1-03-phase-ir-trace
- model: haiku
- big: false
- title: Port PHASE-IR trace system (25 event types, JSONL export)
- objective: Port trace system from platform. 25 event types, JSONL export/import, trace routes. Source: platform trace.py (~420 lines). Target: engine/phase_ir/trace.py + hivenode/routes/phase_ir_trace.py. Follow store.py pattern already in engine/phase_ir/store.py.
- acceptance: Trace module with 25 event types | JSONL export and import working | Trace API routes registered | Tests written and passing
- smoke_test: python -m pytest tests/engine/phase_ir/ -v

### w1-04-phase-ir-models
- model: haiku
- big: false
- title: Port PHASE-IR models + schema_routes + validate_schema
- objective: Port remaining PHASE-IR files: models.py (~82 lines), schema_routes.py, validate_schema.py (~140 lines). Rewrite models.py as SQLite store (follow hivenode/efemera/store.py pattern). Add jsonschema>=4.0 to pyproject.toml if not present.
- acceptance: models.py ported as SQLite store | validate_schema.py ported with correct schema path | schema_routes registered in hivenode | Tests written and passing
- smoke_test: python -m pytest tests/engine/phase_ir/ -v

### w1-05-des-engine-routes
- model: haiku
- big: false
- title: Port DES engine_routes.py
- objective: Port DES engine routes from platform (~265 lines). Provides API endpoints for simulation execution: /sim/start, /sim/step, /sim/status, /sim/results. Source: platform engine_routes.py. Target: hivenode/routes/des_routes.py. Register in routes/__init__.py.
- acceptance: DES engine routes ported | Endpoints /sim/start /sim/step /sim/status /sim/results | Routes registered in hivenode | Tests written and passing
- smoke_test: python -m pytest tests/hivenode/test_des_routes.py -v

### w1-06-canvas-node-types
- model: sonnet
- big: true
- title: Port canvas missing node types (13 BPMN + annotation types)
- objective: Port 13 missing canvas node type components from platform: BPMN gateway types (exclusive, parallel, inclusive, event-based, complex), BPMN event types (intermediate, boundary, signal, timer, error, compensation, escalation), and annotation node. ~1,110 lines total. Source: platform canvas/nodes/. Target: browser/src/apps/sim/components/flow-designer/nodes/.
- acceptance: All 13 node type components ported | Each node renders correctly in canvas | Node type registry updated | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/components/flow-designer/

### w1-07-canvas-animation
- model: haiku
- big: false
- title: Port canvas animation system (6 components)
- objective: Port 6 canvas animation components from platform (~749 lines): TokenAnimation, NodePulse, EdgeFlow, ResourceMeter, SimClock, AnimationController. Source: platform canvas/animation/. Target: browser/src/apps/sim/components/flow-designer/animation/.
- acceptance: All 6 animation components ported | Animation controller manages playback state | Token animations follow edges | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/

### w1-08-canvas-lasso-zoom
- model: haiku
- big: false
- title: Port canvas lasso selection + zoom controls + annotation badge
- objective: Port 3 canvas interaction components (~435 lines): LassoSelection (multi-select by drawing rectangle), ZoomControls (fit, zoom in/out, reset), AnnotationBadge (comment count indicator on nodes). Source: platform canvas/. Target: browser/src/apps/sim/components/flow-designer/.
- acceptance: Lasso selection component ported | Zoom controls component ported | Annotation badge component ported | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/components/flow-designer/

### w1-09-canvas-tests
- model: haiku
- big: true
- title: Port canvas test files (10 test files)
- objective: Port 10 canvas test files from platform (~2,348 lines). Fix imports to use shiftcenter paths. Update mocks to match current component structure. Source: platform canvas/__tests__/. Target: browser/src/apps/sim/components/flow-designer/__tests__/.
- acceptance: All 10 test files ported | Imports updated to shiftcenter paths | All tests pass | No regressions in existing tests
- smoke_test: cd browser && npx vitest run src/apps/sim/components/flow-designer/__tests__/

### w1-10-rag-indexer
- model: sonnet
- big: true
- title: Port RAG indexer service
- objective: Port RAG indexer service from platform (~3,060 lines). Document chunking, embedding generation, vector storage, similarity search. Source: platform/rag/indexer/. Target: hivenode/rag/indexer/. Use SQLite for vector storage (not pgvector).
- acceptance: Indexer service ported with document chunking | Embedding generation working | Vector storage using SQLite | Similarity search API endpoint | Tests written and passing
- smoke_test: python -m pytest tests/hivenode/test_rag_indexer.py -v

### w1-11-rag-entity-vectors
- model: sonnet
- big: true
- title: Port RAG entity vectors + Voyage AI + BOK services
- objective: Port RAG entity vectors, Voyage AI adapter, and BOK (Body of Knowledge) services (~1,497 lines). Entity extraction, named entity vectors, BOK document management. Source: platform/rag/. Target: hivenode/rag/.
- acceptance: Entity vector extraction ported | Voyage AI adapter ported | BOK service ported | Tests written and passing
- smoke_test: python -m pytest tests/hivenode/test_rag*.py -v

### w1-12-shell-chrome-menubar
- model: sonnet
- big: false
- title: Port shell chrome MenuBar + ShellTabBar + WorkspaceBar
- objective: Port 3 shell chrome components (~906 lines): MenuBar (app menu with File/Edit/View/Help), ShellTabBar (workspace tabs), WorkspaceBar (workspace selector). Source: platform shell/components/. Target: browser/src/shell/components/.
- acceptance: MenuBar component ported with menu structure | ShellTabBar component ported | WorkspaceBar component ported | All use var(--sd-*) CSS variables | Tests written and passing
- smoke_test: cd browser && npx vitest run src/shell/components/__tests__/

### w1-13-shell-chrome-governance
- model: haiku
- big: false
- title: Port shell chrome GovernanceProxy + SpotlightOverlay + PaneMenu
- objective: Port 3 shell chrome components (~361 lines): GovernanceProxy (approval modal for gate_enforcer), SpotlightOverlay (command palette overlay), PaneMenu (right-click context menu for panes). Source: platform shell/. Target: browser/src/shell/components/.
- acceptance: GovernanceProxy ported | SpotlightOverlay ported | PaneMenu ported | Tests written and passing
- smoke_test: cd browser && npx vitest run src/shell/components/__tests__/

### w1-14-shell-chrome-remaining
- model: haiku
- big: false
- title: Port shell chrome remaining (6 small components)
- objective: Port 6 remaining shell chrome components (~281 lines): NotificationModal, ShortcutsPopup, LayoutSwitcher, PinnedPaneWrapper, MaximizedOverlay, dragDropUtils. Source: platform shell/. Target: browser/src/shell/components/.
- acceptance: All 6 components ported | Tests written and passing | No regressions in existing shell tests
- smoke_test: cd browser && npx vitest run src/shell/

### w1-15-canvas-chatbot-dialect
- model: haiku
- big: false
- title: Port canvas chatbot dialect + chat-with-process spec
- objective: Port the canvas chatbot dialect .md file from platform and find/port the chat-with-process spec. The dialect defines how the terminal talks to the canvas (NL to LLM to to_ir to render). Source: platform/dialects/. Target: eggs/ or docs/specs/.
- acceptance: Canvas chatbot dialect file ported | Chat-with-process spec located and ported | Dialect integrates with terminal routeTarget system
- smoke_test: File exists and is valid markdown

### w1-16-kanban-board
- model: sonnet
- big: false
- title: Find and port kanban board component (BL-071)
- objective: Find the kanban board component in the platform repo and port it to shiftcenter. BL-071. The kanban should be a pane-compatible applet that renders columns (To Do, In Progress, Done) with draggable cards. Source: find in platform. Target: browser/src/apps/kanban/.
- acceptance: Kanban board component ported | Columns render with cards | Drag and drop between columns works | Registered as a pane applet | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/kanban/

---

## Wave 2: Wire It Together

### w2-01-process13-quality-gates
- model: sonnet
- big: true
- title: Wire Process 13 quality gates into dispatch pipeline
- objective: Wire Process 13 quality gates (spec validation then build then test then review) into the dispatch pipeline. Read .deia/processes/PROCESS-LIBRARY-V2.md for P-13 definition. Implement gates in spec_processor.py: validate spec format, run tests before/after, check for regressions, flag for review if tests fail.
- acceptance: Quality gates implemented in spec_processor.py | Spec format validation before dispatch | Pre/post test comparison | Regression detection flags NEEDS_DAVE | Tests written and passing
- smoke_test: python -m pytest .deia/hive/scripts/queue/tests/ -v

### w2-02-canvas-chatbot-wire
- model: sonnet
- big: true
- title: Wire canvas chatbot terminal NL to LLM to to_ir to canvas renders
- objective: Wire the canvas chatbot flow: user types natural language in terminal, LLM converts to PHASE-IR, canvas renders nodes. Connect terminal routeTarget=canvas to LLM adapter, parse response into IR, send to canvas via bus events.
- acceptance: Terminal NL input reaches LLM | LLM response parsed into PHASE-IR flow | Canvas receives and renders flow | End-to-end demo works | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/

### w2-03-properties-canvas-wire
- model: sonnet
- big: false
- title: Wire properties panel to canvas select then edit then update
- objective: Wire properties panel to canvas: clicking a node on canvas opens its properties in the properties panel. Editing a property updates the node on canvas in real-time. Uses bus events: node:selected, node:property-changed.
- acceptance: Clicking canvas node opens properties panel | Editing property updates canvas node | Bus events connected correctly | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/

### w2-04-flow-des-wire
- model: sonnet
- big: true
- title: Wire flow designer to DES engine load then simulate then stream
- objective: Wire flow designer to DES simulation engine: load a flow, call /sim/start, events stream back to browser. Connect the flow designer run button to the DES engine routes. Display sim results in a results pane.
- acceptance: Run button calls /sim/start with current flow | Simulation events stream to browser | Results displayed in pane | Tests written and passing
- smoke_test: python -m pytest tests/hivenode/test_des_routes.py -v

### w2-05-des-canvas-visual
- model: sonnet
- big: true
- title: Wire DES events to canvas tokens move nodes light up
- objective: Wire DES simulation events to canvas visualization: tokens move along edges, active nodes light up, resources change color based on utilization. Uses animation system from w1-07.
- acceptance: Token animations follow simulation events | Active nodes highlight during simulation | Resource nodes show utilization colors | Animation playback controls work | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/components/flow-designer/animation/

### w2-06-shell-chrome-wire
- model: haiku
- big: false
- title: Wire shell chrome menu renders tabs switch spotlight opens
- objective: Wire shell chrome components: MenuBar renders with working menu items, ShellTabBar switches between workspaces, spotlight overlay opens with Ctrl+Shift+P. Connect to shell reducer actions.
- acceptance: MenuBar renders with menu items | Tab switching works | Spotlight overlay opens/closes | Tests written and passing
- smoke_test: cd browser && npx vitest run src/shell/

### w2-07-tree-browser-volumes
- model: sonnet
- big: false
- title: Wire tree-browser to real volume storage home reads files
- objective: Wire tree-browser to volume storage: home:// protocol reads actual files from the volume system. List directories, read files, show file sizes and dates. Connect volumeAdapter to real backend.
- acceptance: home:// lists real directories | File contents load in text-pane | File metadata (size, date) displayed | Tests written and passing
- smoke_test: cd browser && npx vitest run src/primitives/tree-browser/

### w2-08-chat-persistence-wire
- model: sonnet
- big: false
- title: Wire chat persistence save to volume list in tree reload
- objective: Wire chat persistence: conversations auto-save to volume storage, tree-browser lists saved conversations, clicking a conversation reloads it in the terminal. Use terminalChatPersist.ts.
- acceptance: Conversations save automatically | Tree-browser shows conversation list | Clicking conversation reloads it | Tests written and passing
- smoke_test: cd browser && npx vitest run src/primitives/terminal/__tests__/useTerminal.chatPersist.test.ts

### w2-09-canvas-palette-dnd
- model: haiku
- big: false
- title: Wire canvas palette drag from tree drop on canvas create node
- objective: Wire drag-and-drop node creation: drag a node type from the tree-browser palette, drop on canvas, node created at drop position. Uses HTML5 drag/drop API.
- acceptance: Palette shows node types in tree-browser | Drag from palette to canvas works | Node created at drop position | Tests written and passing
- smoke_test: cd browser && npx vitest run src/apps/sim/

### w2-10-governance-visual
- model: haiku
- big: false
- title: Wire governance GovernanceProxy shows approval modal
- objective: Wire GovernanceProxy: when gate_enforcer returns warn or ask disposition, show approval modal to user. User can approve or reject. Result fed back to gate_enforcer.
- acceptance: Approval modal appears on warn/ask dispositions | User can approve or reject | Result propagated to gate_enforcer | Tests written and passing
- smoke_test: cd browser && npx vitest run src/shell/
