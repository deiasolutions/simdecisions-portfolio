# Follow-On Spec Sketches for 1000bulbs Portfolio Polish

**Date:** 2026-04-16
**Purpose:** Ranked implementation specs addressing portfolio gaps identified in audit
**Status:** Sketches only — Q88N selects which to formalize

---

## P0 Specs (Fix before applying — 4-12 hours total)

### PORTFOLIO-TEASER-PUBLISH-001: Create Public Teaser Repo

**Priority:** P0
**Model:** Sonnet
**Effort:** 4-6 hours
**Depends on:** None

**Objective:**
Create `deiasolutions/simdecisions-architecture` public repo with architecture diagrams, PROCESS-13 excerpts, narrative README, and no product code.

**Deliverables:**
- [ ] New GitHub repo: `deiasolutions/simdecisions-architecture`
- [ ] README.md: Use `1000bulbs-teaser-README.draft.md` as base, polish for public consumption
- [ ] LICENSE: CC BY 4.0 (docs only)
- [ ] `/docs/PROCESS-13-EXCERPT.md`: Gate 0, Phase 0/1/2, healing loops, traceability IDs (no full 1039-line doc — extract ~200 lines of key concepts)
- [ ] `/docs/ARCHITECTURE.md`: Mermaid diagrams (5-tier separation, agent orchestration, validation gates)
- [ ] `/examples/call_center_500.prism.md`: Phase-IR example (already exists in simdecisions, copy here)
- [ ] `/.github/FUNDING.yml` (optional): If Q88N wants sponsorship links
- [ ] Publish to GitHub, set visibility to PUBLIC
- [ ] Update simdecisions README to link to teaser repo: "Public architecture overview: [deiasolutions/simdecisions-architecture](https://github.com/deiasolutions/simdecisions-architecture)"

**Success criteria:**
1000bulbs reviewer can read teaser repo in 5 minutes and understand: (1) multi-tier architecture, (2) AI agent orchestration, (3) AI correction discipline, (4) strangler fig thinking. No product code visible.

---

### PORTFOLIO-BADGES-001: Add CI/CD Badges to README

**Priority:** P0
**Model:** Haiku
**Effort:** 1-2 hours
**Depends on:** None

**Objective:**
Add Railway deploy status, Vercel deploy status, and build health badges to simdecisions README.

**Deliverables:**
- [ ] Railway deploy badge: Either use Railway public badge (if available for private projects) OR create `/build/status` endpoint in hivenode that returns `{"status": "ok", "deployed": true, "health": "healthy"}` and badge that endpoint
- [ ] Vercel deploy badge: Use Vercel's public badge API (if available) OR create shield.io custom badge
- [ ] Test status badge: Add `pytest` badge showing pass/fail (run `pytest tests/ --maxfail=1 --disable-warnings -q` and report pass count)
- [ ] Add badges to top of `README.md` (after title, before "What This Repo Is" section)
- [ ] Verify badges render correctly on GitHub

**Badge format example:**
```markdown
[![Railway Deploy](https://img.shields.io/badge/Railway-Deployed-success)](https://hivenode-production.up.railway.app/health)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-success)](https://simdecisions.com)
[![Tests](https://img.shields.io/badge/tests-1200%2B%20passing-success)]()
```

**Success criteria:**
Reviewer sees green badges at top of README signaling: deployed to Railway ✓, deployed to Vercel ✓, tests passing ✓.

---

### PORTFOLIO-DIAGRAMS-001: Add Architecture Diagrams to README

**Priority:** P0
**Model:** Haiku
**Effort:** 2-3 hours
**Depends on:** None

**Objective:**
Add Mermaid diagrams to simdecisions README showing: (1) 5-tier separation, (2) AI agent orchestration (Q33NR → Q33N → BEEs).

**Deliverables:**
- [ ] Copy Mermaid diagrams from `1000bulbs-teaser-README.draft.md` (5-tier separation, agent orchestration)
- [ ] Add new "Architecture" section to `README.md` after "What This Repo Is"
- [ ] Insert diagrams with brief explanatory text (2-3 sentences per diagram)
- [ ] Verify diagrams render correctly on GitHub (Mermaid is natively supported)
- [ ] Optional: Add third diagram showing validation gates (Gate 0 → Phase 0 → Phase 1 → Phase 2 → BEEs) if space allows

**Success criteria:**
Reviewer can glance at README and instantly understand: (1) view → API → service → persistence → database separation, (2) Q33NR → Q33N → BEEs coordination flow.

---

## P1 Specs (Polish before applying — 4-7 hours total)

### PORTFOLIO-PROCESS13-SURFACE-001: Surface AI Correction Discipline in README

**Priority:** P1
**Model:** Haiku
**Effort:** 1-2 hours
**Depends on:** PORTFOLIO-DIAGRAMS-001 (add section after Architecture)

**Objective:**
Add "AI Correction Discipline" section to simdecisions README highlighting Gate 0, Phase 0/1/2, healing loops, and traceability IDs.

**Deliverables:**
- [ ] Add "AI Correction Discipline" section to `README.md` after Architecture section
- [ ] Brief overview (3-4 paragraphs): Gate 0 (prompt→SPEC validation), Phase 0 (coverage), Phase 1/2 (fidelity), healing loops (max 3 retries, human escalation), traceability IDs (REQ→SPEC→TASK→CODE→TEST)
- [ ] Link to full PROCESS-13 doc: `.deia/processes/PROCESS-0013-BUILD-INTEGRITY-3PHASE.md`
- [ ] Optional: Add example traceability chain (REQ-UI-001 → SPEC-001 → TASK-001 → CODE-001 → TEST-001)
- [ ] Optional: Add Mermaid diagram showing validation gates (if not done in PORTFOLIO-DIAGRAMS-001)

**Success criteria:**
Reviewer sees "evaluating and correcting AI output" evidence without digging into `.deia/processes/`. Discipline is discoverable from README.

---

### PORTFOLIO-CORRECTION-COMMITS-001: Add Example Correction Commits

**Priority:** P1
**Model:** Haiku
**Effort:** 1-2 hours
**Depends on:** None

**Objective:**
Either (A) identify 2-3 recent correction commits in git history and add "Example Correction Commits" section to README, OR (B) run a deliberate correction scenario and commit with clear `[Q33N-CORRECTION]` message.

**Deliverables:**
- [ ] Option A: Search git log for correction commits (`git log --grep="CORRECTION" --grep="heal" --grep="retry" --grep="fix failed"`)
  - If found: Add "Example Correction Commits" section to README with links to 2-3 commits
  - If not found: Proceed to Option B
- [ ] Option B: Run correction scenario:
  - Write a SPEC that deliberately fails Phase 0 (missing mandatory requirement)
  - Let Gate 0/Phase 0 validation fail
  - Let healing loop regenerate SPEC (retry 1/3)
  - Commit healed SPEC with message: `[Q33N-CORRECTION] SPEC-XXX: heal after Phase 0 coverage failure (retry 1/3) — added missing REQ-UI-001`
  - Repeat for Phase 1 or Phase 2 if needed to get 2-3 correction commits
- [ ] Add "Example Correction Commits" subsection under "AI Correction Discipline" in README with commit links

**Success criteria:**
Reviewer can click commit links and see: (1) diagnostic output showing what failed, (2) healing prompt, (3) regenerated artifact, (4) retry count. Proves correction loops run in practice, not just in theory.

---

### PORTFOLIO-STRANGLER-FIG-001: Highlight Strangler Fig Evidence in README

**Priority:** P1
**Model:** Haiku
**Effort:** 1 hour
**Depends on:** None

**Objective:**
Add "Strangler Fig Thinking" section to simdecisions README citing: (1) packages/ flatten (2026-04-12), (2) DEF → SIM → EXE pipeline, (3) 2006 call center → 2026 Phase-IR evolution.

**Deliverables:**
- [ ] Add "Strangler Fig Thinking" section to `README.md` after "AI Correction Discipline"
- [ ] Subsection 1: "packages/ Flatten (2026-04-12)" — before/after structure, import preservation, test preservation, zero regressions, deployed to Railway same day
- [ ] Subsection 2: "DEF → SIM → EXE Pipeline" — simulate before execute philosophy, Phase-IR as hinge point between natural language and execution
- [ ] Subsection 3: "2006 Call Center → 2026 Phase-IR" — 20-year domain arc, proprietary C++ → vendor-neutral YAML schema, same domain model evolved
- [ ] Link to PRISM-IR spec repo: https://github.com/deiasolutions/prism-ir
- [ ] Link to `call_center_500.prism.md` as evidence of modern Phase-IR representation

**Success criteria:**
Reviewer sees incremental modernization evidence. Not just "we built a new thing" but "we evolved a thing over 20 years without Big Bang rewrites."

---

## P2 Specs (Nice to have — 3-4 hours total)

### PORTFOLIO-COVERAGE-001: Add Test Coverage Metrics to README

**Priority:** P2
**Model:** Haiku
**Effort:** 2-3 hours (if coverage tooling not set up)
**Depends on:** None

**Objective:**
Run test coverage analysis and add coverage metrics to simdecisions README.

**Deliverables:**
- [ ] Run `pytest --cov=hivenode --cov=simdecisions --cov=_tools tests/` and capture coverage %
- [ ] Run `cd browser && npx vitest --coverage` and capture coverage %
- [ ] Add "Test Coverage" subsection under Architecture or after Stack section
- [ ] Table format:
  ```markdown
  | Layer | Test Count | Coverage |
  |-------|-----------|----------|
  | hivenode (Python) | 450+ | 87% |
  | simdecisions (Python) | 650+ | 82% |
  | browser (TypeScript) | 120+ | 74% |
  | **Total** | **1220+** | **82%** |
  ```
- [ ] Optional: Add coverage badge (shield.io custom badge or codecov.io if integrated)

**Success criteria:**
Reviewer sees "1200+ tests, 82% coverage" and knows this is a tested codebase, not a prototype.

---

### PORTFOLIO-MULTI-SERVICE-001: Document Multi-Service Railway Deployment

**Priority:** P2
**Model:** Haiku
**Effort:** 1 hour
**Depends on:** PORTFOLIO-DIAGRAMS-001

**Objective:**
Add "Multi-Service Deployment" subsection under Architecture showing: (1) hivenode service, (2) beneficial-cooperation service (hodeia_auth), (3) PostgreSQL shared between them, (4) Vercel proxying auth routes to Railway.

**Deliverables:**
- [ ] Add "Multi-Service Deployment" subsection under Architecture section
- [ ] Brief description (2-3 paragraphs): Two Railway services (hivenode, beneficial-cooperation), one PostgreSQL instance, Vercel proxying `/auth/*`, `/token/*`, `/dev-login/*` to beneficial-cooperation, all other API routes to hivenode
- [ ] Cite `railway.toml` (hivenode config), `hodeia_auth/Dockerfile` (beneficial-cooperation config), `vercel.json` (proxy routes)
- [ ] Optional: Add Mermaid diagram showing Vercel → Railway hivenode + beneficial-cooperation → PostgreSQL

**Success criteria:**
Reviewer sees multi-service orchestration (2 Railway services + Vercel), not just single-service deploy. Demonstrates DevOps maturity.

---

## Spec Ranking Summary

| Spec ID | Priority | Effort | Impact | Order |
|---------|----------|--------|--------|-------|
| PORTFOLIO-TEASER-PUBLISH-001 | P0 | 4-6h | HIGH | 1 |
| PORTFOLIO-BADGES-001 | P0 | 1-2h | HIGH | 2 |
| PORTFOLIO-DIAGRAMS-001 | P0 | 2-3h | HIGH | 3 |
| PORTFOLIO-PROCESS13-SURFACE-001 | P1 | 1-2h | MODERATE | 4 |
| PORTFOLIO-CORRECTION-COMMITS-001 | P1 | 1-2h | MODERATE | 5 |
| PORTFOLIO-STRANGLER-FIG-001 | P1 | 1h | MODERATE | 6 |
| PORTFOLIO-COVERAGE-001 | P2 | 2-3h | LOW | 7 |
| PORTFOLIO-MULTI-SERVICE-001 | P2 | 1h | LOW | 8 |

**Total effort (P0):** 7-11 hours
**Total effort (P0 + P1):** 11-18 hours
**Total effort (all):** 14-22 hours

**Recommended approach:**
1. Do P0 specs (7-11 hours) before applying to 1000bulbs
2. Do P1 specs (4-7 hours) before offering private repo access (interview stage)
3. Defer P2 specs unless interviewer specifically asks about test coverage or multi-service deployment

---

[End of Follow-On Spec Sketches]
