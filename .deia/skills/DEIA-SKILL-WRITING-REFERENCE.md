# DEIA Skill Writing Reference

**Purpose:** Quick-reference for writing SKILL.md files in the DEIA stack. Follows the agentskills.io open standard with DEIA governance extensions.

---

## What a Skill Is

A skill is a script for an operator (actor) to follow. It teaches an agent how to perform a specific task repeatedly. It loads at the time it's needed, in the context it's needed, at the level it needs to be played out.

A skill is NOT a spec (specs describe what to build). A skill is NOT a task file (task files are one-shot dispatches). A skill persists and is reusable.

---

## Directory Structure

```
skill-name/
├── SKILL.md           # Required — frontmatter + instructions
├── governance.yml     # Required in DEIA — governance metadata
├── scripts/           # Optional — executable code
├── references/        # Optional — supplementary docs
└── assets/            # Optional — templates, resources
```

Internal skills live at `.deia/skills/internal/`.  
Imported skills live at `.deia/skills/imported/`.

---

## SKILL.md Format

### Frontmatter (YAML between `---` markers)

```yaml
---
name: my-skill-name
description: >-
  What this skill does AND when to use it. Include keywords
  that help agents identify relevant tasks. 1-1024 chars.
license: Apache-2.0
compatibility: Requires Python 3.12+
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: light
    requires_human: false
---
```

**Required fields:**
- `name` — lowercase + hyphens only, max 64 chars. No uppercase, no underscores, no spaces. Examples: `bee-dispatch`, `spec-writer`, `hive-diagnostics`
- `description` — must describe BOTH what the skill does and when to use it. This is how progressive disclosure works — agents match tasks to skills using this field. Vague descriptions = skill never loads.

**Optional fields:**
- `license` — required for Global Commons publication
- `compatibility` — environment requirements (Python version, tools needed)
- `metadata` — arbitrary key-value. DEIA convention: nest DEIA-specific fields under `metadata.deia`

### Body (Markdown after frontmatter)

```markdown
# Skill Name

## Steps

### Step 1: [First action]
[Detailed instructions...]

### Step 2: [Second action]
[Detailed instructions...]

## Output Format
[What the final result should look like]

## Gotchas
- [Common mistake or misconception]
- [Edge case to watch for]
- [UNDOCUMENTED — needs process doc] ← use this for gaps
```

**Rules:**
- Keep SKILL.md under 500 lines. Move detailed reference material to `references/` files.
- Steps should be concrete and actionable, not abstract guidance.
- Gotchas section is the most valuable part — document real problems the agent will hit.
- If something is undocumented or unresolved, write `[UNDOCUMENTED — needs process doc]` — never invent process details.
- Reference files within the skill using relative paths: `See [reference](references/REFERENCE.md)`

---

## governance.yml (DEIA Extension)

Every skill in the DEIA stack gets a governance.yml sidecar. This is proprietary — not part of the agentskills.io standard.

```yaml
cert_tier: -1              # -1 (untrusted) to 3 (certified)
promoted_from: null
promoted_at: null
promoted_by: null

capabilities:
  filesystem_read: false
  filesystem_write: false
  network_access: false
  shell_exec: false
  user_data_access: false
  model_invocation: false
  event_ledger_write: false

blast_radius: contained    # contained | local | platform | external

budget:
  clock_max_seconds: 60
  coin_max_usd: 0.10
  carbon_max_grams: 5.0

last_scan:
  timestamp: null
  threats_detected: []
  prompt_injection_risk: unknown
  pii_exposure_risk: unknown

event_ledger_id: null
```

### Certification Tiers

| Tier | Label | What It Gets | Who Approves |
|------|-------|-------------|--------------|
| -1 | Untrusted | No filesystem, no network, no shell | Default for all imports |
| 0 | Verified | Read-only filesystem | TASaaS scan clean |
| 1 | Audited | Standard capabilities | Q33NR or Q88N manual review |
| 2 | Tested | Elevated capabilities + network | BAT holdout-set validation |
| 3 | Certified | Unrestricted within policy | Q88N approval, internal only (initially) |

### Carbon Classes

| Class | Budget | Examples |
|-------|--------|---------|
| none | 0g | Deterministic scripts, no LLM |
| light | 5g / invocation | Document generation, test automation |
| medium | 20g / invocation | Code review, data analysis |
| heavy | 50g / invocation | Content creation, multi-model workflows |

---

## Writing Good Descriptions

The description field drives skill activation. Bad descriptions mean the skill never loads.

**Good:**
```yaml
description: >-
  Format and send task files to Mr. Code via the hive dispatch system.
  Use when preparing bee assignments, writing dispatch prompts, or
  routing work through Q33NR to the factory.
```

**Bad:**
```yaml
description: Helps with dispatch.
```

Include: what it does, when to use it, keywords the agent might encounter in a task that should trigger this skill.

---

## Checklist Before Committing

- [ ] `name` is lowercase-hyphenated, max 64 chars
- [ ] `description` says what AND when, 1-1024 chars
- [ ] Body has Steps, Output Format, and Gotchas sections
- [ ] SKILL.md is under 500 lines
- [ ] governance.yml capabilities match what the skill actually needs
- [ ] No invented process details — everything sourced from repo or marked `[UNDOCUMENTED]`
- [ ] No hardcoded colors if frontend-related (`var(--sd-*)` only)
- [ ] Three currencies budgeted in governance.yml

---

## Key Relationships

- **Skills ≠ EGGs.** Skills live in the Global Commons as standard agentskills.io directories. EGGs carry Sets and other artifacts, not skills.
- **Skills ≠ Sets.** Skills talk to the agent. Sets talk to the stage (HiveHostPanes).
- **Skills are entities.** They get four-vector profiles (σ/π/ρ/α) and Event Ledger entries.
- **Operators can author skills.** Same governance applies — enters at tier -1, promotes through certification.
- **Canonical spec:** `docs/specs/SPEC-SKILL-PRIMITIVE-001.md`
