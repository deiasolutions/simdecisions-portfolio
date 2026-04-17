# PROCESS-DOC-DRIVEN-DEVELOPMENT

**Version:** 1.0.0-draft  
**Status:** PROPOSED — DEFERRED until MW build completes  
**Author:** Q88N  
**Date:** 2026-04-06

---

## Rollout Plan

**Do not activate mid-MW-build.** This spec is on file for Phase 1 implementation.

| Phase | When | What |
|-------|------|------|
| **Now** | Tonight | Spec on file. No pipeline changes. |
| **Phase 1** | After MW build | Create directories, add IMPL requirement, manual QA |
| **Phase 2** | After Phase 1 stable | QA bee automation, state machine, scheduler integration |
| **Phase 3** | After Phase 2 stable | Backfill tasks since 2026-04-05T18:00Z |

---

## Purpose

Embed documentation as a gate in the build cycle, not an afterthought. Every task produces structured documentation optimized for:
1. **Human consumption** — readable status, decisions, implementation notes
2. **Bee consumption** — structured headers, YAML frontmatter, embedding-friendly chunks

---

## Precedent

| Pattern | Source | What we take |
|---------|--------|--------------|
| README-Driven Development | Preston-Werner 2010 | Spec before code |
| Behavior-Driven Development | Cucumber/Gherkin | Spec = test = doc |
| Design-by-Contract | Eiffel/Meyer | Preconditions as executable spec |
| Literate Programming | Knuth | Code + doc as unified artifact |

We already do spec-before-build (DDD). This closes the loop with **IMPL-after-build**.

---

## Document Lifecycle

Every feature/task produces **three documents**:

```
SPEC-{ID}.md   →   IMPL-{ID}.md   →   TEST-{ID}.md
   (intent)         (actuals)         (validation)
```

| Document | Written by | When | Contains |
|----------|------------|------|----------|
| **SPEC** | Human or Q33N | Before build | Intent, acceptance criteria, constraints |
| **IMPL** | Build bee | After build | What was built, deltas from spec, file locations, decisions |
| **TEST** | Test bee (BAT) | After validation | Test coverage, edge cases, pass/fail |

---

## Integration with Scheduler/Dispatcher

### Build Cycle Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         SCHEDULER                                │
│                                                                  │
│   Reads: _done/, dispatched.jsonl                               │
│   Writes: schedule.json, schedule_log.jsonl                     │
│   Monitors: velocity, task completions                          │
│                                                                  │
│   Sees tasks in _done/ only after full QA cycle completes       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ schedule.json
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DISPATCHER                               │
│                                                                  │
│   Reads: schedule.json, backlog/                                │
│   Writes: queue/, dispatched.jsonl                              │
│                                                                  │
│   Task file includes IMPL doc generation requirement            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ queue/
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        QUEUE-RUNNER                              │
│                                                                  │
│   Executes task → Build bee produces code + draft IMPL doc      │
│   Emits: task_completed event to hive event bus                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ task_completed event
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BEE-QA-*                                 │
│                    (doc quality check)                          │
│                                                                  │
│   Reads: draft IMPL doc, SPEC, code diff                        │
│   Produces: diff recommendation (approve / revise)              │
│   Role assignable per-plan (Claude, Gemini, etc.)               │
│   Emits: qa_review_ready event                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ qa_review_ready event
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Q33N                                   │
│                    (orchestrator review)                        │
│                                                                  │
│   Reviews: QA bee diff recommendation                           │
│   Decides: approve → _done/ | return → _needs_revision/         │
│   Can fast-track urgent items to schedule staging (high prio)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              ┌──────────┐        ┌──────────────────┐
              │  _done/  │        │ _needs_revision/ │
              │          │        │                  │
              │ Complete │        │ Back to builder  │
              └──────────┘        └──────────────────┘
```

### Task State Machine (extended)

```
backlog → queue → running → code_complete → qa_review → q33n_review → _done
                                 │              │            │
                                 │              │            └── Q33N approves
                                 │              └── QA bee reviews IMPL
                                 └── Build bee finishes code + draft IMPL
                     
                 ↓ (if Q33N returns)
                 
            _needs_revision → back to running (same or different bee)
```

**States:**

| State | Location | Meaning |
|-------|----------|---------|
| `backlog` | `backlog/` | Waiting for scheduler |
| `queue` | `queue/` | Ready for execution |
| `running` | `running/` | Bee actively working |
| `code_complete` | `_code_complete/` | Code done, awaiting QA |
| `qa_review` | `_qa_review/` | QA bee reviewing |
| `q33n_review` | `_q33n_review/` | Awaiting Q33N decision |
| `_done` | `_done/` | Fully complete |
| `_needs_revision` | `_needs_revision/` | Returned for fixes |

---

## Document Schema

### YAML Frontmatter (required)

All three doc types share a common header for indexing:

```yaml
---
# Required
id: MW-S01
type: SPEC | IMPL | TEST
status: draft | complete | superseded
created: 2026-04-06T02:30:00Z
updated: 2026-04-06T02:30:00Z

# Task metadata
task_id: MW-S01
task_title: "Scheduler daemon implementation"
phase: SPEC | BUILD | TEST | VERIFY

# Traceability
parent_spec: SPEC-MW-S01.md  # for IMPL/TEST
parent_impl: IMPL-MW-S01.md  # for TEST
supersedes: null             # if this replaces an earlier doc

# Files (IMPL only)
files_created: []
files_modified: []
files_deleted: []

# Dependencies
depends_on: [MW-S00]
blocks: [MW-S02, MW-S03]

# Three currencies (IMPL only)
clock_actual_minutes: 45
coin_actual_usd: 0.12
carbon_actual_gco2e: 0.08
model: claude-sonnet-4-20250514
tokens_in: 12500
tokens_out: 3200

# Index hints (for embedding/search)
keywords: [scheduler, daemon, ortools, constraint]
domain: hivenode/scheduler
---
```

### SPEC Document Structure

```markdown
---
(frontmatter)
---

# SPEC-{ID}: {Title}

## Intent

What we're trying to accomplish. Natural language. 1-3 sentences.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints

- Three-currency budget: clock ≤ X min, coin ≤ $Y, carbon ≤ Z gCO2e
- Dependencies: requires {dep_ids}
- Operator tier: T0 (compute) | T1 (supervised) | T2 (reviewed) | T3 (approved) | T4 (human)

## Design Notes

Optional. Architecture decisions, alternatives considered, references.

## Out of Scope

Explicitly what this task does NOT include.
```

### IMPL Document Structure

```markdown
---
(frontmatter with files_*, three currencies, tokens)
---

# IMPL-{ID}: {Title}

## Summary

What was actually built. 1-3 sentences.

## Deltas from Spec

| Spec said | We did | Why |
|-----------|--------|-----|
| ... | ... | ... |

(If no deltas: "None — implementation matches spec exactly.")

## Implementation Details

### Files Created
- `path/to/file.py` — purpose

### Files Modified  
- `path/to/file.py` — what changed

### Key Decisions
1. Decision 1: rationale
2. Decision 2: rationale

## Dependencies Introduced

New dependencies (packages, services, files) this implementation requires.

## Known Issues

Any gotchas, TODOs, or deferred work.

## Verification

How to verify this works:
```bash
# command to run
```
```

### TEST Document Structure

```markdown
---
(frontmatter)
---

# TEST-{ID}: {Title}

## Test Summary

| Metric | Value |
|--------|-------|
| Tests written | N |
| Tests passing | N |
| Coverage | X% |

## Test Cases

### {test_name}
- **Type:** unit | integration | e2e
- **Status:** pass | fail | skip
- **Description:** what it tests

## Edge Cases Covered

1. Edge case 1
2. Edge case 2

## Edge Cases NOT Covered

1. Deferred edge case (reason)

## Reproduction

```bash
pytest path/to/test.py -v
```
```

---

## Bee Instructions

### For Build Bees (BEE-CODE-*)

Task files include this footer:

```markdown
## REQUIRED OUTPUT

In addition to code changes, you MUST produce:

1. **IMPL-{task_id}.md** in `.deia/docs/impl/`
   - Use the schema in PROCESS-DOC-DRIVEN-DEVELOPMENT.md
   - Include accurate frontmatter (files, tokens, currencies)
   - Document any deltas from the SPEC

This is a DRAFT. A QA bee will review and may request revisions.
Your task moves to _code_complete/ when you finish, not _done/.
```

### For QA Bees (BEE-QA-*)

QA bee receives task when build bee completes. Instructions:

```markdown
## QA REVIEW TASK

Review the IMPL doc produced by the build bee.

**Inputs:**
- SPEC-{task_id}.md (original intent)
- IMPL-{task_id}.md (build bee's draft)
- Code diff (files created/modified)

**Check for:**
1. Frontmatter complete and accurate (files match actual changes)
2. Deltas from spec documented honestly (not glossed over)
3. Key decisions explained (not just "we did X")
4. Three currencies recorded (clock, coin, carbon, tokens)
5. Verification instructions actually work

**Output:**
Produce a QA recommendation in `.deia/logs/qa_review_log.jsonl`:

{
  "task_id": "{task_id}",
  "qa_bee": "{bee_id}",
  "model": "{model_used}",
  "timestamp": "ISO8601",
  "recommendation": "approve" | "revise",
  "diff": [
    {"section": "Deltas from Spec", "issue": "Missing rationale for X", "suggested": "..."}
  ],
  "notes": "Optional QA notes for Q33N"
}

Q33N will review your recommendation.
```

### For Test Bees (BAT)

```markdown
## REQUIRED OUTPUT

In addition to running tests, you MUST produce:

1. **TEST-{task_id}.md** in `.deia/docs/test/`
   - Use the schema in PROCESS-DOC-DRIVEN-DEVELOPMENT.md
   - Include pass/fail for each test case
   - Document edge cases covered and NOT covered
```

---

## Directory Structure

```
.deia/
├── docs/
│   ├── spec/           # SPEC-*.md (input, human-authored or Q33N)
│   ├── impl/           # IMPL-*.md (output, build bee draft → QA reviewed)
│   └── test/           # TEST-*.md (output, BAT-generated)
├── hive/
│   ├── backlog/        # Tasks waiting for scheduler
│   ├── queue/          # Tasks ready for execution
│   ├── running/        # Tasks currently executing
│   ├── _code_complete/ # Code done, awaiting QA bee
│   ├── _qa_review/     # QA bee reviewing IMPL
│   ├── _q33n_review/   # Awaiting Q33N decision
│   ├── _done/          # Fully complete (Q33N approved)
│   └── _needs_revision/# Returned for fixes
└── logs/
    ├── schedule.json
    ├── schedule_log.jsonl
    ├── dispatched.jsonl
    ├── dispatcher_log.jsonl
    └── qa_review_log.jsonl   # QA bee recommendations
```

---

## Validation Rules

### Schema Validation (automated, pre-QA)

Before QA bee receives task:

1. **Existence:** `IMPL-{task_id}.md` exists in `.deia/docs/impl/`
2. **Frontmatter:** Valid YAML, all required fields present
3. **Schema:** Matches IMPL structure (Summary, Deltas, Files, Decisions)
4. **Traceability:** `parent_spec` points to existing SPEC doc

If schema fails → task stays in `_code_complete/`, build bee gets error.

### QA Bee Review (semantic)

QA bee checks what automation can't:

1. **Honesty:** Deltas actually reflect what changed vs spec
2. **Completeness:** Key decisions explained, not just listed
3. **Accuracy:** Files in frontmatter match actual changes
4. **Verifiability:** Verification commands actually work
5. **Currencies:** Three currencies recorded and plausible

### Q33N Review (approval gate)

Q33N reviews QA bee recommendation:

1. **Approve:** Task moves to `_done/`
2. **Return:** Task moves to `_needs_revision/` with Q33N notes
3. **Escalate:** Flag for human (Q88N) review if ambiguous

---

## PROCESS-13 Alignment

This extends PROCESS-13's three-phase quality control:

| Phase | Original | With Doc-Driven |
|-------|----------|-----------------|
| **Validate Plan** | Roundtrip spec fidelity | Spec exists, schema valid |
| **Execute + Self-Check** | Code compiles, tests pass | + IMPL doc generated |
| **Validate Output** | Superior agent reviews | + IMPL doc validates, TEST doc generated |

The IMPL doc IS the output artifact that superior agent validates.

---

## Embedding Optimization

For bee consumption (search, context injection):

1. **Frontmatter first** — structured metadata for filtering
2. **Keywords field** — explicit index terms
3. **Domain field** — path prefix for scoping
4. **Chunking boundary** — each H2 section is an independent chunk
5. **No prose headers** — H2s are semantic labels ("## Deltas from Spec"), not narrative

---

## Decisions (2026-04-06)

1. **Doc QA bee:** Separate QA bee reviews IMPL docs — builder does NOT self-approve. Role: `BEE-QA-*` (not model-locked). Plan can assign different LLMs to QA role for experimentation.

2. **Q33N review:** QA bee issues diff recommendation → Q33N reviews → approves or returns. Standard Q33N oversight, not bypassed.

3. **Monitoring integration:** Doc validation hooks into existing hive event flow (same patterns as scheduler/dispatcher). Not a separate daemon — one event bus, multiple consumers.

4. **Retroactive scope:** Apply to tasks completed since 2026-04-05T18:00Z. Earlier tasks remain as-is unless explicitly backfilled.

5. **Supersession:** When IMPL-v2 replaces IMPL-v1, use `supersedes` field in frontmatter.

---

## Implementation Tasks

To enable this process:

1. [ ] Create `.deia/docs/{spec,impl,test}/` directories
2. [ ] Create new state directories: `_code_complete/`, `_qa_review/`, `_q33n_review/`, `_needs_revision/`
3. [ ] Add IMPL requirement to task file template
4. [ ] Add event emission to queue-runner on task completion
5. [ ] Create QA bee dispatch logic (triggered by `task_completed` event)
6. [ ] Create Q33N review interface (see `_q33n_review/` items)
7. [ ] Update scheduler to recognize new states
8. [ ] Backfill: Generate IMPL docs for tasks completed since 2026-04-05T18:00Z

### Backfill Scope

Tasks completed between 2026-04-05T18:00Z and process activation:
- Enumerate from `_done/` with `completed_at` in range
- Generate IMPL docs from git diff + any existing notes
- Mark as `backfill: true` in frontmatter
- QA review optional for backfills (Q33N discretion)

---

## References

- Preston-Werner, T. (2010). "Readme Driven Development"
- PROCESS-13: Three-phase quality control
- Scheduler/Dispatcher architecture (2026-04-05 session)
