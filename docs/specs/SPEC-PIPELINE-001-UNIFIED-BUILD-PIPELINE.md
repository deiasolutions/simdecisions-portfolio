# SPEC-PIPELINE-001: Unified Build Pipeline

**Author:** Q88N (Dave) × Claude (Opus 4.6)
**Date:** 2026-03-16
**Status:** AWAITING Q88N APPROVAL
**Supersedes:** Partial overlap with PROCESS-0013, PROCESS-0018, PROCESS-0016/0019
**Incorporates:** Q33NR directory state machine proposal, Q33NR dev process flow proposal

---

## 1. Problem

Five processes describe overlapping stages of the same pipeline:

| Process | Covers | Gap |
|---------|--------|-----|
| PROCESS-0013 (Build Integrity) | IR fidelity gates (Gate 0, Phase 0–2) | Not wired into dev process flow |
| PROCESS-0018 (Living Feature Inventory) | Bee response YAML frontmatter | No ledger emission |
| PROCESS-0016/0019 (Bee Response Format) | 8-section response template | Duplicates parts of P-0018 |
| Q33NR directory state machine | `_active/`, `_failed/`, crash recovery | Missing manifest, missing LLM triage |
| Q33NR dev process flow | Path A (manual) + Path B (queue runner) | Missing IR fidelity gates, no DES compatibility |

No single document answers: "What happens to a piece of work from the moment Dave says 'build X' through to shipped, measured, archived code — and can I simulate that pipeline before running it?"

Additionally, the queue runner is filesystem-only. It cannot run in DES mode (in-memory, cloud, fast-forward) for capacity planning and bottleneck analysis.

---

## 2. Solution

One pipeline. Two runtimes. Same IR.

### 2.1 One Pipeline

Every piece of work passes through a fixed sequence of stages. Each stage has: an input artifact, an output artifact, a success criterion, a failure route, and a ledger event. No stage is optional. No stage is undocumented.

### 2.2 Two Runtimes

**Local (Production mode):** The filesystem IS the state. Directories are queues. Files are tokens. LLM calls are real subprocess dispatches. Side effects are real. This is what `run_queue.py` does today, enhanced.

**Cloud/DES (Simulation mode):** The same pipeline encoded as PHASE-IR, executed by the DES engine on Railway. Directories become in-memory dicts. Files become Python dicts. LLM calls become activity nodes with service time distributions calibrated from Event Ledger data. No side effects. Statistical output: throughput, bottlenecks, optimal pool sizing.

### 2.3 Same IR

The bridge: a `PipelineStore` protocol with two implementations. The queue runner and all stage logic are written against the protocol. Swap the adapter, swap the runtime. No code changes.

---

## 3. Pipeline Stages

```
Q88N DIRECTION
  │
  ▼
GATE 0 ─── Intent Validation
  │         Did Q33NR correctly interpret Dave?
  │         Input: Q88N direction (verbal/text)
  │         Output: Briefing file
  │         Gate: Requirements tree extraction, coverage check
  │         Fail: Q33NR rewrites briefing
  │
  ▼
PHASE 0 ── Coverage Validation
  │         Are ALL requirements from briefing in the spec?
  │         Input: Briefing + spec draft
  │         Output: Coverage report
  │         Gate: 100% coverage, 0 violations
  │         Fail: Heal (LLM rewrite, max 3 retries) → Escalate to Q88N
  │
  ▼
PHASE 1 ── SPEC Fidelity
  │         Does SPEC → IR → SPEC' preserve meaning?
  │         Input: Spec
  │         Output: Fidelity report + IR encoding
  │         Gate: Fidelity ≥ 0.85
  │         Fail: Heal (LLM rewrite, max 3 retries) → Escalate to Q88N
  │
  ▼
TASK BREAKDOWN ── Q33N writes task files
  │
  ▼
PHASE 2 ── TASK Fidelity
  │         Do TASKS → IR → TASKS' preserve spec intent?
  │         Input: Task files
  │         Output: Fidelity report
  │         Gate: Fidelity ≥ 0.85
  │         Fail: Heal (LLM rewrite, max 3 retries) → Escalate to Q88N
  │
  ▼
Q33NR REVIEW ── Task files approved
  │
  ▼
DISPATCH ── Path A (manual) or Path B (queue runner)
  │          Directory state machine takes over here
  │
  ▼
BEE EXECUTION ── TDD, code, 8-section response, PROCESS-18 YAML
  │
  ▼
POST-DISPATCH VERIFICATION ── Test count comparison, regression check
  │
  ▼
Q33N REVIEW ── Response complete? Tests pass? Stubs?
  │
  ▼
Q33NR REVIEW ── All bees clean? Report to Q88N
  │
  ▼
ARCHIVE + INVENTORY ── Feature registered, backlog updated, ledger emitted
```

### 3.1 Every Stage Emits to Event Ledger

No exceptions. Event schema for validation stages:

```yaml
event_type: phase_validation
spec_id: SPEC-XXX
phase: gate_0 | phase_0 | phase_1 | phase_2
fidelity_score: 0.91        # null for gate_0
tokens_in: 1200
tokens_out: 800
model: haiku
cost_usd: 0.002
attempt: 1                   # 1 = first try, 2+ = healing retry
result: PASS | FAIL | HEALED
healing_attempts: 0
wall_time_seconds: 12
```

Event schema for execution stages:

```yaml
event_type: bee_execution
spec_id: SPEC-XXX
task_id: TASK-XXX
bee_id: BEE-HAIKU-1
model: haiku-4.5
session_id: ses_abc123
tokens_in: 45000
tokens_out: 12000
cost_usd: 0.08
wall_time_seconds: 180
result: CLEAN | TIMEOUT | NEEDS_DAVE | CRASH
tests_before: 185
tests_after: 197
tests_new_passing: 12
tests_new_failing: 0
features_delivered: [SHELL-042, SHELL-043]
features_broken: []
```

This is ABCDEFG. Over 50–100 specs, the data answers: "Does the IR round-trip actually reduce bee failure rate enough to justify its token cost?"

---

## 4. Directory State Machine

### 4.1 Layout

```
.deia/hive/queue/
├── *.md              ← PENDING: eligible for pickup
├── _hold/            ← HELD: not yet released (wave gate)
├── _active/          ← IN-FLIGHT: bee working
├── _done/            ← COMPLETED: clean, tests passed
├── _failed/          ← FAILED: may retry
├── _needs_review/    ← BLOCKED: needs human decision
└── _dead/            ← CANCELLED: permanently removed
```

### 4.2 Transitions

| From | To | Trigger | Who |
|------|----|---------|-----|
| `_hold/` | `queue/` | Wave release | Q88N / Q33NR (manual) |
| `queue/` | `_active/` | Pickup (priority + deps + FIFO) | Queue runner |
| `_active/` | `_done/` | Bee returns CLEAN | Queue runner |
| `_active/` | `_failed/` | Bee returns error/timeout | Queue runner |
| `_active/` | `_needs_review/` | Regression detected | Queue runner |
| `_active/` | `queue/` | Crash recovery (orphan, retries remain) | Queue runner on startup |
| `_active/` | `_needs_review/` | Crash recovery (max retries exhausted) | Queue runner on startup |
| `_failed/` | `queue/` | Fix spec generated, retries remain | Queue runner |
| `_failed/` | `_needs_review/` | Ambiguous failure, needs human | Queue runner or human |
| `_failed/` | `_dead/` | Give up (max retries, human decision) | Q88N / Q33NR |
| `_needs_review/` | `queue/` | Human edits spec, retries | Q88N / Q33NR |
| `_needs_review/` | `_dead/` | Human abandons | Q88N / Q33NR |
| `_done/` | `_archive/` | Sprint boundary sweep | Q33N |

### 4.3 Pickup Logic

```python
for spec in queue_store.list_specs("queue"):
    if spec.hold_until and spec.hold_until > now:
        continue  # gated
    if not queue_store.deps_satisfied(spec):
        continue  # BLOCKED
    if slots_used >= max_parallel:
        break     # capacity
    queue_store.move_spec(spec.id, "queue", "_active", manifest={
        "bee_id": assigned_bee,
        "model": assigned_model,
        "session_id": None,  # filled on dispatch
        "started_at": now.isoformat(),
        "pid": None,         # filled on dispatch
    })
    dispatch_bee(spec)
```

### 4.4 Priority (P0–P3 integer only)

| P | Meaning |
|---|---------|
| P0 | Emergency hotfix |
| P1 | Current wave |
| P2 | Next wave |
| P3 | Backlog |

Within same priority: FIFO by file modification time. Existing fractional priorities are floored.

### 4.5 Dependencies

Specs declare via `## Depends On` section. Queue runner checks `_done/` for matching IDs. After each completion, re-scan blocked specs.

### 4.6 Manifest (NEW — not in Q33NR proposal)

When a spec moves to `_active/`, the queue runner appends a `## Execution Manifest` section:

```markdown
## Execution Manifest
- bee_id: BEE-HAIKU-1
- model: haiku-4.5
- session_id: ses_abc123
- started_at: 2026-03-16T14:30:00
- pid: 12345
```

On completion, appends `## Completion Record`:

```markdown
## Completion Record
- completed_at: 2026-03-16T14:45:00
- result: CLEAN
- response_file: .deia/hive/responses/20260316-SPEC-XXX-RESPONSE.md
- tests_before: 185
- tests_after: 197
- cost_usd: 0.08
- wall_time_seconds: 180
```

### 4.7 Failure Log

On failure, appends `## Failure Log`:

```markdown
## Failure Log
- 2026-03-16T14:30:00 | TIMEOUT | Attempt 1/2 | Triage: PARTIAL_SAFE | Fix spec: SPEC-fix-foo.md
- 2026-03-16T14:45:00 | NEEDS_DAVE | Attempt 2/2 | Triage: REVERT | Max retries exhausted
```

### 4.8 Timeout Escalation

Items in `_needs_review/` for >24 hours emit a warning event. Configurable in `queue.yml`.

### 4.9 Archive Sweep

`_done/` contents move to `.deia/hive/tasks/_archive/` at sprint boundary per PROCESS-0002. `_dead/` contents also archive (with `cancelled: true` tag).

---

## 5. LLM Triage Layer

Three integration points where a cheap LLM (Haiku) adds intelligence to the state machine.

### 5.1 Crash Recovery Triage

**When:** Queue runner finds orphan in `_active/` on startup.
**Input:** Spec file, manifest (bee_id, session_id), `git diff` since session start, test output if any.
**Prompt:** "This bee was working on spec X and crashed. Here is the diff. Assess: (a) % of acceptance criteria met, (b) are changes safe to keep or revert, (c) if partial, write a continuation spec."

**Verdicts:**

| Verdict | Action |
|---------|--------|
| COMPLETE_ENOUGH | Commit diff, move to `_done/`, note recovered |
| PARTIAL_SAFE | Keep diff, generate continuation spec in `queue/`, move original to `_done/` with partial flag |
| REVERT | `git checkout` changed files, move spec back to `queue/` for full retry |

### 5.2 Failure Diagnosis

**When:** Bee returns NEEDS_DAVE or error.
**Input:** Spec, response file, error output, test results.
**Prompt:** "Diagnose why this spec failed. Classify: (a) spec ambiguous — needs rewrite, (b) coding error — needs fix spec, (c) dependency issue — upstream broken, (d) environment issue."

**Routing:**

| Classification | Route |
|---------------|-------|
| Ambiguous spec | `_needs_review/` (human rewrites) |
| Coding error | Generate fix spec in `queue/` |
| Dependency issue | Block on upstream dep, move to `queue/` with dep added |
| Environment issue | `_needs_review/` with env tag |

### 5.3 Completion Validation (Advisory)

**When:** Bee reports CLEAN, before moving to `_done/`.
**Input:** Spec acceptance criteria, `git diff`, test results.
**Prompt:** "Review this diff against the spec's acceptance criteria. Flag anything missing or suspicious."

**Phase 1 (now):** Advisory only — log the review, don't gate on it.
**Phase 2 (when trust is established):** Gate on it. Suspicious results go to `_needs_review/`.

**Holdout principle:** The reviewing LLM is NEVER the same model/session that did the work.

### 5.4 Cost Model

Each triage call: ~$0.01–0.03 (Haiku). At 10% failure rate on 50 specs/day = 5 calls = $0.05–0.15/day. Trivial vs. cost of re-running a full Sonnet bee on 80%-done work.

---

## 6. PipelineStore Protocol

The abstraction that enables dual-runtime.

### 6.1 Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class SpecFile:
    id: str
    filename: str
    priority: int              # 0-3
    depends_on: list[str]
    hold_until: Optional[str]  # ISO datetime or None
    added_at: str              # ISO datetime
    content: str               # full markdown
    manifest: Optional[dict]   # execution manifest when in _active/

class PipelineStore(ABC):
    """Protocol for pipeline state management.
    
    Two implementations:
    - FilesystemPipelineStore: pathlib, real files (Production mode)
    - InMemoryPipelineStore: dicts, no I/O (DES mode)
    """

    @abstractmethod
    def list_specs(self, stage: str) -> list[SpecFile]:
        """List all specs in a given stage directory."""

    @abstractmethod
    def move_spec(self, spec_id: str, from_stage: str, to_stage: str,
                  metadata: Optional[dict] = None):
        """Move spec between stages. metadata is appended to the spec."""

    @abstractmethod
    def append_section(self, spec_id: str, section_name: str, content: str):
        """Append a markdown section to the spec file."""

    @abstractmethod
    def get_done_ids(self) -> set[str]:
        """Return set of spec IDs in _done/ (for dependency checking)."""

    @abstractmethod
    def deps_satisfied(self, spec: SpecFile) -> bool:
        """Check if all dependencies are in _done/."""

    @abstractmethod
    def emit_event(self, event: dict):
        """Emit to Event Ledger (DB for filesystem, list for in-memory)."""

    @abstractmethod
    def get_orphans(self) -> list[SpecFile]:
        """Return specs in _active/ (for crash recovery)."""
```

### 6.2 FilesystemPipelineStore

```python
class FilesystemPipelineStore(PipelineStore):
    """Production runtime. Filesystem is the state machine."""

    def __init__(self, queue_root: Path, ledger_db: Path):
        self.queue_root = queue_root
        self.ledger = EventLedger(ledger_db)
        self.stages = {
            "hold": queue_root / "_hold",
            "queue": queue_root,
            "active": queue_root / "_active",
            "done": queue_root / "_done",
            "failed": queue_root / "_failed",
            "needs_review": queue_root / "_needs_review",
            "dead": queue_root / "_dead",
        }

    def move_spec(self, spec_id, from_stage, to_stage, metadata=None):
        src = self._find_spec_path(spec_id, from_stage)
        dst = self.stages[to_stage] / src.name
        src.rename(dst)
        if metadata:
            self.append_section(spec_id, metadata["section"], metadata["content"])
        self.emit_event({
            "event_type": "spec_transition",
            "spec_id": spec_id,
            "from": from_stage,
            "to": to_stage,
            "timestamp": datetime.utcnow().isoformat(),
        })
```

### 6.3 InMemoryPipelineStore

```python
class InMemoryPipelineStore(PipelineStore):
    """DES runtime. Dicts are the state machine."""

    def __init__(self):
        self.stages = {
            "hold": [], "queue": [], "active": [], "done": [],
            "failed": [], "needs_review": [], "dead": [],
        }
        self.events = []  # append-only list

    def move_spec(self, spec_id, from_stage, to_stage, metadata=None):
        spec = self._pop_spec(spec_id, from_stage)
        if metadata:
            spec.content += f"\n## {metadata['section']}\n{metadata['content']}\n"
        self.stages[to_stage].append(spec)
        self.events.append({
            "event_type": "spec_transition",
            "spec_id": spec_id,
            "from": from_stage,
            "to": to_stage,
        })
```

---

## 7. DES Model of the Pipeline

### 7.1 PHASE-IR Node Mapping

| Pipeline Stage | DES Primitive | Service Time Source |
|---------------|---------------|---------------------|
| Gate 0 (Intent) | Activity | ~5s (Haiku call) |
| Phase 0 (Coverage) | Activity + Decision | ~8s (Haiku + embedding) |
| Phase 1 (SPEC Fidelity) | Activity + Decision | ~12s (encode + decode + compare) |
| Phase 2 (TASK Fidelity) | Activity + Decision | ~12s (same) |
| Q33NR Review | Activity (human resource) | Distribution from ledger data |
| Bee Execution | Activity | Distribution from ledger data (60–600s) |
| Post-Dispatch Verify | Activity | ~10s (test runner) |
| Q33N Review | Activity | ~30s (Haiku review) |
| Archive | Activity | ~5s (file ops) |

### 7.2 Resources

| Resource | Capacity | Notes |
|----------|----------|-------|
| Bee pool | max_parallel (default 5) | Configurable |
| Human reviewer (Q88N) | 1 | Only used for `_needs_review/` |
| LLM triage | 3 | Parallel Haiku calls for triage |

### 7.3 Decision Nodes

| Decision | Branches |
|----------|----------|
| Fidelity check | PASS (≥0.85) → next stage / FAIL → heal loop |
| Heal loop | Retry (attempt < 3) → re-validate / Escalate (attempt ≥ 3) → human |
| Bee result | CLEAN → `_done/` / TIMEOUT → triage / NEEDS_DAVE → triage / CRASH → recovery |
| Triage verdict | COMPLETE_ENOUGH → `_done/` / PARTIAL_SAFE → continuation / REVERT → retry |

### 7.4 Calibration

Service time distributions are fitted from Event Ledger data:

```python
# After 50+ specs processed:
bee_service_time = fit_distribution(
    ledger.query("event_type = 'bee_execution'")["wall_time_seconds"]
)
# Likely LogNormal or Gamma — heavy right tail (some bees take 10x longer)

fidelity_pass_rate = (
    ledger.query("event_type = 'phase_validation' AND result = 'PASS'").count()
    / ledger.query("event_type = 'phase_validation'").count()
)
```

### 7.5 What DES Answers

- **Throughput:** Specs completed per hour at current pool size
- **Bottleneck:** Which stage has the highest WIP / longest queue
- **Optimal pool size:** Run sweep on bee pool capacity → diminishing returns curve
- **Failure impact:** If failure rate doubles, what happens to cycle time?
- **Fidelity ROI:** Compare: pipeline WITH Phase 1/2 vs. pipeline WITHOUT → difference in downstream failure rate × cost per failure = value of fidelity gates

---

## 8. Build Plan

### Wave 1 — No dependencies, can start immediately

| Task | Description | Model | Est. Lines | Depends On |
|------|-------------|-------|-----------|------------|
| W1-A | PipelineStore interface + FilesystemPipelineStore | Haiku | ~130 | Nothing |
| W1-B | Validation ledger events (schema + emission) | Haiku | ~40 | Nothing |

**W1-A detail:** Extract filesystem operations from `run_queue.py` behind `PipelineStore` ABC. Implement `FilesystemPipelineStore`. Refactor `run_queue.py` to use it. All existing queue runner tests still pass. Pure refactor, zero new behavior.

**W1-B detail:** Add `phase_validation` and `bee_execution` event types to Event Ledger. Add `emit_validation_event()` and `emit_execution_event()` helper functions. Wire into existing code paths where fidelity checks and bee dispatches happen.

### Wave 2 — Depends on W1-A

| Task | Description | Model | Est. Lines | Depends On |
|------|-------------|-------|-----------|------------|
| W2-A | Directory state machine transitions | Sonnet | ~110 | W1-A |
| W2-B | InMemoryPipelineStore | Haiku | ~60 | W1-A |

**W2-A detail:** Implement `_active/` pickup with manifest, `_done/`/`_failed/` routing, crash recovery (orphan scan on startup), failure log appending, completion record appending. All through `PipelineStore` interface. New tests: ~15 (transitions, crash recovery, failure log).

**W2-B detail:** Dict-backed implementation of PipelineStore. In-memory event list. Tests mirror filesystem tests but run in-memory. ~10 tests.

### Wave 3 — Depends on W2-A + W2-B

| Task | Description | Model | Est. Lines | Depends On |
|------|-------------|-------|-----------|------------|
| W3-A | PHASE-IR flow encoding of the build pipeline | Sonnet | ~200 (IR JSON) | W2-A, W2-B |
| W3-B | LLM triage functions (3 integration points) | Sonnet | ~100 | W2-A |

**W3-A detail:** Author the `.ir.json` that describes the full pipeline as a PHASE-IR flow. Nodes for every stage, edges for every transition, resources for bee pool and human reviewer. This is the artifact that lets DES consume the pipeline. Can also be rendered to English via round-trip (the process documents itself).

**W3-B detail:** Three functions: `triage_crash_recovery(spec, diff, tests)`, `triage_failure(spec, response, errors)`, `validate_completion(spec, diff, tests)`. Each dispatches a Haiku call, returns a verdict enum. Wired into state machine transitions from W2-A.

### Wave 4 — Depends on W3-A

| Task | Description | Model | Est. Lines | Depends On |
|------|-------------|-------|-----------|------------|
| W4-A | DES runner for build pipeline | Sonnet | ~120 | W3-A, W2-B |

**W4-A detail:** Load PHASE-IR flow from W3-A. Instantiate `InMemoryPipelineStore`. Run through DES engine with service time distributions (hardcoded initially, calibrated from ledger data later). FastAPI endpoint on Railway: `POST /api/pipeline/simulate`. Returns: throughput, bottleneck analysis, WIP distribution, optimal pool size recommendation.

### Total Estimate

| Metric | Value |
|--------|-------|
| Tasks | 7 |
| Waves | 4 (W1–W2 parallelizable internally) |
| Total new code | ~560 lines |
| Total new tests | ~40 |
| LLM cost | ~$7–10 |
| Sessions | 2–3 overnight queue runs |

---

## 9. Unified Process Document

This spec, once built, replaces the need for separate process docs. The PHASE-IR flow (W3-A) IS the canonical process definition. English rendered from the IR is the human-readable version.

Prior processes become sections of PROCESS-0020:

| Prior Process | Becomes |
|--------------|---------|
| PROCESS-0013 (Build Integrity) | Section 3: Pipeline Stages (Gate 0, Phase 0–2) |
| PROCESS-0018 (Living Feature Inventory) | Section 3: Archive + Inventory stage |
| PROCESS-0016/0019 (Bee Response Format) | Section 3: Bee Execution stage (8-section + YAML) |
| Q33NR directory state machine | Section 4: Directory State Machine |
| Q33NR dev process flow | Section 3: Pipeline Stages (full sequence) |

PROCESS-0013, 0018, 0016/0019 are not deleted — they're marked as "incorporated into PROCESS-0020" and retained for historical reference.

---

## 10. Success Criteria

This spec is done when:

1. `run_queue.py` uses `PipelineStore` interface (no raw pathlib calls)
2. Specs move through `_active/` with manifests and completion records
3. Crash recovery triages with LLM instead of blind retry
4. Every validation gate and bee execution emits to Event Ledger
5. `InMemoryPipelineStore` passes the same test suite as filesystem version
6. DES engine can load the pipeline IR and produce throughput/bottleneck analysis
7. After 50 specs, the data answers: "Is the IR fidelity gate worth its tokens?"

---

## 11. Open Questions for Q88N

1. **Fidelity threshold:** Currently 0.85. Raise to 0.90 after initial data, or keep?
2. **Triage model:** Haiku for all three triage points, or Sonnet for crash recovery (more complex)?
3. **`_needs_review/` timeout:** 24 hours before warning event — right number?
4. **DES endpoint:** Deploy as part of existing Railway backend, or separate service?
5. **PROCESS-0020 naming:** Unified Build Pipeline, or something else?

---

*"The filesystem is the state machine. The IR is the process. The ledger is the proof. The simulation is the prediction."*
