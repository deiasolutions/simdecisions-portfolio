# SPEC-PORTFOLIO-1000BULBS-001: Portfolio Audit + Teaser Skeleton for 1000bulbs Job Application

## Priority

P1

## Depends On

None

## Model Assignment

sonnet

## Objective

Q88N is applying for a role at **1000bulbs** that screens at the portfolio stage for four specific signals:

1. **Multi-tier, 12-factor apps built with AI agent teams** (not just AI-assisted — AI-orchestrated).
2. **Clean architectural separation** across view / API / service / persistence / database layers.
3. **CI/CD pipelines visible** in repos.
4. **Evidence of evaluating and correcting AI output** (commit history, READMEs, design docs showing review loops).

Q88N has a deep bench of work that maps well (SimDecisions/ShiftCenter multi-tier stack, the DEIA Hive factory orchestrating Q33N/BEE agents under governance, PROCESS-13's "builders can't test their own output" rule, PRISM-IR as an open spec, the CLOCK/COIN/CARBON three-currencies measurement discipline), plus a 2006 call center simulator that predates the modern AI-orchestration era but demonstrates long-arc domain expertise. Much of this is in private repos; a minority is public.

The deliverable is a **portfolio audit + positioning strategy** that:

- Scores every known repo against the 1000bulbs criteria.
- Recommends a public / teaser / private-on-request classification for each.
- Lists portfolio gaps where remediation would materially strengthen the application.
- Drafts a **teaser repo README skeleton** (no code, narrative + Mermaid architecture diagrams) that a reviewer can read in five minutes and understand what Q88N builds, why it matters for 1000bulbs, and where to look next.

This is research + strategic drafting — no code changes, no publishing, no PRs. Q88N decides what happens with the output; Q33NR writes the follow-on implementation specs after review.

## Files to Read First

CLAUDE.md
README.md
PRISM-IR.md
DEIA-ELEVATOR-PITCH-60s.md
DEPLOYMENT.md
DEPLOYMENT-WIRING-NOTES.md
LOCAL-DEV.md
MOBILE-WORKDESK-E2E-VERIFICATION.md
FEATURE-INVENTORY.md
killed-specs-2026-04-10-intent.md
INVESTIGATION-REPO-COMPARISON-REPORT.md
call_center_500.prism.md
pyproject.toml
Dockerfile
railway.toml
vercel.json
.deia/BOOT.md
.deia/HIVE.md
.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md
.deia/processes/PROCESS-DOC-DRIVEN-DEVELOPMENT.md
.deia/processes/PROCESS-LIBRARY-V2.md
.deia/processes/P-DISPATCHER.md
.deia/processes/P-SCHEDULER.md
.deia/processes/bee-watchdog.md
.deia/config/ethics-default.yml
.deia/config/carbon.yml
.deia/config/grace.yml
hivenode/main.py
hivenode/scheduler/scheduler_daemon.py
hivenode/scheduler/dispatcher_daemon.py
simdecisions/des/loader_v2.py
browser/src/App.tsx
browser/vite.config.ts
hodeia_auth/main.py

## Acceptance Criteria

- [ ] Repo inventory table produced covering: this repo (simdecisions), all public repos in the `deiasolutions` GitHub org (pull via `gh repo list deiasolutions --json name,description,visibility,url`), private repos under `deiasolutions` listed by name with "not directly readable" noted, and a placeholder row for **the 2006 call center simulator** with a `[Q88N to provide materials]` note so the strategy can reference it without the bee needing to find it.
- [ ] For each repo, a **1000bulbs job-fit scorecard** filled in with citations:
  - [ ] `shows_multi_tier` (bool + one-line evidence) — clear view / API / service / persistence / database separation.
  - [ ] `shows_agent_orchestration` (bool + evidence) — directing AI agents, not just using them.
  - [ ] `shows_ai_correction` (bool + evidence) — commits, READMEs, or process docs showing AI output reviewed, fixed, or rejected.
  - [ ] `shows_cicd` (bool + evidence) — pipeline configs visible (GitHub Actions, Railway deploy, Vercel build).
  - [ ] `twelve_factor_signals` (list of observed 12-factor markers — config via env, stateless processes, port binding, logs as streams, etc.).
  - [ ] `strangler_fig_evidence` (any incremental modernization patterns, e.g., the DEF → SIM → EXE pipeline, the packages/ flatten, the egg/set rename).
  - [ ] `overall_fit_rating` (strong / moderate / weak / out-of-scope) with a one-sentence rationale.
- [ ] **Public / Teaser / Private-on-request classification** for each repo with rationale:
  - `PUBLIC` — already public or ready to make public with minor polish.
  - `TEASER` — public teaser repo stripped of proprietary code, architecture-only.
  - `PRIVATE_ON_REQUEST` — keep private, mention in application, share on request during interview.
  - `EXCLUDE` — not relevant / too rough / legacy stack.
- [ ] **Portfolio gap list** — concrete things that, if added/fixed in ≤ 1 day of polish, would materially improve the 1000bulbs fit. Examples: "README lacks architecture diagram," "no visible CI/CD badge," "commit history doesn't show AI-correction loop — add a post-mortem doc." Each gap ranked P0 / P1 / P2 by impact on the application.
- [ ] **Teaser repo README skeleton** saved as a draft at `docs/portfolio/1000bulbs-teaser-README.draft.md` with:
  - [ ] Five-minute narrative (who Q88N is, what DEIA/Hive/SimDecisions is, why it maps to the job).
  - [ ] Architecture diagram in Mermaid showing the multi-tier separation (browser → hivenode → simdecisions engine → PostgreSQL).
  - [ ] Second Mermaid diagram showing the agent-orchestration loop (Q88N → Q33NR → Q33N → BEEs → governance gates).
  - [ ] "How I work with AI agents" section mapping directly to the 1000bulbs criteria using specific DEIA artifacts (PROCESS-13, Gate 0, the queue runner, the triage daemon).
  - [ ] "Strangler Fig thinking" section citing DEF → SIM → EXE and the packages/ flatten as examples.
  - [ ] "Three Currencies" sidebar explaining CLOCK/COIN/CARBON as the measurement discipline behind the factory.
  - [ ] Closing CTA: "private repos available on request — DM for walkthrough."
- [ ] **Ranked follow-on spec sketches** (title + priority + model + one-line objective, no full drafts) covering the polishing work the audit identifies. Examples the bee may or may not recommend: PORTFOLIO-POLISH-001 (fix P0 gaps in flagship repo), PORTFOLIO-TEASER-PUBLISH-001 (create the teaser repo from the draft README), PORTFOLIO-DIAGRAMS-001 (produce the full diagram set beyond the teaser). These are sketches, not submissions.
- [ ] Report includes a front-loaded "What Q88N decides next" section listing the 3–5 highest-leverage decisions with their trade-offs so the application can move forward in one review pass.

## Smoke Test

After reading the report, Q88N can (a) point to a single repo or teaser README skeleton that fits the 1000bulbs filter, (b) name the one or two polish tasks that matter most before applying, and (c) decide which private repos to mention versus omit. If any of those three answers requires more research, the report fails its smoke test.

## Constraints

- Read-only. No repo modifications, no commits, no PRs, no publishing actions.
- Do not run `gh repo create`, `gh repo edit`, or any write operation on GitHub.
- `gh repo list deiasolutions` and `gh repo view <repo>` are allowed for enumeration and README reads of public repos.
- For the 2006 call center simulator, assume Q88N will brief separately — do NOT go searching for it on the internet or in unrelated directories. Use the `[Q88N to provide materials]` placeholder in the scorecard.
- Do not publish or draft social posts / application cover letters. The output is portfolio materials only.
- Cite specific files + line numbers for every evidence claim in the scorecards.
- The teaser README draft goes to `docs/portfolio/1000bulbs-teaser-README.draft.md`. Do not create a new GitHub repo for it.
- Do not write the full follow-on implementation specs — just the sketches. Q33NR formalizes the chosen ones.
- Keep architectural diagrams to Mermaid only. No external diagramming tools, no image generation.
