# IMPL Document Schema

This document defines the canonical structure for IMPL (implementation) documents produced by build bees.

**Version:** 1.0.0
**Source:** PROCESS-DOC-DRIVEN-DEVELOPMENT.md
**Status:** ACTIVE

---

## Purpose

IMPL documents capture what was actually built, bridging the gap between spec intent and delivered code. They serve both human reviewers and automated systems (QA bees, search, embeddings).

---

## Document Structure

Every IMPL document MUST contain:

1. **YAML frontmatter** (structured metadata)
2. **Summary** (1-3 sentence overview)
3. **Deltas from Spec** (what changed vs intent)
4. **Implementation Details** (files, decisions)
5. **Dependencies Introduced** (new requirements)
6. **Known Issues** (gotchas, deferred work)
7. **Verification** (how to test)

---

## YAML Frontmatter (Required)

```yaml
---
# Required fields
id: MW-S01                           # Task identifier
type: IMPL                            # Always "IMPL" for implementation docs
status: draft | complete | superseded # Document status
created: 2026-04-06T02:30:00Z        # ISO8601 timestamp
updated: 2026-04-06T02:30:00Z        # ISO8601 timestamp (same as created initially)

# Task metadata
task_id: MW-S01                       # Task identifier (same as id)
task_title: "Scheduler daemon implementation"
phase: BUILD                          # Always "BUILD" for IMPL docs

# Traceability
parent_spec: SPEC-MW-S01.md          # Link to original spec file
parent_impl: null                     # For TEST docs only, null for IMPL
supersedes: null                      # If this replaces an earlier IMPL doc

# Files modified (IMPL only)
files_created: []                     # List of file paths created
files_modified: []                    # List of file paths modified
files_deleted: []                     # List of file paths deleted

# Dependencies
depends_on: [MW-S00]                  # Task IDs this depends on
blocks: [MW-S02, MW-S03]              # Task IDs blocked by this

# Three currencies (IMPL only)
clock_actual_minutes: 45              # Wall-clock time spent
coin_actual_usd: 0.12                 # Cost in USD
carbon_actual_gco2e: 0.08             # Carbon footprint (optional)
model: claude-sonnet-4-20250514       # Model used
tokens_in: 12500                      # Input tokens
tokens_out: 3200                      # Output tokens

# Index hints (for embedding/search)
keywords: [scheduler, daemon, ortools, constraint]
domain: hivenode/scheduler            # Path prefix for scoping
---
```

### Frontmatter Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique task identifier |
| `type` | string | Yes | Always "IMPL" |
| `status` | string | Yes | "draft", "complete", or "superseded" |
| `created` | ISO8601 | Yes | When doc was created |
| `updated` | ISO8601 | Yes | Last modification time |
| `task_id` | string | Yes | Task identifier (matches id) |
| `task_title` | string | Yes | Human-readable title |
| `phase` | string | Yes | Always "BUILD" |
| `parent_spec` | string | Yes | Path to SPEC-*.md file |
| `parent_impl` | string | No | Null for IMPL docs |
| `supersedes` | string | No | Previous IMPL doc if applicable |
| `files_created` | array | Yes | Paths of created files |
| `files_modified` | array | Yes | Paths of modified files |
| `files_deleted` | array | Yes | Paths of deleted files |
| `depends_on` | array | Yes | Task dependencies |
| `blocks` | array | Yes | Tasks blocked by this |
| `clock_actual_minutes` | number | Yes | Time spent in minutes |
| `coin_actual_usd` | number | Yes | Cost in USD |
| `carbon_actual_gco2e` | number | No | Carbon footprint |
| `model` | string | Yes | LLM model identifier |
| `tokens_in` | number | Yes | Input token count |
| `tokens_out` | number | Yes | Output token count |
| `keywords` | array | No | Search terms |
| `domain` | string | No | Path/module scope |

---

## Markdown Body Structure

### Required Sections

#### 1. Summary

One to three sentences describing what was actually built.

```markdown
## Summary

Built a scheduler daemon that monitors the queue backlog and dispatches tasks
to available bees based on priority and dependency constraints. Uses OR-Tools
for constraint solving.
```

#### 2. Deltas from Spec

Table format showing what changed from the original spec and why.

```markdown
## Deltas from Spec

| Spec said | We did | Why |
|-----------|--------|-----|
| Use Redis for queue | Used in-memory dict | Redis not in dependencies, deferred to later task |
| 5-second poll interval | 10-second poll interval | Reduced load on filesystem |
```

**If no deltas exist:**

```markdown
## Deltas from Spec

None — implementation matches spec exactly.
```

#### 3. Implementation Details

Structured breakdown of what was built.

```markdown
## Implementation Details

### Files Created

- `.deia/hive/scripts/queue/scheduler_daemon.py` — Main scheduler loop
- `.deia/hive/scripts/queue/constraint_solver.py` — Dependency resolver

### Files Modified

- `.deia/hive/scripts/queue/run_queue.py` — Added scheduler integration hooks
- `.deia/config/queue.yml` — Added scheduler config section

### Key Decisions

1. **Used OR-Tools for constraint solving:** Handles dependency graphs more reliably than manual topological sort. Adds ~2MB to dependencies but worth the correctness gain.

2. **Poll interval configurable:** Made it a config var (default 10s) so we can tune without code changes.

3. **Graceful shutdown on SIGTERM:** Scheduler finishes current cycle before exiting to avoid partial states.
```

#### 4. Dependencies Introduced

Any new packages, services, or files required.

```markdown
## Dependencies Introduced

- **ortools** (Python package): Constraint solving library
- **queue.yml config file**: Must exist in `.deia/config/`
- **schedule.json state file**: Created on first run in `.deia/hive/`
```

**If no dependencies:**

```markdown
## Dependencies Introduced

None.
```

#### 5. Known Issues

Any gotchas, TODOs, or deferred work.

```markdown
## Known Issues

1. **No Redis persistence yet:** Using in-memory state. Scheduler restart loses queue state. Deferred to MW-S05.

2. **No backpressure handling:** If queue fills faster than dispatch, scheduler doesn't throttle. Added TODO for MW-S12.

3. **Windows path handling:** Used `Path.resolve()` everywhere but not tested on Windows yet. Needs smoke test.
```

**If no issues:**

```markdown
## Known Issues

None.
```

#### 6. Verification

Step-by-step instructions to verify the implementation works.

```markdown
## Verification

How to verify this works:

```bash
# 1. Start the scheduler daemon
python .deia/hive/scripts/queue/scheduler_daemon.py

# 2. Check that schedule.json is created
ls -la .deia/hive/schedule.json

# 3. Add a spec to backlog
cp SPEC-TEST-001.md .deia/hive/queue/backlog/

# 4. Verify scheduler picks it up (check logs)
tail -f .deia/hive/schedule_log.jsonl

# Expected: Task appears in schedule within 10 seconds
```

**Expected output:**

- `schedule.json` contains task entry
- `schedule_log.jsonl` shows `TASK_SCHEDULED` event
```
```

---

## Writing Guidelines

### 1. Frontmatter Accuracy

- **Files arrays MUST match actual changes:** Use git diff or file comparison to verify
- **Tokens/cost MUST be actual values:** No estimates, no placeholders
- **Timestamps in ISO8601 UTC:** `2026-04-06T14:30:00Z`

### 2. Delta Honesty

- **Document ALL deltas:** Even small deviations from spec
- **Explain WHY:** "Because" is mandatory, not optional
- **No glossing over:** If you broke a constraint, say so and explain

### 3. Decision Rationale

- **Key Decisions = choices with alternatives:** Not "we wrote a function", but "we chose X over Y because Z"
- **Include tradeoffs:** "Adds 2MB to bundle but improves correctness"
- **No obvious statements:** "Used Python because the repo is Python" is noise

### 4. Verification Clarity

- **Actual commands:** Not "run the tests", but `pytest path/to/test.py -v`
- **Expected output:** What success looks like
- **Failure modes:** What to check if verification fails

### 5. Embedding Optimization

For bee consumption (search, context injection):

- **Each H2 section is a chunk:** Keep sections focused and independent
- **No prose headers:** Use semantic labels ("Deltas from Spec"), not narrative ("What Changed and Why We Did It")
- **Keywords explicit:** Add relevant terms to frontmatter, don't rely on full-text search alone

---

## QA Checklist

Before submitting an IMPL doc, verify:

- [ ] Frontmatter complete (all required fields present)
- [ ] Files arrays match actual git diff
- [ ] Deltas documented or "None" stated explicitly
- [ ] Key decisions include rationale, not just actions
- [ ] Verification commands are copy-pasteable and work
- [ ] No TODOs or placeholders in the doc body
- [ ] Tokens/cost reflect actual usage (not estimates)
- [ ] No stubs (every section has content or explicit "None")

---

## Examples

### Minimal Valid IMPL (No Deltas)

```markdown
---
id: BUG-042
type: IMPL
status: complete
created: 2026-04-06T10:00:00Z
updated: 2026-04-06T10:00:00Z
task_id: BUG-042
task_title: "Fix typo in README"
phase: BUILD
parent_spec: SPEC-BUG-042.md
parent_impl: null
supersedes: null
files_created: []
files_modified: ["README.md"]
files_deleted: []
depends_on: []
blocks: []
clock_actual_minutes: 5
coin_actual_usd: 0.002
carbon_actual_gco2e: 0.001
model: claude-haiku-4-20250301
tokens_in: 1200
tokens_out: 150
keywords: [documentation, typo]
domain: docs/
---

# IMPL-BUG-042: Fix typo in README

## Summary

Fixed "recieve" → "receive" typo in README.md line 42.

## Deltas from Spec

None — implementation matches spec exactly.

## Implementation Details

### Files Created

None.

### Files Modified

- `README.md` — Corrected spelling on line 42

### Key Decisions

None (trivial fix).

## Dependencies Introduced

None.

## Known Issues

None.

## Verification

```bash
grep "receive" README.md
# Expected: Line 42 shows correct spelling
```
```

### Complex IMPL (Multiple Deltas)

See PROCESS-DOC-DRIVEN-DEVELOPMENT.md section "IMPL Document Structure" for the full "Scheduler daemon" example with multiple deltas, decisions, and dependencies.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-06 | Initial schema from PROCESS-DOC-DRIVEN-DEVELOPMENT |

---

## References

- PROCESS-DOC-DRIVEN-DEVELOPMENT.md (parent process spec)
- SPEC document schema (sibling doc)
- TEST document schema (sibling doc)
