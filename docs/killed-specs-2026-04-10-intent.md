# Killed Specs — Intent Preservation (2026-04-10)

**Purpose:** On 2026-04-10, during escalation chain cleanup (ESC-001 forensic survey), 7 spec families were determined to be structurally unrecoverable (phantom specs, Gate 0 failures from birth, `(NEEDS_DAVE)` markers, or ironically self-escalated). Q88N approved killing all 7.

This document preserves the **intent** of each killed spec so the underlying ideas are not lost. If any of these remain desirable, a clean new spec can be written from scratch referencing this record — do NOT attempt to resurrect the polluted originals.

**Related records:**
- Survey response: `.deia/hive/responses/20260410-ESC-001-RESPONSE.md`
- Cleanup briefing: `.deia/hive/coordination/2026-04-10-BRIEFING-ESCALATION-CLEANUP.md`
- Canonical decision: `shiftcenter/.deia/hive/coordination/2026-04-10-DECISION-SIMDECISIONS-CANONICAL.md`

---

## 1. SPEC-BL-146 — Bot Activity + Bot Settings UI

**Kill reason:** No clean original found in shiftcenter git history. File appeared already escalated at first observation (`bc17fb9`). Escalation chain 2 levels deep.

### Original Objective
Port the bot token system and bot mutation API from `platform/simdecisions-2` to the shiftcenter/simdecisions platform. Give users a way to create named bot tokens, let those bots mutate efemera state via a restricted API, and surface bot activity in a settings UI.

### Key Technical Details Worth Preserving
- **Backend files:**
  - `hivenode/efemera/bot_store.py` — bot token CRUD, SHA-256 hashing
  - `hivenode/efemera/bot_routes.py` — mutation endpoints with rate limiting
  - `hivenode/efemera/keeper.py` — keeper chat integration
- **Database tables:**
  - `sd_bot_tokens` — id, user_id, name, token_hash, active (bool), created_at, revoked_at
  - `sd_bot_mutations` — id, bot_id, operation, payload, created_at
- **Behavior constraints:**
  - One active bot per user
  - SHA-256 hash of token (plaintext never stored)
  - Rate limit: 60 mutations/hour per bot
- **Source reference:** `platform/simdecisions-2` (existing implementation to port from)

### Rewrite Guidance
A fresh SPEC-BL-146 should have path validation for platform sources, explicit `sd_` table prefixes, and a concrete migration script. Reference the existing `platform/simdecisions-2` implementation before writing.

---

## 2. SPEC-FLAPPY-100 — Self-Learning Flappy Bird v2

**Kill reason:** Marked `(NEEDS_DAVE)` from first commit (`99428a6`). Multiple fix attempts at `5b19942` and `9853b7b` all failed. Ambiguous viability.

### Original Objective
Coordinate a NEAT (NeuroEvolution of Augmenting Topologies) implementation of Flappy Bird — a self-learning AI where 50+ birds train simultaneously, the neural network is visualizable in real time, and evolutionary progress is observable across generations.

### Key Technical Details Worth Preserving
- **Target file:** `browser/public/games/flappy-bird-ai-v2-20260407.html` (single HTML file, no build step)
- **Rendering:** Canvas API only, vanilla JS, no frameworks
- **Simulation scale:** 50+ birds learning concurrently per generation
- **Generation evolution:** Visible improvement curve 1→10→50 generations
- **Neural network visualization:** Live rendering of network topology and activations per bird
- **Controls:** PC + mobile responsive
- **Algorithm:** NEAT (NeuroEvolution of Augmenting Topologies) — species, fitness, crossover, mutation of both weights and topology

### Why (NEEDS_DAVE)
The original spec lacked concrete hyperparameters (population size, mutation rates, species compatibility threshold, elitism count) and input/output layer definitions. Requires human design input before bee dispatch.

### Rewrite Guidance
A fresh spec should pin: input neurons (bird y, velocity, next pipe gap center, next pipe distance), output neurons (jump/no-jump), hidden layer starting topology, mutation rates for add-node/add-connection/weight-jiggle, species compatibility formula, and target fitness curve.

---

## 3. SPEC-MW-VERIFY-001 — Mobile Workdesk Full Build Verification

**Kill reason:** No clean original in shiftcenter git. Escalated at `dd2eedf` already. Rejection chain 13 levels deep. Ambiguous origin.

### Original Objective
Audit the Mobile Workdesk build — verify all 66 `SPEC-MW-*` specs marked `_done/` actually produced working code, and identify any gaps between planned scope and shipped reality.

### Key Technical Details Worth Preserving
- **Reference document:** `C:/Users/davee/Downloads/SPEC-MOBILE-WORKDESK-001.md` (42 tasks)
- **8 new primitives to verify:**
  1. `command-interpreter` — natural language command parsing
  2. `voice-input` — speech-to-text integration
  3. `quick-actions` (FAB) — floating action button with context menu
  4. `conversation-pane` — chat-style dialog pane
  5. `mobile-nav` — bottom nav bar
  6. `notification-pane` — toast/inline notification system
  7. `queue-pane` — task queue viewer
  8. `diff-viewer` — side-by-side or inline diff primitive
- **11 existing primitives to check for mobile CSS:**
  - (not enumerated in the polluted spec — would need re-derivation from existing primitive list)
- **Status categories per item:**
  - `SHIPPED` — in `_done/`, code exists, passes smoke test
  - `STUB` — file exists but no real implementation
  - `PLAN ONLY` — spec only, no code
  - `MISSING` — neither spec nor code

### Rewrite Guidance
A fresh audit spec should enumerate all 66 `SPEC-MW-*` files by name, produce a CSV/markdown matrix (SpecID × Status), and include smoke-test commands per primitive. Should be a read-only research task (no code changes).

---

## 4. SPEC-TRIAGE-ESCALATED-001 — Evaluate Escalated Queue Items

**Kill reason:** Ironically self-escalated. Created to triage the escalated queue, then itself got caught in the triage daemon's recursive loop. Superseded by ESC-001/ESC-002 cleanup work. Rejection chain 13 levels deep.

### Original Objective
Evaluate every spec in `_escalated/`, produce a triage report per spec with a disposition (KILL / REWRITE / REQUEUE / HOLD), and output a consolidated decision record for Q88N review.

### Key Technical Details Worth Preserving
- **Dispositions:**
  - `KILL` — spec is obsolete, malformed, or superseded
  - `REWRITE` — intent is valid but spec needs restructuring
  - `REQUEUE` — spec is clean and should return to backlog
  - `HOLD` — needs human decision (Q88N)
- **Budget:** 15 min research-only, no file writes in queue directories
- **Output target:** `.deia/hive/responses/20260409-TRIAGE-ESCALATED-001-RESPONSE.md`
- **Original scope:** 8 escalated specs listed (the pre-cleanup backlog)

### Why Superseded
ESC-001 (escalation survey) and ESC-002 (escalation restore) executed the same triage work with better forensic depth (cross-repo git archaeology, 15 spec families, disposition table with evidence column). The TRIAGE-ESCALATED-001 concept is fulfilled by ESC-001's response.

### Rewrite Guidance
Do not rewrite. The ESC-00N series is the canonical triage process going forward. If a future escalation loop occurs, run ESC-001 again (read-only survey + disposition table).

---

## 5. SPEC-WIKI-V1.1 — LLM Wiki Pattern Integration ⭐

**Kill reason:** First commit `8064d76` shows the spec was already polluted (1 prepended `## Clean Retry` block) AND failed Gate 0 (missing Priority, missing acceptance criteria). Structurally broken from birth. **However, the intellectual content is substantial and worth preserving.**

### Original Objective
Amend SPEC-WIKI-V1 with the Karpathy LLM Wiki pattern (April 2026) — treat the wiki as a compounding artifact where an LLM curates knowledge via strict architectural rules, with a first application building the tool taxonomy for the AI Solutions Architecture practice.

### Core Insight (from Karpathy, April 2026)
> A wiki is a compounding artifact. Each well-written page makes the next page easier to write because context, taxonomy, and cross-links accumulate. If an LLM is the primary author, the structure must prevent drift and hallucination — achieved via a three-layer architecture with strict write boundaries.

### Three-Layer Architecture
1. **`raw/`** — immutable sources (PDFs, web clips, data exports). LLM **never writes** here. Human-curated only.
2. **`wiki/`** — LLM-generated pages with YAML frontmatter. Each page has provenance links back to `raw/`. LLM writes, but only in response to Ingest or Query operations.
3. **`SCHEMA.md`** — LLM behavior rules per wiki instance. Defines allowed page types, required frontmatter fields, linking rules, and forbidden patterns. Human-edited, LLM-read-only.

### Operations
- **Ingest** — LLM reads a `raw/` source, produces one or more `wiki/` pages with provenance
- **Query** — LLM reads `wiki/` + optionally `raw/`, produces a synthesized answer (may write a new wiki page as a side effect)
- **Lint** — LLM reads `SCHEMA.md` + `wiki/`, reports violations (broken links, missing frontmatter, orphan pages)

### Supporting Artifact: `log.md`
- File-based activity log, append-only
- Records every Ingest/Query/Lint operation with timestamp, operation type, input path, output path, LLM model, cost
- Enables audit and rollback

### First Application: AI Solutions Architecture Tool Taxonomy
A living wiki documenting the tool landscape for an AI Solutions Practice. 28+ tool categories identified:
- workflow-orchestration
- llm-providers
- document-processing
- vector-databases
- agent-frameworks
- prompt-engineering
- evaluation-frameworks
- observability
- data-annotation
- fine-tuning-platforms
- rag-frameworks
- code-generation
- voice-stt-tts
- image-generation
- video-generation
- synthetic-data
- guardrails
- jailbreak-testing
- cost-optimization
- gpu-infrastructure
- inference-optimization
- model-registries
- feature-stores
- experiment-tracking
- multi-modal
- embeddings
- semantic-search
- (plus ~2 more not recovered from the pollution)

### ONET Integration
To ground the tool taxonomy in real labor-market data:
- `onet_occupations` — O*NET occupation codes, titles, descriptions
- `onet_skills` — O*NET skill taxonomy
- `onet_occupation_skills` — many-to-many skill→occupation mapping with importance/level scores
- `bls_wages` — BLS wage data by occupation
- `ai_exposure` — per-occupation AI exposure scores (from research indices)

### Data Sources Referenced
- **MIT Iceberg Index** (AI task exposure research)
- **Anthropic Economic Index** (LLM task performance measurement)
- O*NET database (occupation/skills/wages)
- BLS occupational wage statistics

### Business Context
> Each client engagement becomes a compounding loop: intake populates the tool taxonomy, tool evaluation produces wiki pages, next client benefits from prior research. The wiki is simultaneously an internal knowledge base, a sales artifact, and a deliverable template.

### Rewrite Guidance
**This spec is worth rewriting from scratch.** A fresh SPEC-WIKI-V2 should:
1. Start with a working Priority and acceptance criteria (Gate 0 clean)
2. Define the three-layer architecture as concrete directories (`wiki-example/raw/`, `wiki-example/wiki/`, `wiki-example/SCHEMA.md`)
3. Implement Ingest/Query/Lint as hivenode routes or CLI commands
4. Build the AI Solutions tool taxonomy as the first proof-of-concept wiki
5. Defer ONET integration to a follow-on spec (too much scope for v1)
6. Keep `log.md` simple: one line per operation, JSON lines format

### Related Killed Spec
The parent `SPEC-WIKI-V1` was NOT killed — it has a clean original in `shiftcenter@dd2eedf:_stage/` and will be restored by ESC-002. WIKI-V1.1 was an amendment that got lost in the escalation loop.

---

## 6. SPEC-GITHUB-005 — Federalist Papers Upload

**Kill reason:** Phantom spec. First commit `6887941` shows only a `.rejection.md` file — no clean SPEC file ever existed in git history. The rejection cites Gate 0 failure (missing `docs/federalist/COMPLETE-COLLECTION.md`) and a scope violation (`complete-collection.md` was forbidden in the project's constraints).

### Original Objective (reconstructed from rejection metadata)
Upload the Federalist Papers as a reference corpus into the project's document store, possibly as training data or as a wiki raw source.

### Why Killed
- **No spec file ever existed** — only rejection metadata survived
- **Constraint violation** — the rejection explicitly cites that `complete-collection.md` is forbidden per project constraints
- **Unclear purpose** — without the original intent statement, we cannot tell if this was for training data, wiki raw material, or something else

### Rewrite Guidance
If a Federalist Papers corpus is actually needed, write a fresh spec that:
1. States a concrete use case (e.g., "RAG test corpus for SPEC-WIKI-V2 Ingest operation")
2. Uses Project Gutenberg IDs (1404, 18) as source URLs, not a monolithic collection file
3. Lands the individual papers in `raw/` (per the WIKI-V1.1 three-layer pattern), not in `docs/`
4. Does NOT name any file `complete-collection.md`

---

## 7. SPEC-WIKI-SURVEY-000 — (Phantom Spec)

**Kill reason:** Pure phantom. No clean original anywhere in git history. Only rejection chains (up to 13 levels deep) exist. Gate 0 fail: missing Priority, missing acceptance criteria. Appears to have been a malformed or test spec that immediately failed.

### Original Objective (unknown)
The name suggests a wiki-related survey task (possibly surveying existing wiki content or doing a gap analysis for the WIKI-V1 family). **No spec content was ever written.**

### What Survived
Only Gate 0 rejection metadata:
- "Priority missing"
- "No acceptance criteria"
- "Survey" in the name suggests read-only research intent

### Rewrite Guidance
If a wiki survey is actually needed, write it as a fresh `SPEC-WIKI-SURVEY-001` with:
- Clear Priority section
- Concrete deliverables (e.g., "Markdown report listing all wiki-related specs and their implementation status")
- Read-only scope
- Reference to the clean SPEC-WIKI-V1 (once restored by ESC-002)

---

## Summary

| # | Spec | Kill Reason | Intellectual Value | Rewrite Priority |
|---|------|-------------|-------------------|------------------|
| 1 | BL-146 | No clean origin | Medium (bot architecture is concrete) | Low — reference `platform/simdecisions-2` |
| 2 | FLAPPY-100 | `(NEEDS_DAVE)` from birth | Low (novelty demo) | None unless Dave asks |
| 3 | MW-VERIFY-001 | No clean origin | Medium (audit methodology) | Low — straightforward to redo |
| 4 | TRIAGE-ESCALATED-001 | Ironically self-escalated | None (superseded by ESC-001) | Do not rewrite |
| 5 | **WIKI-V1.1** | Gate 0 fail from birth | **HIGH — substantial design** | **Medium — worth a clean v2** |
| 6 | GITHUB-005 | Only rejection metadata exists | None | None unless Federalist corpus needed |
| 7 | WIKI-SURVEY-000 | Pure phantom | None | None |

**Only SPEC-WIKI-V1.1 carries substantial intellectual content worth preserving and potentially rewriting.** The other 6 were either phantoms, ambiguous, or trivially redoable.

---

## Process Lesson (for Triage Daemon Autopsy — ESC-005)

All 7 of these specs would have been caught at Gate 0 if the triage daemon had:
1. **Capped retry depth at 1** — no spec should have more than 1 `## Clean Retry` block prepended
2. **Never escalated rejection files** — `.rejection.md` files are disposable metadata, not specs
3. **Locked escalated files** — once in `_escalated/`, no re-escalation; flag for human review instead
4. **Detected zombie specs** — >3 rejection files = auto-halt processing

These rules should be baked into the daemon rewrite or the daemon should be killed outright and replaced with a synchronous Gate 0 validator.

---

*Intent preservation record written 2026-04-10 by Q33NR during ESC-002 scope finalization. Source files in `simdecisions/.deia/hive/queue/_escalated/` remain as forensic evidence until ESC-003 cleanup.*
