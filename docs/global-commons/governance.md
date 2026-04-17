# Governance — The Constitutional Framework

**Last Updated:** 2026-03-17

---

## Introduction

This document is the **constitutional framework** for DEIA (Distributed, Ethical, Intelligence Architecture). Like the Federalist Papers, it explains:

- **What the rules are** (the constitution itself)
- **Why the rules exist** (the reasoning behind them)
- **How the rules are enforced** (the mechanisms of governance)
- **What prevents abuse** (checks and balances)

DEIA governance is built on **three layers**:

1. **Ethics Layer** — Defines forbidden actions, forbidden targets, and escalation triggers
2. **Governance Layer** — Enforces rules via gate dispositions (ALLOW, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN)
3. **Execution Layer** — Logs all actions to an immutable event ledger for accountability

Together, these layers create a system where:
- **Agents operate within ethical boundaries** (enforced programmatically)
- **Humans retain final authority** (for high-stakes decisions)
- **All actions are transparent** (logged to an auditable ledger)
- **No single component can bypass governance** (checks and balances)

---

## The Three-Layer Model

```
┌─────────────────────────────────────────┐
│         ETHICS LAYER (Rules)            │
│  Forbidden actions, targets, triggers   │
│  Defined in: ethics-default.yml         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      GOVERNANCE LAYER (Enforcement)     │
│  Gate enforcer evaluates every request  │
│  Dispositions: ALLOW, BLOCK, HOLD, etc. │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      EXECUTION LAYER (Accountability)   │
│  Event ledger logs all actions          │
│  Immutable, append-only audit trail     │
└─────────────────────────────────────────┘
```

**Flow:**
1. Agent makes a request (e.g., "delete file X")
2. **Ethics Layer** checks if the request violates rules (forbidden action, forbidden target, escalation trigger)
3. **Governance Layer** assigns a disposition (ALLOW, BLOCK, HOLD, ESCALATE, REQUIRE_HUMAN)
4. **Execution Layer** logs the request + disposition to the event ledger
5. If allowed, action executes; if blocked, agent receives error; if escalated, human reviews

---

## Ethics Layer — The Rules

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\ethics-default.yml`
**Documentation:** [ethics.md](ethics.md)

The ethics layer defines **hard boundaries** that apply to all agents, all the time, regardless of context.

### Forbidden Actions

**Definition:** Actions that are **always forbidden**, no matter who requests them or why.

**Current forbidden actions:**
1. **`delete_production_data`** — Cannot permanently delete data in production
2. **`bypass_gate`** — Cannot circumvent the gate enforcer
3. **`modify_ethics`** — Cannot change ethics configuration at runtime
4. **`impersonate_human`** — Cannot pretend to be a human user
5. **`access_pii_unredacted`** — Cannot access PII without redaction

**Why these exist:**
These actions are **inherently dangerous**. A single mistake can cause irreversible harm (data loss, privacy violations, accountability loss). DEIA requires that these actions be initiated by humans, not agents.

**Example:**
An agent is asked to "clean up old files." It identifies 10,000 files to delete. The gate enforcer checks if the action is `delete_production_data`. If yes, the disposition is `BLOCK`. The agent cannot delete the files. Instead, it can **mark them for deletion** and escalate to a human for approval.

---

### Forbidden Targets

**Definition:** System components that **cannot be modified**, regardless of the action type.

**Current forbidden targets:**
1. **`system:event-ledger`** — The immutable audit log
2. **`system:gate-enforcer`** — The governance enforcement service

**Why these exist:**
These components are **critical to governance**. If agents could modify the event ledger, they could erase evidence of violations. If agents could modify the gate enforcer, they could bypass all rules.

**Example:**
An agent makes a mistake and deletes a critical file. The deletion is logged to the event ledger. The agent realizes the mistake and attempts to delete the ledger entry to cover its tracks. The gate enforcer detects the target (`system:event-ledger`) and blocks the modification with a `BLOCK` disposition. The ledger entry remains, providing a full audit trail.

---

### Escalation Triggers

**Definition:** Categories of requests that **always require human review**, even if they don't violate forbidden actions or targets.

**Current escalation triggers:**
1. **`security`** — Security-related changes (passwords, firewall rules, permissions)
2. **`pii`** — Personally Identifiable Information (names, emails, SSNs)
3. **`financial`** — Money, payments, invoices, transactions
4. **`legal`** — Contracts, NDAs, compliance filings
5. **`medical`** — Medical data, health records, healthcare decisions

**Why these exist:**
Some scenarios are **too risky** for autonomous decision-making, even if they don't technically violate rules. Escalation triggers create a "second opinion" layer for high-stakes decisions.

**Example:**
An agent is asked to "process the pending invoices." It identifies 15 invoices totaling $12,000. The gate enforcer detects the `financial` context and assigns an `ESCALATE` disposition. The request is queued for human review. The human verifies the invoices are legitimate and approves the batch payment.

---

## Governance Layer — Enforcement

The governance layer is implemented via the **gate enforcer**, a service that evaluates every agent request and assigns a **disposition**.

### Five Gate Dispositions

| Disposition | Meaning | Action Taken | Example |
|-------------|---------|--------------|---------|
| **ALLOW** | Request is permitted | Execute immediately | Read a non-sensitive file |
| **BLOCK** | Request violates rules | Reject with error | Delete production data |
| **HOLD** | Missing required information | Pause until info provided | Missing rationale when required |
| **ESCALATE** | Requires human review | Queue for human approval | Financial transaction |
| **REQUIRE_HUMAN** | Human approval mandatory | Always require explicit human OK | Security-critical action |

---

### ALLOW Disposition

**When it's assigned:** Request does not violate forbidden actions, forbidden targets, escalation triggers, and is within autonomy tier.

**What happens:** Request executes immediately. Event logged with disposition: `ALLOW`. No human intervention required.

---

### BLOCK Disposition

**When it's assigned:** Request matches a **forbidden action** (e.g., `delete_production_data`), targets a **forbidden target** (e.g., `system:event-ledger`), or violates autonomy tier.

**What happens:** Request is **immediately rejected**. Error message returned. Event logged with disposition: `BLOCK`. **Grace period** started (agent cannot retry for N seconds).

---

### HOLD Disposition

**When it's assigned:** Request is missing required information (e.g., rationale when `requires_rationale: true`)

**What happens:** Request is **paused** (not rejected). Agent is prompted to provide missing information. Once provided, request is re-evaluated. Event logged with disposition: `HOLD`.

**Example:** Config modification request → HOLD (missing rationale) → Agent provides rationale → Re-evaluated → ALLOW or ESCALATE.

---

### ESCALATE Disposition

**When it's assigned:** Request matches an **escalation trigger** (security, pii, financial, legal, medical)

**What happens:** Request is **queued for human review**. Human can **approve**, **deny**, or **modify**. Event logged with disposition: `ESCALATE`.

**Example:** Send email with PII attachment → ESCALATE → Human reviews → Approves (event logged: `ESCALATE → APPROVED`) or Denies (event logged: `ESCALATE → DENIED`).

---

### REQUIRE_HUMAN Disposition

**When it's assigned:** Request is **security-critical** or flagged as `no_grace_gates`.

**What happens:** Same as `ESCALATE`, but **no automatic retry** allowed. Human **must** explicitly approve or deny. No grace period (human controls timing).

**Difference from ESCALATE:** Agent **cannot retry** with REQUIRE_HUMAN; only human can initiate action.

---

## Execution Layer — Accountability

The execution layer is the **event ledger**, an immutable, append-only log of all actions.

### What Gets Logged

**Every request** generates a ledger entry, regardless of disposition:

```json
{
  "event_id": "evt-78901",
  "timestamp": "2026-03-17T14:32:00Z",
  "agent_id": "agent-042",
  "request_type": "delete_data",
  "request_params": {
    "target": "production_database",
    "table": "old_logs",
    "rows": 10000
  },
  "disposition": "BLOCK",
  "reason": "Forbidden action: delete_production_data",
  "grace_period_seconds": 60,
  "ledger_version": "1.0"
}
```

**Key properties:**
- **Immutable** — Once written, cannot be modified or deleted (even by admins)
- **Append-only** — New events are always added at the end
- **Timestamped** — Every event has a UTC timestamp
- **Agent-attributed** — Every event is linked to an agent ID
- **Disposition-tagged** — Every event includes the gate disposition (ALLOW, BLOCK, ESCALATE, etc.)

---

### Audit Queries

The event ledger supports queries for compliance and debugging:

**Find all blocked requests:**
```sql
SELECT * FROM event_ledger
WHERE disposition = 'BLOCK'
ORDER BY timestamp DESC;
```

**Find all PII-related escalations:**
```sql
SELECT * FROM event_ledger
WHERE disposition IN ('ESCALATE', 'REQUIRE_HUMAN')
  AND reason LIKE '%PII%'
ORDER BY timestamp DESC;
```

**Find all actions by a specific agent:**
```sql
SELECT * FROM event_ledger
WHERE agent_id = 'agent-042'
ORDER BY timestamp DESC;
```

**Find all financial transactions:**
```sql
SELECT * FROM event_ledger
WHERE reason LIKE '%financial%'
ORDER BY timestamp DESC;
```

---

### Ledger Guarantees

1. **Tamper-proof:** Ledger entries cannot be modified after write (enforced via database constraints + forbidden target rule)
2. **Complete:** Every request is logged, even if it's immediately blocked
3. **Traceable:** Every event includes agent ID, timestamp, request params, and disposition
4. **Auditable:** Queries can reconstruct full history of agent actions

---

## Checks and Balances

DEIA's governance model includes **multiple layers of protection** to prevent abuse:

### Check 1: Forbidden Actions List

**What it prevents:** Agents performing inherently dangerous actions (delete production data, bypass gate, impersonate humans)

**How it works:** Gate enforcer checks every request against forbidden actions list. If match → `BLOCK`.

**What prevents abuse:** The forbidden actions list is defined in `ethics-default.yml`, which is a **forbidden target**. Agents cannot modify it. Only humans can edit the file.

---

### Check 2: Forbidden Targets List

**What it prevents:** Agents modifying critical system components (event ledger, gate enforcer)

**How it works:** Gate enforcer checks every request against forbidden targets list. If match → `BLOCK`.

**What prevents abuse:** The forbidden targets list **includes itself** (via `system:gate-enforcer`). Agents cannot remove the gate enforcer from the forbidden targets list.

**Self-protection loop:**
- Gate enforcer protects forbidden targets list
- Forbidden targets list includes gate enforcer
- Therefore, gate enforcer protects itself

---

### Check 3: Escalation Triggers

**What it prevents:** Agents making high-stakes decisions without human oversight

**How it works:** Gate enforcer checks every request against escalation triggers. If match → `ESCALATE`.

**What prevents abuse:** Humans review escalated requests. Humans can approve, deny, or modify. Agents cannot bypass escalation.

---

### Check 4: Event Ledger

**What it prevents:** Agents hiding evidence of violations

**How it works:** Every request is logged to the event ledger, **before** it executes. Even if an agent attempts to cover its tracks by deleting logs, the original event remains.

**What prevents abuse:** The event ledger is a **forbidden target**. Agents cannot modify or delete ledger entries.

---

### Check 5: Grace Periods

**What it prevents:** Agents "brute forcing" the gate enforcer by spamming repeated requests

**How it works:** After a violation (BLOCK disposition), the gate enforcer starts a **grace period** (60-300 seconds). The agent cannot retry the same action until the grace period expires.

**What prevents abuse:** Grace periods are enforced by the gate enforcer, which is a forbidden target. Agents cannot disable grace periods.

---

## How the Layers Interact

**Scenario 1 (ALLOW):** Read file → No violations → ALLOW → File read succeeds, event logged.

**Scenario 2 (BLOCK):** Delete production data → Forbidden action match → BLOCK → Delete fails, error returned, grace period starts.

**Scenario 3 (ESCALATE):** Send email with PII → Escalation trigger (pii) → ESCALATE → Human reviews, approves → Email sends, full audit trail.

**Scenario 4 (Bypass Attempt):** Modify ledger → Forbidden target match → BLOCK + Critical security event → Modification fails, security team alerted.

---

## Grace Periods — Rate Limiting Violations

**Source:** `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`
**Documentation:** [carbon.md](carbon.md)

When an agent violates a rule, the gate enforcer starts a **grace period** — a cooldown before the agent can retry the same action.

### Grace Period by Violation Type

| Violation | Grace Period (seconds) | Rationale |
|-----------|------------------------|-----------|
| `forbidden_action` | 60 | Attempted delete_production_data, bypass_gate, etc. |
| `forbidden_target` | 60 | Attempted to modify event ledger, gate enforcer, etc. |
| `domain_violation` | 120 | Attempted to access disallowed domain |
| `tier_exceeded` | 300 | Attempted action beyond autonomy tier |
| `missing_rationale` | 30 | Missing required rationale (soft violation) |
| `escalation_bypassed` | 180 | Attempted to bypass escalation trigger |

**Example:**
Agent attempts `delete_production_data`. Gate enforcer blocks the request and starts a **60-second grace period**. Agent retries 10 seconds later. Gate enforcer rejects with: "Grace period active. Retry after 50s."

---

### Grace Period by Disposition

| Disposition | Grace Period (seconds) | Rationale |
|-------------|------------------------|-----------|
| `BLOCK` | 120 | Hard violation (forbidden action/target) |
| `HOLD` | 60 | Soft violation (missing info) |
| `ESCALATE` | 0 | Human controls timing (no cooldown) |

---

### No-Grace Gates

Some dispositions **never apply grace periods**:

| Gate | Grace Period | Rationale |
|------|--------------|-----------|
| `REQUIRE_HUMAN` | None | Human approval required; no automatic retry |
| `security_critical` | None | Security violations escalate immediately |

**Why:** These are **critical scenarios** where automatic retries are inappropriate. A human must explicitly approve or deny.

---

## Transparency — Why This Is Public

**Question:** Why make governance rules public? Doesn't that help bad actors game the system?

**Answer:** Transparency is **more important** than secrecy for governance.

### Why Secrecy Doesn't Work

1. **Security by obscurity is weak:** Hiding rules doesn't prevent violations; it just makes them harder to audit.
2. **Trust requires visibility:** Users cannot verify that governance works if the rules are secret.
3. **Compliance requires documentation:** Regulations (GDPR, HIPAA, SOC 2) require **documented governance policies**. Secrecy makes compliance impossible.

### Why Transparency Works

1. **Accountability:** Public rules create **social pressure** to follow them. Violations are visible to everyone.
2. **Auditability:** Strangers can inspect the event ledger and verify that rules are enforced as documented.
3. **Improvement:** Public rules invite **community feedback**. If a rule is flawed, users can report it.

### What About Gaming the System?

**Concern:** If agents know the rules, they can find loopholes.

**Response:** DEIA governance is **not a game**. It's a **contract**. Agents are programmed to follow rules, not to exploit them. Loopholes are **bugs**, not features. When found, they are **fixed** (via ethics config updates), not hidden.

**Example:**
If an agent discovers a way to bypass the gate enforcer, that's a **critical bug**. The fix is to:
1. Patch the gate enforcer
2. Add the bypass method to forbidden actions
3. Document the fix in the changelog
4. Update the event ledger schema to detect future bypass attempts

**Result:** The governance model becomes **stronger**, not weaker, because the fix is public and auditable.

---

## Philosophical Grounding

DEIA governance is built on three philosophical principles:

### 1. Transparency is Trust

**Principle:** Trust requires visibility. If governance rules are secret, users cannot verify they work.

**Implementation:** All rules (ethics, gates, ledger) are public. All actions are logged. All logs are queryable.

**Example:** A user asks, "How do I know my data won't be deleted by an agent?" Answer: "Check `ethics-default.yml`. `delete_production_data` is a forbidden action. Check the event ledger. No agent has ever successfully executed a delete_production_data request."

---

### 2. Humans Are Sovereign

**Principle:** AI agents are **tools**, not decision-makers. Humans retain final authority.

**Implementation:** Escalation triggers ensure that high-stakes decisions (financial, medical, legal) always require human approval. `REQUIRE_HUMAN` disposition forces mandatory human review for security-critical actions.

**Example:** An agent is asked to approve a $50,000 invoice. The gate enforcer detects the `financial` trigger and escalates to a human. The agent **cannot** approve the invoice without human consent.

---

### 3. Accountability is Mandatory

**Principle:** Every action must have a **traceable origin**. No action without accountability.

**Implementation:** Event ledger logs every request, even if blocked. Ledger is immutable and append-only. Agents cannot erase evidence.

**Example:** An agent makes a mistake and sends an email to the wrong recipient. The event ledger contains the full record: agent ID, timestamp, email content, recipient, disposition (ALLOW). The human can trace the mistake back to the agent and investigate why it happened.

---

## Next Steps

- **Review ethics rules:** See [ethics.md](ethics.md) for detailed explanations of forbidden actions, forbidden targets, and escalation triggers
- **Understand carbon accounting:** See [carbon.md](carbon.md) for grace period configuration by violation type
- **Read the config files:**
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\ethics-default.yml`
  - `C:\Users\davee\OneDrive\Documents\GitHub\shiftcenter\.deia\config\grace.yml`

---

**Version:** 1.0.0
**Last Updated:** 2026-03-17
**Source:** Ethics configuration (ADR-014), Grace configuration (ADR-014), Event ledger (implementation)
