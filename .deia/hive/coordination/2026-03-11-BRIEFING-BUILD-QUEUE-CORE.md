# Briefing: SPEC-BUILD-QUEUE-001 — Core Queue Infrastructure (Phase 1)

**From:** Q33NR
**To:** Q33N
**Date:** 2026-03-11
**Priority:** Alpha Part 2, Step 1
**Spec:** `docs/specs/SPEC-BUILD-QUEUE-001.md`

---

## Objective

Build the core automated build queue infrastructure. This is Phase 1 — the queue runner loop, regent bot prompt, queue config, and morning report generator. Smoke test scripts come in Phase 2 after we verify the core loop works.

---

## What We're Building

An automated spec-to-build pipeline. Dave writes specs during the day, drops them in `.deia/hive/queue/`. The queue runner processes them overnight using the HIVE.md chain: Q88NR-bot reads spec → writes briefing → dispatches Q33N → Q33N writes tasks → dispatches bees → bees code and test → results flow up → commit → deploy → smoke test.

Phase 1 deliverables (this briefing):

1. **Queue runner script** (`run_queue.py`) — orchestration loop
2. **Regent bot prompt template** (`regent-bot-prompt.md`) — mechanical review checklist for Q88NR-bot
3. **Queue config** (`queue.yml`) — budget, models, limits
4. **Morning report generator** — summary markdown from queue state

---

## Deliverable 1: Queue Runner (`run_queue.py`)

**File:** `.deia/hive/scripts/queue/run_queue.py`

### What It Does

1. Loads specs from `.deia/hive/queue/` sorted by priority (P0 → P1 → P2), then by filename (chronological within same priority)
2. For each spec:
   a. Parse the spec (extract priority, objective, acceptance criteria, model assignment, smoke test criteria)
   b. Dispatch Q88NR-bot with the spec (using dispatch.py)
   c. Q88NR-bot drives the HIVE.md chain (briefing → Q33N → bees)
   d. Track cost from each dispatch response
   e. Log queue events to a session ledger
   f. On success: move spec to `.deia/hive/queue/_done/`
   g. On failure after max fix cycles: move spec to `.deia/hive/queue/_needs_review/`
3. After all specs processed (or budget exhausted): generate morning report
4. Exit

### Key Functions

```python
def load_queue(queue_dir: Path) -> list[SpecFile]:
    """Load and sort specs by priority then filename."""

def parse_spec(spec_path: Path) -> SpecFile:
    """Parse a spec markdown file into structured data."""

def process_spec(spec: SpecFile, config: QueueConfig, session: SessionState) -> SpecResult:
    """Run the full pipeline for one spec. Returns result with cost/status."""

def run_queue(queue_dir: Path, config_path: Path) -> SessionResult:
    """Main entry point. Process all specs in queue."""
```

### Budget Enforcement

- Track cumulative `session_cost_usd` across all specs
- At 80% of `max_session_usd`: log warning, stop accepting NEW specs (finish current)
- At 100%: stop immediately after current spec completes
- Each dispatch response includes cost — extract and accumulate

### Fix Cycle Logic

- When a spec fails (bees fail tests, or later smoke tests fail), Q88NR-bot creates a fix spec
- Fix specs get priority P0 and enter the queue ahead of remaining specs
- Max 2 fix cycles per original spec
- After 2 failed fixes: move to `_needs_review/`, log as `NEEDS_DAVE`

### Event Logging

Log each event to a session JSON file (`.deia/hive/queue/session-YYYY-MM-DD-HHMM.json`):

```python
@dataclass
class QueueEvent:
    event_type: str  # QUEUE_SPEC_STARTED, QUEUE_BEES_COMPLETE, etc.
    timestamp: str   # ISO 8601
    spec_id: str
    cost_usd: float
    duration_ms: int
    model_used: str
    details: dict    # extra context
```

Event types from spec section 10: `QUEUE_SPEC_STARTED`, `QUEUE_BRIEFING_WRITTEN`, `QUEUE_TASKS_APPROVED`, `QUEUE_BEES_COMPLETE`, `QUEUE_COMMIT_PUSHED`, `QUEUE_DEPLOY_CONFIRMED`, `QUEUE_SMOKE_PASSED`, `QUEUE_SMOKE_FAILED`, `QUEUE_FIX_CYCLE`, `QUEUE_NEEDS_DAVE`, `QUEUE_SESSION_COMPLETE`, `QUEUE_BUDGET_WARNING`.

### CLI Interface

```bash
python .deia/hive/scripts/queue/run_queue.py [--config .deia/config/queue.yml] [--dry-run]
```

- `--config`: path to queue config (default: `.deia/config/queue.yml`)
- `--dry-run`: parse and sort specs, print execution plan, don't dispatch

### Constraints

- Must use `dispatch.py` for ALL dispatches — never call claude CLI directly
- Must respect the 10 hard rules (especially: no more than 5 parallel bees, dev branch only)
- Must NOT modify `.deia/config/`, `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`
- File under 500 lines. If over, split into modules (e.g., `spec_parser.py`, `event_logger.py`)

---

## Deliverable 2: Regent Bot Prompt Template

**File:** `.deia/config/regent-bot-prompt.md`

### What It Is

The system prompt injected into Q88NR-bot when it processes a spec. This is NOT a task file — it's a reusable prompt template that tells the bot how to behave.

### Contents

1. **Identity:** "You are Q88NR-bot, a mechanical regent. You follow the HIVE.md process exactly."
2. **Abbreviated chain of command** (from HIVE.md — Q88NR-bot reads spec → writes briefing → dispatches Q33N → reviews → approves → waits for bees → reviews results)
3. **Mechanical review checklist** for Q33N's task files:
   - Do deliverables match the spec's acceptance criteria?
   - Are file paths absolute?
   - Are test requirements present (TDD)?
   - Is CSS var(--sd-*) only?
   - Are files projected under 500 lines?
   - Are there any stubs or TODOs?
4. **Correction rule:** Max 2 correction cycles on Q33N's task files. After 2 rounds, approve with a `⚠️ APPROVED_WITH_WARNINGS` flag.
5. **Fix cycle rule:** If bees fail, create a fix spec (P0) and return it. Max 2 fix cycles per original spec. After 2: flag as `NEEDS_DAVE`.
6. **Budget awareness:** "You do not control the budget. The queue runner enforces limits. Report your costs accurately."
7. **What you NEVER do:** Make strategic decisions, modify specs, override hard rules, write code, skip the Q33N step.

### Size

Should be 100-200 lines. Concise. Mechanical. No philosophy.

---

## Deliverable 3: Queue Config (`queue.yml`)

**File:** `.deia/config/queue.yml`

### Contents (from spec section 4)

```yaml
budget:
  max_session_usd: 20.00
  warn_threshold: 0.80
  max_fix_cycles_per_spec: 2
  max_specs_per_session: 50
  max_parallel_bees: 3

models:
  regent_bot: "ollama:llama3.1:8b"
  q33n: "claude-sonnet-4-6"
  bee_default: "claude-haiku-4-5"
  bee_complex: "claude-sonnet-4-6"

paths:
  queue_dir: ".deia/hive/queue"
  needs_review_dir: ".deia/hive/queue/_needs_review"
  done_dir: ".deia/hive/queue/_done"
  smoke_dir: ".deia/hive/smoke"
  coordination_dir: ".deia/hive/coordination"
  tasks_dir: ".deia/hive/tasks"
  responses_dir: ".deia/hive/responses"

deploy:
  railway_health_url: "https://dev-api.shiftcenter.com/health"
  vercel_url: "https://dev.shiftcenter.com"
  health_poll_interval_seconds: 15
  health_poll_timeout_seconds: 300

git:
  branch: "dev"
  commit_prefix: "[Q33N]"
  auto_push: true
```

This is a simple YAML file. The bee writes it, the queue runner reads it via PyYAML.

---

## Deliverable 4: Morning Report Generator

**File:** `.deia/hive/scripts/queue/morning_report.py`

### What It Does

Called by `run_queue.py` at the end of a session. Reads the session event log and generates a markdown report.

**Output file:** `.deia/hive/queue/YYYY-MM-DD-MORNING-REPORT.md`

### Report Template

From spec section 8.3:

```markdown
# Morning Report — YYYY-MM-DD

## Queue Summary
- Specs processed: N
- Specs succeeded: N
- Specs failed (needs Dave): N
- Specs remaining in queue: N
- Session cost: $X.XX
- Session duration: Xh Xm

## Completed
| Spec | Status | Tests | Cost | Time |
|------|--------|-------|------|------|
| SPEC-xxx | CLEAN | N new | $X.XX | Xm |

## Needs Your Review
| Spec | Issue | Fix Attempts |
|------|-------|-------------|
| SPEC-yyy | [error summary] | N |

## Screenshots
- .deia/hive/smoke/YYYY-MM-DD-HHMM/ (SPEC-xxx)

## Remaining Queue
| Spec | Priority |
|------|----------|
| SPEC-zzz | P1 |
```

### Key Functions

```python
def generate_morning_report(
    session_events: list[QueueEvent],
    queue_dir: Path,
    output_path: Path
) -> Path:
    """Generate morning report markdown from session events."""
```

### Constraints

- Under 500 lines
- Pure Python (no external dependencies beyond PyYAML which run_queue.py already uses)
- Reads from session event log JSON file
- Writes markdown to queue directory

---

## Files Q33N Must Read Before Writing Tasks

| File | Why |
|------|-----|
| `docs/specs/SPEC-BUILD-QUEUE-001.md` | The full spec — authoritative source |
| `.deia/BOOT.md` | Hard rules that the queue must enforce |
| `.deia/HIVE.md` | Chain of command the queue runner automates |
| `.deia/hive/scripts/dispatch/dispatch.py` | The dispatch script the queue runner must call |
| `.deia/config/` | Existing config directory structure |

## Task Breakdown Guidance

Four deliverables → four task files. Some can be parallel, some sequential:

1. **TASK for queue.yml** — trivial, assign **haiku**. No dependencies. Dispatch first.
2. **TASK for regent-bot-prompt.md** — small, assign **haiku**. No dependencies. Parallel with queue.yml.
3. **TASK for morning_report.py** — medium, assign **sonnet**. Needs the QueueEvent dataclass defined (shared with run_queue.py). Can define its own copy or import from a shared types module.
4. **TASK for run_queue.py** — medium-large, assign **sonnet**. The core orchestration. Should import from morning_report.py. Dispatch after the others so it can import from them.

Suggest: dispatch 1+2+3 in parallel, then dispatch 4 after they land.

## Test Requirements

- `run_queue.py`: test queue sorting, spec parsing, budget enforcement, fix cycle limits, dry-run mode. Minimum 15 tests.
- `morning_report.py`: test report generation from sample events. Minimum 5 tests.
- `queue.yml`: validation test — load the YAML and verify all required keys exist.
- `regent-bot-prompt.md`: no code tests needed (it's a markdown template), but verify it contains the required sections programmatically.

Test files go in `.deia/hive/scripts/queue/tests/`.

## Constraints (apply to all tasks)

- Python 3.13
- No file over 500 lines
- TDD: tests first
- No stubs
- Must use existing `dispatch.py` — never call claude CLI directly
- Queue runner must NOT modify config files, BOOT.md, HIVE.md, or CLAUDE.md
- All paths relative to repo root (resolve via `Path(__file__).resolve().parents[4]` or similar)
