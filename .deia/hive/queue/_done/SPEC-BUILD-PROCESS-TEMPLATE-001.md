# SPEC-BUILD-PROCESS-TEMPLATE-001

**MODE: EXECUTE**

**Spec ID:** SPEC-BUILD-PROCESS-TEMPLATE-001  
**Created:** 2026-04-14  
**Author:** Q88N  
**Type:** BUILD — IR template + wiring for build process orchestration  
**Status:** READY  
**Blocks:** All future IR-driven builds  
**Audit Source:** AUDIT-BUILD-PROCESS-INFRA-2026-04-14.md  

---

## Priority

P0

## Depends On

- SPEC-FACTORY-BRIDGE-001-service-bridge
- SPEC-FACTORY-CLEANUP-001-dead-wiring
- SPEC-FACTORY-NOTIFY-001-completion-notify

## Model Assignment

opus (architecture) + sonnet (implementation)

---

## Purpose

Define the Build Process Template (BPT) — a PRISM-IR flow that orchestrates
all builds from intake through cataloged capability. This spec:

1. Documents the existing 17-phase factory flow (`pipeline.ir.json`)
2. Extends it with front-end phases (IDEATE, DESIGN, TABLETOP)
3. Extends it with back-end gates (SMOKE, HAT, CATALOG as IR nodes)
4. Defines skip criteria and BPT variants by project scale
5. Wires `des_integration.py` into `run_queue.py` to enable IR execution

**Thesis:** The factory IS a PRISM-IR flow. We dogfood SimDecisions for
internal development. Trial and error moves from BUILD (expensive) to
DESIGN (cheap simulation).

---

## Current State (from Audit)

### What EXISTS

| Component | Status | Location |
|-----------|--------|----------|
| DES Production Execution | ✅ DONE | `simdecisions/des/executors.py` |
| Factory IR Flow | ✅ EXISTS | `.deia/hive/scripts/queue/pipeline.ir.json` |
| IR-to-Queue Bridge | ✅ EXISTS | `des_integration.py` |
| PRISM-IR Parser | ✅ DONE | `simdecisions/phase_ir/` |
| Human Gates (file) | ✅ WORKS | FileChannel → `_needs_review/` |

### What's MISSING

| Component | Status | Action |
|-----------|--------|--------|
| Queue runner IR execution | ❌ NOT WIRED | Wire `des_integration.py` |
| Front-end phases | ❌ MISSING | Add IDEATE, DESIGN, TABLETOP |
| Post-build gates | ❌ MANUAL | Add SMOKE, HAT, CATALOG nodes |
| Inventory auto-update | ❌ MANUAL | Add catalog node at sink |
| Efemera channel | ⚠️ NOT WIRED | Add EfemeraChannel to DeciderRouter |

---

## Existing Factory Flow (17 Phases)

`pipeline.ir.json` already defines these phases:

```
source (Q88N Direction)
    ↓
gate_0 (Intent Validation)
    ↓
phase_0 (Coverage Validation — fidelity >= 1.0)
    ↓
phase_1 (SPEC Fidelity — fidelity >= 0.85)
    ↓
phase_2 (TASK Fidelity — fidelity >= 0.85)
    ↓
task_breakdown (Q33N writes task files)
    ↓
q33nr_review (mechanical review)
    ↓
dispatch (directory state machine)
    ↓
bee_execution (TDD + code + response)
    ↓
post_dispatch_verify (test count comparison)
    ↓
triage_crash (LLM triage for crash recovery)
    ↓
triage_failure (LLM triage for NEEDS_DAVE)
    ↓
triage_completion (advisory review)
    ↓
q33n_review (response complete? tests pass?)
    ↓
q33nr_final_review (all bees clean?)
    ↓
archive_inventory (feature registered)
    ↓
sink (completed work)
```

**This flow covers:** Intake through code. What's missing is the front-end
(exploration, design, simulation) and back-end automation (gates, catalog).

---

## Extended Flow: Full BPT

### Front-End Phases (NEW)

Add before `source`:

```
INTAKE
    ↓
IDEATE (explore, branch, shape — may loop)
    ↓
DESIGN (DDD → response definitions, skeleton, integration maps — no code)
    ↓
[BRANCH] (Alterverse: multiple design alternatives)
    ↓
TABLETOP (DES walks the plan in simulation mode — gaps surface)
    ↓
[COMP] (Compare branches: CCC estimates, complexity, risk, reuse)
    ↓
[DEC] (Pick path — human or criteria-based)
    ↓
SPEC-REVIEW (Human gate: approve spec before build?)
    ↓
source (existing flow begins)
```

### Back-End Gates (NEW)

Add after `q33nr_final_review`:

```
q33nr_final_review (existing)
    ↓
SMOKE (automated smoke test — pytest subset)
    ↓
HAT (human acceptance test — Efemera gate)
    ↓
CATALOG (auto-update inv_features)
    ↓
sink (completed work → unblocks dependents)
```

---

## Phase Definitions

### INTAKE

```yaml
id: intake
type: task
op: human
intention: "Capture idea or request"
config:
  channel: efemera  # or file, email
  prompt: "[[.wiki/prompts/intake-capture]]"
outputs:
  - idea_text: string
  - source: enum[q88n, external, backlog]
  - urgency: enum[now, soon, later]
```

### IDEATE

```yaml
id: ideate
type: task
op: llm
intention: "Explore solution space"
config:
  model: sonnet
  prompt: "[[.wiki/prompts/ideate-explore]]"
  max_branches: 3
outputs:
  - approaches: list[Approach]
  - recommended: string  # approach_id
  - rationale: string
guard: "token.idea_text != null"
```

### DESIGN

```yaml
id: design
type: task
op: llm
intention: "Define response to each requirement — no code"
config:
  model: opus
  prompt: "[[.wiki/prompts/design-skeleton]]"
outputs:
  - skeleton: DesignSkeleton
  - integration_map: list[IntegrationPoint]
  - dependencies: list[Dependency]
  - ccc_estimate: CCCEstimate
guard: "token.approaches != null"
```

### TABLETOP (Simulation Gate)

```yaml
id: tabletop
type: subprocess
intention: "Simulate build plan — find gaps before code"
config:
  command: "python -m simdecisions.des.runner"
  args:
    flow: "token.design.skeleton"
    mode: simulation
    track_state: true
    surface_gaps: true
outputs:
  - gaps: list[Gap]
  - blocked_steps: list[string]
  - revised_estimate: CCCEstimate
  - sim_trace: TraceBuffer
sla:
  target: 5min
  escalate: q88n
```

**On gap found:** Back-edge to DESIGN with gap context.

```yaml
edges:
  - from: tabletop
    to: design
    condition: "len(token.gaps) > 0"
    label: "remediation_loop"
  - from: tabletop
    to: spec_review
    condition: "len(token.gaps) == 0"
    label: "clean_pass"
```

### BRANCH (Alterverse)

```yaml
id: branch
type: fork
intention: "Explore alternative designs in parallel"
config:
  branch_count: "len(token.approaches)"
  branch_on: "token.approaches"
  create_timeline: true
outputs:
  - timelines: list[TimelineID]
```

### COMP (Compare Branches)

```yaml
id: comp
type: task
op: llm
intention: "Compare alternatives on CCC, complexity, risk, reuse"
config:
  model: sonnet
  prompt: "[[.wiki/prompts/comp-compare]]"
  inputs:
    - timelines: "token.timelines"
    - criteria: [clock, coin, carbon, complexity, risk, reuse_ratio]
outputs:
  - comparison_matrix: Matrix
  - pareto_frontier: list[TimelineID]
  - recommendation: TimelineID
  - rationale: string
```

### DEC (Decide Path)

```yaml
id: dec
type: decision
op: human
intention: "Select build path"
config:
  channel: efemera
  prompt: "[[.wiki/prompts/dec-select]]"
  options: "token.pareto_frontier"
  default: "token.recommendation"
  timeout: 4h
outputs:
  - selected_timeline: TimelineID
  - decision_rationale: string
```

### SPEC-REVIEW

```yaml
id: spec_review
type: decision
op: human
intention: "Approve spec before build"
config:
  channel: efemera
  prompt: "[[.wiki/prompts/spec-review]]"
  attachments:
    - "token.skeleton"
    - "token.integration_map"
    - "token.ccc_estimate"
  timeout: 24h
outputs:
  - approved: boolean
  - feedback: string
```

**On rejection:** Back-edge to DESIGN or IDEATE.

### SMOKE

```yaml
id: smoke
type: subprocess
intention: "Automated smoke test"
config:
  command: "pytest tests/smoke/ -v --tb=short"
  timeout_s: 120
  cwd: "{{repo_root}}"
outputs:
  - passed: boolean
  - failures: list[string]
  - duration_s: float
guard: "token.tests_passing == true"
```

### HAT (Human Acceptance Test)

```yaml
id: hat
type: decision
op: human
intention: "Human accepts or rejects build"
config:
  channel: efemera
  prompt: "[[.wiki/prompts/hat-review]]"
  attachments:
    - "token.response_file"
    - "token.test_summary"
    - "token.diff_link"
  timeout: 48h
outputs:
  - accepted: boolean
  - feedback: string
```

**On rejection:** Back-edge to BUILD with feedback.

### CATALOG

```yaml
id: catalog
type: python
intention: "Register capability in inventory"
config:
  code: |
    from hivenode.inventory.store import add_feature
    add_feature(
        id=token.feature_id,
        title=token.feature_title,
        task_id=token.task_id,
        status="BUILT",
        layer=token.layer,
        source_files=token.files_created,
        test_count=token.tests_added,
    )
outputs:
  - registered: boolean
  - feature_id: string
```

---

## Skip Criteria

Not all work needs all phases. Define skip rules:

### BPT Variants by Scale

| Scale | Phases Used | Criteria |
|-------|-------------|----------|
| **BUGFIX** | INTAKE → BUILD → BAT → DONE | `scope == 'bugfix' and lines_changed < 50` |
| **SMALL** | INTAKE → SPEC → BUILD → BAT → CATALOG → DONE | `scope == 'small' and touches_files < 3` |
| **MEDIUM** | Full existing flow (17 phases) | `scope == 'medium'` |
| **LARGE** | Full extended flow (IDEATE → TABLETOP → all gates) | `scope == 'large' or new_capability == true` |
| **RISKY** | Full flow + mandatory HAT | `risk == 'high' or user_facing == true` |

### Skip Logic (Guard Expressions)

```yaml
# Skip IDEATE for bugfixes
edges:
  - from: intake
    to: design
    condition: "token.scope == 'bugfix'"
  - from: intake
    to: ideate
    condition: "token.scope != 'bugfix'"

# Skip TABLETOP for small changes
edges:
  - from: design
    to: spec_review
    condition: "token.scope in ['bugfix', 'small']"
  - from: design
    to: tabletop
    condition: "token.scope in ['medium', 'large', 'risky']"

# Skip HAT if BAT sufficient
edges:
  - from: smoke
    to: catalog
    condition: "token.scope == 'bugfix' and token.smoke_passed == true"
  - from: smoke
    to: hat
    condition: "token.scope != 'bugfix' or token.smoke_passed == false"
```

---

## Wiring Tasks

### Task 1: Wire `des_integration.py` into `run_queue.py`

**File:** `.deia/hive/scripts/queue/run_queue.py`

**Change:** After loading spec, check if IR-driven execution is enabled:

```python
# In run_queue.py main loop, after loading spec:
from . import des_integration

if des_integration.should_use_des_flow(spec.path):
    result = des_integration.run_build_integrity_flow(
        spec_path=spec.path,
        repo_root=repo_root,
        mode="production",
    )
    if result.success:
        move_to_done(spec.path)
    else:
        move_to_needs_review(spec.path, result.errors)
    continue  # Skip procedural dispatch

# ... existing procedural dispatch for specs that don't opt in
```

**Effort:** 1 hour  
**Impact:** Enables IR-driven execution for opted-in specs

### Task 2: Add SMOKE node to `pipeline.ir.json`

**File:** `.deia/hive/scripts/queue/pipeline.ir.json`

**Change:** Add node after `q33nr_final_review`:

```json
{
  "id": "smoke_test",
  "type": "subprocess",
  "intention": "Automated smoke test",
  "config": {
    "command": "pytest tests/smoke/ -v --tb=short",
    "timeout_s": 120
  },
  "outputs": ["passed", "failures", "duration_s"]
}
```

**Add edge:**
```json
{ "from": "q33nr_final_review", "to": "smoke_test" },
{ "from": "smoke_test", "to": "catalog", "c": "result.passed == true" },
{ "from": "smoke_test", "to": "hat", "c": "result.passed == false" }
```

**Effort:** 30 minutes  
**Impact:** Automated smoke testing in flow

### Task 3: Add CATALOG node to `pipeline.ir.json`

**File:** `.deia/hive/scripts/queue/pipeline.ir.json`

**Change:** Add node before `sink`:

```json
{
  "id": "catalog",
  "type": "python",
  "intention": "Register capability in inventory",
  "config": {
    "code": "subprocess.run(['python', '_tools/inventory.py', 'add', '--from-response', token.response_path])"
  },
  "outputs": ["registered", "feature_id"]
}
```

**Effort:** 30 minutes  
**Impact:** Removes manual inventory step

### Task 4: Add HAT node to `pipeline.ir.json`

**File:** `.deia/hive/scripts/queue/pipeline.ir.json`

**Change:** Add human decision node:

```json
{
  "id": "hat",
  "type": "decision",
  "op": "human",
  "intention": "Human acceptance test",
  "config": {
    "channel": "file",
    "prompt_file": ".wiki/prompts/hat-review.md",
    "timeout_h": 48
  },
  "outputs": ["accepted", "feedback"]
}
```

**Effort:** 1 hour  
**Impact:** Formal human acceptance gate

### Task 5: Add front-end phases to `pipeline.ir.json`

**File:** `.deia/hive/scripts/queue/pipeline.ir.json`

**Change:** Add INTAKE, IDEATE, DESIGN, TABLETOP, BRANCH, COMP, DEC, SPEC-REVIEW
nodes before `source`. Wire skip logic based on `token.scope`.

**Effort:** 4 hours  
**Impact:** Full front-end design simulation capability

### Task 6: Wire EfemeraChannel to DeciderRouter

**File:** `simdecisions/des/adapters.py`

**Change:** Add EfemeraChannel class:

```python
class EfemeraChannel:
    """Send decision requests to Efemera relay."""
    
    async def send(self, request: DecisionRequest) -> None:
        from hivenode.relay.store import create_message
        await create_message(
            channel="efemera",
            content=request.prompt,
            metadata={"decision_id": request.id, "options": request.options},
        )
    
    async def receive(self, request_id: str, timeout: float) -> DecisionResponse:
        from hivenode.relay.store import wait_for_response
        return await wait_for_response(request_id, timeout)
```

Register in `DeciderRouter._select_channel()`:

```python
if channel_type == "efemera":
    return EfemeraChannel()
```

**Effort:** 2 hours  
**Impact:** Rich human gates via Efemera (mobile, chat, etc.)

---

## Acceptance Criteria

- [ ] `des_integration.py` called from `run_queue.py` for opted-in specs
- [ ] SMOKE node added to `pipeline.ir.json` and executing
- [ ] CATALOG node added and auto-updating `inv_features`
- [ ] HAT node added with file-based human gate
- [ ] Front-end phases (IDEATE through SPEC-REVIEW) added
- [ ] Skip logic implemented via guard expressions
- [ ] Event Ledger captures all phase transitions
- [ ] At least one spec successfully runs through IR-driven execution

## Smoke Test

```bash
# IR execution wired
grep -l "des_integration" .deia/hive/scripts/queue/run_queue.py && echo "WIRED" || echo "NOT WIRED"

# SMOKE node exists
grep -l "smoke_test" .deia/hive/scripts/queue/pipeline.ir.json && echo "EXISTS" || echo "MISSING"

# CATALOG node exists
grep -l '"catalog"' .deia/hive/scripts/queue/pipeline.ir.json && echo "EXISTS" || echo "MISSING"

# Test IR execution
python -c "from simdecisions.des import runner; print('DES importable')"
```

## Constraints

- Do not break existing procedural queue runner — hybrid approach
- All new nodes must pass PRISM-IR validation
- All human gates must work with FileChannel before Efemera
- Skip criteria must be testable via dry-run
- Event Ledger must capture all transitions for audit

## Response File

`.deia/hive/responses/SPEC-BUILD-PROCESS-TEMPLATE-001-RESPONSE.md`

---

## Appendix A: Full Extended Flow Diagram

```
                    ┌─────────────────────────────────────────────┐
                    │            FRONT-END (NEW)                  │
                    └─────────────────────────────────────────────┘
                                        │
    INTAKE ──→ IDEATE ──→ DESIGN ──→ BRANCH ──→ TABLETOP ──→ COMP ──→ DEC
        │         │                      │           │
        │         │                      │           │ (gaps found)
        │    (bugfix)                    │           ↓
        │         │                      │      back to DESIGN
        ↓         ↓                      │
    ┌─────────────────────────────────────────────────────────────┐
    │                  SPEC-REVIEW (Human Gate)                   │
    └─────────────────────────────────────────────────────────────┘
                                        │
                                        ↓
    ┌─────────────────────────────────────────────────────────────┐
    │            EXISTING 17 PHASES (pipeline.ir.json)            │
    │  source → gate_0 → phase_0/1/2 → task_breakdown → dispatch  │
    │  → bee_execution → verify → triage → reviews → ...          │
    └─────────────────────────────────────────────────────────────┘
                                        │
                                        ↓
    ┌─────────────────────────────────────────────────────────────┐
    │             BACK-END GATES (NEW)                            │
    └─────────────────────────────────────────────────────────────┘
                                        │
                    SMOKE ──→ HAT ──→ CATALOG ──→ DONE
                      │         │
                 (fail)│    (reject)
                      ↓         ↓
                 back to    back to
                  BUILD      BUILD
```

---

## Appendix B: CCCEstimate Schema

```yaml
CCCEstimate:
  clock:
    total_hours: float
    by_phase: dict[phase_id, hours]
  coin:
    total_usd: float
    by_model: dict[model_name, usd]
  carbon:
    total_co2e_kg: float
    by_phase: dict[phase_id, kg]
  model_assignments:
    - phase: string
      model: enum[opus, sonnet, haiku]
      rationale: string
```

---

## Appendix C: Alterverse Query Pattern

When BUILD hits a snag, query the Alterverse for similar patterns:

```python
from simdecisions.alterverse import query_timelines

results = query_timelines(
    pattern="dependency_gap",
    context={
        "missing": token.error_context,
        "phase": "build",
    },
    limit=5,
)

# Returns: list of timelines where this pattern occurred
# with resolution context from DESIGN phase
```

This enables: "Did we see this in any branch? How did we solve it?"

---

*SPEC-BUILD-PROCESS-TEMPLATE-001 — Q88N — 2026-04-14*
