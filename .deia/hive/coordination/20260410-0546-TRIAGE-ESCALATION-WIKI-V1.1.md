# TRIAGE ESCALATION: WIKI-V1.1

**Date:** 2026-04-10 05:46:50 UTC
**Reason:** 3 requeue attempts (max 3)
**Status:** NEEDS MANUAL REVIEW

## Summary

Spec `SPEC-WIKI-V1.1-LLM-WIKI-PATTERN.md` has been requeued 3 times and failed each time.
Automated triage has moved it to `_escalated/` for manual review.

## Triage History

- 2026-04-10T01:44:28.607789Z — requeued (empty output)
- 2026-04-10T05:41:50.074041Z — requeued (empty output)
- 2026-04-10T05:44:29.030462Z — requeued (empty output)

## Next Steps

1. **Review spec file** in `queue/_escalated/SPEC-WIKI-V1.1-LLM-WIKI-PATTERN.md`
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

# SPEC-WIKI-V1.1: LLM Wiki Pattern Integration

**Spec ID:** SPEC-WIKI-V1.1
**Created:** 2026-04-09
**Status:** PROPOSED
**Amends:** SPEC-WIKI-V1
**Inspiration:** Andrej Karpathy's LLM Wiki (April 2026)

---

## Executive Summary

This spec amends SPEC-WIKI-V1 to incorporate the **LLM Wiki pattern** — a methodology where LLMs compile, maintain, and query structured knowledge bases rather than performing RAG on raw documents.

**Core insight:** The wiki is a compounding artifact. Knowledge is compiled once and kept current, not re-derived on every query.

---

## 1. What We Already Built (WIKI-V1 Complete)

Per SPEC-WIKI-V1, the following is implemented (WIKI-01 through WIKI-109, all in `_done/`):

### 1.1 Wiki Core
- `wiki_pages` table with versioning, frontmatter, embeddings
- WikiPane component (tree browser, markdown editor, viewer)
- Wikilinks `[[page]]` parsing and navigation
- Backlinks panel (inbound link discovery)
- `.wiki/` directory convention with `index.md` navigation
- Page types: doc, adr, process, index, notebook, spec, task, runbook

### 1.2 LLM Navigation
- Bees read `index.md` first, follow wikilinks to relevant pages
- Replaces full-repo scans with targeted navigation
- Wiki search via embeddings (Voyage AI, pgvector)

### 1.3 Notebooks
- NotebookPane renders `.ipynb` files
- Ephemeral outputs (not saved)
- Export to .html, .py, .zip

### 1.4 Eggs (Local)
- Pack/inflate CLI
- Manifest validation
- No auth (V1 scope)

### 1.5 Event Emissions
- All operations emit to Event Ledger
- Gamification scores wiki events (PAGE_CREATED, PAGE_UPDATED, etc.)

### 1.6 Prompt Injection (BOK)
- Book of Knowledge with patterns/antipatterns
- Voyage AI embeddings for semantic matching
- Prompt builder queries BOK, injects relevant snippets into bee prompts

### 1.7 Dispatch Injections
- `.deia/config/injections/base.md` — shared across all models
- `.deia/config/injections/claude_code.md` — CC-specific behavior guardrails
- `injection_loader.py` loads base + model-specific, prepends to system prompt
- **This IS the schema file pattern** — we call it "injections"

---

## 2. What This Spec Adds

### 2.1 Three-Layer Architecture (Formalized)

```
wiki-name/
├── raw/                    # Layer 1: Immutable sources
│   ├── articles/
│   ├── docs/
│   ├── data/
│   └── assets/
├── wiki/                   # Layer 2: LLM-generated pages
│   ├── index.md
│   ├── log.md
│   ├── concepts/
│   ├── entities/
│   ├── sources/
│   └── comparisons/
└── SCHEMA.md               # Layer 3: Behavior rules for LLM
```

**Layer 1: raw/**
- Immutable source documents (articles, papers, data files, images)
- LLM reads from here, NEVER writes
- Source of truth for provenance

**Layer 2: wiki/**
- LLM-generated and LLM-maintained markdown files
- Structured pages with frontmatter
- Cross-referenced via wikilinks
- Human reads, LLM writes

**Layer 3: SCHEMA.md**
- Tells the LLM how to operate this specific wiki
- Page conventions, frontmatter requirements
- Ingest/query/lint workflows
- **Equivalent to our injection files, but wiki-specific**

---

### 2.2 log.md (File-Based Activity Log)

**Decision:** Use `log.md` instead of `wiki_edit_log` database table.

**Rationale:**
- Transparency — `git log` shows everything, no SQL query needed
- Portability — move the wiki anywhere, history travels with it
- LLM readability — bee can read `log.md` directly, no API call
- Simplicity — one less table to maintain

**Format:**

```markdown
# Activity Log

## [2026-04-09T14:30:00Z] ingest | Tool Name
Source: raw/tools/zapier/pricing.md
Pages created: wiki/tools/zapier.md
Pages updated: wiki/categories/workflow-orchestration.md, wiki/index.md
Notes: Added pricing tiers, integration surface.

## [2026-04-09T15:00:00Z] query | Compare workflow tools
Question: Compare Zapier vs Make vs n8n for high-volume webhooks
Pages read: wiki/tools/zapier.md, wiki/tools/make.md, wiki/tools/n8n.md
Output: Filed as wiki/comparisons/webhook-processing.md

## [2026-04-09T16:00:00Z] lint | Weekly health check
Contradictions found: 1
Orphan pages: 2
Missing pages suggested: 3
```

**Convention:**
- Each entry starts with `## [ISO-timestamp] operation | subject`
- Parseable with grep: `grep "^## \[" log.md | tail -10`
- Append-only — never edit past entries

---

### 2.3 Ingest Operation

When a new source arrives in `raw/`, the LLM:

1. **Read** the source file
2. **Discuss** key takeaways with human (if interactive) or summarize (if batch)
3. **Create/update** wiki pages:
   - Summary page in `wiki/sources/`
   - Update relevant concept/entity pages
   - Update `wiki/index.md`
4. **Append** entry to `wiki/log.md`
5. **Emit** PAGE_CREATED/PAGE_UPDATED events to Event Ledger

**Trigger phrase:** "Ingest raw/path/to/file.md"

**Single source may touch 10+ wiki pages** — that's the compounding effect.

---

### 2.4 Query Operation

When human asks a question:

1. **Read** `wiki/index.md` to find relevant pages
2. **Read** those pages
3. **Synthesize** answer with `[[wikilink]]` citations
4. **Offer** to file valuable answers as new wiki pages

**Query → file back pattern:**
- Comparisons, analyses, insights that emerge from queries
- If valuable, file as `wiki/comparisons/` or `wiki/analyses/`
- Explorations compound in the knowledge base

---

### 2.5 Lint Operation

Periodic wiki health check:

1. **Contradictions** — pages with conflicting claims
2. **Orphan pages** — no inbound links
3. **Missing pages** — concepts mentioned but lacking own page
4. **Stale claims** — superseded by newer sources
5. **Suggested investigations** — gaps worth filling

**Trigger phrase:** "Lint the wiki"

**Output:** Health report with actionable items

---

### 2.6 Enhanced Frontmatter

Add to SPEC-WIKI-V1 frontmatter:

```yaml
---
title: Page Title
page_type: concept | entity | source-summary | comparison | tool
sources: [raw/path/to/source1.md, raw/path/to/source2.md]
confidence: high | medium | low
created: 2026-04-09
updated: 2026-04-09
---
```

**New fields:**
- `sources[]` — which raw files informed this page (provenance)
- `confidence` — how certain is this information

---

## 3. SCHEMA.md Template

Each wiki gets its own schema file defining LLM behavior:

```markdown
# Wiki Schema: [Wiki Name]

## Project Structure
- `raw/` — immutable source documents. NEVER modify.
- `wiki/` — LLM-generated wiki. You own this entirely.
- `wiki/index.md` — master catalog. Update on every ingest.
- `wiki/log.md` — append-only activity log.

## Page Conventions
Every wiki page MUST have YAML frontmatter:
```yaml
---
title: Page Title
page_type: [type]
sources: [list of raw/ files referenced]
related: [list of wiki pages linked]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

## Ingest Workflow
When told "ingest [path]":
1. Read the source file in raw/
2. Discuss key takeaways
3. Create/update summary page in wiki/sources/
4. Update wiki/index.md
5. Update all relevant concept and entity pages
6. Append entry to wiki/log.md

## Query Workflow
When asked a question:
1. Read wiki/index.md to find relevant pages
2. Read those pages
3. Synthesize answer with [[wiki-link]] citations
4. If answer is valuable, offer to file as new wiki page

## Lint Workflow
When told "lint":
1. Check for contradictions between pages
2. Find orphan pages with no inbound links
3. List concepts mentioned but lacking own page
4. Check for stale claims superseded by newer sources
5. Suggest questions to investigate next

## Domain-Specific Rules
[Wiki-specific conventions go here]
```

---

## 4. Relationship to Existing Systems

### 4.1 Dispatch Injections
- `injections/base.md` + `injections/claude_code.md` = generic bee behavior
- `SCHEMA.md` = wiki-specific bee behavior
- Both get prepended to system prompt; schema is additive

### 4.2 BOK (Book of Knowledge)
- BOK = patterns/antipatterns for code quality
- Wiki = domain knowledge compiled from sources
- BOK injections + wiki page context = complete prompt

### 4.3 Event Ledger
- Ingest/query/lint operations emit events
- New event kinds: `WIKI_INGEST`, `WIKI_QUERY_FILED`, `WIKI_LINT`

---

## 5. First Application: Tool Taxonomy for AI Solutions Practice

### 5.1 Business Context

**The Service:** AI Solutions Architecture — you diagnose client process problems, design optimal tool stacks, and either build or source the implementation.

**The Differentiator:** You're not the guy who knows Zapier, Make, and ChatGPT. You're the architect with a researched taxonomy of 50+ tools across categories, matching the *right* tool to the problem. Better solutions, defensible positioning.

**The Wiki's Role:**
- When a client says "we spend 22 hours on candidate screening," you query the wiki
- Pull workflow-orchestration category, document-processing tools, LLM providers
- Compare pricing models, integration surfaces, scale limits
- Architect a solution from documented facts, not memory

**The Compounding Effect:**
- Every client engagement adds to `raw/` (vendor docs, evaluations, lessons learned)
- Ingest compiles into `wiki/` (updated tool pages, new comparisons)
- Next client gets the benefit of all prior research

### 5.2 Wiki Structure

### 5.2 Wiki Structure

```
tool-taxonomy/
├── raw/
│   ├── vendors/
│   │   ├── zapier/
│   │   │   ├── pricing-2026-04.md
│   │   │   └── api-docs.md
│   │   └── make/
│   └── evaluations/
│       └── workflow-tools-2026-04.md
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── categories/
│   │   ├── workflow-orchestration.md      # Zapier, Make, n8n, Temporal
│   │   ├── llm-providers.md               # OpenAI, Anthropic, Google, Mistral
│   │   ├── document-processing.md         # Docling, Unstructured, Textract
│   │   ├── data-extraction.md             # Firecrawl, Apify, Browserbase
│   │   ├── vector-stores.md               # Pinecone, Weaviate, Qdrant, Chroma
│   │   ├── voice-transcription.md         # Whisper, Deepgram, AssemblyAI
│   │   ├── agent-frameworks.md            # CrewAI, AutoGen, LangGraph
│   │   ├── infrastructure-hosting.md      # AWS, GCP, Railway, Vercel
│   │   ├── email-communications.md        # SendGrid, Postmark, Twilio
│   │   ├── auth-identity.md               # Auth0, Clerk, WorkOS
│   │   ├── payments-billing.md            # Stripe, Paddle, LemonSqueezy
│   │   ├── search.md                      # Algolia, Typesense, Meilisearch
│   │   ├── scheduling-booking.md          # Calendly, Cal.com, Acuity
│   │   ├── forms-data-capture.md          # Typeform, Tally, Jotform
│   │   ├── notifications.md               # Knock, Novu, OneSignal
│   │   ├── monitoring-observability.md    # Datadog, Sentry, Axiom
│   │   ├── etl-pipelines.md               # Airbyte, Fivetran, dbt
│   │   ├── spreadsheet-backends.md        # Airtable, Notion, Rows
│   │   ├── low-code-internal.md           # Retool, Appsmith, Budibase
│   │   ├── contract-signing.md            # DocuSign, PandaDoc
│   │   ├── knowledge-base.md              # Notion, Confluence, GitBook
│   │   ├── customer-support.md            # Intercom, Zendesk, Plain
│   │   ├── project-management.md          # Linear, Asana, ClickUp
│   │   ├── analytics.md                   # Amplitude, Mixpanel, PostHog
│   │   ├── fine-tuning.md                 # Together.ai, Anyscale, Modal
│   │   ├── prompt-management.md           # PromptLayer, Humanloop, Langfuse
│   │   ├── evaluation-testing.md          # Promptfoo, Ragas, DeepEval
│   │   └── guardrails-safety.md           # Guardrails AI, NeMo, Lakera
│   ├── tools/
│   │   ├── zapier.md
│   │   ├── make.md
│   │   └── [one page per tool]
│   └── comparisons/
│       └── webhook-processing.md
└── SCHEMA.md
```

### 5.3 Keep-Tabs Categories (Track, Don't Sell)

These categories are tracked for awareness but outside core practice scope:

- Image generation
- Video generation  
- Hardware / edge AI
- Robotics / IoT
- Gaming / 3D / procedural gen
- Bioinformatics / scientific computing
- GIS / mapping
- Defense / gov tech

### 5.4 ONET Integration (Database-Backed Reference Data)

**Why ONET matters for the practice:**

When a client says "we have 15 recruiters spending 22 hours/week on candidate screening," you need to know:
- What skills define that occupation?
- Which skills are automatable vs. relational?
- What's the AI exposure score for this role?

ONET (O*NET OnLine, onetcenter.org) provides this — 923 occupations × skill/importance/difficulty matrices, freely available via API.

**Architecture decision:** ONET is relational, not wiki.

The data is inherently relational: occupations → skills → importance scores → difficulty scores → BLS wage data. Wiki markdown is the wrong shape. The right shape is PostgreSQL tables that the wiki can *query*, not store.

**Database schema:**

```sql
-- Core ONET tables
onet_occupations (
    soc_code TEXT PRIMARY KEY,      -- e.g., "13-1071.00"
    title TEXT NOT NULL,             -- e.g., "Human Resources Specialists"
    description TEXT,
    job_zone INTEGER                 -- 1-5 complexity rating
);

onet_skills (
    element_id TEXT PRIMARY KEY,     -- e.g., "2.A.1.a"
    name TEXT NOT NULL,              -- e.g., "Reading Comprehension"
    category TEXT                    -- e.g., "Basic Skills"
);

onet_occupation_skills (
    soc_code TEXT REFERENCES onet_occupations,
    element_id TEXT REFERENCES onet_skills,
    importance NUMERIC,              -- 1-5 scale
    level NUMERIC,                   -- 0-7 scale
    PRIMARY KEY (soc_code, element_id)
);

onet_tasks (
    task_id TEXT PRIMARY KEY,
    soc_code TEXT REFERENCES onet_occupations,
    description TEXT,
    dwa_id TEXT                      -- Detailed Work Activity reference
);

-- BLS wage overlay
bls_wages (
    soc_code TEXT REFERENCES onet_occupations,
    year INTEGER,
    median_annual_wage NUMERIC,
    employment INTEGER,
    PRIMARY KEY (soc_code, year)
);

-- AI exposure scores (from MIT Iceberg / Anthropic research)
ai_exposure (
    soc_code TEXT REFERENCES onet_occupations,
    source TEXT,                     -- 'mit_iceberg' | 'anthropic_economic_index'
    theoretical_pct NUMERIC,         -- theoretical exposure
    observed_pct NUMERIC,            -- actual observed adoption
    date_captured DATE,
    PRIMARY KEY (soc_code, source, date_captured)
);
```

**How the wiki uses it:**

The wiki gets a **read view**. When answering "what roles are most exposed to AI in this client's org?", the LLM:

1. Queries `ai_exposure` for the relevant SOC codes
2. Pulls skill profiles from `onet_occupation_skills`
3. Synthesizes the answer with wiki context (tool capabilities, client industry)
4. Cites both wiki pages AND database queries in the response

**Data sources to ingest:**

| Source | Data | Status |
|--------|------|--------|
| ONET API | 923 occupations, skills, tasks | Free, queryable |
| BLS OES | Wage data by occupation | Free, annual release |
| MIT Iceberg Index | AI exposure by state/occupation | Pending — may need scrape or outreach |
| Anthropic Economic Index | Observed vs. theoretical exposure | anthropic.com/research — extractable |

**Pending action:** Email Ayush Chopra (MIT contact on Iceberg arXiv paper) requesting research collaboration access to the 13,000+ AI tool capability profiles.

### 5.5 The Compounding Loop

```
Client engagement
    ↓
Discovery call → identify roles/processes
    ↓
Query ONET → skill profiles, AI exposure scores
    ↓
Query wiki → tool capabilities, pricing, integrations
    ↓
Architect solution → tool selection + implementation plan
    ↓
Lessons learned → ingest to raw/
    ↓
Wiki pages updated → next client benefits
    ↓
Event Ledger captures → Three Currencies tracked
```

Every client engagement makes the next one faster and more accurate. The database provides the foundation (occupations, skills, exposure). The wiki provides the tooling layer (capabilities, pricing, gotchas). Together they answer: "For THIS role with THESE skills at THIS exposure level, which tools should we deploy?"

---

## 6. Acceptance Criteria

### 6.1 Three-Layer Structure
- [ ] `raw/` directory convention documented
- [ ] `wiki/` directory convention updated
- [ ] `SCHEMA.md` template available

### 6.2 log.md
- [ ] Activity log format defined
- [ ] Append-only behavior enforced
- [ ] Parseable with grep

### 6.3 Operations
- [ ] Ingest workflow documented and tested
- [ ] Query workflow documented
- [ ] Lint workflow documented
- [ ] Query → file back pattern works

### 6.4 Frontmatter
- [ ] `sources[]` field added to schema
- [ ] `confidence` field added to schema

### 6.5 First Wiki
- [ ] Tool taxonomy wiki created
- [ ] SCHEMA.md written for tool taxonomy
- [ ] 10+ tools ingested as proof of concept

### 6.6 ONET Integration
- [ ] `onet_occupations` table created and seeded
- [ ] `onet_skills` table created and seeded
- [ ] `onet_occupation_skills` junction table created and seeded
- [ ] `bls_wages` table created with current year data
- [ ] `ai_exposure` table created with MIT Iceberg + Anthropic data
- [ ] Wiki can query ONET tables via API endpoint
- [ ] Query responses can cite both wiki pages and ONET data

---

## 7. Out of Scope

- Graph view (V2)
- Auto-compilation from external URLs (V2)
- Multi-user wiki collaboration (V2)
- Wiki-to-wiki federation (V2+)

---

## 8. References

- SPEC-WIKI-V1 — Base wiki system
- Andrej Karpathy, "LLM Wiki" (GitHub Gist, April 2026)
- `.deia/config/injections/` — Existing injection system
- SPEC-GAMIFICATION-V1 — Event scoring
- SPEC-EVENT-LEDGER-GAMIFICATION — Event schema
- O*NET OnLine (onetcenter.org) — Occupation/skill matrices, free API
- MIT Iceberg Index (iceberg.mit.edu) — AI task displacement research
- Anthropic Economic Index (anthropic.com/research/labor-market-impacts) — Observed vs. theoretical exposure

---

**Spec Version:** 1.1
**Author:** Q88N × Claude
**Review Required:** Architecture approval before dispatch

## Triage History
- 2026-04-10T01:44:28.607789Z — requeued (empty output)
- 2026-04-10T05:41:50.074041Z — requeued (empty output)
- 2026-04-10T05:44:29.030462Z — requeued (empty output)

```

---

**Automated escalation by triage daemon**
