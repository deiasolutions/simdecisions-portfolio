---
name: spec-writer
description: >-
  Write specifications in DEIA format for new features, processes, or
  architectural decisions. Use when designing a new component, planning
  a major refactor, documenting a decision, or converting informal
  requirements into formal specs. Covers frontmatter fields, standard
  sections, status values, storage location, and the NEEDS DAVE INPUT
  convention for unresolved design questions.
license: Proprietary
compatibility: Markdown knowledge
metadata:
  author: Q88N
  version: "1.0"
  deia:
    cert_tier: 3
    carbon_class: medium
    requires_human: false
---

# Spec Writer

## When to Use

- Planning a new feature or architectural change
- Converting verbal requirements into formal specifications
- Documenting a design decision before implementation
- Writing an ADR (Architecture Decision Record)
- Creating process documentation (PROCESS-XXXX format)
- Responding to "write a spec for X" requests

## Steps

### Step 1: Survey Existing Specs

Before writing a new spec, grep the repo to understand the current pattern:

```bash
# Find recent specs
ls -lt docs/specs/SPEC-*.md | head -10

# Sample a few to extract structure
cat docs/specs/SPEC-SKILL-PRIMITIVE-001.md
cat docs/specs/SPEC-BUILD-QUEUE-001.md
```

**Observed pattern (as of 2026-04-12):**
- Frontmatter with metadata
- Standard sections (varies by spec type)
- Status field tracks lifecycle
- Tags for categorization
- Cross-references to ADRs, tasks, other specs

### Step 2: Choose Spec Type

DEIA specs come in several flavors:

| Type | Prefix | What It Describes | Example |
|------|--------|-------------------|---------|
| **Feature Spec** | SPEC-XXX-NNN | New user-facing capability | SPEC-SKILL-PRIMITIVE-001 |
| **Architecture Decision** | SPEC-XXX-NNN or ADR-NNN | System design choice | SPEC-PIPELINE-001-UNIFIED-BUILD-PIPELINE |
| **Process Spec** | PROCESS-XXXX | Workflow or procedure | PROCESS-0013 (Gate 0 validation) |
| **Wave Plan** | WAVE-N-XXX | Multi-task coordination | WAVE-3-QUEUE-SPECS |
| **Port Spec** | SPEC-PORT-XXX-NNN | Migration from old system | SPEC-PORT-RAG-001-rag-pipeline-port |

### Step 3: Write Frontmatter

Every spec starts with YAML frontmatter:

```markdown
---
title: SPEC-XXX-NNN: Short Title
version: 1.0
date: YYYY-MM-DD
author: Q88N | Q33N | Dave
status: DRAFT | REVIEW | APPROVED | IMPLEMENTED | DEPRECATED
tags: [#keyword1, #keyword2, #component]
related:
  - ADR-NNN
  - TASK-XXX
  - SPEC-YYY-MMM
---
```

**Field explanations:**
- `title` — Full identifier + human-readable title
- `version` — Increments on major revisions (usually starts at 1.0)
- `date` — ISO format (YYYY-MM-DD)
- `author` — Who wrote it (Q88N = Dave, Q33N = coordinator, specific bee ID)
- `status` — Lifecycle state (see §Step 5)
- `tags` — Searchable keywords, component names, cross-cutting concerns
- `related` — Links to ADRs, tasks, other specs (optional)

### Step 4: Write Standard Sections

**Minimum sections for feature specs:**

```markdown
## Problem Statement
[What problem does this solve? Why does it matter? What's broken/missing today?]

## Objective
[What will be different after this is implemented? 1-3 sentences.]

## Proposed Solution
[High-level approach. Not implementation details yet — just the strategy.]

### Design Decisions
[Key choices made. Format: "Decision: X. Rationale: Y."]

## Implementation
[Detailed technical design. File paths, APIs, data models, algorithms.]

### Files to Create/Modify
- `path/to/file1.py` — What changes
- `path/to/file2.tsx` — What changes

### API Surface
[New routes, function signatures, CLI commands, etc.]

### Data Models
[New tables, schemas, types]

## Acceptance Criteria
- [ ] Criterion 1 (testable, measurable)
- [ ] Criterion 2
- [ ] Criterion 3

## Testing Strategy
[Unit tests, integration tests, e2e tests, manual smoke tests]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Risk 1 | High | Mitigation strategy |

## ADR Cross-References
- **ADR-NNN:** Related decision, how it impacts this spec

## Open Questions
- **NEEDS DAVE INPUT:** Unresolved design question 1?
- **NEEDS DAVE INPUT:** Unresolved design question 2?
```

**Optional sections (add as needed):**
- **Dependencies:** Other specs/tasks that must complete first
- **Migration Path:** How to transition from old to new
- **Performance Considerations:** Expected throughput, latency, resource usage
- **Security Implications:** Auth, permissions, data exposure
- **Carbon Impact:** If LLM-heavy or compute-intensive

### Step 5: Status Values

Specs move through this lifecycle:

| Status | Meaning | Who Can Set |
|--------|---------|-------------|
| **DRAFT** | Work in progress, not ready for review | Author |
| **REVIEW** | Ready for Q88N review | Q33N or author |
| **APPROVED** | Q88N approved, ready to implement | Q88N only |
| **IMPLEMENTED** | Code merged, tests passing, in production | Q33N after verification |
| **DEPRECATED** | No longer relevant, superseded | Q88N only |
| **HOLD** | Blocked on external dependency or strategic pause | Q88N or Q33NR |

**State transitions:**
```
DRAFT → REVIEW → APPROVED → IMPLEMENTED
   ↓        ↓         ↓
  HOLD    HOLD      HOLD
   ↓        ↓         ↓
DEPRECATED
```

### Step 6: Use NEEDS DAVE INPUT Convention

If you encounter unresolved design questions, do NOT invent answers. Flag them:

```markdown
## Open Questions

- **NEEDS DAVE INPUT:** Should we use Postgres or stick with .data/ local files for inventory?
- **NEEDS DAVE INPUT:** OAuth flow — redirect to Vercel frontend or Railway backend?
- **NEEDS DAVE INPUT:** Carbon budget for this feature — 50g or 200g per invocation?
```

**Why this matters:**
- Prevents bees from making strategic decisions (violates chain of command)
- Forces explicit human approval on architecture choices
- Documents decision points for future reference

### Step 7: Store in Correct Location

**Feature specs:** `docs/specs/SPEC-XXX-NNN-<slug>.md`

**Process specs:** `docs/processes/PROCESS-XXXX-<slug>.md` (or inline in .deia/hive/ if hive-specific)

**Wave plans:** `docs/specs/WAVE-N-<slug>.md`

**Archived specs:** `docs/specs/_archive/` (for deprecated/superseded specs)

**Absolute paths (Windows):**
```
C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\docs\specs\SPEC-XXX-NNN.md
```

### Step 7b: Queue Submission (Factory Specs)

If this spec will be submitted to the **factory queue** (not just stored in `docs/specs/`), it must pass Gate 0 automated validation. The full format guide is in `.deia/hive/queue/SUBMISSION-CHECKLIST.md` — **read it before writing a queue spec.**

Key differences from `docs/specs/` specs:

**1. YAML frontmatter uses queue fields (not docs/specs fields):**

```yaml
---
id: SPEC-XXX-NNN
priority: P0
model: sonnet
role: bee          # or: queen, regent
depends_on: [SPEC-OTHER-001, SPEC-OTHER-002]
---
```

| Field | Required | Values |
|-------|----------|--------|
| `id` | Yes | Unique spec ID matching filename |
| `priority` | Yes | P0 (urgent), P1 (normal), P2 (later), P3 (backlog) |
| `model` | Yes | haiku, sonnet, opus |
| `role` | Yes | bee, queen, or regent (see Role Guide) |
| `depends_on` | No | List of spec IDs that must be in `_done/` first |

**Role Guide — when to use each value:**

| Role | Who Runs It | What It Does | When to Use |
|------|-------------|--------------|-------------|
| `bee` | Worker (b33) | Writes code, runs tests, reports results | Default. Any spec that produces code changes |
| `queen` | Coordinator (Q33N) | Reads spec, writes sub-specs, dispatches bees | Multi-phase work that produces other specs as output |
| `regent` | Regent (Q33NR) | Communicates with human, delegates to coordinator | Rare. Strategic review or escalation tasks |

Queen specs must include an EXECUTE mode directive in constraints so the coordinator acts immediately:

```markdown
## Constraints
- You are in EXECUTE mode. Create all sub-specs. Do NOT ask for approval.
- Every sub-spec must conform to `.deia/hive/queue/SUBMISSION-CHECKLIST.md`
- Sub-specs go to `.deia/hive/queue/backlog/`
```

**2. Gate 0 checks (6 automated validations, ALL must pass):**

| Check | What It Validates | How to Pass |
|-------|------------------|-------------|
| `priority_present` | `## Priority` section exists with P0-P3 | Add `## Priority` heading with value on next line |
| `acceptance_criteria_present` | At least 1 `- [ ]` item under `## Acceptance Criteria` | Use `- [ ]` checkbox format, NOT numbered lists |
| `file_paths_exist` | Every path in `## Files to Read First` exists on disk | Verify paths before submitting |
| `deliverables_coherence` | Deliverables don't contradict acceptance criteria | Don't say "DO NOT modify X" if AC says "fix X" |
| `scope_sanity` | Objective doesn't reference forbidden files | Align objective with constraints |
| `ir_density` | Information density score >= 0.200 | Use tables, checklists, file paths, code blocks |

**3. IR density >= 0.200 is mandatory.** The score measures the ratio of structured content (tables, checklists, file paths, code blocks) to total prose. Specs that are mostly prose will fail. Add:
- Tables for deliverables, file mappings, test matrices
- `- [ ]` checklists for acceptance criteria (minimum 3-5 items)
- Concrete file paths in `## Files to Read First` and `## Files to Modify`
- Code blocks for commands, examples, formulas

**4. Where to place queue specs:**

| Destination | When |
|-------------|------|
| `.deia/hive/queue/backlog/` | Non-urgent, wait for queue runner to pick up |
| `.deia/hive/queue/` (root) | Urgent, queue runner scans root first |

**5. Queue runner rejection caching:** If a spec is rejected by Gate 0, the queue runner caches the filename in memory. Even if you fix the file in place, the runner won't re-scan it until restarted. After fixing a bounced spec, either restart the queue runner or move the file to a new location.

### Step 8: Link from Related Artifacts

After writing a spec, link it from:

- **Task files** that implement it (in Context section)
- **ADRs** that reference it
- **Other specs** that depend on it (in related: frontmatter)
- **README or index** if it's a major feature

## Output Format

A complete spec should be:

- **Self-contained:** Readable without external context (but can link out for details)
- **Testable:** Acceptance criteria are measurable (not vague like "should be fast")
- **Unambiguous:** No "maybe" or "probably" in design decisions — if uncertain, use NEEDS DAVE INPUT
- **Versioned:** Frontmatter tracks version, date, status
- **Under 500 lines** if possible (Hard Rule #4). For longer specs, split into sub-specs or move detail to references/

## Gotchas

### 1. Spec vs. Task File Confusion

**Spec:** Describes WHAT to build and WHY (strategy, design, acceptance criteria). Lives in `docs/specs/`.

**Task file:** Describes WHO does it, WHEN, and HOW MUCH (worker assignment, three currencies). Lives in `.deia/hive/tasks/`.

A spec can spawn multiple task files. A task file implements part of a spec.

### 2. Inventing Architecture Without Survey

**Bad:**
```markdown
## Proposed Solution
We'll use Redis for caching because it's fast.
```

**Good:**
```markdown
## Proposed Solution
Survey shows we currently use .data/ local files for all state.
Redis would require new infrastructure (Railway addon, cost increase).

**NEEDS DAVE INPUT:** Add Redis (cost/complexity) or optimize .data/ access?
```

**Rule:** Always grep the repo first. Don't assume what exists or doesn't exist.

### 3. Vague Acceptance Criteria

**Bad:**
- [ ] UI should look good
- [ ] Performance should be acceptable

**Good:**
- [ ] UI renders in under 200ms on 3G network (measured via Lighthouse)
- [ ] All interactive elements have hover states using `var(--sd-hover-bg)`
- [ ] No hardcoded colors (Hard Rule #3 compliance)

### 4. No Status Field

Every spec must have `status:` in frontmatter. If missing, spec is assumed DRAFT.

### 5. Hardcoding File Paths (Relative Instead of Absolute)

When referencing files in Implementation section, use absolute paths:

**Bad:**
```markdown
Modify `core/routes/health.py`
```

**Good:**
```markdown
Modify `C:\Users\davee\OneDrive\Documents\GitHub\simdecisions\hivenode\routes\health.py`
```

Or use repo-relative format:
```markdown
Modify `hivenode/routes/health.py` (repo-relative)
```

### 6. Spec Too Long (Over 500 Lines)

**Symptom:** Spec approaches or exceeds 500 lines.

**Fix:** Split into sub-specs or move detailed appendices to `docs/specs/references/`.

**Example:**
- Main spec: `SPEC-SKILL-PRIMITIVE-001.md` (300 lines)
- Skill threat rubric: `docs/research/SKILL-THREAT-RUBRIC.md` (referenced from main spec)

### 7. Forgetting ADR Cross-References

If a spec makes architectural decisions, link to relevant ADRs or create a new ADR.

**Pattern:**
```markdown
## ADR Cross-References

- **ADR-005:** Agent Skills Governance — this spec formalizes the artifact that ADR governs
- **ADR-001:** Event Ledger — skill lifecycle events are a new event category
```

### 8. No Testing Strategy

Every feature spec needs a testing section. If tests aren't needed (pure docs, config), state that explicitly:

```markdown
## Testing Strategy
No automated tests required — this is configuration only. Manual verification: load config and check schema validation.
```

### 9. Overspecifying Implementation Details Too Early

**Bad (DRAFT stage):**
```markdown
## Implementation
Line 47 of health.py will change from `return {"status": "ok"}` to `return {"status": "ok", "version": VERSION}`.
```

**Good (DRAFT stage):**
```markdown
## Implementation
Health endpoint will include version field. Exact implementation TBD during task breakdown.
```

**Good (APPROVED stage, in task file):**
```markdown
## Implementation
Modify `hivenode/routes/health.py:47`:
- Old: `return {"status": "ok"}`
- New: `return {"status": "ok", "version": VERSION}`
```

Specs describe strategy. Task files describe tactics.

### 10. Spec Without an Owner

Every spec must have `author:` field. If written collaboratively, list primary author:

```markdown
author: Dave × Claude (Opus 4.6)
```

Or use role:
```markdown
author: Q33N
```

Never leave `author:` blank.

### 11. Writing a Queue Spec Without Reading SUBMISSION-CHECKLIST.md

**Symptom:** Spec bounces to `_needs_review/` with Gate 0 failures (missing acceptance criteria, low IR density, bad file paths).

**Fix:** Read `.deia/hive/queue/SUBMISSION-CHECKLIST.md` **before** writing any spec destined for the factory queue. It has the canonical template, all 6 Gate 0 checks, common failure modes, and a diagnostic command to run Gate 0 manually.

**Key traps:**
- `## Acceptance Criteria` must use `- [ ]` checkboxes — numbered lists and plain bullets are silently ignored
- The parser finds the FIRST `## Acceptance Criteria` heading in the file — if a template/example block contains one, put your real section BEFORE it
- IR density must be >= 0.200 — specs that are mostly prose will fail even if content is correct
- YAML frontmatter for queue specs uses `id`, `priority`, `model`, `depends_on` — NOT `title`, `version`, `author`, `status`

### 12. Confusing docs/specs/ Frontmatter with Queue Frontmatter

**Symptom:** Queue spec has `title:`, `version:`, `author:`, `status:` in frontmatter but no `id:`, `priority:`, `model:`.

**Fix:** Queue specs and docs/specs use different frontmatter schemas:

| Field | `docs/specs/` | Queue (`backlog/`) |
|-------|--------------|-------------------|
| `title` | Yes | No |
| `version` | Yes | No |
| `author` | Yes | No |
| `status` | Yes (DRAFT/REVIEW/...) | No (lifecycle is positional: backlog → _active → _done) |
| `id` | No | Yes |
| `priority` | No | Yes (P0-P3) |
| `model` | No | Yes (haiku/sonnet/opus) |
| `role` | No | Yes (bee / queen / regent) |
| `depends_on` | No | Yes (list of spec IDs) |

If a spec will go into **both** `docs/specs/` (for reference) and the queue (for execution), write two files: one design doc in `docs/specs/` and one queue spec in `backlog/` that references it.

## Examples from Repo

**High-quality spec (comprehensive, clear, testable):**
- `docs/specs/SPEC-SKILL-PRIMITIVE-001.md` — Skill as a first-class primitive

**Wave plan (multi-task coordination):**
- `docs/specs/WAVE-3-QUEUE-SPECS.md` — Queue runner specs

**Process spec:**
- `docs/specs/SPEC-BUILD-QUEUE-001.md` — Build queue implementation

**Port spec (migration):**
- `docs/specs/SPEC-PORT-RAG-001-rag-pipeline-port.md` — RAG pipeline port
