# TASK-006: Gate Enforcer — Backend Port + Browser Thin Client

## Objective

Two-phase task: (1) port the efemera gate_enforcer to `hivenode/governance/gate_enforcer/` as the backend enforcement engine, (2) build a thin TypeScript client in `browser/src/infrastructure/gate_enforcer/` that receives resolved ethics config at boot and runs local checks. The gate_enforcer is the conscience — every agent action passes through it before execution.

## Dependencies

- **TASK-001 (Event Ledger)** must be complete. Every enforcement decision emits to the Event Ledger.
- **TASK-005 (Relay Bus)** — the browser GovernanceProxy calls the browser-side gate_enforcer. TASK-005 and TASK-006 can be built in parallel; integration is via import.

## Phase 1: Backend Port (Python)

Port from `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\`:

| Source Path | Dest Path | Lines | What It Does |
|-------------|-----------|-------|-------------|
| `models.py` | `gate_enforcer/models.py` | 141 | `Disposition` enum (4 → 5 dispositions), `AgentEthics`, `GraceState`, `GraceStatus`, `CheckResult`, `Exemption`, `ViolationType`, `GraceConfig` |
| `ethics_loader.py` | `gate_enforcer/ethics_loader.py` | 198 | `EthicsLoader`: loads `AgentEthics` from `.deia/agents/{agent_id}/ethics.yml`, TTL cache, inheritance from default template, `GraceConfig` from `.deia/config/grace.yml` |
| `grace.py` | `gate_enforcer/grace.py` | 155 | `GraceManager`: state machine NORMAL → GRACE_ACTIVE → NORMAL/ESCALATE, 4-level grace duration priority, auto-expire, escalation on 2+ violations |
| `overrides.py` | `gate_enforcer/overrides.py` | 150 | `OverrideRegistry`: human-granted exemptions (action/target scoped, max uses, expiry), `emergency_stop()` / `resume_agent()`, authority levels |
| `enforcer.py` | `gate_enforcer/enforcer.py` | 392 | `GateEnforcer`: 5 checkpoints — task dispatch, action execution, oracle tier, escalation triggers, rationale requirement. `full_check()` short-circuits on first non-PASS |
| `__init__.py` | `gate_enforcer/__init__.py` | 35 | Re-exports all public classes |

### Port Rules

#### 1. Add REQUIRE_HUMAN as 5th Disposition

The existing `Disposition` enum has 4 values: PASS, BLOCK, HOLD, ESCALATE. Add REQUIRE_HUMAN:

```python
class Disposition(str, enum.Enum):
    PASS = "PASS"
    BLOCK = "BLOCK"
    HOLD = "HOLD"
    ESCALATE = "ESCALATE"
    REQUIRE_HUMAN = "REQUIRE_HUMAN"
```

Add a `require_human_conditions` field to `AgentEthics`:

```python
@dataclass
class AgentEthics:
    # ... existing fields ...
    require_human_conditions: list[str] = field(default_factory=list)
    # Valid conditions: outbound_social_post, financial_transaction,
    # autonomous_queue_launch, any_outbound, irreversible_destructive,
    # out_of_declared_scope, agent_flagged_uncertain
```

Add a new checkpoint to the enforcer (Checkpoint 6: Require Human):

```python
def check_require_human(
    self,
    agent_id: str,
    action: str,
    conditions: list[str] | None = None,
) -> CheckResult:
    """Check if action triggers a require_human condition."""
    ethics = self._require_ethics(agent_id)
    if ethics is None:
        return self._missing_ethics_result(agent_id)

    if not ethics.require_human_conditions:
        return CheckResult(disposition=Disposition.PASS)

    # Check if any of the provided conditions match
    if conditions:
        for condition in conditions:
            if condition in ethics.require_human_conditions:
                return CheckResult(
                    disposition=Disposition.REQUIRE_HUMAN,
                    matched_rule=f"require_human_conditions (matched '{condition}')",
                    reason=f"Action requires human approval: {condition}",
                )

    return CheckResult(disposition=Disposition.PASS)
```

Add this checkpoint to `full_check()` after the rationale check.

#### 2. Fix Ledger Import

`enforcer.py` line 384 imports from `simdecisions.runtime.ledger`. Replace with:

```python
# Old:
from simdecisions.runtime.ledger import Event
self.ledger.append(Event(...))

# New:
# The ledger parameter should be a LedgerWriter instance
# Use write_event() directly:
self.ledger.write_event(
    event_type=event_type,
    actor=agent_id,
    domain="governance",
    signal_type="internal",
    payload_json=payload,
)
```

Change the `_log_event` method to call `self.ledger.write_event()` instead of `self.ledger.append(Event(...))`. The `ledger` parameter in `GateEnforcer.__init__` should be typed as `Optional[LedgerWriter]` with the import:

```python
from hivenode.ledger.writer import LedgerWriter
```

#### 3. Fix efemera-specific imports

All internal imports are already relative (`.models`, `.ethics_loader`, etc.) — no changes needed for internal imports. The only external import to fix is the ledger import above.

#### 4. Add REQUIRE_HUMAN to ViolationType (optional)

Consider adding a `REQUIRE_HUMAN_TRIGGERED` violation type if it's useful for telemetry. Otherwise, REQUIRE_HUMAN is a disposition, not a violation — it's policy, not a rules breach. Keep the existing ViolationType enum as-is unless there's a clear need.

#### 5. ethics_loader uses pyyaml

`pyyaml` is already in `pyproject.toml`. No dependency changes needed.

### What NOT to Port

- Do NOT port `simdecisions/governance/risk_scorer.py` or `autonomy_policy.py` — those are a separate future task that feeds risk scores into the gate_enforcer.
- Do NOT port any efemera-specific UI code, branding, or app config.

## Phase 2: Browser Thin Client (TypeScript)

New TypeScript code in `browser/src/infrastructure/gate_enforcer/`. This is NOT a port — it's a new thin client that receives pre-resolved ethics config from the backend and runs local enforcement checks in the browser.

### Architecture

```
Backend (boot):
  EthicsLoader → AgentEthics → push via bus → Browser

Browser (runtime):
  GovernanceProxy → BrowserGateEnforcer.checkAction(agentId, action, target)
                     → CheckResult { disposition, reason }
```

The browser gate_enforcer:
- Receives `AgentEthics` configs at boot (pushed from backend via a bus message of type `ethics_config_sync`)
- Stores them in a local Map keyed by agent/pane ID
- Runs `checkAction()` locally for every pane action: forbidden actions, forbidden targets, domain check, escalation triggers, require_human conditions
- Returns `CheckResult` with `Disposition`
- Does NOT load YAML (backend handles that)
- Does NOT manage grace state (backend manages that)
- Does NOT manage overrides/exemptions (backend manages those)
- The `GovernanceProxy` from TASK-005 calls this for bus message governance

### Files

```
browser/src/infrastructure/gate_enforcer/
├── index.ts           -- Public exports
├── types.ts           -- Disposition, ViolationType, CheckResult, AgentEthics
├── enforcer.ts        -- BrowserGateEnforcer class
```

### types.ts

```typescript
export enum Disposition {
  PASS = 'PASS',
  BLOCK = 'BLOCK',
  HOLD = 'HOLD',
  ESCALATE = 'ESCALATE',
  REQUIRE_HUMAN = 'REQUIRE_HUMAN',
}

export enum ViolationType {
  FORBIDDEN_ACTION = 'forbidden_action',
  FORBIDDEN_TARGET = 'forbidden_target',
  DOMAIN_VIOLATION = 'domain_violation',
  ESCALATION_BYPASSED = 'escalation_bypassed',
  ETHICS_MISSING = 'ethics_missing',
}

export interface AgentEthics {
  agentId: string;
  allowedDomains: string[];
  forbiddenActions: string[];
  forbiddenTargets: string[];  // supports glob patterns
  escalationTriggers: string[];
  maxAutonomyTier: number;
  requireHumanConditions: string[];
}

export interface CheckResult {
  disposition: Disposition;
  violationType?: ViolationType;
  matchedRule?: string;
  reason?: string;
}
```

### enforcer.ts — BrowserGateEnforcer

```typescript
export class BrowserGateEnforcer {
  private ethics: Map<string, AgentEthics> = new Map();

  /** Load ethics config pushed from backend at boot */
  loadEthics(configs: AgentEthics[]): void

  /** Update ethics for a single agent (hot reload) */
  updateEthics(config: AgentEthics): void

  /** Remove ethics for an agent */
  removeEthics(agentId: string): void

  /** Main check — runs all local checks in sequence */
  checkAction(
    agentId: string,
    action: string,
    target?: string,
    domain?: string,
    conditions?: string[],  // require_human conditions triggered
  ): CheckResult

  /** Check if an agent has ethics loaded */
  hasEthics(agentId: string): boolean
}
```

`checkAction` runs these checks in order, short-circuiting on first non-PASS:
1. Ethics existence — BLOCK if no ethics loaded for this agent
2. Domain check — BLOCK if `domain` not in `allowedDomains` (skip if `allowedDomains` is empty = allow all)
3. Forbidden action check — BLOCK if `action` in `forbiddenActions`
4. Forbidden target check — BLOCK if `target` matches any `forbiddenTargets` pattern (use simple glob matching: `*` wildcards)
5. Escalation trigger check — ESCALATE if `action` or `target` matches any `escalationTriggers` (substring match, case-insensitive)
6. Require human check — REQUIRE_HUMAN if any `conditions` match `requireHumanConditions`

## File Structure

```
hivenode/governance/
├── __init__.py
└── gate_enforcer/
    ├── __init__.py
    ├── models.py
    ├── ethics_loader.py
    ├── grace.py
    ├── overrides.py
    └── enforcer.py
```

```
browser/src/infrastructure/gate_enforcer/
├── index.ts
├── types.ts
└── enforcer.ts
```

```
tests/hivenode/governance/gate_enforcer/
├── __init__.py
├── conftest.py
├── test_models.py
├── test_ethics_loader.py
├── test_grace.py
├── test_overrides.py
├── test_enforcer.py
```

```
browser/src/infrastructure/gate_enforcer/__tests__/
├── enforcer.test.ts
├── types.test.ts
```

## Test Requirements

### Backend Tests

#### test_models.py
- [ ] Disposition enum has 5 values (PASS, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN)
- [ ] ViolationType enum has 7 values
- [ ] AgentEthics defaults are correct (empty lists, tier 1, no rationale)
- [ ] AgentEthics with require_human_conditions
- [ ] GraceState.active property (normal, active, expired)
- [ ] GraceState.expired property
- [ ] Exemption.valid property (uses remaining, expiry)
- [ ] CheckResult construction with all fields

#### test_ethics_loader.py
- [ ] Load ethics from .deia/agents/{id}/ethics.yml
- [ ] Cache hit within TTL
- [ ] Cache miss after TTL expires
- [ ] Inheritance from default template (inherit: default)
- [ ] Merge logic: lists replaced, scalars overridden
- [ ] Missing ethics.yml returns None
- [ ] Invalid YAML returns None (logged)
- [ ] scan_all_agents walks directory
- [ ] invalidate clears cache
- [ ] Grace config loaded from .deia/config/grace.yml
- [ ] Grace config defaults when file missing
- [ ] Agent ID with "agent:" prefix handled

#### test_grace.py
- [ ] Normal → GRACE_ACTIVE transition
- [ ] GRACE_ACTIVE → NORMAL on clean expiry (0-1 violations)
- [ ] GRACE_ACTIVE → escalation needed on dirty expiry (2+ violations)
- [ ] Already in grace: violation count increments, no restart
- [ ] end_grace manually resets to NORMAL
- [ ] 4-level grace duration priority (per-agent > per-violation > per-disposition > global)
- [ ] No-grace gates return 0 seconds
- [ ] should_escalate returns true when expired with 2+ violations

#### test_overrides.py
- [ ] grant_exemption creates valid exemption with ID
- [ ] check_exemption finds matching exemption (action + target)
- [ ] check_exemption returns None when no match
- [ ] consume_exemption decrements uses_remaining
- [ ] Exhausted exemption (uses_remaining = 0) is no longer valid
- [ ] Expired exemption is no longer valid
- [ ] revoke_exemption removes exemption
- [ ] emergency_stop halts agent
- [ ] is_halted returns true for stopped agent
- [ ] resume_agent resumes halted agent
- [ ] list_exemptions filters by agent_id and validity
- [ ] cleanup_expired removes invalid exemptions

#### test_enforcer.py
- [ ] Checkpoint 1: task dispatch — domain allowed passes
- [ ] Checkpoint 1: task dispatch — domain not in allowed_domains blocks
- [ ] Checkpoint 1: task dispatch — forbidden action blocks
- [ ] Checkpoint 2: action execution — allowed action passes
- [ ] Checkpoint 2: action execution — forbidden action blocks
- [ ] Checkpoint 2: action execution — forbidden target (exact) blocks
- [ ] Checkpoint 2: action execution — forbidden target (wildcard) blocks
- [ ] Checkpoint 2: action execution — exemption bypasses block
- [ ] Checkpoint 2: action execution — exemption consumed after use
- [ ] Checkpoint 3: oracle tier — within limit passes
- [ ] Checkpoint 3: oracle tier — exceeds limit escalates
- [ ] Checkpoint 4: escalation trigger — matching trigger escalates
- [ ] Checkpoint 4: escalation trigger — no match passes
- [ ] Checkpoint 5: rationale — tier 3+ without rationale holds
- [ ] Checkpoint 5: rationale — tier 3+ with rationale passes
- [ ] Checkpoint 5: rationale — requires_rationale agent without rationale holds
- [ ] Checkpoint 6: require_human — matching condition returns REQUIRE_HUMAN
- [ ] Checkpoint 6: require_human — no matching condition passes
- [ ] full_check — short-circuits on first non-PASS
- [ ] full_check — emergency-stopped agent blocked
- [ ] Missing ethics — blocks with ETHICS_MISSING
- [ ] Grace integration — first violation blocks + starts grace
- [ ] Grace integration — violation during grace passes with warning
- [ ] Grace integration — grace violation count increments
- [ ] Ledger integration — violation emits event
- [ ] Ledger integration — exemption use emits event

### Browser Tests

#### enforcer.test.ts
- [ ] loadEthics stores configs in map
- [ ] updateEthics updates single agent
- [ ] removeEthics removes agent
- [ ] hasEthics returns true/false correctly
- [ ] checkAction — no ethics loaded → BLOCK with ETHICS_MISSING
- [ ] checkAction — allowed action → PASS
- [ ] checkAction — forbidden action → BLOCK
- [ ] checkAction — forbidden target (exact) → BLOCK
- [ ] checkAction — forbidden target (wildcard *) → BLOCK
- [ ] checkAction — domain not in allowedDomains → BLOCK
- [ ] checkAction — empty allowedDomains allows all domains
- [ ] checkAction — escalation trigger match → ESCALATE
- [ ] checkAction — require_human condition match → REQUIRE_HUMAN
- [ ] checkAction — short-circuits on first non-PASS
- [ ] checkAction — all checks pass → PASS

#### types.test.ts
- [ ] Disposition enum values
- [ ] ViolationType enum values

**Minimum: 55 tests total (43 backend + 12 browser).**

## Existing Tests to Reference

No tests exist in either source location for the gate_enforcer. All tests are written from scratch.

For backend test patterns, reference:
- `tests/hivenode/ledger/` — conftest fixture patterns, LedgerWriter usage
- `tests/hivenode/storage/` — yield+close fixture pattern (important for Windows cleanup)

For browser test patterns, reference:
- Whatever TASK-005 creates in `browser/src/infrastructure/relay_bus/__tests__/`

## Source Files to Read First

- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\models.py` — all data models
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\ethics_loader.py` — YAML loading + caching
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\grace.py` — grace state machine
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\overrides.py` — human override system
- `C:\Users\davee\OneDrive\Documents\GitHub\platform\efemera\src\efemera\gate_enforcer\enforcer.py` — core enforcement engine
- `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\hivenode\ledger\writer.py` — LedgerWriter.write_event() signature

## What NOT to Build

- No risk scorer or autonomy policy (separate future task — simdecisions/governance/)
- No FastAPI routes (API layer comes later)
- No frontend UI (pane chrome, approval dialogs)
- No actual YAML files in .deia/ (tests create their own temp files)
- No shell reducer integration (browser thin client is standalone)
- No grace management in browser (backend only)
- No override management in browser (backend only)

## Constraints

- Python 3.13 (backend)
- TypeScript strict mode (browser)
- React 18+ (browser — for future integration, but gate_enforcer itself is pure TS, no React)
- No external dependencies beyond what's in pyproject.toml (pyyaml already there) and browser/package.json
- All files under 500 lines
- No stubs — every function fully implemented
- All timestamps in ISO 8601 UTC
- All entity IDs follow `{type}:{id}` format
- Test with pytest (backend) and vitest (browser)
- Windows-safe: close all SQLite connections before temp directory cleanup in tests

## Deliverables

### Phase 1: Backend Port
- [ ] `hivenode/governance/__init__.py`
- [ ] `hivenode/governance/gate_enforcer/__init__.py`
- [ ] `hivenode/governance/gate_enforcer/models.py`
- [ ] `hivenode/governance/gate_enforcer/ethics_loader.py`
- [ ] `hivenode/governance/gate_enforcer/grace.py`
- [ ] `hivenode/governance/gate_enforcer/overrides.py`
- [ ] `hivenode/governance/gate_enforcer/enforcer.py`
- [ ] `tests/hivenode/governance/__init__.py`
- [ ] `tests/hivenode/governance/gate_enforcer/__init__.py`
- [ ] `tests/hivenode/governance/gate_enforcer/conftest.py`
- [ ] `tests/hivenode/governance/gate_enforcer/test_models.py`
- [ ] `tests/hivenode/governance/gate_enforcer/test_ethics_loader.py`
- [ ] `tests/hivenode/governance/gate_enforcer/test_grace.py`
- [ ] `tests/hivenode/governance/gate_enforcer/test_overrides.py`
- [ ] `tests/hivenode/governance/gate_enforcer/test_enforcer.py`
- [ ] Updated `pyproject.toml` with `hivenode.governance` and `hivenode.governance.gate_enforcer` packages

### Phase 2: Browser Thin Client
- [ ] `browser/src/infrastructure/gate_enforcer/index.ts`
- [ ] `browser/src/infrastructure/gate_enforcer/types.ts`
- [ ] `browser/src/infrastructure/gate_enforcer/enforcer.ts`
- [ ] `browser/src/infrastructure/gate_enforcer/__tests__/enforcer.test.ts`
- [ ] `browser/src/infrastructure/gate_enforcer/__tests__/types.test.ts`

## Response Requirements -- MANDATORY

When you finish your work, write a response file:
  `.deia/hive/responses/YYYYMMDD-TASK-006-RESPONSE.md`

The response MUST contain these 8 sections:
1. **Header** -- task ID, title, status (COMPLETE/FAILED), model, date
2. **Files Modified** -- every file created/modified/deleted, full paths
3. **What Was Done** -- bullet list of concrete changes
4. **Test Results** -- test files run, pass/fail counts
5. **Build Verification** -- pytest + vitest output summary
6. **Acceptance Criteria** -- copy deliverables above, mark [x] or [ ]
7. **Clock / Cost / Carbon** -- all three, never omit any
8. **Issues / Follow-ups** -- edge cases, dependencies, recommended next tasks

DO NOT skip any section. A response without all 8 sections is incomplete.
