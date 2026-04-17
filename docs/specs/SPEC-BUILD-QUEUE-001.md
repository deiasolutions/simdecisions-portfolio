# SPEC-BUILD-QUEUE-001: Automated Build Queue

**Date:** 2026-03-11
**Author:** Q88N (Dave) × Mr. AI (Claude)
**Status:** DRAFT — pending Q88N review
**Priority:** Alpha Part 2, Step 1 (build first)

---

## 1. Purpose

Automate the spec → build → deploy → test → fix cycle so Dave can write specs during the day and the hive executes them overnight. The pipeline runs unattended. Dave reviews results in the morning.

This is SimDecisions eating its own dogfood — a governed process with measurement, quality gates, and autonomous execution with human review at the boundaries.

---

## 2. The Pipeline

```
                    ┌─────────────────────────────┐
                    │  Q88N writes specs during    │
                    │  the day, drops in queue     │
                    └──────────┬──────────────────┘
                               │
                               ▼
                    ┌─────────────────────────────┐
                    │  hive dispatch-queue         │
                    │  (manual start, runs until   │
                    │   queue is empty)            │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Q88NR-bot reads next spec   │
                    │  (Ollama or Haiku — cheap)   │
                    │  writes briefing for Q33N    │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Q33N writes task files      │
                    │  Q88NR-bot reviews + approves│
                    │  Q33N dispatches bees        │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Bees code + test            │
                    │  Write response files        │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Q33N commits to dev branch  │
                    │  git push to GitHub          │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Railway auto-deploys dev    │
                    │  Wait for deploy complete    │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │  Smoke test bot              │
                    │  - Hit deployed URL          │
                    │  - Screenshot each page      │
                    │  - Check HTTP status codes   │
                    │  - Check /health endpoint    │
                    │  - Check browser console     │
                    │  - Measure load time         │
                    └──────────┬──────────────────┘
                               │
                         ┌─────┴─────┐
                         │           │
                    ┌────▼───┐  ┌───▼────────────────┐
                    │ CLEAN  │  │ ERRORS             │
                    │        │  │                    │
                    │ Log    │  │ Q88NR-bot creates  │
                    │ success│  │ error spec from    │
                    │ to     │  │ smoke test output  │
                    │ ledger │  │                    │
                    │        │  │ Re-enters queue    │
                    │ Next   │  │ as fix task        │
                    │ spec   │  │                    │
                    │ ↑      │  │ Max 2 fix cycles   │
                    └────────┘  │ then flag for Dave │
                               └────────────────────┘
```

---

## 3. Spec Format

Specs go in the queue as markdown files. Dave writes them. They live at:

`home://hive/queue/` (on the local hivenode)

Also accessible at: `.deia/hive/queue/` in the repo (syncs to hivenode)

### Spec File Format

```markdown
# SPEC: [Title]

## Priority
[P0 | P1 | P2] — queue processes P0 first, then P1, then P2

## Objective
[What needs to happen. One paragraph max.]

## Context
[What the builder needs to know. File paths, existing code, design decisions.]

## Acceptance Criteria
- [ ] [Concrete, testable criterion 1]
- [ ] [Concrete, testable criterion 2]

## Smoke Test
- [ ] [What the smoke test bot should verify after deploy]
- [ ] [URL to hit, expected response, expected UI state]

## Model Assignment
[haiku | sonnet | opus — for the bees. Q88NR-bot is always cheap (ollama/haiku). Q33N is always sonnet.]

## Constraints
[Any special rules beyond the standard 10 hard rules]
```

### File Naming

`YYYY-MM-DD-HHMM-SPEC-<short-name>.md`

Example: `2026-03-12-0900-SPEC-sdeditor-raw-mode.md`

### Queue Order

Files are processed in priority order (P0 first), then by filename (oldest first within same priority). The queue reader sorts:
1. P0 specs by filename (chronological)
2. P1 specs by filename
3. P2 specs by filename

---

## 4. Q88NR-bot (Bot Regent)

This is NOT Dave. This is a cheap LLM that mechanically follows the HIVE.md process.

### What It Is

A headless Claude/Ollama instance dispatched with `--role regent-bot`. It reads one spec at a time from the queue and drives the HIVE.md chain:

1. Read the spec
2. Write a briefing for Q33N (to `.deia/hive/coordination/`)
3. Dispatch Q33N with the briefing
4. Wait for Q33N to return task files
5. Review task files against the spec (mechanical check: do deliverables match acceptance criteria? Are file paths absolute? Are test requirements present?)
6. Approve or request corrections (max 2 correction cycles, then approve anyway with a warning flag)
7. Q33N dispatches bees
8. Wait for bees to complete
9. Q33N reports results
10. Q88NR-bot reviews results (tests pass? response files complete? no stubs?)
11. If clean → proceed to commit/deploy/smoke
12. If failures → create a fix spec and re-enter the queue (max 2 fix cycles)

### What It Does NOT Do

- Make strategic decisions (Dave made those when writing the spec)
- Modify specs (it executes them as written)
- Override the 10 hard rules
- Dispatch more than 5 bees in parallel
- Run indefinitely (stops when queue is empty or budget is hit)

### Model Assignment

Q88NR-bot: **Ollama local** (free, no API cost) or **Haiku** ($0.001 per spec — negligible)

The Q88NR-bot prompt is injected from a template file at `.deia/config/regent-bot-prompt.md`. This file contains:
- The HIVE.md chain of command (abbreviated)
- The mechanical review checklist
- The "approve after 2 correction cycles" rule
- The budget limit
- The fix cycle limit (max 2 per spec)

### Budget Control

The queue runner tracks cumulative cost per session. Config in `.deia/config/queue.yml`:

```yaml
budget:
  max_session_usd: 20.00
  warn_threshold: 0.80
  max_fix_cycles_per_spec: 2
  max_specs_per_session: 50
  max_parallel_bees: 3  # overnight = lower parallelism, lower cost
models:
  regent_bot: "ollama:llama3.1:8b"  # free, local
  q33n: "claude-sonnet-4-6"
  bee_default: "claude-haiku-4-5"
  bee_complex: "claude-sonnet-4-6"
```

When budget hits `warn_threshold` (80%), Q88NR-bot logs a warning and stops accepting new specs. Currently running specs finish. When budget hits `max_session_usd`, the queue stops completely.

---

## 5. Commit + Deploy Step

After bees complete and Q33N reports clean results:

### 5.1 Commit

Q33N runs:
```bash
git add -A
git commit -m "[Q33N] SPEC-<name>: <objective summary>"
git push origin dev
```

Commit message format: `[Q33N] SPEC-XXX: brief imperative description`

### 5.2 Wait for Deploy

Railway auto-deploys from dev branch. The queue runner polls the Railway health endpoint:

```bash
curl -s https://dev-api.shiftcenter.com/health
```

Poll every 15 seconds, timeout after 5 minutes. If deploy fails (health check doesn't return 200), log the error and create a fix spec.

Vercel also auto-deploys. Poll:

```bash
curl -s https://dev.shiftcenter.com/ -o /dev/null -w "%{http_code}"
```

Both must return 200 before proceeding to smoke test.

---

## 6. Smoke Test Bot

After deploy is confirmed healthy, run automated smoke tests.

### 6.1 What It Tests

| Test | How | Pass Criteria |
|------|-----|---------------|
| Frontend loads | `curl -s https://dev.shiftcenter.com/` | HTTP 200, response contains `<div id="root">` |
| API health | `curl -s https://dev-api.shiftcenter.com/health` | HTTP 200, JSON `{"status": "ok"}` |
| Auth health | `curl -s https://dev-api.shiftcenter.com/auth/verify` | HTTP 401 (expected — no token) |
| Page screenshot | Playwright `page.screenshot()` | File saved to `.deia/hive/smoke/YYYY-MM-DD/` |
| Console errors | Playwright `page.on('console', ...)` | Zero `error` level messages |
| Load time | Playwright `performance.timing` | `domContentLoaded < 3000ms` |
| Spec-specific tests | From the spec's `## Smoke Test` section | Per-spec criteria |

### 6.2 Playwright Config

```javascript
// .deia/hive/scripts/smoke/playwright.config.ts
{
  testDir: '.deia/hive/scripts/smoke/tests/',
  use: {
    baseURL: 'https://dev.shiftcenter.com',
    screenshot: 'on',
    trace: 'retain-on-failure'
  },
  outputDir: '.deia/hive/smoke/results/'
}
```

### 6.3 Screenshot Archive

Every smoke test run saves screenshots to:

`.deia/hive/smoke/YYYY-MM-DD-HHMM/`

Contents:
- `home.png` — landing page
- `chat.png` — chat EGG loaded
- `console-errors.json` — any console errors captured
- `timing.json` — load performance data
- `smoke-report.md` — pass/fail summary

These persist so Dave can review in the morning. Not gitignored — they're evidence.

### 6.4 Spec-Specific Smoke Tests

Each spec can include custom smoke test criteria:

```markdown
## Smoke Test
- [ ] Navigate to /chat, terminal pane visible
- [ ] Type "hello", response appears in text-pane within 5 seconds
- [ ] Settings modal opens when clicking API key badge
```

The smoke test bot reads these and generates Playwright assertions. If the criteria are too vague for automated testing, the bot logs them as "manual verification needed" for Dave's morning review.

---

## 7. Error → Fix Cycle

When smoke tests fail:

### 7.1 Error Report

The smoke test bot generates an error report:

```markdown
# SMOKE-FAIL: SPEC-<name>

## Failed Tests
- [ ] Console error: "TypeError: Cannot read property 'x' of undefined" at main.js:1234
- [ ] Load time: 4,200ms (limit: 3,000ms)

## Screenshots
- .deia/hive/smoke/2026-03-12-0300/chat-error.png

## Deploy Log
- Railway deploy ID: abc123
- Deploy time: 45s
- Health check: passed

## Suggested Fix
[Q88NR-bot's assessment of what might be wrong — this is the cheap LLM's best guess, not authoritative]
```

### 7.2 Fix Spec Generation

Q88NR-bot creates a fix spec from the error report:

```markdown
# SPEC: Fix smoke test failures from SPEC-<name>

## Priority
P0 — fix before processing next spec in queue

## Objective
Fix the errors reported in SMOKE-FAIL-SPEC-<name>.md

## Context
[error report contents]

## Acceptance Criteria
- [ ] Console error resolved
- [ ] Load time under 3,000ms
- [ ] All original spec acceptance criteria still pass
```

This fix spec enters the queue as P0 (processes next). The fix cycle runs: Q33N → bees → commit → deploy → re-smoke.

### 7.3 Fix Cycle Limits

- Max 2 fix cycles per original spec
- After 2 failed fix cycles, the spec is flagged as `NEEDS_DAVE` and moved to `.deia/hive/queue/_needs_review/`
- The queue skips it and moves to the next spec
- Dave reviews in the morning

---

## 8. Queue Runner

### 8.1 Start Command

```bash
python .deia/hive/scripts/queue/run_queue.py
```

Or via hivenode:

```bash
python -m hivenode --run-queue
```

### 8.2 Queue Runner Logic

```python
# Pseudocode
def run_queue():
    specs = load_queue_sorted_by_priority()
    session_cost = 0.0
    
    for spec in specs:
        if session_cost >= config.budget.max_session_usd:
            log("Budget exhausted. Stopping.")
            break
        
        result = process_spec(spec)  # the full pipeline
        session_cost += result.cost
        
        if result.status == "CLEAN":
            archive_spec(spec)
            log_success(spec, result)
        elif result.status == "NEEDS_DAVE":
            move_to_needs_review(spec)
            log_failure(spec, result)
        
        log_to_ledger(spec, result)
    
    generate_morning_report()
```

### 8.3 Morning Report

When the queue finishes (empty or budget exhausted), the runner generates:

`.deia/hive/queue/YYYY-MM-DD-MORNING-REPORT.md`

```markdown
# Morning Report — 2026-03-12

## Queue Summary
- Specs processed: 7
- Specs succeeded: 5
- Specs failed (needs Dave): 1
- Specs remaining in queue: 3
- Session cost: $12.47
- Session duration: 6h 23m

## Completed
| Spec | Status | Tests | Cost | Time |
|------|--------|-------|------|------|
| SPEC-sdeditor-raw-mode | ✅ Clean | 45 new | $1.80 | 18m |
| SPEC-chat-bubbles | ✅ Clean | 12 new | $0.90 | 11m |
| ... | | | | |

## Needs Your Review
| Spec | Issue | Fix Attempts |
|------|-------|-------------|
| SPEC-freeform-canvas | Console error after 2 fix cycles | 2 |

## Screenshots
- .deia/hive/smoke/2026-03-12-0100/ (SPEC-sdeditor-raw-mode)
- .deia/hive/smoke/2026-03-12-0130/ (SPEC-chat-bubbles)
- ...

## Remaining Queue
| Spec | Priority |
|------|----------|
| SPEC-focus-manager | P1 |
| SPEC-vertical-tabs | P2 |
| SPEC-merge-rules | P2 |
```

---

## 9. File System

| Purpose | Path |
|---------|------|
| Spec queue (input) | `.deia/hive/queue/` |
| Specs needing Dave review | `.deia/hive/queue/_needs_review/` |
| Processed specs (archive) | `.deia/hive/queue/_done/` |
| Smoke test results | `.deia/hive/smoke/YYYY-MM-DD-HHMM/` |
| Morning reports | `.deia/hive/queue/YYYY-MM-DD-MORNING-REPORT.md` |
| Queue config | `.deia/config/queue.yml` |
| Regent bot prompt | `.deia/config/regent-bot-prompt.md` |
| Queue runner script | `.deia/hive/scripts/queue/run_queue.py` |
| Smoke test scripts | `.deia/hive/scripts/smoke/` |

**Everything else uses existing paths:** briefings → `.deia/hive/coordination/`, task files → `.deia/hive/tasks/`, responses → `.deia/hive/responses/`.

---

## 10. Event Ledger Integration

Every queue event is logged:

| Event Type | When |
|-----------|------|
| `QUEUE_SPEC_STARTED` | Q88NR-bot picks up a spec |
| `QUEUE_BRIEFING_WRITTEN` | Q88NR-bot writes briefing for Q33N |
| `QUEUE_TASKS_APPROVED` | Q88NR-bot approves Q33N's task files |
| `QUEUE_BEES_COMPLETE` | All bees for a spec have finished |
| `QUEUE_COMMIT_PUSHED` | Git push to dev |
| `QUEUE_DEPLOY_CONFIRMED` | Railway + Vercel healthy |
| `QUEUE_SMOKE_PASSED` | All smoke tests pass |
| `QUEUE_SMOKE_FAILED` | Smoke tests failed, fix spec created |
| `QUEUE_FIX_CYCLE` | Fix spec entered queue |
| `QUEUE_NEEDS_DAVE` | Spec flagged for manual review after max fix cycles |
| `QUEUE_SESSION_COMPLETE` | Queue empty or budget exhausted |
| `QUEUE_BUDGET_WARNING` | 80% of session budget consumed |

Every event includes: timestamp, spec_id, cost_usd, duration_ms, model_used.

---

## 11. Security

- Q88NR-bot has NO access to production. Only dev branch, only dev deployment.
- Q88NR-bot cannot modify `.deia/config/`, `.deia/BOOT.md`, `.deia/HIVE.md`, or `CLAUDE.md`. Read only.
- Q88NR-bot cannot modify the queue runner itself or the smoke test scripts.
- Budget hard cap is enforced by the queue runner, not by Q88NR-bot. Q88NR-bot cannot increase its own budget.
- All commits are to dev branch only. Merge to main requires Dave.

---

## 12. Implementation Priority

| Step | What | Effort |
|------|------|--------|
| 1 | Queue runner script (`run_queue.py`) | M — orchestration loop, file management |
| 2 | Regent bot prompt template | S — markdown file with mechanical review checklist |
| 3 | Queue config (`queue.yml`) | S — YAML file |
| 4 | Smoke test base suite (health, screenshot, console, timing) | M — Playwright scripts |
| 5 | Spec-specific smoke test generator | M — parse spec → Playwright assertions |
| 6 | Morning report generator | S — markdown template from queue state |
| 7 | Fix spec generator (error report → fix spec) | S — template from smoke failures |
| 8 | Event Ledger wiring | S — emit events from queue runner |
| 9 | Railway deploy polling | S — curl + retry loop |
| 10 | Wire `hive dispatch-queue` CLI entry point | S — pyproject.toml script entry |

Total: ~3-5 days of bee time. The queue runner is the hardest piece. Everything else is templating and wiring.

---

## 13. First Test Run

Before trusting the pipeline overnight:

1. Write 3 simple specs (small S-sized items from the Alpha backlog)
2. Run `hive dispatch-queue` manually, watch it execute
3. Verify: briefing written, task files created, bees dispatched, code committed, deployed, smoke tested
4. Fix any issues in the queue runner itself
5. Run 3 more specs unattended for 1 hour
6. Review morning report
7. If clean: trust it for overnight runs

---

**End of SPEC-BUILD-QUEUE-001.**

*daaaave-atx × Claude (Anthropic) · CC BY 4.0*
