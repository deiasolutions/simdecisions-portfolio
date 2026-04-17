# PRISM-IR: Factory Dual-Loop Process v1.1

```yaml
prism_version: "1.0.0"
process_id: FACTORY-DUAL-LOOP-001
version: "1.1.0"
title: "Adaptive Factory with Spec Loop and Build Loop"
description: |
  Two parallel loops operating on one tree (or DAG when shared modules exist):
  - SPEC LOOP: Ideas decompose into specs until leaves are build-ready
  - BUILD LOOP: Specs at leaves enter factory, products come out
  Bundling is a routing decision based on granularity fit, operator fit, and vendor fit.
  
  v1.1 changes:
  - Added FAILED to phase enum
  - Added node_type for DAG support (ORIGINAL vs SHARED_REF)
  - Added depends_on for non-parent dependencies
  - Added acceptance_criteria per node
  - Added building_ttl_seconds for stall detection
  - Added max_bundle_tokens guard
  - Split learning into telemetry_log vs policy_recommendation
author: Q33NR + Q88N
created: 2026-04-07
updated: 2026-04-07
status: PROPOSAL
```

---

## 1. ENTITIES

### 1.1 Node (Tree/DAG Element)

Every item in the system is a node. Nodes form a tree, or a DAG when shared modules are extracted.

```yaml
entity: Node
attributes:
  # Identity
  - id: string                    # e.g., "IDEA-001-A-2-b"
  - parent_id: string|null        # null for roots
  - root_id: string               # ancestor root for lineage queries
  - branch_path: list             # ["001", "A", "2", "b"]
  
  # DAG support
  - node_type: enum               # ORIGINAL | SHARED_REF
  - target_id: string|null        # if SHARED_REF, points to ORIGINAL node
  
  # Dependencies (beyond parent)
  - depends_on: list[string]      # node IDs this node requires (siblings, cousins, etc.)
  
  # Content
  - title: string
  - description: string
  - output_type: enum             # PLAN | PRODUCT
  - content_type: string|null     # e.g., "python_file", "react_component", "architecture_doc"
  
  # Lifecycle
  - phase: enum                   # IDEA | SPECCING | SPECCED | BUILDING | BUILT | INTEGRATED | FAILED
  - status: enum                  # PENDING | IN_PROGRESS | SUCCEEDED | FAILED | BLOCKED
  - attempts: integer             # how many times execution attempted
  - split_reason: string|null     # if split, why
  - failure_reason: string|null   # if FAILED, why
  
  # Routing
  - model_used: string|null       # which model succeeded (or last failed)
  - routing_affinity: object|null # operator/vendor preferences
  
  # Acceptance
  - acceptance_criteria: object   # typed contract for what "accepted" means (see 1.2)
  
  # Hierarchy
  - children: list[string]        # child node IDs
  
  # Timestamps
  - created_at: timestamp
  - updated_at: timestamp
  - building_started_at: timestamp|null  # for TTL enforcement
```

### 1.2 Acceptance Criteria (Per Node)

Each node defines what "accepted" means. Schema varies by output_type and content_type.

```yaml
entity: AcceptanceCriteria
variants:
  
  # For PRODUCT nodes producing code
  - content_type: "python_file"
    criteria:
      - syntax_valid: boolean       # compiles without syntax errors
      - imports_resolve: boolean    # all imports available
      - tests_pass: boolean|null    # if tests provided, they pass
      - linting_clean: boolean      # passes configured linter
      - type_check: boolean|null    # if typed, passes mypy/pyright
      - custom_checks: list[string] # additional validation scripts
  
  # For PRODUCT nodes producing React components
  - content_type: "react_component"
    criteria:
      - syntax_valid: boolean
      - builds_clean: boolean       # no build errors
      - renders_without_crash: boolean
      - tests_pass: boolean|null
      - accessibility_check: boolean|null
  
  # For PLAN nodes producing architecture docs
  - content_type: "architecture_doc"
    criteria:
      - sections_present: list[string]  # required sections
      - diagrams_valid: boolean|null    # if diagrams, they parse
      - round_trip_valid: boolean       # survives English→IR→English
  
  # For PLAN nodes producing task decomposition
  - content_type: "task_decomposition"
    criteria:
      - children_defined: boolean       # all children have IDs and titles
      - no_orphan_refs: boolean         # all depends_on refs are valid
      - coverage_complete: boolean      # children cover parent scope
  
  # Fallback for untyped nodes
  - content_type: null
    criteria:
      - human_approved: boolean         # requires REQUIRE_HUMAN gate
```

### 1.3 Bundle (Dispatch Grouping)

Bundles are ephemeral dispatch-time groupings. They are NOT tree nodes.

```yaml
entity: Bundle
attributes:
  - bundle_id: string
  - spec_ids: list[string]            # node IDs included
  - bundle_reason: enum               # GRANULARITY_FIT | OPERATOR_FIT | VENDOR_FIT
  - operator_id: string|null
  - vendor_id: string|null
  - estimated_tokens: integer         # total tokens estimated for bundle
  - status: enum                      # PENDING | DISPATCHED | SUCCEEDED | FAILED | UNBUNDLED
  - created_at: timestamp
  - dispatched_at: timestamp|null
  - completed_at: timestamp|null
```

### 1.4 Operator

An operator is an execution context — a model, a human, an API endpoint.

```yaml
entity: Operator
attributes:
  - operator_id: string
  - type: enum                        # LLM | HUMAN | API
  - vendor_id: string
  - capabilities:
      max_context_tokens: integer     # context window size
      max_output_tokens: integer
      specializations: list[string]   # e.g., ["python", "react", "architecture"]
      batch_preference: enum          # NONE | PREFERRED | REQUIRED
      success_rate_by_scope: object   # historical data
  - cost_profile:
      coin_per_input_token: float
      coin_per_output_token: float
      clock_latency_ms: integer       # typical response time
      carbon_per_call: float          # CO2e estimate
  - batch_mode: boolean               # true if operator prefers/requires batches
```

### 1.5 Configuration

System-level settings.

```yaml
entity: FactoryConfig
attributes:
  - max_depth: integer                # maximum branch_path length before escalation
  - max_attempts: integer             # maximum attempts per node before escalation
  - building_ttl_seconds: integer     # TTL for BUILDING phase before marking stale
  - max_bundle_tokens: integer        # maximum tokens per bundle (must fit operator context)
  - token_buffer_ratio: float         # reserve ratio (e.g., 0.8 = use 80% of context window)
  - default_operator_id: string       # fallback operator
  - three_currency_weights:
      clock: float                    # weight for latency optimization
      coin: float                     # weight for cost optimization
      carbon: float                   # weight for emissions optimization
```

---

## 2. STATES

### 2.1 Node Phases

```
IDEA ──► SPECCING ──► SPECCED ──► BUILDING ──► BUILT ──► INTEGRATED
  │         │            │           │            │
  │         │            │           │            └──► [parent integration]
  │         │            │           │
  │         │            │           └──► FAILED ──► [split or escalate]
  │         │            │
  │         │            └──► [children enter SPECCING or BUILDING]
  │         │
  │         └──► [decompose into child nodes]
  │
  └──► [initial state]
```

| Phase | Meaning |
|-------|---------|
| IDEA | Raw concept, not yet decomposed |
| SPECCING | Being broken down into child specs |
| SPECCED | All children defined; leaves are build-ready |
| BUILDING | Spec dispatched to build loop |
| BUILT | Product produced and accepted |
| INTEGRATED | Product merged into parent deliverable |
| FAILED | Execution failed; pending split, retry, or escalation |

### 2.2 Node Status (Orthogonal to Phase)

| Status | Meaning |
|--------|---------|
| PENDING | Awaiting action |
| IN_PROGRESS | Currently being worked |
| SUCCEEDED | Last action succeeded |
| FAILED | Last action failed |
| BLOCKED | Waiting on dependencies |

### 2.3 Bundle States

```
PENDING ──► DISPATCHED ──► SUCCEEDED
                │               │
                │               └──► [each spec marked BUILT]
                │
                └──► FAILED ──► UNBUNDLED
                                    │
                                    └──► [specs return to ready queue individually]
```

---

## 3. SPEC LOOP (Planning)

The spec loop grows the tree downward until leaves are atomic enough to build.

```
┌─────────────────────────────────────────────────────────────────┐
│                         SPEC LOOP                               │
│                                                                 │
│   ┌──────────┐      ┌──────────────┐      ┌──────────────┐     │
│   │   IDEA   │ ───► │   SPECCING   │ ───► │   SPECCED    │     │
│   │  (root)  │      │ (decompose)  │      │ (leaves OK)  │     │
│   └──────────┘      └──────────────┘      └──────────────┘     │
│                            │                     │              │
│                            ▼                     ▼              │
│                     ┌────────────┐        ┌────────────┐        │
│                     │ Child Node │        │ Leaf ready │        │
│                     │  (IDEA)    │        │ for BUILD  │        │
│                     └────────────┘        └────────────┘        │
│                            │                     │              │
│                            ▼                     │              │
│                      [recurse]                   │              │
│                                                  ▼              │
│                                         ════════════════        │
│                                         ║ BUILD LOOP  ║        │
│                                         ════════════════        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 Spec Loop Process

```yaml
process: spec_loop
trigger: Node enters IDEA phase OR child completion triggers parent re-evaluation
steps:
  - id: evaluate_node
    action: ASSESS
    input: node
    output: decision
    description: |
      Is this node atomic enough to build?
      - If output_type = PRODUCT and scope is small: YES → mark SPECCED, eligible for build
      - If output_type = PLAN or scope too large: NO → decompose

  - id: decompose
    action: SPLIT
    condition: decision = "decompose"
    input: node
    output: child_nodes[]
    description: |
      Break node into children. Each child:
      - Gets unique ID: {parent.id}-{index}
      - Inherits root_id from parent
      - Starts in IDEA phase
      - output_type assigned (PLAN or PRODUCT)
      - content_type assigned if known
      - acceptance_criteria defined based on content_type
      - depends_on populated if cross-branch dependencies exist

  - id: recurse
    action: LOOP
    condition: child_nodes exist
    description: Each child enters spec_loop

  - id: mark_specced
    action: UPDATE
    condition: all children SPECCED or node is atomic leaf
    input: node
    output: node.phase = SPECCED
    description: |
      Node is fully specified. If output_type = PRODUCT, 
      node is eligible for build loop.
```

### 3.2 Spec Validation (Round-Trip)

```yaml
process: spec_validation
trigger: Spec written in English
steps:
  - id: english_to_ir
    action: TRANSLATE
    input: english_spec
    output: ir_spec
    description: Convert English spec to PRISM-IR

  - id: ir_to_english
    action: TRANSLATE
    input: ir_spec
    output: english_roundtrip
    description: Convert IR back to English

  - id: compare
    action: VALIDATE
    input: [english_spec, english_roundtrip]
    output: validation_result
    description: |
      Did the spec survive the round trip?
      - If YES: IR is solid, proceed
      - If NO: spec is ambiguous, refine and retry

  - id: proceed_or_refine
    action: BRANCH
    condition: validation_result
    branches:
      - condition: valid
        next: mark_specced
      - condition: invalid
        next: refine_spec → english_to_ir
```

---

## 4. BUILD LOOP (Execution)

The build loop consumes SPECCED leaves and produces BUILT products.

```
┌─────────────────────────────────────────────────────────────────┐
│                         BUILD LOOP                              │
│                                                                 │
│   ┌──────────┐      ┌──────────────┐      ┌──────────────┐     │
│   │  READY   │ ───► │   ROUTING    │ ───► │  DISPATCH    │     │
│   │  QUEUE   │      │  (bundle?)   │      │  (execute)   │     │
│   └──────────┘      └──────────────┘      └──────────────┘     │
│        ▲                   │                     │              │
│        │                   ▼                     ▼              │
│        │            ┌────────────┐        ┌────────────┐        │
│        │            │  BUNDLE    │        │   BEE      │        │
│        │            │ (grouped)  │        │ (executes) │        │
│        │            └────────────┘        └────────────┘        │
│        │                   │                     │              │
│        │                   ▼                     ▼              │
│        │            ┌────────────┐        ┌────────────┐        │
│        │            │  DISPATCH  │        │  OUTPUT    │        │
│        │            │  (batch)   │        │ (product)  │        │
│        │            └────────────┘        └────────────┘        │
│        │                   │                     │              │
│        │                   ▼                     ▼              │
│        │            ┌─────────────────────────────────┐         │
│        │            │         EVALUATE OUTPUT         │         │
│        │            │    (apply acceptance_criteria)  │         │
│        │            └─────────────────────────────────┘         │
│        │                          │                             │
│        │              ┌───────────┴───────────┐                 │
│        │              ▼                       ▼                 │
│        │       ┌──────────┐           ┌──────────────┐          │
│        │       │ ACCEPTED │           │   REJECTED   │          │
│        │       │  (BUILT) │           │   (FAILED)   │          │
│        │       └──────────┘           └──────────────┘          │
│        │              │                       │                 │
│        │              ▼                       ▼                 │
│        │       ┌──────────┐           ┌──────────────┐          │
│        │       │ COMPLETE │           │    SPLIT     │          │
│        │       │  (done)  │           │ (decompose)  │          │
│        │       └──────────┘           └──────────────┘          │
│        │                                      │                 │
│        └──────────────────────────────────────┘                 │
│                  (children re-enter ready queue)                │
└─────────────────────────────────────────────────────────────────┘
```

### 4.1 Build Loop Process

```yaml
process: build_loop
trigger: Node reaches SPECCED with output_type = PRODUCT
steps:
  - id: check_dependencies
    action: EVALUATE
    input: node.depends_on
    output: deps_satisfied
    description: |
      Check all dependencies (parent AND depends_on list):
      - All referenced nodes must be BUILT or INTEGRATED
      - If any dependency not met: node.status = BLOCKED, wait

  - id: enter_ready_queue
    action: ENQUEUE
    condition: deps_satisfied
    input: node
    output: node in ready_queue
    description: Leaf spec enters ready queue for dispatch

  - id: routing_decision
    action: EVALUATE
    input: ready_queue, operators[], vendors[], config
    output: dispatch_plan
    description: |
      Scheduler evaluates:
      1. GRANULARITY FIT: Can any operator handle multiple specs together?
      2. OPERATOR FIT: Does any operator prefer/require batches?
      3. VENDOR FIT: Is bundling economical for any vendor?
      4. CONTEXT WINDOW CHECK: Does bundle fit in operator's max_context_tokens?
      
      Output: individual specs OR bundles (respecting max_bundle_tokens)

  - id: form_bundles
    action: GROUP
    condition: bundling advantageous AND fits context window
    input: spec_ids[], bundle_reason, estimated_tokens
    output: Bundle
    description: |
      Create bundle envelope. Bundle is NOT a tree node.
      Specs retain their lineage. Bundle is dispatch-time grouping.
      
      Guard: estimated_tokens <= operator.max_context_tokens * config.token_buffer_ratio

  - id: dispatch
    action: EXECUTE
    input: spec OR bundle
    output: execution_started
    description: |
      - Move spec(s) to _active/
      - Set node.building_started_at = now()
      - Spawn bee subprocess (or human task, or API call)
      - Track operator, model, start time

  - id: execute
    action: WORK
    input: spec content, operator
    output: raw_output
    description: Bee produces output (code, artifact, documentation)

  - id: evaluate_output
    action: VALIDATE
    input: raw_output, node.acceptance_criteria
    output: evaluation_result
    description: |
      Apply typed acceptance criteria for this node:
      - Run all checks defined in acceptance_criteria
      - All must pass for acceptance
      - Partial pass → identify which failed

  - id: accept_or_reject
    action: BRANCH
    input: evaluation_result
    branches:
      - condition: all_criteria_passed
        next: mark_built
      - condition: criteria_failed
        next: handle_failure

  - id: mark_built
    action: UPDATE
    input: node
    output: |
      node.phase = BUILT
      node.status = SUCCEEDED
    description: |
      Product accepted. Node complete.
      - Move spec to _done/
      - Record model_used, completion time
      - Trigger parent re-evaluation
      - Trigger dependents re-evaluation (nodes with this in depends_on)

  - id: handle_failure
    action: BRANCH
    input: node, failure_reason
    output: |
      node.phase = FAILED
      node.status = FAILED
      node.failure_reason = <reason>
    branches:
      - condition: retriable
        next: retry
        description: Same spec, same or different operator
      - condition: too_complex
        next: split_and_requeue
        description: Spec was too big; decompose into children
      - condition: fundamentally_broken
        next: escalate
        description: Requires human intervention or spec rewrite

  - id: split_and_requeue
    action: DECOMPOSE
    input: node
    output: child_nodes[]
    description: |
      - node.split_reason = failure analysis
      - node.phase = SPECCING (demoted back to spec loop)
      - Children created and enter spec loop
      - After children SPECCED, they enter build loop
```

### 4.2 TTL Enforcement

```yaml
process: ttl_enforcement
trigger: Periodic scan (every 60 seconds)
steps:
  - id: find_stale_building
    action: QUERY
    input: config.building_ttl_seconds
    output: stale_nodes[]
    description: |
      SELECT * FROM nodes
      WHERE phase = BUILDING
      AND building_started_at < (now() - building_ttl_seconds)

  - id: mark_stale_failed
    action: UPDATE
    input: stale_nodes[]
    output: |
      For each node:
        node.phase = FAILED
        node.status = FAILED
        node.failure_reason = "TTL exceeded: presumed stalled"
    description: |
      Stale nodes are marked FAILED.
      handle_failure logic then applies (retry, split, or escalate).
```

---

## 5. ROUTING DECISION LOGIC

### 5.1 Three Bundling Reasons

```yaml
process: routing_evaluation
input: ready_queue[], operators[], vendors[], config
output: dispatch_plan (individual specs + bundles)

steps:
  - id: estimate_tokens
    action: CALCULATE
    input: ready_queue[]
    output: token_estimates[]
    description: |
      For each spec, estimate input tokens:
      - Spec content + context + prompt template
      Store as spec.estimated_tokens

  - id: evaluate_granularity_fit
    action: ANALYZE
    description: |
      For each operator, assess:
      - Historical success rate at various spec scopes
      - Current ready specs that are semantically related
      - If operator handles coarse specs well, bundle related specs
      
      Signal: past success/failure at similar scope
      Decision: bundle related specs for capable operator

  - id: evaluate_operator_fit
    action: ANALYZE
    description: |
      For each operator, check:
      - Does operator prefer batches? (batch_preference = PREFERRED)
      - Does operator require batches? (batch_preference = REQUIRED)
      - Operator metadata, batch_mode flag
      
      Signal: operator.capabilities.batch_preference
      Decision: bundle to match operator's preferred input shape

  - id: evaluate_vendor_fit
    action: ANALYZE
    description: |
      For each vendor, check:
      - Pricing tiers (volume discounts?)
      - Rate limits (better to send one large request than many small?)
      - Context window (can fit multiple specs in one call?)
      
      Signal: vendor.cost_profile, operator.capabilities.max_context_tokens
      Decision: bundle if economical (COIN), faster (CLOCK), or greener (CARBON)

  - id: context_window_guard
    action: VALIDATE
    input: candidate_bundle, target_operator
    output: fits_context
    description: |
      Check: sum(spec.estimated_tokens for spec in bundle) 
             <= operator.max_context_tokens * config.token_buffer_ratio
      
      If not: reduce bundle size or reject bundling

  - id: three_currencies_optimization
    action: OPTIMIZE
    input: candidate_plans[]
    output: optimal_plan
    description: |
      Given candidate bundling strategies, select the one that optimizes:
      - CLOCK: minimize total latency (bundling reduces round-trips)
      - COIN: minimize cost (volume discounts vs. wasted tokens)
      - CARBON: minimize emissions (larger models = more carbon)
      
      Weighted by config.three_currency_weights
```

### 5.2 Bundle Lifecycle

```yaml
process: bundle_lifecycle
steps:
  - id: create_bundle
    action: CREATE
    input: spec_ids[], bundle_reason, operator_id, vendor_id, estimated_tokens
    output: Bundle(status=PENDING)

  - id: dispatch_bundle
    action: DISPATCH
    input: Bundle
    output: Bundle(status=DISPATCHED)
    description: All specs in bundle sent to operator as single request

  - id: evaluate_bundle_result
    action: BRANCH
    input: bundle_output
    branches:
      - condition: all_succeeded
        next: mark_bundle_succeeded
      - condition: all_failed
        next: unbundle_and_retry
      - condition: partial
        next: unbundle_failed_only

  - id: mark_bundle_succeeded
    action: UPDATE
    input: Bundle
    output: |
      Bundle.status = SUCCEEDED
      For each spec_id in Bundle.spec_ids:
        node.phase = BUILT
        node.status = SUCCEEDED

  - id: unbundle_and_retry
    action: DECOMPOSE
    input: Bundle
    output: |
      Bundle.status = UNBUNDLED
      For each spec_id in Bundle.spec_ids:
        node returns to ready_queue (individual dispatch)
```

---

## 6. DAG SUPPORT (Shared Modules)

### 6.1 Node Types

```yaml
node_type: ORIGINAL
description: |
  Standard node. Has its own content, acceptance criteria, and lifecycle.
  Can have parent, children, and depends_on relationships.

node_type: SHARED_REF
description: |
  Reference to an ORIGINAL node. Used when multiple nodes depend on the same module.
  - target_id: points to the ORIGINAL node
  - Does not have its own content or acceptance_criteria (inherits from target)
  - Phase mirrors target's phase
  - When target is BUILT, all SHARED_REFs are automatically BUILT
```

### 6.2 Common Module Extraction

```yaml
process: common_module_extraction
trigger: Manual annotation OR automated similarity detection
steps:
  - id: detect_similarity
    action: ANALYZE
    input: built_nodes[]
    output: similarity_clusters
    description: |
      Content similarity or explicit annotation identifies:
      - WORD and EXCEL both have file-save logic
      - POWERPOINT and WORD both have text-formatting

  - id: extract_shared_module
    action: REFACTOR
    input: similarity_cluster
    output: shared_node (ORIGINAL)
    description: |
      Create new ORIGINAL node representing shared module.
      - Assign unique ID
      - Define acceptance_criteria
      - Set output_type = PRODUCT

  - id: create_references
    action: UPDATE
    input: dependent_nodes[], shared_node
    output: |
      For each dependent:
        - Add SHARED_REF child with target_id = shared_node.id
        - OR add shared_node.id to depends_on list
    description: |
      Original nodes now reference the shared module.
      Tree becomes DAG.

  - id: version_tracking
    action: METADATA
    description: |
      Shared modules may evolve. Track:
      - version: integer (increments on change)
      - dependents: list of nodes referencing this module
      - On shared module update: dependents may need re-evaluation
```

---

## 7. FEEDBACK LOOPS

### 7.1 Completion Triggers Re-evaluation

```yaml
process: completion_feedback
trigger: Node marked BUILT
steps:
  - id: check_siblings
    action: QUERY
    input: node.parent_id
    output: sibling_states
    description: Are all siblings BUILT?

  - id: parent_eligible
    action: EVALUATE
    condition: all siblings BUILT
    description: |
      Parent can transition:
      - If parent.output_type = PLAN: parent.phase = INTEGRATED (planning complete)
      - If parent has integration step: parent.phase = BUILDING (integration task)

  - id: unblock_dependents
    action: QUERY
    input: node.id
    output: blocked_nodes[]
    description: |
      Find nodes where node.id is in their depends_on list.
      Re-evaluate their readiness:
      - If all depends_on now BUILT: node.status = PENDING (unblocked)
```

### 7.2 Learning from Outcomes (Telemetry vs Policy)

```yaml
process: outcome_learning
trigger: Build attempt completes (success or failure)
steps:
  - id: record_telemetry
    action: LOG
    input: node, operator, result, duration, tokens_used
    output: event_ledger_entry
    description: |
      ALWAYS log to Event Ledger (descriptive, no policy change):
      - spec_id, operator_id, vendor_id
      - success/failure, duration, token count
      - if failed: failure_reason, split_decision
      - acceptance_criteria results (which passed, which failed)
      
      This is TELEMETRY_LOG: pure observation, no side effects.

  - id: generate_policy_recommendation
    action: ANALYZE
    condition: sufficient_data (e.g., 10+ attempts for this operator/scope combo)
    input: telemetry_log entries
    output: policy_recommendation
    description: |
      Propose routing policy changes based on observed patterns:
      - "Operator X succeeds 90% on python_file specs < 500 lines"
      - "Bundling 3+ react_component specs for Opus saves 40% COIN"
      - "Haiku fails 80% on specs with depends_on.length > 2"
      
      This is POLICY_RECOMMENDATION: proposed change, NOT auto-applied.

  - id: human_approval_gate
    action: REQUIRE_HUMAN
    input: policy_recommendation
    output: approved | rejected | modified
    description: |
      Policy changes require human approval:
      - Review recommendation
      - Approve, reject, or modify
      - If approved: update routing heuristics
      
      No autonomous policy change without this gate.
```

---

## 8. DEPTH LIMIT AND ESCAPE HATCHES

### 8.1 Infinite Decomposition Prevention

```yaml
process: depth_guard
trigger: split_and_requeue action
steps:
  - id: check_depth
    action: EVALUATE
    input: node.branch_path.length, config.max_depth
    output: depth_ok

  - id: depth_exceeded
    action: ESCALATE
    condition: not depth_ok
    description: |
      Node has been split too many times.
      Options:
      - Escalate to human (REQUIRE_HUMAN gate)
      - Mark as BLOCKED with reason "max_depth_exceeded"
      - Attempt with most capable operator regardless of cost

  - id: check_attempt_count
    action: EVALUATE
    input: node.attempts, config.max_attempts
    output: attempts_ok

  - id: attempts_exceeded
    action: ESCALATE
    condition: not attempts_ok
    description: |
      Same spec failed too many times.
      Likely fundamentally broken, not just too complex.
      Escalate for human rewrite.
```

---

## 9. ORPHAN DETECTION

### 9.1 Tree/DAG Integrity Queries

```yaml
process: orphan_detection
trigger: Periodic scan OR on-demand query
steps:
  - id: find_incomplete_subtrees
    action: QUERY
    input: root_id
    output: incomplete_nodes[]
    description: |
      SELECT * FROM nodes 
      WHERE root_id = :root_id 
      AND phase NOT IN (BUILT, INTEGRATED)
      ORDER BY branch_path

  - id: find_stalled_nodes
    action: QUERY
    input: config.building_ttl_seconds
    output: stalled_nodes[]
    description: |
      Nodes in BUILDING for too long.
      (Handled by ttl_enforcement process)

  - id: find_blocked_nodes
    action: QUERY
    output: blocked_nodes[]
    description: |
      Nodes with status = BLOCKED.
      Check: are their dependencies actually incomplete, or is this stale?

  - id: find_orphaned_nodes
    action: QUERY
    output: orphaned_nodes[]
    description: |
      Nodes whose parent is INTEGRATED but they are not BUILT.
      Tree inconsistency — should not happen, but detectable if it does.

  - id: find_dangling_refs
    action: QUERY
    output: dangling_refs[]
    description: |
      SHARED_REF nodes whose target_id points to non-existent ORIGINAL.
      DAG inconsistency — requires repair.

  - id: find_circular_deps
    action: VALIDATE
    output: circular_deps[]
    description: |
      Nodes where depends_on creates a cycle.
      Should be caught at creation time, but validate periodically.

  - id: alert_or_requeue
    action: BRANCH
    input: problematic_nodes[]
    branches:
      - condition: stalled
        next: re-dispatch or escalate
      - condition: blocked_stale
        next: re-evaluate dependencies
      - condition: orphaned
        next: alert human, investigate tree integrity
      - condition: dangling_ref
        next: alert human, repair DAG
      - condition: circular_dep
        next: alert human, break cycle
```

---

## 10. INTEGRATION WITH FACTORY PROPOSAL

This PRISM-IR process integrates with the Factory Refactor proposal as follows:

| Factory Component | PRISM-IR Process |
|-------------------|------------------|
| `backlog/` | Nodes in IDEA or SPECCING phase |
| `ready/` | Nodes in SPECCED phase with output_type=PRODUCT and deps satisfied |
| `ready/manifest.json` | Serialized ready_queue + bundles |
| `_active/` | Nodes in BUILDING phase |
| `_done/` | Nodes in BUILT phase |
| `_needs_review/` | Nodes in FAILED phase pending escalation |
| Scheduler | Runs spec_loop, dependency_check, routing_evaluation, forms bundles |
| Executor | Runs build_loop dispatch, execution, acceptance evaluation |
| Heartbeat | Emitted during BUILDING phase |
| TTL enforcement | Periodic scan marks stale BUILDING nodes as FAILED |
| Event Ledger | Records telemetry_log for every attempt |
| Policy recommendations | Generated from telemetry, require human approval |

### 10.1 Manifest Entry (Extended)

```json
{
  "version": 2,
  "updated_at": "2026-04-07T12:00:00Z",
  "entries": [
    {
      "spec_id": "IDEA-001-A-1-a",
      "spec_file": "SPEC-IDEA-001-A-1-a-cursor-logic.md",
      "parent_id": "IDEA-001-A-1",
      "root_id": "IDEA-001",
      "branch_path": ["001", "A", "1", "a"],
      "depends_on": [],
      "node_type": "ORIGINAL",
      "output_type": "PRODUCT",
      "content_type": "python_file",
      "model": "sonnet",
      "role": "bee",
      "priority": "P1",
      "queued_at": "2026-04-07T11:30:00Z",
      "status": "pending",
      "phase": "SPECCED",
      "building_started_at": null,
      "completed_at": null,
      "result": null,
      "estimated_tokens": 2400,
      "bundle_id": null
    }
  ]
}
```

---

## 11. EXAMPLE: Office Suite (Extended)

```
IDEA-001 (Office Suite) [PLAN, SPECCING]
│
├── SPEC-001-A (Word) [PLAN, SPECCING]
│   ├── SPEC-001-A-1 (Editor) [PRODUCT, FAILED → split]
│   │   ├── attempt 1: failed (too complex for Haiku)
│   │   ├── split_reason: "scope exceeded model capability"
│   │   ├── children created:
│   │   │   ├── SPEC-001-A-1-a (Cursor) [PRODUCT, BUILT] ✓
│   │   │   │   └── acceptance_criteria: {syntax_valid: ✓, tests_pass: ✓}
│   │   │   ├── SPEC-001-A-1-b (Selection) [PRODUCT, BUILT] ✓
│   │   │   │   └── depends_on: [SPEC-001-A-1-a]  ← non-parent dependency
│   │   │   └── SPEC-001-A-1-c (Undo) [PRODUCT, BUILDING]
│   │   │       └── depends_on: [SPEC-001-A-1-a, SPEC-001-A-1-b]
│   │   └── phase: SPECCING (waiting for children)
│   │
│   └── SPEC-001-A-2 (Save/Load) [PRODUCT, BUILT] ✓
│       └── attempt 1: succeeded (Sonnet handled it)
│
├── SPEC-001-B (Excel) [PLAN, SPECCING]
│   ├── SPEC-001-B-1 (Grid) [PRODUCT, SPECCED]
│   └── SPEC-001-B-2 (Formulas) [PRODUCT, SPECCED]
│       └── depends_on: [SPEC-001-B-1]
│
├── SPEC-001-C (PowerPoint) [PLAN, IDEA]
│   └── [not yet decomposed]
│
└── SHARED-001 (File Save Module) [PRODUCT, BUILT] ← extracted common module
    └── node_type: ORIGINAL
    └── referenced by: [SPEC-001-A-2, SPEC-001-B-1] via SHARED_REF
```

**Query examples:**

```
Q: "Show me all incomplete descendants of IDEA-001"
A: SPEC-001-A-1, SPEC-001-A-1-c, SPEC-001-B, SPEC-001-B-1, SPEC-001-B-2, SPEC-001-C

Q: "What blocked SPEC-001-A-1?"
A: Child SPEC-001-A-1-c still BUILDING. Parent cannot complete until all children BUILT.

Q: "What depends on SPEC-001-A-1-a?"
A: SPEC-001-A-1-b (via depends_on), SPEC-001-A-1-c (via depends_on)

Q: "Show nodes with depends_on not yet satisfied"
A: SPEC-001-B-2 (depends on SPEC-001-B-1 which is SPECCED, not BUILT)

Q: "Show SHARED_REF nodes"
A: References to SHARED-001 in SPEC-001-A-2 and SPEC-001-B-1
```

---

## 12. NEXT STEPS

1. **Validate this IR** — Round-trip test: does this spec survive English → IR → English?
2. **Implement tree storage** — Extend manifest.json or separate tree.json for lineage + depends_on
3. **Define acceptance_criteria schemas** — Per content_type, what checks apply?
4. **Add routing heuristics** — Initial rules for granularity/operator/vendor fit
5. **Implement TTL enforcement** — Periodic scan for stale BUILDING nodes
6. **Implement context window guard** — Token estimation + max_bundle_tokens check
7. **Instrument Event Ledger** — Telemetry for every attempt
8. **Build policy recommendation pipeline** — Analysis + human approval gate
9. **Build orphan detection queries** — Dashboard for tree/DAG health
10. **Integrate with scheduler** — Scheduler becomes spec loop + dependency checker + router
11. **Integrate with executor** — Executor becomes build loop machinery + acceptance evaluator

---

## 13. CHANGELOG

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-07 | Initial draft |
| 1.1.0 | 2026-04-07 | Added FAILED to phase enum; added node_type for DAG support; added depends_on for non-parent dependencies; added acceptance_criteria per node; added building_ttl_seconds for stall detection; added max_bundle_tokens and context window guard; split learning into telemetry_log vs policy_recommendation |

---

*PRISM = Process Representation, Intent Simulation & Manifestation*
