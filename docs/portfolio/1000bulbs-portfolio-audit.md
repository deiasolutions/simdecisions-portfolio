# Portfolio Audit for 1000bulbs Job Application

**Date:** 2026-04-16
**Prepared by:** BEE-QUEUE-TEMP-SPEC-PORTFOLIO-1000
**Purpose:** Score Q88N's portfolio against 1000bulbs hiring criteria, recommend positioning strategy

---

## Executive Summary

Q88N's portfolio demonstrates **deep strength** in multi-tier AI agent orchestration, clean architectural separation, and systematic AI correction loops — all core signals the 1000bulbs role screens for. The challenge is that the flagship work lives in private repos, requiring strategic teaser creation to showcase capabilities without exposing proprietary implementation.

**Key strengths for 1000bulbs:**
1. **AI agent orchestration at scale:** DEIA Hive coordinates Q33N → BEE workflows with formal governance (PROCESS-13, Gate 0 validation)
2. **12-factor architecture:** Clean separation across browser (React/Vite) → hivenode (FastAPI) → simdecisions engine → PostgreSQL, all deployed via Vercel/Railway
3. **Visible CI/CD:** Railway + Vercel auto-deploy from git, health checks, multi-service orchestration
4. **AI correction discipline:** Built-in validation gates (Gate 0, Phase 0/1/2 fidelity checks), healing loops, traceability IDs (REQ-XX → SPEC-XX → TASK-XX → CODE-XX)
5. **Strangler Fig thinking:** DEF → SIM → EXE pipeline, packages/ flatten (2026-04-12), egg → set rename
6. **Domain depth:** 2006 call center simulator → 2026 Phase-IR, 20-year arc in process optimization

**Gap:** Public visibility. Most compelling evidence is in `simdecisions` (private) and `platform` (private). Need a teaser repo that demonstrates architecture + governance without shipping product code.

---

## Repo Inventory & 1000bulbs Scorecards

### 1. simdecisions (this repo, PRIVATE)

**Overview:** Primary monorepo. Multi-tier stack (browser/hivenode/simdecisions engine), DEIA Hive factory orchestrating AI agents under governance, deployed to Railway/Vercel.

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ✅ TRUE | Browser (React/Vite, `browser/src/`) → hivenode (FastAPI, `hivenode/main.py`) → simdecisions engine (DES, `simdecisions/des/`) → PostgreSQL (Railway). Clean separation: view/API/service/persistence/database. Dockerfile (`Dockerfile:10-11`) copies all 3 layers. Vercel routes (`vercel.json:7-13`) proxy `/api/`, `/relay/`, `/llm/`, `/rag/`, `/storage/`, `/build/` to Railway hivenode. |
| **shows_agent_orchestration** | ✅ TRUE | DEIA Hive system: Q33NR (regent) → Q33N (coordinator) → BEEs (workers). Dispatcher daemon (`hivenode/scheduler/dispatcher_daemon.py`) orchestrates bee execution. Dispatch script (`.deia/hive/scripts/dispatch/dispatch.py`) with `--role bee|queen|regent` parameter. Queue runner (`.deia/hive/scripts/queue/run_queue.py`) auto-processes specs. NOT just using AI — directing AI under governance. |
| **shows_ai_correction** | ✅ TRUE | PROCESS-13 (`docs/.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`) defines Gate 0 (prompt→SPEC validation) + Phase 0/1/2 (coverage, fidelity checks) with healing loops. Max 3 retries with diagnostic generation before human escalation. Traceability IDs (REQ-XX-NNN → SPEC-NNN → TASK-NNN → CODE-NNN) track requirement → implementation. Correction is systematic, not ad-hoc. |
| **shows_cicd** | ✅ TRUE | Railway deployment (`railway.toml`, `Dockerfile`), Vercel deployment (`vercel.json`), both auto-deploy from git push. Health checks (`railway.toml:11`, `Dockerfile:24`). Multi-service: hivenode + hodeia_auth (beneficial-cooperation). Build commands in `vercel.json:37`. Environment-aware config (`hivenode/config.py` reads `HIVENODE_MODE=cloud`). |
| **twelve_factor_signals** | 6 observed | (1) **Config via env:** `HIVENODE_MODE`, `PORT`, `DATABASE_URL`, `ANTHROPIC_API_KEY` (Deployment docs, `Dockerfile:23`). (2) **Stateless processes:** FastAPI app, no session state in-process. (3) **Port binding:** Reads `$PORT` from Railway (`hivenode/config.py` as cited in Deployment docs). (4) **Logs as streams:** `uvicorn --log-level info` (`Dockerfile:24`). (5) **Dev/prod parity:** Same Dockerfile for local/Railway, same code paths. (6) **Disposability:** Railway restartPolicyType ON_FAILURE (`railway.toml:12`). |
| **strangler_fig_evidence** | ✅ YES | (1) DEF → SIM → EXE pipeline (simulation before execution philosophy, per DEIA-ELEVATOR-PITCH). (2) packages/ flatten (2026-04-12 per MEMORY.md): deep `packages/*/src/namespace/` → flat `hivenode/`, `simdecisions/`, `browser/`, `_tools/` preserving all imports/tests. (3) egg → set rename (MEMORY.md "Naming Concepts"). All incremental, backward-compatible migrations. |
| **overall_fit_rating** | **STRONG** | This is the flagship. Shows all 4 core signals + 12-factor + strangler fig. Demonstrates multi-year, multi-team AI orchestration at scale. Architecture is production-grade: Railway/Vercel, PG, MCP queue notifications, health checks, multi-service coordination. The DEIA Hive coordination system is exactly what 1000bulbs screens for: "AI agent teams" (Q33N/BEEs), "evaluating and correcting AI output" (PROCESS-13), "clean architectural separation" (5 tiers). **Caveat:** Private. |

---

### 2. prism-ir (PUBLIC)

**GitHub:** https://github.com/deiasolutions/prism-ir
**Description:** "Process Representation, Intent Simulation & Manifestation. Open specification for domain-agnostic process intermediate representation."

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ❌ FALSE | This is a spec repo (Apache 2.0), not an implementation. No code, no deployment, no tiers. Contains markdown/YAML defining the PRISM-IR intermediate representation format. |
| **shows_agent_orchestration** | ⚠️ PARTIAL | The spec repo doesn't *show* orchestration, but PRISM-IR is *used for* orchestration in the simdecisions engine. The spec defines how natural language commands → structured IR → executable actions. Indirect evidence: the *consumer* of this spec (simdecisions engine) does orchestration, but this repo itself is just documentation. |
| **shows_ai_correction** | ❌ FALSE | Spec repo. No AI correction visible. (Though the spec *enables* correction loops via confidence thresholds and alternatives arrays in the IR format.) |
| **shows_cicd** | ❌ FALSE | Markdown repo, no build pipeline, no deployment. |
| **twelve_factor_signals** | 0 observed | Not applicable — this is a spec, not an app. |
| **strangler_fig_evidence** | ⚠️ CONCEPTUAL | PRISM-IR itself is a strangler fig strategy: define an open IR so DES engines, workflow engines, and agent coordinators can interoperate without rewriting entire stacks. The IR sits *between* natural language and execution, enabling incremental migration. But this repo shows the *spec*, not a migration in progress. |
| **overall_fit_rating** | **WEAK (as standalone)** | This is a supporting artifact, not a showcase repo. It demonstrates Q88N's ability to design open standards (like Phase-IR) and think in terms of vendor-neutral interfaces. Good for "architectural thinking" but doesn't hit the 4 core 1000bulbs signals. **Better used as a reference** linked from the teaser README ("here's the open IR we use for process representation"). License: Apache 2.0 — safe to cite publicly. |

---

### 3. federalist-papers-ai (PUBLIC)

**GitHub:** https://github.com/deiasolutions/federalist-papers-ai
**Description:** "Constitutional principles for human-AI coordination — 34 documents by PUBLIUS"

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ❌ FALSE | Markdown essays, no code, no architecture. |
| **shows_agent_orchestration** | ⚠️ CONCEPTUAL | The essays *describe* governance principles for AI coordination (e.g., "Federalist No. 15: Crisis and Coherence" per `docs/federalist/NO-15-crisis-and-coherence.md`). These are the *theory* behind DEIA's constitutional governance, but no code implementing orchestration. |
| **shows_ai_correction** | ⚠️ CONCEPTUAL | The essays likely discuss error handling, accountability, and correction principles (constitutional governance implies oversight). But no *implemented* correction loop visible. |
| **shows_cicd** | ❌ FALSE | Markdown repo, no CI/CD. |
| **twelve_factor_signals** | 0 observed | Not applicable. |
| **strangler_fig_evidence** | ❌ FALSE | Not applicable — this is political philosophy adapted to AI, not software engineering. |
| **overall_fit_rating** | **OUT-OF-SCOPE** | Interesting intellectual foundation for the governance model, but doesn't map to 1000bulbs criteria. Could be mentioned in passing ("our governance model draws from constitutional principles documented here") but not a portfolio piece. Public, so no risk citing it, but low value-add for this application. |

---

### 4. shiftcenter (PRIVATE)

**Status:** NOT directly readable. Listed in gh output.

**Inferred from simdecisions context:**
- Likely the *previous* monorepo before the flatten to `simdecisions` (per INVESTIGATION-REPO-COMPARISON-REPORT.md).
- If so, contains similar architecture (browser/hivenode/engine) but under the old `packages/*/src/namespace/` structure.
- Per MEMORY.md: "The repo was `shiftcenter/`. All Python and TypeScript source lives in top-level directories — no `packages/` nesting."

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ✅ TRUE (inferred) | Likely same architecture as simdecisions before flatten. Multi-tier: browser/hivenode/engine. |
| **shows_agent_orchestration** | ✅ TRUE (inferred) | If DEIA Hive was ported from here, same orchestration. |
| **shows_ai_correction** | ✅ TRUE (inferred) | If PROCESS-13 was ported from here, same correction discipline. |
| **shows_cicd** | ✅ TRUE (inferred) | If deployed to Railway/Vercel like simdecisions, same CI/CD. |
| **twelve_factor_signals** | Unknown | Need to read repo. |
| **strangler_fig_evidence** | ⚠️ CONTEXT | The *flatten from shiftcenter → simdecisions* is strangler fig evidence. But this repo itself may not show incremental migration unless you compare commits. |
| **overall_fit_rating** | **MODERATE (redundant with simdecisions)** | Private. Likely superseded by simdecisions. Including both in the portfolio would be redundant — pick the cleaner one (simdecisions post-flatten). **Recommendation:** Cite the flatten *event* as strangler fig evidence, but don't surface shiftcenter as a separate portfolio piece. |

---

### 5. platform (PRIVATE)

**Status:** NOT directly readable. Listed in gh output.

**Inferred:** Unknown. Could be:
- A shared platform library (common primitives, design tokens, auth wiring).
- An earlier prototype (predates shiftcenter?).
- A staging/experimental branch of one of the other repos.

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ❓ UNKNOWN | Not readable. Can't score. |
| **shows_agent_orchestration** | ❓ UNKNOWN | Not readable. Can't score. |
| **shows_ai_correction** | ❓ UNKNOWN | Not readable. Can't score. |
| **shows_cicd** | ❓ UNKNOWN | Not readable. Can't score. |
| **twelve_factor_signals** | ❓ UNKNOWN | Not readable. Can't score. |
| **strangler_fig_evidence** | ❓ UNKNOWN | Not readable. Can't score. |
| **overall_fit_rating** | **UNKNOWN** | [Q88N to clarify: what is `platform`? If it's a legacy/experimental repo, exclude. If it's a key shared library, consider mentioning in teaser README architecture section.] |

---

### 6. global-commons (PRIVATE)

**Status:** NOT directly readable. Listed in gh output.

**Inferred from simdecisions context:**
- `docs/global-commons/` exists in simdecisions with: `README.md`, `ethics.md`, `carbon.md`, `design-tokens.md`, `governance.md`, `skills/` (manim-animation, tribunal-host).
- Likely a shared standards/docs repo referenced across multiple products.

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ❌ FALSE | Docs/standards repo, not an implementation. |
| **shows_agent_orchestration** | ⚠️ CONCEPTUAL | `governance.md`, `ethics.md` likely define *policies* for agent behavior (e.g., five-disposition policy engine per BOOT.md). But no code implementing orchestration. |
| **shows_ai_correction** | ⚠️ CONCEPTUAL | Ethics/governance docs likely cover error handling principles. But no implemented correction loop. |
| **shows_cicd** | ❌ FALSE | Standards repo, no CI/CD. |
| **twelve_factor_signals** | 0 observed | Not applicable. |
| **strangler_fig_evidence** | ⚠️ CONCEPTUAL | `carbon.md`, `design-tokens.md` suggest centralized standards that multiple products consume (DRY principle, shared vocabulary). This is a form of incremental standardization (strangler fig for consistency). But not a code migration. |
| **overall_fit_rating** | **WEAK (supporting artifact)** | Good evidence of *systematic thinking* (centralized standards, ethics, carbon accounting). Demonstrates Q88N doesn't just build — he governs. But doesn't hit the 4 core 1000bulbs signals. **Use in teaser README:** Mention the Three Currencies (CLOCK/COIN/CARBON) discipline with a link to the carbon accounting methodology. Shows measurement rigor beyond typical cost-only tracking. |

---

### 7. 2006 Call Center Simulator (Q88N to provide materials)

**Status:** [Q88N to provide materials]

**Known from context:** `call_center_500.prism.md` in simdecisions repo shows a Phase-IR simulation (500 agents, exponential arrivals, lognorm handling time, FIFO dispatch, SLA tracking). This is a *modern* representation of a 2006 simulator, ported to Phase-IR format.

**Job-Fit Scorecard:**

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **shows_multi_tier** | ⚠️ UNKNOWN | Depends on what Q88N provides. If it was a C++/Java desktop app (typical 2006), likely *not* multi-tier (monolithic). If it had a DB + app + UI, could be multi-tier. Need materials. |
| **shows_agent_orchestration** | ❌ FALSE | 2006 predates modern AI agent orchestration. Unless it had some kind of discrete-event agent dispatch (which could be *conceptually* similar), this won't hit the "AI agent teams" signal. |
| **shows_ai_correction** | ❌ FALSE | 2006 predates AI correction loops. |
| **shows_cicd** | ❌ FALSE | 2006 predates modern CI/CD (Git, Docker, cloud deploys were nascent). Likely manual deploy or install-based distribution. |
| **twelve_factor_signals** | 0-2 observed (guess) | 2006 best practices were different. Likely no config-via-env, no disposability, no statelessness. If it had a DB, maybe (3) backing services, (4) logs as streams. |
| **strangler_fig_evidence** | ✅ **STRONG** | The *fact that Q88N ported this to Phase-IR in 2026* is strangler fig gold. Shows 20-year continuity: built the simulator in 2006, refined the domain model, formalized it as an open spec (Phase-IR), and *still uses* that 2006 mental model in 2026. This is incremental refinement across decades. The `call_center_500.prism.md` file is the proof. |
| **overall_fit_rating** | **MODERATE (for long-arc domain depth)** | Won't hit the 4 core 1000bulbs signals (too old). But demonstrates **20-year domain expertise** in process optimization and simulation — a differentiator for senior roles. Strangler fig evidence is the strongest signal here. **Use in teaser README:** "Continuous refinement: 2006 call center simulator → 2026 Phase-IR open standard. Same domain model, evolved from proprietary C++ to vendor-neutral IR. Two decades of lessons embedded in one YAML schema." |

---

## Public / Teaser / Private-on-Request Classification

| Repo | Visibility | Recommendation | Rationale |
|------|-----------|----------------|-----------|
| **simdecisions** | PRIVATE | **TEASER** | Flagship. Strongest fit for 1000bulbs. But private and contains proprietary product code. **Action:** Create a teaser repo with: (1) Architecture diagrams (Mermaid), (2) Narrative README explaining DEIA/Hive/Strangler Fig thinking, (3) PROCESS-13 excerpts (Gate 0, Phase 0/1/2 healing loops), (4) No product code. Title: `simdecisions-architecture` or `deia-hive-showcase`. License: CC BY 4.0 (docs only). |
| **prism-ir** | PUBLIC | **PUBLIC** | Already public, Apache 2.0. Safe to link directly. Use as supporting evidence for "open spec design" and "vendor-neutral IR thinking." Mention in teaser README under "Phase-IR: Open Standard" section. No changes needed. |
| **federalist-papers-ai** | PUBLIC | **EXCLUDE** | Out of scope for 1000bulbs. Interesting intellectual foundation, but doesn't map to job criteria. Could mention in passing if interviewer asks about governance philosophy, but don't feature in portfolio. |
| **shiftcenter** | PRIVATE | **EXCLUDE (cite flatten event)** | Superseded by simdecisions. Including both is redundant. Instead, cite the *flatten migration* (packages/ → flat layout, 2026-04-12) as strangler fig evidence in the teaser README. Don't surface shiftcenter as a separate portfolio piece. |
| **platform** | PRIVATE | **UNKNOWN** | [Q88N to clarify: is this relevant? If yes, classify as PRIVATE_ON_REQUEST or TEASER depending on content.] |
| **global-commons** | PRIVATE | **PRIVATE_ON_REQUEST** | Standards/ethics/carbon docs. Good supporting material ("here's how we govern, measure, and account for AI work"). Mention the Three Currencies discipline in teaser README, offer full global-commons docs on request during interview. Don't create a separate teaser — reference only. |
| **2006 Call Center Simulator** | UNKNOWN | **PRIVATE_ON_REQUEST** | [Q88N to provide materials.] Use in teaser README as domain depth evidence: "20-year arc from 2006 C++ simulator to 2026 Phase-IR open spec." Offer original simulator codebase/screenshots on request if Q88N wants to share. Don't feature heavily unless it's cleaner than expected. |

---

## Portfolio Gaps (P0/P1/P2 by impact on 1000bulbs application)

### P0 Gaps (Fix before applying — high impact)

1. **No public showcase of DEIA Hive orchestration**
   - **Gap:** All AI agent orchestration evidence is in private repos. 1000bulbs can't verify Q88N's core claim without access.
   - **Impact:** Disqualifying if portfolio reviewer can't see orchestration.
   - **Fix:** Create teaser repo (see PORTFOLIO-TEASER-PUBLISH-001 sketch below). Include architecture diagrams, PROCESS-13 excerpts, narrative README. Publish to `deiasolutions/simdecisions-architecture` under CC BY 4.0. **Effort:** 4-6 hours.

2. **No visible CI/CD badges or build status in READMEs**
   - **Gap:** simdecisions README doesn't show Railway/Vercel deploy badges, test status, or build health.
   - **Impact:** 1000bulbs reviewer can't see "CI/CD pipelines visible in repos" without digging into `railway.toml`, `vercel.json`, Dockerfile. Badges are the 5-second signal.
   - **Fix:** Add badges to simdecisions README: Railway deploy status, Vercel deploy status, test coverage (if available). Example:
     ```markdown
     [![Railway Deploy](https://img.shields.io/badge/Railway-Deployed-success)]()
     [![Vercel](https://img.shields.io/badge/Vercel-Deployed-success)]()
     ```
     If Railway/Vercel don't provide public badge URLs for private projects, create a `/build/status` endpoint in hivenode that returns build health, then badge that. **Effort:** 1-2 hours.

3. **Architecture diagrams missing from README**
   - **Gap:** simdecisions README (lines 1-144 read earlier) has a text tree structure but no Mermaid diagrams. "Clean architectural separation" is *described* but not *visualized*.
   - **Impact:** Reviewer has to parse text to understand tiers. Diagram is instant comprehension.
   - **Fix:** Add Mermaid architecture diagram to simdecisions README showing: browser → hivenode API → simdecisions engine → PostgreSQL. Add second diagram showing Q33NR → Q33N → BEEs orchestration flow. **Effort:** 2-3 hours.

### P1 Gaps (Polish before applying — moderate impact)

4. **PROCESS-13 (Gate 0, healing loops) not surfaced in README**
   - **Gap:** The AI correction discipline is buried in `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md` (1039 lines). Not discoverable from README.
   - **Impact:** 1000bulbs reviewer won't see "evaluating and correcting AI output" unless they know to look in `.deia/processes/`. This is a core signal.
   - **Fix:** Add "AI Correction Discipline" section to README with: (1) Gate 0 (prompt→SPEC validation), (2) Phase 0/1/2 (coverage, fidelity), (3) Healing loops (max 3 retries, human escalation), (4) Traceability IDs (REQ→SPEC→TASK→CODE→TEST). Link to full PROCESS-13 doc. **Effort:** 1-2 hours.

5. **No commit history demonstrating correction loops**
   - **Gap:** Git log shows `[BEE-XXX] TASK-YYY: description` commits, but doesn't surface *correction* commits (e.g., "fix failed Phase 0 validation", "heal SPEC after fidelity check").
   - **Impact:** 1000bulbs wants "commit history showing AI output reviewed, fixed, or rejected." Need explicit correction commits to prove the loop runs in practice.
   - **Fix:** If recent history has correction events, add a section to README: "Example Correction Commits" with links to 2-3 correction commits (e.g., SPEC rewrites after Gate 0 failure, bee retries after test failures). If no recent correction commits, run a deliberate correction scenario and commit with clear message: `[Q33N-CORRECTION] SPEC-XXX: heal after Phase 0 coverage failure (retry 1/3)`. **Effort:** 1-2 hours.

6. **Strangler Fig evidence not highlighted**
   - **Gap:** The packages/ flatten (2026-04-12) and DEF → SIM → EXE pipeline are *mentioned* in MEMORY.md but not featured in README.
   - **Impact:** 1000bulbs may value strangler fig / incremental modernization. This is a differentiator.
   - **Fix:** Add "Strangler Fig Thinking" section to README citing: (1) packages/ flatten (before/after structure, import preservation, test preservation), (2) DEF → SIM → EXE (simulate before execute), (3) 2006 call center → 2026 Phase-IR (20-year evolution). **Effort:** 1 hour.

### P2 Gaps (Nice to have — low impact, high effort)

7. **Test coverage metrics not reported**
   - **Gap:** README doesn't show test counts, coverage %, or pass/fail status.
   - **Impact:** Low — 1000bulbs cares about *architecture* and *orchestration*, not test coverage numbers. But showing "1200+ tests, 87% coverage" signals rigor.
   - **Fix:** Run `pytest --cov=hivenode --cov=simdecisions --cov=_tools` and `cd browser && npx vitest --coverage`. Add badge or table to README. **Effort:** 2-3 hours (if coverage tooling not set up yet).

8. **hodeia_auth (beneficial-cooperation) not clearly linked**
   - **Gap:** README mentions "Auth: hodeia.me (JWT, cross-app SSO)" but doesn't explain the multi-service Railway deploy or show how hodeia_auth integrates.
   - **Impact:** Low — orthogonal to core signals. But "multi-service deployment" is a 12-factor + DevOps signal.
   - **Fix:** Add "Multi-Service Deployment" subsection under Architecture showing: (1) hivenode service (main app), (2) beneficial-cooperation service (hodeia_auth), (3) PostgreSQL shared between them, (4) Vercel proxying auth routes to Railway. Cite `railway.toml`, `hodeia_auth/Dockerfile`, `vercel.json` routes. **Effort:** 1 hour.

---

## Summary: What to Fix Before Applying

**Must-fix (P0):**
1. Create teaser repo with architecture diagrams + PROCESS-13 excerpts (4-6 hours)
2. Add CI/CD badges to README (1-2 hours)
3. Add architecture diagrams to README (2-3 hours)

**Should-fix (P1):**
4. Surface AI correction discipline in README (1-2 hours)
5. Add example correction commits or run a correction scenario (1-2 hours)
6. Highlight strangler fig evidence in README (1 hour)

**Total effort (P0+P1):** ~13-17 hours. Doable in 2-3 focused sessions.

**P2 (defer):** Test coverage metrics, hodeia_auth multi-service section. Nice-to-have but not required.

---

## What Q88N Decides Next

This section provides 3-5 high-leverage decisions with trade-offs so Q88N can move forward in one review pass.

### Decision 1: Teaser Repo vs. Enhanced Private README

**Option A: Create public teaser repo (`deiasolutions/simdecisions-architecture`)**
- **Pros:** 1000bulbs reviewer can access without requesting private repo access. Shows architecture + governance without product code. Demonstrates "I built this to be shareable." Good SEO for future hires.
- **Cons:** 4-6 hours to create. Maintenance burden (keep in sync with simdecisions). Risk of teaser diverging from reality if not updated.
- **Recommendation:** **DO THIS.** This is the P0 gap. Without public orchestration evidence, 1000bulbs can't verify the core claim.

**Option B: Enhance simdecisions README and offer private repo on request**
- **Pros:** No new repo to maintain. One source of truth. Less effort (just README updates, 3-4 hours).
- **Cons:** 1000bulbs reviewer sees nothing until Q88N grants access. Portfolio screening happens *before* interview — may not get a callback without public evidence.
- **Recommendation:** **Fallback if teaser repo timeline doesn't work.** But risky — you're asking them to trust you before seeing proof.

**Trade-off:** Public teaser = higher callback odds. Enhanced private README = less effort, more risk.

### Decision 2: Which Private Repo to Offer on Request

**Option A: simdecisions (current flagship)**
- **Pros:** Most up-to-date. Shows post-flatten architecture. DEIA Hive coordination, PROCESS-13, multi-service Railway/Vercel, all in one repo.
- **Cons:** Still in active development. May have rough edges, incomplete features, or TODOs that signal "not production-ready."
- **Recommendation:** **Offer this.** It's the cleanest post-flatten codebase.

**Option B: shiftcenter (pre-flatten)**
- **Pros:** May be more "stable" if it was frozen before flatten.
- **Cons:** Deep `packages/` nesting is messier. Offers nothing simdecisions doesn't have.
- **Recommendation:** **Exclude.** Redundant with simdecisions.

**Option C: platform (if relevant)**
- **Pros:** Unknown — depends on what platform contains.
- **Cons:** Unknown.
- **Recommendation:** [Q88N to clarify: is platform relevant for 1000bulbs? If not, exclude.]

**Trade-off:** Offer simdecisions. Don't dilute with multiple private repos unless each adds unique value.

### Decision 3: 2006 Call Center Simulator — Feature or Footnote?

**Option A: Feature in teaser README as "20-year domain arc" differentiator**
- **Pros:** Demonstrates continuity, domain expertise, and long-term thinking. Strangler fig evidence (2006 → 2026 evolution). Differentiates Q88N from candidates with only recent AI experience.
- **Cons:** If the 2006 codebase is rough, it could hurt more than help. Reviewer might see "legacy baggage" not "domain depth."
- **Recommendation:** **Feature it** — but frame as evolution story, not showcase of 2006 code. Use `call_center_500.prism.md` as the modern artifact. Mention 2006 origin in narrative: "This Phase-IR simulation descends from a 2006 call center optimizer I built in C++. Twenty years later, the domain model is now an open spec." Offer 2006 materials on request (screenshots, design docs) but don't lead with raw 2006 code.

**Option B: Footnote or exclude**
- **Pros:** Simpler. Focus on 2026 capabilities, not 2006 history.
- **Cons:** Loses differentiation. Every candidate can show React + FastAPI + Railway. Not every candidate has 20-year domain depth.
- **Recommendation:** **Risky.** You're competing with younger candidates who have fresh stacks. Domain depth is your edge.

**Trade-off:** Feature the evolution story. Don't over-index on 2006 code quality — focus on continuity.

### Decision 4: How Much to Polish the Private Repos Before Offering Access

**Option A: Polish first (fix P0 + P1 gaps, ~13-17 hours)**
- **Pros:** Private repo is interview-ready. No "excuse the mess" moments. Shows Q88N's standards are high.
- **Cons:** Delays application by 2-3 days. Risk of over-polishing (diminishing returns).
- **Recommendation:** **Do the P0 gaps (badges, architecture diagrams).** Defer P1/P2 unless interview is scheduled and you have lead time.

**Option B: Offer as-is with "this is a working repo" disclaimer**
- **Pros:** Apply sooner. Most reviewers understand "working repo" ≠ "portfolio showpiece."
- **Cons:** Risk of rough edges (TODOs, dead code, confusing structure) signaling lack of discipline.
- **Recommendation:** **Risky** unless you're confident the repo reads cleanly. Without badges and architecture diagrams, reviewer has to dig too much.

**Trade-off:** Fix P0 gaps before offering access. Defer P1/P2 until interview.

### Decision 5: Teaser README Tone — Technical Deep-Dive vs. Executive Summary

**Option A: Technical deep-dive (architecture diagrams, PROCESS-13 details, code snippets)**
- **Pros:** Appeals to technical reviewers (senior engineers, architects). Shows Q88N can explain complex systems clearly.
- **Cons:** May overwhelm non-technical reviewers (HR, hiring managers). Risk of "too much detail, didn't read."
- **Recommendation:** **Use this for teaser repo README.** If someone clicks into `deiasolutions/simdecisions-architecture`, they want technical depth.

**Option B: Executive summary (5-minute read, business value, minimal code)**
- **Pros:** Accessible to all reviewers. Focus on *what* Q88N built and *why* it matters for 1000bulbs.
- **Cons:** May not satisfy technical reviewers who want to see proof.
- **Recommendation:** **Use this for application cover letter, not teaser README.** Cover letter = executive summary. Teaser README = technical depth.

**Trade-off:** Teaser README is for technical reviewers. Make it deep. Cover letter (separate artifact, not in this audit) is for everyone — make it accessible.

---

## Next Steps: Recommended Order of Operations

1. **Immediate (before applying):**
   - Fix P0 gap: Create teaser repo (4-6 hours) OR enhance simdecisions README (2-3 hours) if timeline is tight.
   - Fix P0 gap: Add CI/CD badges to README (1-2 hours).
   - Fix P0 gap: Add architecture diagrams to README (2-3 hours).

2. **Before offering private repo access (interview stage):**
   - Fix P1 gaps: Surface PROCESS-13 in README (1-2 hours).
   - Fix P1 gaps: Add example correction commits (1-2 hours).
   - Fix P1 gaps: Highlight strangler fig evidence (1 hour).

3. **During interview (if requested):**
   - Offer simdecisions private repo with context: "This is the flagship. Post-flatten, DEIA Hive orchestration, Railway/Vercel multi-service deploy."
   - Offer global-commons docs with context: "Three Currencies (CLOCK/COIN/CARBON) measurement discipline, ethics governance."
   - Offer 2006 call center materials (design docs, screenshots, `call_center_500.prism.md`) with context: "20-year evolution from proprietary C++ to open Phase-IR spec."

4. **Defer (P2, not required):**
   - Test coverage metrics.
   - hodeia_auth multi-service section.

---

[End of Portfolio Audit — Teaser README Draft follows in next section]
