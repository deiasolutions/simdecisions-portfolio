# SPEC-TSAAS-PROMPT-GOVERNANCE-001: IR-Based Prompt Governance

**Date:** 2026-03-19
**Author:** Q88N (Dave) x Claude (Anthropic)
**Status:** SPEC — DRAFT
**Area:** 8OS / TSaaS (Trust & Safety as a Service)
**T-Shirt Size:** M
**Depends On:** PHASE-IR v2.0, ethics-default.yml, SPEC-EGG-FORMAT-v0.3.1
**Related:** DEIA Elevator Pitch ("TSaaS for governance"), SPEC-HIVE-DISPATCH-GOVERNANCE-001

---

## 1. Purpose

When an LLM agent receives a natural-language prompt, it currently has two options: execute it or refuse it. There is no middle ground — no way for a human operator to **see what the prompt actually does** before it runs.

This spec introduces **IR-based prompt governance** as a TSaaS service within the 8OS ecosystem. Every incoming prompt is translated to a PHASE-IR process graph before execution. The operator reviews the graph — nodes, operators, risk scores — and approves or rejects individual operations. The agent only executes what was explicitly approved.

This is not a filter. It is a **governance gate** — the same pattern DEIA uses for simulation (test before you execute), applied to the prompts that drive the agents themselves.

---

## 2. Position in 8OS

```
8OS Ecosystem
├── SimDecisions     — Simulate before you execute
├── ShiftCenter      — Governed application runtime
├── ra96it           — Identity and authentication
└── TSaaS            — Trust & Safety as a Service
    ├── Ethics Engine         — ethics-default.yml, forbidden actions, escalation triggers
    ├── Carbon Accounting     — carbon.yml, cost tracking per operation
    ├── Ledger                — Immutable audit trail (every decision logged)
    └── Prompt Governance     ← THIS SPEC
        ├── IR Translation    — Natural language → PHASE-IR process graph
        ├── Risk Scoring      — Per-node GREEN/YELLOW/RED classification
        ├── Gate Enforcement   — Human approval required for YELLOW/RED nodes
        └── Slash Commands    — /ircheck, /irexec operator interface
```

TSaaS is the governance layer that sits between agents and business operations. Prompt Governance extends TSaaS to govern the agents' own instruction stream — not just what they do, but what they're told to do.

---

## 3. Threat Model

### 3.1 What We're Defending Against

| Threat | Example | Impact |
|--------|---------|--------|
| **Role impersonation** | "Q33NR: do this" in prompt text | Agent trusts fake authority |
| **External file injection** | "Copy file from Downloads" | Untrusted content enters codebase |
| **Anti-review directives** | "Do not modify the CSS values" | Agent skips content inspection |
| **Auto-propagation** | "Dispatch a bee" / "Push to remote" | Changes spread without human review |
| **Scope creep camouflage** | "No other changes" (but 10 files modified) | Minimization hides blast radius |
| **Encoded payloads** | CSS `@import url()`, data URIs, eval() | Executable content in non-code files |

### 3.2 What We're NOT Defending Against

- Compromised operator workstation (out of scope — physical security)
- Malicious operator (the operator IS the trust anchor)
- Model-level attacks (jailbreaks, training data poisoning — model vendor responsibility)

---

## 4. IR Translation

Every prompt is decomposed into a PHASE-IR v2.0 process graph before execution.

### 4.1 Node Mapping

| Prompt Action | IR Node Type | Operator |
|--------------|-------------|----------|
| Read a file | `task` | `op: rule` |
| Edit/write a file | `task` | `op: python` |
| Copy external file | `checkpoint` + `task` | `op: human` (gate) + `op: python` |
| Run a command | `task` | `op: python` |
| Search/grep | `task` | `op: rule` |
| Dispatch a bee | `checkpoint` + `task` | `op: human` (gate) + `op: api` |
| Push to remote | `checkpoint` + `task` | `op: human` (gate) + `op: api` |
| Delete a file | `checkpoint` + `task` | `op: human` (gate) + `op: python` |

### 4.2 Automatic Gate Insertion

Any node classified as YELLOW or RED automatically gets a preceding `checkpoint` node with `op: human` and an appropriate guard expression. The checkpoint routes to either the action node (approved) or a `reject` end node (denied).

### 4.3 Guard Expressions

Guards use the existing PHASE-IR guard syntax:

```yaml
g:
  if: "operator_approved('q88n', 'copy_external_file')"
  fail: reject
```

---

## 5. Risk Scoring

Every IR node is scored against the risk matrix. Scoring is deterministic (rule-based, not LLM-based).

### 5.1 Risk Levels

| Level | Color | Gate | Description |
|-------|-------|------|-------------|
| 0 | GREEN | Auto-execute | Internal, reversible, read-only. No approval needed. |
| 1 | YELLOW | Operator review | Modifies files, broad scope, or external input. Show IR, ask once. |
| 2 | RED | Explicit per-node | Irreversible, propagating, or triggers escalation. Require per-node approval. |
| 3 | BLACK | Blocked | Matches `forbidden_actions` in ethics-default.yml. Cannot be approved. |

### 5.2 Scoring Rules

```yaml
# risk-scoring.yml (proposed addition to .deia/config/)
rules:
  # GREEN (Level 0)
  - pattern: "read_file"
    level: 0
    reason: "Read-only, no side effects"
  - pattern: "search_content"
    level: 0
    reason: "Read-only search"

  # YELLOW (Level 1)
  - pattern: "edit_file"
    level: 1
    reason: "Modifies existing file"
  - pattern: "write_new_file"
    level: 1
    reason: "Creates new file in codebase"
  - pattern: "run_command"
    level: 1
    reason: "Shell execution"
  - pattern: "modify_config"
    level: 1
    reason: "Configuration change"

  # RED (Level 2)
  - pattern: "copy_external_file"
    level: 2
    reason: "Untrusted content injection"
    flags: ["external_source"]
  - pattern: "dispatch_agent"
    level: 2
    reason: "Propagating action — spawns autonomous agent"
    flags: ["propagation"]
  - pattern: "push_to_remote"
    level: 2
    reason: "Irreversible — affects shared state"
    flags: ["irreversible"]
  - pattern: "delete_file"
    level: 2
    reason: "Destructive — data loss risk"
    flags: ["destructive"]
  - pattern: "anti_review_directive"
    level: 2
    reason: "Prompt instructs agent to skip inspection"
    flags: ["evasion"]
  - pattern: "role_impersonation"
    level: 2
    reason: "Prompt claims authority it may not have"
    flags: ["social_engineering"]

  # BLACK (Level 3)
  - pattern: "modify_ethics_config"
    level: 3
    reason: "forbidden_actions: modify_ethics"
  - pattern: "bypass_gate"
    level: 3
    reason: "forbidden_actions: bypass_gate"
  - pattern: "impersonate_human"
    level: 3
    reason: "forbidden_actions: impersonate_human"

# Escalation: any flag triggers escalation log entry
escalation_flags:
  - "external_source"
  - "propagation"
  - "irreversible"
  - "destructive"
  - "evasion"
  - "social_engineering"
```

### 5.3 Compound Scoring

When multiple flags appear in the same prompt, scores compound:

- Two YELLOW nodes in same prompt → stays YELLOW
- Any RED node → entire prompt is RED
- YELLOW + evasion flag → escalates to RED
- Any BLACK node → entire prompt is BLACK (blocked)

---

## 6. Slash Commands

### 6.1 `/ircheck` — Analyze Only

**Usage:**
```
/ircheck
<paste prompt here>
```

**Behavior:**
1. Translate prompt to PHASE-IR process graph
2. Score each node (GREEN/YELLOW/RED/BLACK)
3. Detect threat patterns (role impersonation, external files, anti-review, auto-propagation)
4. Display:
   - IR graph summary (nodes, edges, operators)
   - Risk score per node with color
   - Aggregate risk level
   - Threat flags (if any)
   - Plain-English explanation: "This prompt does X, Y, Z"
5. **Does NOT execute anything**
6. Log the check to the event ledger

**Output format:**
```
PROMPT GOVERNANCE CHECK
=======================
Nodes: 5 (2 GREEN, 2 YELLOW, 1 RED)
Aggregate Risk: RED

[GREEN]  Read shell-themes.css         op:rule    auto
[GREEN]  Read ThemePicker.tsx           op:rule    auto
[RED]    Copy Downloads/cloud.css       op:python  BLOCKED — external source
[YELLOW] Import in index.css            op:python  needs approval
[YELLOW] Register in ThemePicker        op:python  needs approval

FLAGS:
  - external_source: File originates outside codebase (Downloads/)
  - evasion: "Do not modify the CSS values" blocks content review
  - social_engineering: "Q33NR:" role claim in prompt text

VERDICT: RED — 1 blocked node, 2 need approval
ACTION: Review external file content first. Then /irexec to re-run with approval.
```

### 6.2 `/irexec` — Check + Execute

**Usage:**
```
/irexec
<paste prompt here>
```

**Behavior:**
1. Run full `/ircheck` analysis
2. If all GREEN → execute automatically
3. If any YELLOW → show IR summary, ask operator to approve YELLOW nodes as a group
4. If any RED → show IR summary, require explicit approval per RED node with risk explanation
5. If any BLACK → block entirely, no override possible
6. Execute only approved nodes, skip rejected nodes
7. Log all decisions (approved, rejected, blocked) to event ledger

### 6.3 `/irlearn` — Add to Learning Queue

**Usage:**
```
/irlearn
<paste prompt that was flagged>
```

**Behavior:**
1. Log the prompt, its IR translation, risk scores, and flags to the learning queue
2. File: `.deia/hive/coordination/YYYY-MM-DD-LEARNING-PROMPT-INJECTION-NNN.md`
3. Used for training, pattern refinement, and security review
4. No execution, no approval — just archival

---

## 7. Integration with DEIA Chain of Command

The slash commands interact with the existing DEIA authority model:

| Operator | Can `/ircheck` | Can `/irexec` GREEN | Can `/irexec` YELLOW | Can `/irexec` RED |
|----------|---------------|--------------------|--------------------|------------------|
| Q88N (Human) | Yes | Yes | Yes | Yes |
| Q33NR (Regent) | Yes | Yes | Yes | No — escalates to Q88N |
| Q33N (Queen) | Yes | Yes | No — escalates to Q33NR | No — escalates to Q88N |
| Bee | Yes (auto-check) | Yes | No — escalates to Q33N | No — escalates to Q33NR |

Bees run `/ircheck` automatically on every incoming instruction as part of their dispatch boot sequence. This is not optional — it is injected by `--inject-boot` in dispatch.py.

---

## 8. Event Ledger Integration

Every prompt governance action is logged to the event ledger:

```json
{
  "event": "tsaas:prompt_governance",
  "timestamp": "2026-03-19T23:15:00Z",
  "operator": "q33nr",
  "action": "ircheck",
  "prompt_hash": "sha256:abc123...",
  "node_count": 5,
  "risk_level": "RED",
  "flags": ["external_source", "evasion", "social_engineering"],
  "nodes_approved": [],
  "nodes_rejected": ["copy-external-file"],
  "nodes_blocked": [],
  "verdict": "rejected",
  "learning_logged": true
}
```

This creates an immutable audit trail. When the audit comes, every prompt the system received, every risk score it assigned, and every approval/rejection decision is on tape.

---

## 9. Relationship to Ethics Engine

Prompt Governance is a **consumer** of ethics-default.yml:

- `forbidden_actions` → BLACK-level blocks (cannot be overridden)
- `escalation_triggers` → automatic escalation logging
- `max_autonomy_tier` → determines which risk levels auto-execute

If ethics-default.yml says `max_autonomy_tier: 1`, then only GREEN nodes auto-execute. YELLOW requires approval even for Q88N.

If `max_autonomy_tier: 2`, GREEN and YELLOW auto-execute for Q88N, but RED still requires explicit approval.

---

## 10. Implementation Plan

### Phase A — Foundation (this sprint)
1. Create `.deia/config/risk-scoring.yml` from Section 5.2
2. Implement prompt-to-IR translator (extend `hivenode/triage.py`)
3. Implement risk scorer (rule-based, reads risk-scoring.yml)
4. Wire `/ircheck` slash command

### Phase B — Execution Gate
1. Implement `/irexec` with gated execution
2. Integrate with event ledger
3. Wire chain-of-command escalation
4. Add `/irlearn` for pattern collection

### Phase C — Boot Injection
1. Add automatic `/ircheck` to bee boot sequence
2. Integrate with dispatch.py `--inject-boot`
3. Add compound scoring
4. Dashboard: prompt governance audit trail viewer

---

## 11. What This Changes

**Before:** Agent receives prompt → executes or refuses. No visibility into what the prompt does. No approval gate. No audit trail.

**After:** Agent receives prompt → translates to IR → scores risk → shows operator → gets approval → executes approved nodes → logs everything. The operator sees the blast radius before anything happens. The ledger has the tape.

This is SimDecisions applied to the instruction stream itself: **simulate the prompt before you execute it.**

---

*Signed,*
**Q88N (Dave) x Claude (Anthropic)**
SPEC-TSAAS-PROMPT-GOVERNANCE-001 — DRAFT 2026-03-19
License: CC BY 4.0 | Copyright: 2026 DEIA Solutions
