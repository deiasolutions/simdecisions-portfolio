# TRIAGE ESCALATION: PORTFOLIO-NUGGET

**Date:** 2026-04-17 02:20:00 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-PORTFOLIO-NUGGET-HUNT-001.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-17T02:05:00.150163Z — requeued (empty output)
- 2026-04-17T02:10:00.157608Z — requeued (empty output)
- 2026-04-17T02:15:00.163192Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-PORTFOLIO-NUGGET-HUNT-001.md`
2. **Diagnose root cause** — why is this spec failing repeatedly?
3. **Options:**
   - Fix spec and move back to backlog/
   - Archive spec if no longer needed
   - Break into smaller specs
   - Escalate to architect (Mr. AI) if systemic issue

## Original Spec

```markdown
## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

## Clean Retry

**Previous attempt failed with no output.**

This is a clean retry — start from scratch. Check logs if available to
understand why the previous attempt failed.

---

# SPEC-PORTFOLIO-NUGGET-HUNT-001: Portfolio Curation for 1000bulbs Application

**Priority:** P0
**Model:** opus (orchestrator + final report); sonnet (queens + bees)
**Effort:** ~30 min wall (goal, not hard limit — faster without sacrificing quality is fine)
**Cost:** ~$20-35 estimated
**Depends On:** None
**Status:** READY

---

## Why This Spec Exists

Q88N is applying for Senior AI Engineer at 1000bulbs. Applications are **screened on GitHub portfolio before any interview.** The prior audit (SPEC-PORTFOLIO-1000BULBS-001) scored at the repo level and missed the point. This spec does a folder/file-level deep dive of `simdecisions` (the flagship monorepo) plus a secondary reference to a shipped consumer product (familybondbot — a full-stack Discord bot with multiple seasons of live usage), curated and tailored to the exact screening criteria below.

---

## 1000bulbs Screening Criteria (from job description — EMBED IN ALL BEE PROMPTS)

Applications are screened on GitHub portfolio. Portfolio **must** demonstrate:

1. **Multi-tier, 12-factor applications built using teams of AI developer agents** — not merely AI-assisted individual features
2. **Clear architectural separation:** view, API interface, service/business logic, persistence, and database as distinct tiers
3. **CI/CD pipelines** integrated into projects
4. **Evidence that you evaluate and correct AI-generated output** (commit history, README notes, code comments, or design documents that demonstrate judgment over compliance)

Additional signals assessed in interview (worth surfacing in portfolio):
- **Strangler Fig / incremental delivery** — modernizing a living codebase
- **AI orchestration expertise** — directing teams of AI developer agents from requirements to deployed application
- **Critical AI evaluation** — identifying SOLID/DRY violations, correcting agent output
- **Full-stack ownership** — React frontend, API design, relational DB, deployment

---

## Orchestration Architecture

This spec uses a **multi-tier bee architecture** mirroring the DEIA Hive itself:

```
OPUS ORCHESTRATOR (this spec's top-level bee)
│
├── reads prior audit artifacts + JD criteria + repo structure
├── decides how many Sonnet Queens to launch and what each covers
│   (the domains below are SUGGESTIONS — Opus decides the actual split)
│
├── launches N Sonnet Queens in parallel
│   Each Queen:
│   ├── receives a domain assignment + the nugget schema + JD criteria
│   ├── decides how many Sonnet Bees to launch for its domain
│   ├── launches bees in parallel (folder assignments per bee)
│   ├── reads all bee reports
│   └── writes a domain-level nugget report + refactor observations
│
├── reads ALL queen reports + raw bee reports
└── writes final deliverables (Phase B — two deliverables)
```

**Suggested domains** (Opus may reorganize, merge, or split as it sees fit):
- Platform architecture (hivenode, engine, browser, auth, deployment configs)
- DEIA Hive & AI orchestration (.deia/, scheduler, dispatch, queue system)
- AI correction evidence (git history, process docs, engineering standards)
- Live services verification (Playwright/curl probes of hodeia.me, Vercel, Railway)
- Secondary product — familybondbot (separate repo)

Queens use `subagent_type: "general-purpose"` with `model: "sonnet"`.
Bees within queens use `subagent_type: "Explore"` for folder surveys, `subagent_type: "Bash"` for Playwright/curl probes.

**Queens MUST launch their bees in parallel** (single message, multiple Task tool calls).
**Opus MUST launch all queens in parallel** (single message, multiple Task tool calls).
**Some research takes longer than others — that's fine.** Opus should NOT wait for all queens to finish before starting synthesis on early returns. But all queens must complete before the final deliverables are written.

---

## Phase A — Parallel Research

### What each bee records

#### Per nugget found (portfolio signal)
```yaml
- path: "absolute path to file or folder"
  kind: README | architecture-doc | diagram | code-pattern | spec | test | config | process-doc | deployment | commit-range
  jd_signal: "which 1000bulbs criterion it demonstrates (1-4) or 'differentiator'"
  one_line_pitch: "why a 1000bulbs reviewer would care"
  share_classification: PUBLIC_TEASER | EXCERPT_OK | REFERENCE_ONLY | DO_NOT_SHARE
  effort_to_extract: "hours to sanitize and publish"
  verbatim_shareable: true | false  # can this be shown as-is or does it need scrubbing?
```

#### Per refactor opportunity found (codebase improvement)
```yaml
- path: "absolute path to file or folder"
  issue: "what's wrong or suboptimal"
  jd_relevance: "which 1000bulbs criterion this would strengthen if fixed"
  severity: cosmetic | structural | blocker
  effort: "hours to fix"
  recommendation: "what to do about it"
```

Bees should flag refactor opportunities as they encounter them during nugget hunting — dead code, missing tests, broken patterns, architectural gaps, incomplete features, anything that weakens the portfolio story or violates the engineering standards a 1000bulbs reviewer would look for (SOLID, DRY, 12-factor, clean separation).

### QUEEN-1: Platform Architecture

**Goal:** Prove multi-tier 12-factor with clear architectural separation.

Bees survey:
- **BEE-1a** `hivenode/` — API interface + service/business logic tier. Routes, relay, ledger, wiki, inventory, shell, adapters. How many routes? What patterns?
- **BEE-1b** `simdecisions/` — domain engine tier. DES, Phase-IR, optimization, flows. Separation from hivenode.
- **BEE-1c** `browser/` — view tier. React, Vite, TypeScript. Pane primitives, shell, sets system. Component count, test coverage.
- **BEE-1d** `hodeia_auth/` — auth service tier. JWT, MFA, OAuth. Standalone Railway deploy. Database layer (SQLAlchemy, raw migrations).

Also examine: `pyproject.toml`, `Dockerfile`, `railway.toml`, `vercel.json` — 12-factor evidence (config via env, port binding, dev/prod parity, stateless processes).

### QUEEN-2: DEIA Hive & AI Orchestration

**Goal:** Prove "teams of AI developer agents" — the #1 screening criterion.

Bees survey:
- **BEE-2a** `.deia/` — BOOT.md, HIVE.md, processes/, config/ethics.yml, config/carbon.yml. The chain of command. Role definitions. How is this NOT just "AI-assisted"?
- **BEE-2b** `hivenode/scheduler/` — scheduler_daemon.py, dispatcher_daemon.py, triage_daemon.py. Automated dispatch infrastructure. How does work flow from human intent to deployed code?
- **BEE-2c** `.deia/hive/queue/` — count specs in _done/ (1357!), _escalated/ (18), _needs_review/ (3), backlog/ (10). This IS the evidence of agent teams at scale. Sample 5-10 completed specs for diversity of work.

### QUEEN-3: Evidence of AI Correction & Engineering Rigor

**Goal:** Prove "evaluate and correct AI-generated output" — the #4 screening criterion that most applicants will fail.

Bees survey:
- **BEE-3a** Git history — run `git log --oneline -100` and look for correction patterns: rejections, re-dos, "fix" commits after bee output, PROCESS-13 references. Find 5-10 concrete correction examples.
- **BEE-3b** Process docs — `.deia/processes/` (especially PROCESS-13 if it exists), Gate 0 validation, triage daemon logic. How does Q88N's system catch and correct bad agent output?
- **BEE-3c** Engineering standards — `_tools/inventory.py` (feature tracking), `tests/` (test structure, coverage), `pyproject.toml` (dependencies, config), `Dockerfile` (build process), `CLAUDE.md` rules (500-line limit, TDD, no stubs, no hardcoded colors). These ARE the correction guardrails.

### QUEEN-4: Live Services Verification (Playwright)

**Goal:** Verify what is actually deployed and reachable. Do not claim "live" in the portfolio if it's not.

Bees probe (use curl or Playwright depending on what's needed):
- **BEE-4a** `https://hodeia.me` — hit `/health`, `/jwks.json`, check if login/register pages render. Record HTTP status codes, response times, what's functional vs placeholder.
- **BEE-4b** Vercel frontend — find the Vercel URL (check `vercel.json`, or `*.vercel.app`). Does it load? Does a set render? Or is it a blank page / error?
- **BEE-4c** Railway hivenode — find the Railway URL (check `railway.toml`, or known prod URL). Hit `/health`, `/build/status`. Record what responds.

**Output:** A truthful "deployment status" table. If something is down, say so. The portfolio must not overclaim.

### QUEEN-5: Secondary Product — familybondbot

**Goal:** Assess familybondbot as evidence of a **shipped end-to-end product** with real users.

**Repo location:** `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\`

Bees survey:
- **BEE-5a** Structure, README, features — what does it do? How many seasons of content? Is there a public-facing presence? Discord bot architecture. What stack?
- **BEE-5b** Code quality — architecture patterns, test coverage, separation of concerns. Is this a toy or a real product?

**Important:** Do NOT link to the product URL in any output. Refer to it as "a full-stack consumer Discord bot with multiple seasons of live usage" or similar. It deserves a lengthy README writeup as a portfolio piece.

---

## Phase B — Synthesis (Opus orchestrator, after all queens return)

The Opus orchestrator reads all 5 queen reports + raw bee reports and produces:

### B1. Recommendation Report for Q88N

**Location:** `docs/portfolio/1000bulbs-nugget-hunt-recommendation.md`

Must include:

- [ ] **Top 10-15 nuggets ranked** by 1000bulbs signal strength x low extraction effort
- [ ] **JD signal coverage matrix** — which nuggets cover which of the 4 screening criteria + differentiators. Every criterion must have ≥2 nuggets. If any criterion has 0 coverage, flag it as a gap.
- [ ] **Deployment truth table** — what's actually live, per Queen-4's Playwright probes. No overclaiming.
- [ ] **Story arc** — the narrative thread for a 1000bulbs reviewer reading the portfolio in 5 minutes
- [ ] **familybondbot assessment** — should it be featured? How prominently? Does it add signal the simdecisions repo doesn't already cover?
- [ ] **Recommended showcase format** — options: (a) enhanced simdecisions README, (b) new public teaser repo, (c) curated page on deiasolutions.com, (d) other. Pick one, justify.
- [ ] **What to drop from prior audit** — which SPEC-PORTFOLIO-1000BULBS-001 recommendations are superseded
- [ ] **Cost-benefit table** — hours-to-ship vs signal-strength per nugget
- [ ] **Q88N decisions needed** — 3-5 explicit choices as "Option A / Option B / Recommendation"

### B2. Follow-on Spec — Portfolio Curation

**Location:** `docs/portfolio/SPEC-PORTFOLIO-CURATE-001.draft.md`

A complete, dispatchable spec that Q88N can read, modify, and submit to the factory. It must:

- [ ] Have SPEC-ID: `SPEC-PORTFOLIO-CURATE-001`
- [ ] List every concrete file to create/modify with absolute paths
- [ ] Specify sanitization needed (remove secrets, scrub internal paths, etc.)
- [ ] Include a lengthy familybondbot README section (if Queen-5 recommends featuring it)
- [ ] Include test/verification steps (links work, no broken refs, badges render, Mermaid diagrams valid)
- [ ] Be executable by a single Sonnet bee
- [ ] Have crisp acceptance criteria (NOT vague "make it look good")
- [ ] Reference the JD criteria explicitly in its acceptance criteria

### B3. Follow-on Spec — Codebase Refactor

**Location:** `docs/portfolio/SPEC-PORTFOLIO-REFACTOR-001.draft.md`

A complete, dispatchable spec aggregating every refactor opportunity the queens/bees identified. This is NOT about making the code portfolio-pretty — it's about fixing real engineering issues that a 1000bulbs reviewer would catch. It must:

- [ ] Have SPEC-ID: `SPEC-PORTFOLIO-REFACTOR-001`
- [ ] Aggregate all refactor observations from all queen reports
- [ ] Rank by: (1) blockers first, (2) structural issues that weaken JD signal coverage, (3) cosmetic
- [ ] Group into dispatchable work units (each unit ≤ 4 hours for a single Sonnet bee)
- [ ] For each unit: list files to touch, what to change, which JD signal it strengthens, acceptance criteria
- [ ] Flag any refactor that would break existing functionality (requires test coverage first)
- [ ] Be honest about what's broken — if the codebase has gaps, the refactor spec should fix them, not hide them

---

## Files the Opus Orchestrator Must Read First

1. This spec (for full context)
2. `docs/portfolio/1000bulbs-portfolio-audit.md` (prior scorecards — explicitly supersede)
3. `docs/portfolio/1000bulbs-teaser-README.draft.md` (prior teaser draft — keep what works)
4. `.deia/BOOT.md` (operating rules)
5. `CLAUDE.md` (repo structure)

---

## Constraints

- **Curation = saying no.** Do NOT propose >15 total nuggets.
- **No overclaiming.** If hodeia.me login is broken, say so. If Vercel frontend is a blank page, say so.
- **No federalist-papers-ai.** Excluded, do not reference.
- **familybondbot: no URL.** Refer to it generically. Do not link to the live product domain.
- **Time is a goal, not a hard limit.** If queens/bees return faster without sacrificing quality, great. If a slice needs more time for thoroughness, take it.

---

## Smoke Test

After reading the deliverables, can Q88N answer in one pass:

1. **What specific files/folders from simdecisions tell the 1000bulbs story?** (paths listed)
2. **Does every screening criterion have ≥2 concrete evidence items?** (coverage matrix)
3. **What's actually deployed and working right now?** (deployment truth table)
4. **Should familybondbot be featured, and how?** (clear yes/no + framing)
5. **Is the portfolio curation spec ready to dispatch with minor edits?** (B2 filename + readiness)
6. **What's broken or weak in the codebase, ranked by impact on the portfolio?** (refactor list)
7. **Is the refactor spec ready to dispatch with minor edits?** (B3 filename + readiness)

All 7 → pass. Any "unclear" → fail.

---

**END OF SPEC**

## Triage History
- 2026-04-17T02:05:00.150163Z — requeued (empty output)
- 2026-04-17T02:10:00.157608Z — requeued (empty output)
- 2026-04-17T02:15:00.163192Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
