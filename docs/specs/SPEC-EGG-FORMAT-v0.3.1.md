
SPEC-EGG-FORMAT
v0.3.1
EGG Format Canonical Specification
ShiftCenter Platform  ·  8OS  ·  SimDecisions
2026-03-09  ·  Status: DRAFT — NOT FOR EXTERNAL DISTRIBUTION
Supersedes: SPEC-EGG-FORMAT-v0.3  (patch: Section 2 framing correction + type registry)
Referenced by: SDK-APP-BUILDER-v0.3, SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3

1. What Is an EGG
An EGG is a structured configuration document that defines how a ShiftCenter deployment behaves. It is the single source of truth for layout, permissions, modes, startup behavior, and UI chrome for a given product surface. Every subdomain — shiftcenter.com, code.shiftcenter.com, efemera.live, simdecisions.com, and any customer deployment — runs as an EGG.

The EGG is not an app. It is a container that declares which applets to mount, in what arrangement, with what permissions and constraints. The inflater reads the EGG and produces a running ShiftCenter instance. The shell (HiveHostPanes) is oblivious to product identity — it only knows what the EGG told it.

This spec defines the EGG format contract. It is consumed by:
The EGG inflater (eggInflater.ts) — parses and validates the EGG, produces eggContext
The shell (HiveHostPanes.jsx) — reads eggContext to configure itself
The GovernanceProxy — reads EGG permissions to enforce capability ceilings
The EGG validator — checks EGG files before deploy
The EGG resolver (eggResolver.ts) — maps hostname/URL param to EGG ID
SDK-APP-BUILDER-v0.3 — the developer guide that references this spec

2. EGG Types
The type field in frontmatter is a discriminator within an open registry — not a closed enum. New types can be defined by platform authors or GC contributors. The full type registry is maintained in EGG-IDEAS-001 and will migrate to a formal registry document at v1.0.

The original EGG concept — predating the ShiftCenter shell by months — is type: hive: a structured .md file that hatches into a complete operational hive (Q33N + bees + KB + config). This spec governs two types relevant to the ShiftCenter shell runtime. They are shell-specific use cases within the broader EGG ecosystem, not the definition of what an EGG is.

2.1  type: app  (ShiftCenter Product Surface)
A shell-inflatable EGG. Defines a complete product surface with layout, applets, permissions, and behavior. The inflater reads it and mounts HiveHostPanes with the resulting eggContext. Used for shiftcenter.com, code.shiftcenter.com, efemera.live, and all subdomain deployments. Active since March 2026.
⚑  type: app is not the primary EGG type — it is one of many. It is primary only within the context of this spec, which covers shell behavior exclusively.

2.2  type: config  (Boot-Loaded Shell Registry)
A non-inflatable EGG loaded at shell boot time, before any app EGG inflates. Config EGGs have no layout block and are never rendered as a product surface. They populate registries and translation tables that the shell inflater needs before processing an app EGG.

Three config EGGs are required at shell boot:
registry.config.egg — applet registry. All known appTypes with metadata (label, icon, accepts patterns, trust tier, loader path). Replaces the hardcoded APP_REGISTRY in shell.constants.js.
schema-v1.config.egg — field translation table. Maps legacy field names (id → nodeId, appConfig → config) for EGGs with schema_version: 1. Kept permanently — never deleted. Old EGGs always work.
routing.config.egg — hostname-to-EGG-ID routing map. Replaces the hardcoded SUBDOMAIN_EGG_MAP in eggResolver.ts. See Section 14.
⚑  Config EGGs are boot-loaded once and cached. They are tiny, immutable, and versioned. Adding a new platform applet = ship a new registry.config.egg. Zero shell code changes.

2.3  Other EGG Types (Out of Scope for This Spec)
For reference only. These types are defined elsewhere and are not governed by this spec:
hive — original type. Complete hive runtime package (.md file that hatches into an operational hive). See HiveEgg spec.
ir — PHASE-IR document envelope.
skill — governance-wrapped skill manifest.
persona — character/agent persona definition (.persona.egg files).
entitlement / transit / world / doc / template / cap-bom / schema / mesh-packet — proposed or exploratory. See EGG-IDEAS-001.

3. Frontmatter Block
All EGGs begin with a YAML frontmatter block. Required for both app and config types.

Required fields
schema_version: 3        # Integer. 1=legacy, 2=v2 format, 3=this spec.
type: app                 # Open registry. "app" | "config" are shell types. See Section 2.
eggId: code-default       # Unique ID. Must match registry.config.egg entry.
name: "ShiftCenter Code"  # Human-readable product name.

Optional fields
description: "IDE surface for code.shiftcenter.com"
author: "SimDecisions Platform Team"
version: "1.0.0"
subdomain: "code.shiftcenter.com"   # Informational only. Resolver owns routing.
headless: true                        # EGG flag for Efemera mode (no chrome).
devOverride: true                     # Enables local dev overrides. Never ships to prod.

⚑  schema_version controls which field translation table the inflater uses. schema_version: 3 passes through as-is. schema_version: 1 runs through schema-v1.config.egg field map. schema_version: 2 runs through schema-v2.config.egg if it exists.

4. Layout Block
The layout block defines the initial pane tree. Present only in type: app EGGs. The inflater reads this and produces the shell's initial state.root.

4.1  Root Structure
The root is always a branches object with four named trunk branches:
layout:
  type: branches
  layout: <node>        # The primary tiled layout tree. Required.
  float: []             # Array of floating pane nodes. Optional.
  pinned: []            # Array of fixed-position pinned pane nodes. Optional.
  spotlight: null       # Single spotlight overlay node, or null. Optional.

4.2  Node Types
app node  (leaf)
- type: app
  nodeId: frank-terminal      # Stable ID. Survives EGG swaps. Required.
  appType: ai-assistant        # Matches an entry in registry.config.egg. Required.
  label: "Frank"              # Display label in pane chrome. Optional.
  config: {}                  # Applet-specific config. Passed to applet as props. Optional.
  loadState: COLD             # COLD | WARM | HOT. Default: COLD. Optional.
  locked: false               # If true: no drag, no close, no swap. Optional.
  chrome: false               # If false: no title bar, no drag handle, no PaneMenu,
                              #   not draggable, not swappable, position fixed. Optional.
  sizeStates:                 # Named size breakpoints. Applet reads its own height. Optional.
    full:    { minHeight: 200 }
    compact: { minHeight: 48, maxHeight: 199 }
    minimal: { minHeight: 32, maxHeight: 47 }
  defaultState: collapsed     # full | collapsed | mini. Overrides loadState. Optional.
  permissions: {}             # Applet-level permission overrides. See Section 6. Optional.

⚑  chrome: false is a hard lock. It cannot be overridden by the user at runtime. An EGG that declares chrome: false on a node means: this pane's position is permanently fixed by the EGG. The shell enforces this — no drag handle is rendered, the SwapTarget overlay is suppressed, and the node is excluded from all user-initiated position changes.

split node  (binary)
- type: split
  nodeId: main-split
  direction: horizontal      # "horizontal" (top/bottom) | "vertical" (left/right)
  ratio: 0.5                 # 0.0–1.0. First child gets this fraction.
  children:
    - <node>                 # Exactly 2 children.
    - <node>

triple-split node  (three-way, first class)
- type: triple-split
  nodeId: code-layout
  direction: horizontal      # "horizontal" (3 columns) | "vertical" (3 rows)
  ratios: [0.18, 0.60, 0.22] # Must sum to 1.0. Left/top, middle, right/bottom.
  children:
    - <node>                 # Exactly 3 children.
    - <node>
    - <node>
⚑  triple-split is not syntactic sugar for nested binary splits. It is a first-class node type rendered with two independent dividers. Each divider can be dragged without affecting the other. Use this for three-column IDE layouts, three-row document layouts, and any composition requiring three sibling panes.

tabbed node
- type: tabbed
  nodeId: editor-tabs
  activeTabIndex: 0
  tabs:
    - <app node>            # Any number of app nodes.
    - <app node>

4.3  Float, Pinned, and Spotlight Nodes
float: [] — Draggable, resizable. Not in tiled layout. Uses react-draggable + react-resizable. Stacking order by array position (last = topmost).
pinned: [] — Fixed-position. Not draggable. Orange border to distinguish from layout panes. Often used for persistent notification panels.
spotlight: <node> — Single node. Always-on-top with full backdrop. Used for REQUIRE_HUMAN gates and critical confirmations. Dismissing returns focus to layout.

4.4  The Handle — Resize, Collapse, and Slides-Over
Every split and triple-split border has a single handle control. Its behavior depends on drag direction and current pane state:


⚑  Slides-over floats respect z-order and sit above all other floats while active. A slides-over float from a chrome: false pane remains chrome-free — no title bar appears because it floated. Slides-over cannot cover a spotlight node.

⚑  Triple-split: the middle pane has two handles — one on each border. Dragging the left border outward slides over the left pane. Dragging the right border outward slides over the right pane.

5. Startup Block
The startup block is processed by startupManager.ts after EGG inflate. It is optional. If absent, no startup sequence runs.
startup:
  sessionRestore: true               # Restore prior layout and tabs. Default: false.
  sessionRestoreScope: perUser        # "perUser" | "perDevice" | "none".
  restoreOrder: sessionFirst          # "sessionFirst" | "defaultFirst".
  defaultDocuments:
    - src: "gc://docs/welcome.md"     # GC path or URL. Required.
      nodeId: editor-pane             # Target pane. Required.
      label: "Welcome"               # Tab label. Optional.
      condition: firstTabAlways       # "always"|"firstRunOnly"|"firstTabAlways"|"never"
    - src: "gc://docs/changelog.md"
      nodeId: editor-pane
      label: "Changelog"
      condition: firstRunOnly

Condition values:
always — opens every time the EGG inflates.
firstRunOnly — opens once per device (localStorage flag). Never again after.
firstTabAlways — opens once per browser session (sessionStorage flag). Default.
never — never opens. Used to disable an entry without removing it.
⚑  The startup sequence has a 3-second hard timeout. Individual document fetches have a 3-second timeout. Failures are logged to Event Ledger and skipped — they never block inflate.

6. Permissions Block
The permissions block is the EGG's capability declaration. It functions as the CAP-BOM (Capability Bill of Materials) for everything that runs inside the EGG. The GovernanceProxy enforces these declarations at runtime.

6.1  EGG-Level Permissions  (the ceiling)
permissions:
  tools:                             # Allowed tool types for any applet in this EGG.
    - web_search
    - wolfram_adapter
  bus_emit:                          # Allowed bus message types this EGG's applets may send.
    - menu_advertisement
    - metrics_advertisement
    - context_advertisement
    - REQUEST_FLOAT_EXPAND
  bus_receive:                       # Allowed bus message types this EGG's applets may receive.
    - menu_command
    - settings_update
    - context_advertisement
  require_human:                     # Actions requiring explicit human approval.
    - condition: outbound_social_post
      locked_by: enterprise          # enterprise | platform | null
    - condition: financial_transaction
      locked_by: platform
    - condition: autonomous_queue_launch
      locked_by: null               # User may remove this.
  autonomy:
    default_scope: per_action        # per_action | per_session | at_launch
    exception_classes:               # Always re-gate regardless of autonomy_scope.
      - irreversible_destructive
      - out_of_declared_scope
      - agent_flagged_uncertain
  max_tokens_per_session: 50000
  byok:
    vendor_trust: false              # Default. User can set true per-vendor. EGG cannot.
  chrome: false                      # EGG-level chrome suppression (headless mode).

6.2  Applet-Node-Level Permissions  (per-pane tightening)
Any app node in the layout block may declare a permissions sub-block. Applet-node permissions can only tighten the EGG ceiling — they cannot grant capabilities the EGG did not permit.
- type: app
  nodeId: restricted-terminal
  appType: ai-assistant
  permissions:
    tools:
      - web_search              # Subset of EGG tools. wolfram_adapter not available here.
    max_tokens_per_session: 10000  # Lower than EGG ceiling of 50000.
    require_human:
      - condition: any_outbound  # Tighter than EGG.
        locked_by: null

The GovernanceProxy computes the effective permissions for each applet as the intersection of EGG-level and node-level declarations. If a node lists a tool not in the EGG permissions, it is silently ignored. The EGG is always the ceiling.

6.3  REQUIRE_HUMAN Hierarchy
Four layers, each can only tighten. No lower layer overrides a higher one.

6.4  Default Permissions for Undecorated EGGs
If an EGG has no permissions block: platform EGGs (shipped with ShiftCenter, signed by SimDecisions) get allow-all defaults. GC-published EGGs (Global Commons applets from external authors) get deny-unknown defaults — no tools, no bus_emit beyond safe defaults, no autonomous operations. Trust tier is set in registry.config.egg per appType.

7. Modes Block
Modes allow an EGG to declare alternate configurations that activate in response to user or system events. The Mode Engine (modeEngine.ts) manages enter/exit/toggle.
modes:
  focus:
    label: "Focus Mode"
    nodes:
      sidebar-pane:
        hidden: true          # Layout instruction only. Not passed to applet.
      editor-pane:
        config:               # Merged into applet config when mode is active.
          lineNumbers: true
    ui:
      hideMenuBar: true
      hideTabBar: false
    away:
      idleTimeoutMs: 300000
⚑  The hidden flag in node config deltas is stripped before passing to the applet. It is a shell layout instruction only. The applet never sees it. The shell sets the pane to WARM when hidden, HOT when unhidden.

8. GovernanceProxy
The GovernanceProxy wraps every applet before mount. It enforces the permissions declared in Section 6. The applet does not know it is wrapped.

8.1  Intercept Points
MessageBus.send() — Primary intercept. Before any pane-to-pane message is delivered, the proxy checks the sender's node permissions against the EGG bus_emit list. Blocked messages are dropped and logged to the Event Ledger as GOVERNANCE_BLOCKED events.
Tool adapter calls — At the tool adapter boundary, before any call leaves the shell environment. Enforces tools[] permissions.
Autonomous action gates — At task dispatch time. Enforces require_human and autonomy_scope declarations.

8.2  Distinction from GateEnforcer and TSaaS
⚑  TSaaS content scanning (PII check, outbound inspection) fires at the tool adapter for any content leaving the user's environment — LLM API calls, social posts, external API writes. BYOK users may set vendor_trust: true per-vendor in their user settings to disable content scanning for that vendor only. This is a user-level sovereignty choice. An EGG cannot set vendor_trust: true — that decision belongs to the user, not the platform.

9. The Two Buses
Two message bus implementations exist in the codebase. They serve different purposes and must not be confused.

9.1  MessageBus  (shell.context.js)
The pane-to-pane bus. Applets use this exclusively for inter-applet communication. Pane-aware, nonce-tracked, telemetry-instrumented, replay-protected. Subscriptions are keyed by paneId. GovernanceProxy intercepts here. This is the bus the EGG permissions block governs.

9.2  bus.ts  (global pub/sub)
Internal service-to-service bus. Routes by message type only. No pane awareness, no nonces, no replay protection. Used for shell-internal coordination between services (modeEngine, awayManager, startupManager). Applets do not interact with this bus. GovernanceProxy does not intercept here.
⚑  Applets that import bus.ts directly are violating the architecture. All applet communication goes through MessageBus via the useShell() hook.

9.3  context_advertisement  (MessageBus pattern)
Any applet that becomes the active/focused pane may publish a context_advertisement message. Layout applets (contextual drawers, toolbars, status strips) subscribe and adapt their contents accordingly.
// Published by any applet when it becomes focused:
{
  type: "context_advertisement",
  fromPaneId: "designer-pane",
  target: "*",
  appType: "designer",
  offers: {
    toolbar: "designer-toolbar-v1",    // Key into drawer applet's own registry.
    properties: "designer-props-v1",
  }
}
⚑  Last-focused applet wins if multiple applets advertise simultaneously. Drawers have fallback contents for when nothing is advertising. The cross-fade transition between contexts is 150ms.

10. Applet Registry and Dispatch
The hardcoded APP_REGISTRY in shell.constants.js and the hardcoded dispatch table in AppFrame.jsx are replaced by the registry.config.egg system.

10.1  registry.config.egg  (metadata)
Lists all known appTypes with display and routing metadata. Read at boot. Replaces APP_REGISTRY.
schema_version: 3
type: config
registry:
  - appType: ai-assistant
    label: "Frank"
    icon: "terminal"
    accepts: ["text/*", "application/json"]
    trustTier: platform       # platform | gc | external
    loaderPath: "platform:ai-assistant"  # Signals platform bundle loader.
    description: "Natural language command interface."
  - appType: designer
    label: "Designer"
    icon: "flow"
    accepts: ["application/x-phase-ir"]
    trustTier: platform
    loaderPath: "platform:designer"

10.2  AppFrame Dispatch  (stays in code)
The mapping of appType string to React component cannot live in a config EGG — React components are not JSON-serializable. AppFrame.jsx becomes a dynamic loader, not a switch statement:
Platform applets (trustTier: platform) — loaded from the bundled module registry by name. loaderPath: "platform:designer" → import the platform designer module. Fast, trusted, no network.
GC applets (trustTier: gc) — loaded at runtime from global-commons://applets/. Sandboxed. Cached after first load.
The EGG declares appType. AppFrame looks it up in the registry. Registry says loader path. AppFrame loads the component. EGG is agnostic to whether the applet is bundled or remote.

11. Storage
All persistent storage uses the named volume system (SPEC-HIVE-DISPATCH-GOVERNANCE-001-v3). No raw localStorage or sessionStorage calls in applet or shell code.

local://shell/layout-tree — Shell layout tree. Previously sd:hhpanes_tree in localStorage. Migrated.
local://shell/theme — Active theme. Previously sd:hhpanes_theme.
local://shell/workspaces — Saved workspace snapshots.
local://startup/{eggId}/{src} — firstRunOnly flags (startup sequence).
session://startup/{eggId}/{src} — firstTabAlways flags (current browser session).
⚑  Shell layout state is infrastructure, not user content. It uses local:// volumes. It does not route through cloud volumes unless the user explicitly enables cross-device sync in settings.

12. Hard Rules
These rules are invariant. No EGG, applet, or configuration can override them.

HARD RULE 1: The EGG is a ceiling, not a floor. Applets cannot exceed the capabilities declared in the EGG permissions block. The GovernanceProxy enforces this silently.
HARD RULE 2: Applet-node permissions can only tighten. A node-level permissions block is intersected with the EGG permissions. It cannot grant capabilities the EGG did not allow.
HARD RULE 3: chrome: false is permanent and user-cannot-override. No drag, no swap, no PaneMenu, position fixed by EGG.
HARD RULE 4: Platform invariants (relay_bus, ledger_writer, gate_enforcer) are always on. No EGG suppresses them.
HARD RULE 5: GC applets default to deny-unknown permissions. Trust must be explicitly granted in the EGG permissions block.
HARD RULE 6: The layout tree is stored in local://shell/layout-tree. No applet or shell code writes layout state to raw localStorage directly.
HARD RULE 7: Applets communicate only through MessageBus (useShell().bus). Direct use of bus.ts in applet code is an architecture violation.
HARD RULE 8: vendor_trust: true is a user-level setting only. EGGs cannot set it. Granting a vendor trust is the user's sovereignty decision, not the platform's.
HARD RULE 9: Shell.tsx is deprecated. HiveHostPanes.jsx is the canonical shell. No new code references Shell.tsx.
HARD RULE 10: triple-split children must be exactly 3. ratios must sum to 1.0. split children must be exactly 2. The inflater rejects malformed trees.

13. Inflater Pipeline
The EGG inflater (eggInflater.ts) executes the following sequence on every EGG inflate:

Load schema-v1.config.egg (and any other schema config EGGs) to initialize field translation tables.
Load registry.config.egg to initialize the applet registry.
Parse the target EGG frontmatter. Read schema_version and type.
Run field translation if schema_version < 3 (map id→nodeId, appConfig→config, etc.).
Validate the translated EGG against the v0.3 schema. Reject and log if invalid.
Build the GovernanceProxy configuration from the permissions block. Compute effective permissions for each node (EGG ∩ node).
Wrap each applet mount in GovernanceProxy before passing to AppFrame.
Produce eggContext with the following shape:
eggContext = {
  eggId: string,
  ui: { hideMenuBar: bool, hideTabBar: bool },
  away: AwayConfig | null,
  startupConfig: StartupConfig | null,
  tabs: EggTab[] | null,
  settings: EggSettings | null,
  permissions: ResolvedPermissions,   // Computed in step 6.
  modeRegistry: ModeRegistry | null,
}
Pass eggContext to HiveHostPanes as a prop. Shell inflates.
After inflate: run startupManager.run(context) asynchronously. Never blocks inflate.

14. EGG Resolver
eggResolver.ts maps the current hostname to an EGG ID. The hardcoded SUBDOMAIN_EGG_MAP moves to a routing.config.egg, making routing configurable without code changes.
# routing.config.egg
schema_version: 3
type: config
routing:
  subdomains:
    code.shiftcenter.com: code-default
    shiftcenter.com: home
    efemera.live: efemera
    simdecisions.com: simdecisions-home
    localhost: code-default
  fallback: home
  urlParam: egg            # ?egg=turtle-draw overrides hostname routing.

15. Open Items
These items are deferred and must be resolved before v1.0:

EGG signing/provenance — how platform EGGs are signed and verified before inflate. Blocks GC launch.
EGG inheritance — can an EGG extend another EGG and override specific blocks? Schema and override rules not yet defined.
Marketplace schema — how GC-published EGGs are listed, reviewed, and distributed.
syndicatesMenu / syndicatesSettings — whether these belong in the EGG node schema or as applet runtime declarations. Pending decision.
formalize startup block in eggInflater.ts type definitions — StartupConfig and DefaultDocument types exist; confirm against this spec.
GovernanceProxy implementation spec — what the inflater enforcement model looks like in TypeScript. This spec defines behavior; implementation spec defines code structure.
schema-v2.config.egg — if needed for field map between v2 and v3 format. Check existing v2 EGGs before writing.

16. Changelog from v2

NEW: schema_version and type in frontmatter — required fields.
NEW: type: config (boot-loaded EGG) — registry.config.egg, schema-v1.config.egg, routing.config.egg.
NEW: permissions block — EGG-level and applet-node-level. GovernanceProxy enforcement model.
NEW: triple-split node type — first-class, two independent dividers, three children, two ratios.
NEW: sizeStates on app nodes — multi-state responsive behavior driven by height.
NEW: Handle behavior table — resize, collapse, slides-over from a single pane border control.
NEW: slides-over mechanism — REQUEST_FLOAT_EXPAND bus message, retract on completion.
NEW: REQUIRE_HUMAN hierarchy — four layers, locked_by field, enterprise lock.
NEW: autonomy block — autonomy_scope, exception_classes, at_launch gate model.
NEW: TSaaS split — governance layer (never disable) vs content scan layer (BYOK opt-out).
NEW: context_advertisement bus pattern — applets broadcast context; drawers/toolbars respond.
NEW: Applet registry via config EGG — replaces hardcoded APP_REGISTRY. AppFrame becomes dynamic loader.
NEW: Routing via routing.config.egg — replaces hardcoded SUBDOMAIN_EGG_MAP.
NEW: Storage via named volumes — local://shell/* replaces raw localStorage keys.
NEW: startup block formally specified from startupManager.ts source.
NEW: Hard Rules extended to 10 (was 8). Shell.tsx deprecated.
RENAMED: appType "terminal" → "ai-assistant" throughout. The ai-assistant is a natural language interface, not a terminal emulator.
LOCKED: Two-bus distinction (MessageBus vs bus.ts). Applets use MessageBus only.
LOCKED: HiveHostPanes.jsx is the canonical shell. Shell.tsx deprecated, flagged for removal.

SPEC-EGG-FORMAT-v0.3.1  ·  daaaave-atx x Claude (Anthropic)  ·  CC BY 4.0  ·  2026-03-09