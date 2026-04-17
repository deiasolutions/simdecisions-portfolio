---
name: process-writer
description: >-
  Write a new PROCESS-XXXX document in DEIA standard format with Rule,
  When to Apply, Steps, Success Criteria, Rollback, Telemetry Plan, and
  Change Log sections. Use when codifying a new workflow, documenting a
  repeated procedure, or creating LLM-agnostic operational guidelines.
license: Proprietary
compatibility: Requires access to .deia/processes/ directory
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: none
    requires_human: false
---

# Process Writer

## Steps

### Step 1: Determine Process Number

Check existing processes to find the next available number:

```bash
ls .deia/processes/PROCESS-*.md
```

**Numbering convention:**
- `PROCESS-XXXX-process-name.md` where XXXX is zero-padded (e.g., PROCESS-0001, PROCESS-0042, PROCESS-0314)
- For meta-processes (process about processes), use `PROCESS-LIBRARY-*.md`

**Example:**
- Existing: `PROCESS-0001.md`, `PROCESS-0013.md`, `PROCESS-0042.md`
- Next available: `PROCESS-0043-your-process-name.md`

### Step 2: Write Process Header

Start with title, metadata, and status:

```markdown
# PROCESS-XXXX: {Process Name}

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** DRAFT | OFFICIAL | DEPRECATED
**Authority:** Q88N | Q33N | Q88NR
**Applies To:** {scope: all bees, Q33N only, specific subsystem, etc.}

---
```

**Status values:**
- **DRAFT** — under review, not yet official
- **OFFICIAL** — approved, in active use
- **DEPRECATED** — replaced by newer process, kept for historical reference

### Step 3: Write Overview Section (Optional)

If the process needs context or background, add a brief overview:

```markdown
## Overview

{1-3 paragraphs explaining what problem this process solves, when it was created, and why it exists}
```

**When to include:**
- Process is complex or non-obvious
- Process was created in response to a specific failure (e.g., PROCESS-0013 from Q33N-003B)
- Process has important historical context

**When to skip:**
- Process is self-explanatory from the title
- Process is trivial (< 5 steps)

### Step 4: Write Rule Section (MANDATORY)

The Rule section answers: "What is this process?" in 1-2 sentences.

```markdown
## Rule

{Concise statement of what this process does and why it exists}
```

**Examples:**
- "All task files must include 8-section response requirements template to ensure consistent reporting."
- "Batch work breakdown uses wave system (Wave 0/A/B/C/D/E) to organize dependencies and parallelization."
- "Build integrity validation runs Gate 0 + 3 phases to ensure requirement coverage and semantic fidelity before implementation."

### Step 5: Write When to Apply Section (MANDATORY)

Specify the trigger conditions for this process:

```markdown
## When to Apply

This process applies when:
- {Condition 1}
- {Condition 2}
- {Condition 3}

This process does NOT apply when:
- {Exception 1}
- {Exception 2}
```

**Be specific.** Vague triggers like "when needed" or "when appropriate" don't help LLMs decide when to invoke the process.

### Step 6: Write Steps Section (MANDATORY)

Numbered steps that any agent can follow:

```markdown
## Steps

### Step 1: {First Action}

{Detailed instructions for this step}

**Inputs:**
- {What you need before starting this step}

**Outputs:**
- {What this step produces}

**Example:**
{Code snippet, command, or concrete example}

### Step 2: {Second Action}

{Instructions}

### Step 3: {Third Action}

{Instructions}
```

**Rules for steps:**
- Numbered sequentially
- Each step is concrete and actionable
- No ambiguity (e.g., "review the code" → "run pytest and verify 0 failures")
- Include examples for non-trivial steps
- LLM-agnostic (any model can follow them)

### Step 7: Write Success Criteria Section (MANDATORY)

How do you know the process completed successfully?

```markdown
## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

**Process succeeds when ALL criteria are met.**
```

**Use checkboxes** for each criterion so bees can mark completion.

### Step 8: Write Rollback Section (MANDATORY)

What to do if the process fails mid-execution:

```markdown
## Rollback

If this process fails:

1. {First rollback action}
2. {Second rollback action}
3. {Escalation: who to notify, what to report}

**When to rollback:**
- {Condition 1}
- {Condition 2}

**When NOT to rollback:**
- {Exception where you continue despite failure}
```

**If no rollback is possible:**
```markdown
## Rollback

This process has no rollback mechanism. If it fails, escalate to Q88N with diagnostic report.
```

### Step 9: Write Telemetry Plan Section (OPTIONAL)

What metrics, logs, or events to capture:

```markdown
## Telemetry Plan

**Events to log:**
- {Event 1}: {when it fires, what data it contains}
- {Event 2}: {when it fires, what data it contains}

**Metrics to track:**
- {Metric 1}: {how to measure, success threshold}
- {Metric 2}: {how to measure, success threshold}

**Reports generated:**
- {Report 1}: {format, location, frequency}
```

**When to include:**
- Process involves automation (queue runner, dispatcher, scheduler)
- Process has measurable outcomes (cost, time, coverage)
- Process needs audit trail (Event Ledger integration)

**When to skip:**
- Process is manual (no automation)
- Process has no measurable outputs

### Step 10: Write Integration Section (OPTIONAL)

How this process relates to other processes or systems:

```markdown
## Integration

**Dependencies:**
- This process requires {other process} to run first
- This process uses {tool/system}

**Upstream processes:**
- {Process A} triggers this process

**Downstream processes:**
- This process outputs to {Process B}

**Related ADRs:**
- ADR-XXX: {title and relevance}
```

### Step 11: Write Change Log Section (MANDATORY)

Track all changes to this process:

```markdown
## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | YYYY-MM-DD | Initial process documentation | Q88N |
```

**Update this table whenever the process changes.** Increment version for major changes (1.0 → 2.0), minor for clarifications (1.0 → 1.1).

### Step 12: Save Process File

Save to `.deia/processes/PROCESS-XXXX-process-name.md`

**Naming rules:**
- Use lowercase for process name part
- Use hyphens, not underscores or spaces
- Keep name short (< 50 chars)

**Examples:**
- `PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`
- `PROCESS-0042-task-lifecycle.md`
- `PROCESS-LIBRARY-V2.md` (meta-process)

## Output Format

Complete process file structure:

```markdown
# PROCESS-XXXX: {Process Name}

**Version:** 1.0
**Date:** YYYY-MM-DD
**Status:** DRAFT | OFFICIAL | DEPRECATED
**Authority:** Q88N | Q33N | Q88NR
**Applies To:** {scope}

---

## Overview (optional)

{Background and context}

---

## Rule

{1-2 sentence statement of what this process is}

---

## When to Apply

This process applies when:
- {Condition 1}
- {Condition 2}

This process does NOT apply when:
- {Exception 1}

---

## Steps

### Step 1: {Action}
{Instructions}

### Step 2: {Action}
{Instructions}

---

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}

---

## Rollback

{What to do if process fails}

---

## Telemetry Plan (optional)

{Events, metrics, reports}

---

## Integration (optional)

{Dependencies, upstream/downstream processes, related ADRs}

---

## Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | YYYY-MM-DD | Initial documentation | Q88N |
```

## Gotchas

### 1. Process ≠ Spec
**Spec** describes WHAT to build (a feature, a system).
**Process** describes HOW to do a task repeatedly (a workflow).

Don't write a process when you need a spec, and vice versa.

### 2. LLM-Agnostic Language
Processes are followed by bees running on different LLM vendors (Claude, Gemini, Codex, Llama). Don't reference Claude-specific features or assume a specific tool is available.

### 3. Steps Must Be Concrete
Vague: "Review the code"
Concrete: "Run `pytest tests/` and verify 0 test failures. If tests fail, document failures in response file."

### 4. Success Criteria Are Binary
Each criterion should be answerable with YES or NO. Avoid vague criteria like "code quality is good" (not measurable).

### 5. Processes Live in .deia/processes/
Not `docs/`, not `.deia/hive/`, not `.deia/config/`. Keep them centralized.

### 6. Status Progression: DRAFT → OFFICIAL → DEPRECATED
New processes start as DRAFT. After review and approval, promote to OFFICIAL. When replaced, mark DEPRECATED (don't delete).

### 7. Change Log Is Mandatory
Even if version 1.0 is the only version, include the Change Log table. It establishes the pattern for future updates.

### 8. Rollback Is Mandatory
Even if rollback is "escalate to Q88N", document it. Don't skip this section.

### 9. Numbering Gaps Are OK
If PROCESS-0013 exists and the next process is PROCESS-0042, that's fine. Gaps indicate processes were written out of sequence or deprecated processes were removed.

### 10. [UNDOCUMENTED — needs process doc]
Process review and approval workflow. Current practice: Q88N reviews DRAFT processes, promotes to OFFICIAL. No formal review checklist or multi-reviewer process exists.

### 11. [UNDOCUMENTED — needs process doc]
Process versioning semantics. When does 1.0 → 2.0 (major) vs 1.0 → 1.1 (minor) vs 1.0.0 → 1.0.1 (patch)? Current practice: informal, no strict semver.

### 12. Meta-Processes Use Different Naming
`PROCESS-LIBRARY-V2.md` is a meta-process (collection of processes). It doesn't follow PROCESS-XXXX numbering. Use `PROCESS-{NAME}-{VERSION}.md` for meta-processes.
