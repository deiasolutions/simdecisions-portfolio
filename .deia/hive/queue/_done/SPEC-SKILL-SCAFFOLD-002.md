# SPEC-SKILL-SCAFFOLD-002: Hive Process Skills (Phase 2b)

**MODE: EXECUTE**

## Priority
P1

## Depends On
SPEC-SKILL-SCAFFOLD-001

## Model Assignment
sonnet

## Files to Read First

- docs/specs/SPEC-SKILL-PRIMITIVE-001.md
- .deia/skills/DEIA-SKILL-WRITING-REFERENCE.md
- .deia/processes/PROCESS-LIBRARY-V2.md
- .deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md
- .deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md

## Objective

Write 6 SKILL.md files that codify the hive's most-used operational processes. These are the workflows that bees perform repeatedly and get wrong most often. Each skill must be sourced from the actual process docs in the repo — not invented.

## Deliverables

```
.deia/skills/internal/task-file-writer/SKILL.md
.deia/skills/internal/task-file-writer/governance.yml
.deia/skills/internal/response-file-writer/SKILL.md
.deia/skills/internal/response-file-writer/governance.yml
.deia/skills/internal/three-phase-validation/SKILL.md
.deia/skills/internal/three-phase-validation/governance.yml
.deia/skills/internal/wave-planner/SKILL.md
.deia/skills/internal/wave-planner/governance.yml
.deia/skills/internal/process-writer/SKILL.md
.deia/skills/internal/process-writer/governance.yml
.deia/skills/internal/coordination-briefing-writer/SKILL.md
.deia/skills/internal/coordination-briefing-writer/governance.yml
```

## Survey Requirements

Before writing ANY skill, grep the repo for the source process. Each skill section below specifies what to find. If a process file has moved or doesn't exist, document what you found and mark gaps as `[UNDOCUMENTED — needs process doc]`.

## Skill Specifications

### 1. task-file-writer

**What this skill teaches an agent:** How to write a properly formatted task file for hive dispatch.

**Survey:** Grep for:
- `.deia/processes/PROCESS-*` — find the task file format requirements
- `.deia/hive/tasks/` — sample at least 5 recent task files to extract the pattern
- `ALL-PROCESSES-COMBINED.md` or equivalent — find the Response Requirements template
- Any references to "8 sections" or "mandatory sections"

**Minimum content:**
- Task file naming convention (`YYYY-MM-DD-HHMM-{AGENT}-{TASK_ID}-ASSIGNMENT.md`)
- All required sections: Objective, Constraints, Output Files, Success Criteria, Three Currencies estimate, Response Requirements block
- The Response Requirements template that must be pasted into every task file (8-section mandate)
- Where task files live (`.deia/hive/tasks/`)
- What goes in the task vs what goes in the spec (task = assignment, spec = design)
- Anti-patterns: vague objectives, missing success criteria, no three-currency estimate

### 2. response-file-writer

**What this skill teaches an agent:** How to write a properly formatted bee response file after completing a task.

**Survey:** Grep for:
- `.deia/processes/PROCESS-*` — find the response file format
- `.deia/hive/responses/` — sample at least 5 recent response files
- The 8-section response mandate (Header, Files Modified, What Was Done, Test Results, Build Verification, Acceptance Criteria, Clock/Cost/Carbon, Issues/Follow-ups)

**Minimum content:**
- Response file naming convention (`YYYYMMDD-{TASK-ID}-RESPONSE.md`)
- All 8 mandatory sections with descriptions of what each must contain
- The three-currency format (Clock, Coin, Carbon — all three, never skip any)
- How to mark acceptance criteria (copy from task, mark [x] or [ ] with explanation)
- Where response files live (`.deia/hive/responses/`)
- Anti-patterns table (from process docs: skip response file, write "tests not needed" without explanation, omit currencies, vague "What Was Done", etc.)

### 3. three-phase-validation

**What this skill teaches an agent:** How to run PROCESS-0013 build integrity validation.

**Survey:** Grep for:
- `PROCESS-0013` or `PROCESS-13` or `BUILD-INTEGRITY` or `3PHASE`
- `.deia/processes/PROCESS-0013*.md`
- Any references to Gate 0, Phase 0, Phase 1, Phase 2, fidelity scores
- The healing loop pattern (FAIL → DIAGNOSE → HEAL → RETRY max 3 → ESCALATE)

**Minimum content:**
- Gate 0: Prompt→SPEC requirements tree validation (disambiguation layer)
- Phase 0: Coverage validation — are ALL requirements from ASSIGNMENT in SPEC?
- Phase 1: SPEC fidelity — does SPEC→IR→SPEC' preserve meaning?
- Phase 2: TASK fidelity — does TASKS→IR→TASKS' preserve meaning?
- Pass/fail thresholds (fidelity scores)
- Healing loop mechanics (max 3 retries per phase)
- Escalation: when and how to escalate to human
- The Q33N-003B case study (the original failure that spawned this process) if found in docs
- Gotchas: fidelity can pass while coverage fails (the original bug), builder bee never tests own output

### 4. wave-planner

**What this skill teaches an agent:** How to organize a batch of work items into execution waves.

**Survey:** Grep for:
- `Wave 0` or `Wave A` or `wave system` or `PROCESS-0017` or `BATCH-WORK-BREAKDOWN`
- `.deia/processes/PROCESS-0017*.md` or `PROCESS-0020*.md`
- `PLATFORM-OPERATIONS.md` — wave system documentation

**Minimum content:**
- Wave definitions: Wave 0 (critical, solo, all bees wait), Wave A/B (parallel, no inter-dependencies), Wave C/D (integration, depends on A/B), Wave E (greenfield, only after foundation stable)
- Triage classification per item: Tier (haiku/sonnet/opus), Type (code/research/clerical/strategic), Dependencies, Parallelizable (yes/no)
- The rule: strategic items stay with Q33NR + Q88N, everything else gets delegated
- How to write a single batch briefing covering all delegatable items
- Dependency graph construction — what blocks what
- Anti-patterns: running integration work before foundation is stable, parallel items with hidden dependencies

### 5. process-writer

**What this skill teaches an agent:** How to write a new PROCESS-XXXX document in DEIA standard format.

**Survey:** Grep for:
- `.deia/processes/PROCESS-*.md` — sample at least 5 to extract the common structure
- The process template (Rule, When to Apply, Steps, Success Criteria, Rollback, Telemetry Plan, Integration, Change Log, Authority)
- Process numbering convention

**Minimum content:**
- File naming: `PROCESS-XXXX-process-name.md`
- Location: `.deia/processes/`
- Status values: DRAFT / OFFICIAL
- All required sections from the template (minimum: Title, Rule, When to Apply, Steps, Timebox, Success Criteria, Rollback, Telemetry Plan)
- The Rule section must answer "why does this process exist?" in 1-2 sentences
- Steps must be numbered and LLM-agnostic (any model can follow them)
- How processes relate to skills (a process is the source of truth; a skill teaches an agent to follow it)

### 6. coordination-briefing-writer

**What this skill teaches an agent:** How to write a sprint coordination briefing that all bees receive.

**Survey:** Grep for:
- `.deia/hive/coordination/` — sample existing briefing files
- `HIVE-008` or `Coordination Briefings` in inventory docs
- Any sprint briefing templates

**Minimum content:**
- What a coordination briefing is (context document all bees in a sprint receive)
- Standard sections: sprint goals, dependencies between tasks, conventions to follow, what other bees are doing
- Where briefings live (`.deia/hive/coordination/`)
- How briefings prevent bees from working at cross-purposes
- Naming convention for briefing files
- When to update vs create new (updated each sprint)

## governance.yml for All Six

All six are internal skills, cert tier 3. Use this base template and adjust capabilities per skill:

```yaml
cert_tier: 3
promoted_from: null
promoted_at: null
promoted_by: Q88N

capabilities:
  filesystem_read: true
  filesystem_write: true
  network_access: false
  shell_exec: false
  user_data_access: false
  model_invocation: false
  event_ledger_write: true

blast_radius: contained

budget:
  clock_max_seconds: 300
  coin_max_usd: 0.00
  carbon_max_grams: 0.0
```

Adjustments:
- **three-phase-validation** needs `model_invocation: true` (runs LLM fidelity checks) and `carbon_max_grams: 20.0`
- **wave-planner** stays as-is (planning is deterministic)

## Constraints

- Every SKILL.md must follow agentskills.io format exactly (see `.deia/skills/DEIA-SKILL-WRITING-REFERENCE.md`)
- `name` field: lowercase-hyphenated, max 64 chars
- `description` field: must describe what AND when, 1-1024 chars
- Body: Steps, Output Format, Gotchas sections required
- Under 500 lines per SKILL.md
- Source all content from actual repo process docs. Never invent process details.
- Mark undocumented items as `[UNDOCUMENTED — needs process doc]`

## Acceptance Criteria

- [ ] All 12 files created (6 SKILL.md + 6 governance.yml) in .deia/skills/internal/
- [ ] Each SKILL.md has valid agentskills.io YAML frontmatter (name, description present)
- [ ] Each SKILL.md body reflects actual process docs found in repo
- [ ] Each governance.yml capabilities match what the skill actually needs
- [ ] No external dependencies, no network calls
- [ ] Each skill description is specific enough to trigger on relevant tasks

## Smoke Test

- [ ] Each SKILL.md file exists and is under 500 lines
- [ ] Each governance.yml file exists and is valid YAML
- [ ] three-phase-validation governance.yml has model_invocation: true
