# SPEC-HIVE-CAPABILITY-AUDIT-001: Hive Capability Self-Assessment

## Priority
P1

## Depends On
None

## Model Assignment
sonnet

## Objective

Before building new capabilities, the hive must know what it already has. Perform a **read-only audit** that scans existing specs, code, and infrastructure to produce a capability inventory against the Seven Pillars + WIRE framework. Output: a structured report showing what exists, what's specced-but-not-built, what's partially built, and what's entirely missing — specifically for the **SCAN/Comms/Daily Research** domain.

## Context

This spec was informed by SPEC-WIKI-V1 and the 2026-04-08-BRAINSTORM-PILLARS-WIRE.md brainstorm session. These are reference inputs, not blocking dependencies.

## 1. Audit Scope

### 1.1 Audit Philosophy: Discovery-First

**Assume nothing.** The audit does not presume gaps. It discovers what exists across all evidence sources:

1. **Running services** — API endpoints that respond, scheduled jobs that execute
2. **Code in repo** — Implementations that may predate or lack specs
3. **Specs and ADRs** — Formal documentation
4. **Brainstorm captures** — Ideas that may or may not have been built
5. **Hive task history** — `.deia/hive/tasks/`, `.deia/hive/responses/`

Code may exist without specs. Specs may exist without code. The audit finds both and reconciles.

### 1.2 Target Capabilities (Research/Comms Domain)

| Capability | Pillar | Description |
|-----------|--------|-------------|
| **Wiki System** | Knowledge Layer | Internal knowledge capture, wikilinks, versioning |
| **SCAN Ingestion** | Comms (7) | External data sources → Event Ledger |
| **Daily Briefing** | Comms (7) | Scheduled report generation for Q88N |
| **Market Research** | Comms (7) | AI/tech news, competitor tracking |
| **Embeddings & Search** | Learning (6) | Content indexed for semantic retrieval |
| **Event Ledger Integration** | Governance (1) | All activity traced |

### 1.3 Status Categories

| Status | Definition |
|--------|------------|
| **LIVE** | Running in production or staging; verified via API call or UI test |
| **BUILT** | Code exists, tests pass, not yet deployed |
| **BUILT-UNDOCUMENTED** | Code exists and works, no spec written yet |
| **SPECCED** | Formal spec exists (SPEC-*, ADR-*), code status unknown |
| **SPECCED-NOT-BUILT** | Spec exists, code confirmed absent |
| **BRAINSTORM** | Mentioned in brainstorm/design docs, no formal spec |
| **GAP** | Required but not found in code, specs, or brainstorm |

**The burden is on the audit to prove absence, not assume it.**

## 2. Audit Process

### 2.1 Core Principle: Mentions Are Leads, Not Gaps

**If it's discussed in project knowledge, assume it might be built.** The hive executes continuously. A brainstorm from April 8 may be running code by April 14. The audit treats every mention as a lead to verify:

1. Search project knowledge → find mentions
2. For EACH mention → probe repo, APIs, task history, hive responses
3. Only mark GAP if all probes return empty

### 2.2 Audit Steps

```yaml
audit_steps:
  - id: FIND-MENTIONS
    action: Search project knowledge for SPEC-*, ADR-*, PROCESS-*, brainstorms
    target: Wiki, SCAN, Comms, Ingestion, Briefing, Report, RSS, arXiv, HackerNews

  - id: VERIFY-EACH-MENTION
    action: For EACH mention, actively probe for implementation
    method: |
      1. Search repo for related code (grep, file names, imports)
      2. Check hive task history for related TASK-* or BEE-* completions
      3. Check hive responses for "features_delivered" matching capability
      4. Test API endpoints if applicable
      5. Check database for related tables/columns

  - id: CHECK-WIKI-STATUS
    action: Verify SPEC-WIKI-V1 implementation status
    method: |
      1. API call to /api/wiki/* endpoints
      2. Grep for WikiPane, useWikiPages, wiki_pages table
      3. Check hive responses for wiki-related features_delivered

  - id: CHECK-INGESTION-SOURCES
    action: For EACH source (RSS, arXiv, HackerNews, GitHub trending)
    method: |
      1. Grep codebase for feed URLs, API clients, scraper code
      2. Check for scheduled jobs / cron definitions
      3. Search hive task history for ingestion-related tasks
      4. Check Event Ledger for ingestion event types

  - id: CHECK-SCHEDULED-JOBS
    action: Find ALL scheduled/periodic tasks
    method: |
      1. Grep for cron, schedule, periodic, APScheduler, Celery beat
      2. Check hivenode for background task definitions
      3. Check for GitHub Actions with schedule triggers

  - id: CHECK-EMBEDDING-PIPELINE
    action: Verify RAG/embedding infrastructure
    method: |
      1. API call to /api/rag/* endpoints
      2. Check for Voyage AI client, pgvector usage
      3. Search hive responses for RAG-related features_delivered

  - id: CHECK-HIVE-TASK-HISTORY
    action: Search hive history for Research/Comms/SCAN work
    method: |
      1. Scan .deia/hive/tasks/ for relevant task files
      2. Scan .deia/hive/responses/ for completed work
      3. Look for features_delivered mentioning wiki, scan, briefing, ingestion

  - id: RECONCILE-AND-CLASSIFY
    action: For each capability, reconcile all evidence and assign status
```

## 3. Capability Matrix Template

The output report should follow this structure:

| Capability | Status | Evidence Source | Spec Reference | Notes |
|------------|--------|-----------------|----------------|-------|
| Wiki Core | {status} | {where found} | {spec if any} | {details} |
| WikiPane UI | {status} | {where found} | {spec if any} | {details} |
| SCAN Ingestion | {status} | {where found} | {spec if any} | {details} |
| RSS Feeds | {status} | {where found} | {spec if any} | {details} |
| arXiv Integration | {status} | {where found} | {spec if any} | {details} |
| HackerNews Scraper | {status} | {where found} | {spec if any} | {details} |
| GitHub Trending | {status} | {where found} | {spec if any} | {details} |
| Daily Briefing | {status} | {where found} | {spec if any} | {details} |
| Market Research | {status} | {where found} | {spec if any} | {details} |
| Embedding Pipeline | {status} | {where found} | {spec if any} | {details} |
| Event Ledger (Comms) | {status} | {where found} | {spec if any} | {details} |

Each capability must include an **Evidence Chain** section with all probes performed and their results.

## Acceptance Criteria

- [ ] All 11 capabilities in §1.2 / §3 assessed with a status from §1.3
- [ ] Each capability has evidence chain (probes performed + results)
- [ ] Gaps clearly identified with recommendations
- [ ] Hive task history scanned for related completed work
- [ ] Report filed to `.deia/hive/audits/AUDIT-CAPABILITY-2026-04-14.md`
- [ ] Post-audit recommendations are actionable and evidence-based

## Smoke Test

- [ ] Report file exists at `.deia/hive/audits/AUDIT-CAPABILITY-2026-04-14.md`
- [ ] Report is under 500 lines
- [ ] All 11 capabilities have a status assigned
- [ ] No capability marked GAP without documented probe results showing absence

## Constraints

- Read-only audit. Do not write code, modify infrastructure, or dispatch bees.
- No file over 500 lines.
- Report goes to `.deia/hive/audits/` only.
- If hivenode is not running, note it and skip API probes (do not start services).

## Files to Modify

- `.deia/hive/audits/AUDIT-CAPABILITY-2026-04-14.md` (create)
