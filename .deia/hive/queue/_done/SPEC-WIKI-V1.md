# ShiftCenter Wiki System Specification

**Spec ID:** SPEC-WIKI-V1
**Created:** 2026-04-06
**Status:** DRAFT
**Depends On:** SPEC-GAMIFICATION-V1, SPEC-EVENT-LEDGER-GAMIFICATION
**Ships With:** V1.0
**Priority:** P2

---

## Acceptance Criteria

- [ ] .wiki/ directory convention implemented and documented
- [ ] WikiPane component renders markdown content
- [ ] Wiki CRUD API endpoints functional
- [ ] Wiki operations emit events to Event Ledger
- [ ] Notebook execution support (Jupyter) functional
- [ ] Egg packaging from wiki content works end-to-end

---

## Executive Summary

This spec defines the **wiki system** for ShiftCenter — a markdown-native knowledge base that serves as:

1. **Repository documentation** — `.wiki/` directories that explain code, architecture, decisions
2. **Notebook execution** — Jupyter notebooks with ephemeral outputs, export on demand
3. **Egg packaging** — Knowledge atoms that can be packed, distributed, and inflated

Every wiki operation emits to the Event Ledger. Gamification scores these events.

### Core Principle

> Every database is a wiki. Every codebase is a notebook. Every deployment is an egg.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SOURCE LOCATIONS                               │
├─────────────────────────────────────────────────────────────────────────┤
│  .wiki/                    │  *.ipynb                │  *.egg           │
│  ├── index.md              │  Jupyter notebooks      │  Packaged units  │
│  ├── architecture/         │  (code + prose)         │  (governed)      │
│  ├── processes/            │                         │                  │
│  └── decisions/            │                         │                  │
└─────────────────────────────────────────────────────────────────────────┘
                │                       │                      │
                ▼                       ▼                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              WikiPane                                    │
│  • Tree browser (directories + files)                                   │
│  • Markdown editor with wikilink support                                │
│  • Notebook renderer (ephemeral outputs)                                │
│  • Backlinks panel                                                       │
│  • Search                                                                │
└─────────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Event Ledger                                   │
│  • PAGE_CREATED, PAGE_UPDATED, PAGE_LINKED                              │
│  • NOTEBOOK_RUN, NOTEBOOK_EXPORTED                                      │
│  • EGG_PACKED, EGG_INFLATED                                             │
│  → Gamification consumes these events                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema

### 2.1 Wiki Pages Table

```sql
CREATE TABLE wiki_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Scoping
    workspace_id UUID NOT NULL,                     -- ShiftCenter workspace
    
    -- Identity
    path VARCHAR(500) NOT NULL,                     -- 'architecture/event-ledger' (no .md)
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) GENERATED ALWAYS AS (
        LOWER(REGEXP_REPLACE(title, '[^a-zA-Z0-9]+', '_', 'g'))
    ) STORED,
    
    -- Content
    content TEXT NOT NULL,                          -- Markdown with [[wikilinks]]
    summary VARCHAR(500),                           -- One-line summary for index
    
    -- Optional embedding for search
    content_embedding VECTOR(1024),
    
    -- Classification
    page_type VARCHAR(50) NOT NULL DEFAULT 'doc',   -- doc, adr, process, index, notebook
    tags JSONB DEFAULT '[]',
    
    -- Frontmatter (parsed YAML)
    frontmatter JSONB DEFAULT '{}',
    
    -- Links (computed on save)
    outbound_links JSONB DEFAULT '[]',
    
    -- Versioning
    version INTEGER DEFAULT 1,
    is_current BOOLEAN DEFAULT TRUE,
    previous_version_id UUID REFERENCES wiki_pages(id),
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(id),
    updated_by UUID REFERENCES users(id),
    
    -- Soft delete
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMPTZ,
    
    CONSTRAINT wiki_pages_unique_path UNIQUE (workspace_id, path, version)
);

-- Indexes
CREATE INDEX idx_wiki_pages_workspace ON wiki_pages(workspace_id) 
    WHERE is_current = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_wiki_pages_path ON wiki_pages(path);
CREATE INDEX idx_wiki_pages_type ON wiki_pages(page_type);
CREATE INDEX idx_wiki_pages_tags ON wiki_pages USING GIN(tags);
CREATE INDEX idx_wiki_pages_links ON wiki_pages USING GIN(outbound_links);
CREATE INDEX idx_wiki_pages_embedding ON wiki_pages 
    USING ivfflat (content_embedding vector_cosine_ops) WITH (lists = 100)
    WHERE content_embedding IS NOT NULL;
```

### 2.2 Page Types

```sql
-- ShiftCenter wiki page types
-- doc         — general documentation
-- adr         — architecture decision record
-- process     — process definition (PROCESS-13, etc.)
-- index       — navigation/overview pages
-- notebook    — Jupyter notebook (.ipynb stored as JSON)
-- spec        — specification document
-- task        — task definition
-- runbook     — operational runbook
```

### 2.3 Wiki Edit Log

```sql
CREATE TABLE wiki_edit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    page_id UUID REFERENCES wiki_pages(id),
    workspace_id UUID NOT NULL,
    
    -- Operation
    operation VARCHAR(50) NOT NULL,      -- 'create', 'update', 'delete', 'link'
    
    -- Change details
    previous_content_hash VARCHAR(64),
    new_content_hash VARCHAR(64),
    diff_summary TEXT,                   -- Human-readable summary
    
    -- Audit
    edited_by UUID REFERENCES users(id),
    edited_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Event Ledger reference
    event_id UUID                        -- Links to ledger event
);

CREATE INDEX idx_wiki_edit_log_page ON wiki_edit_log(page_id);
CREATE INDEX idx_wiki_edit_log_time ON wiki_edit_log(edited_at DESC);
```

---

## 3. Page Schema (Markdown + Frontmatter)

### 3.1 Standard Page Example

```markdown
---
title: Event Ledger Architecture
page_type: adr
status: accepted
created: 2026-02-04
author: Q88N
tags: [architecture, governance, audit]
related: [three-currencies, process-13]
---

# Event Ledger Architecture

## Context

Every operation in ShiftCenter must be auditable...

## Decision

We will implement a hash-chained event ledger...

## Consequences

- All state changes emit events
- Events are immutable once written
- Prev_hash enables tamper detection

## See Also

- [[three-currencies]] — Cost tracking per event
- [[process-13]] — Quality gates that emit events
```

### 3.2 Process Page Example

```markdown
---
title: PROCESS-13
page_type: process
status: active
version: 1.2
owner: Q88N
---

# PROCESS-13: Three-Phase Quality Control

## Overview

Every task passes through three phases...

## Phases

### Phase 1: Validate Plan
- Spec → IR → Spec roundtrip
- Fidelity check before build

### Phase 2: Execute with Self-Check
- Builder bee implements
- Self-validates against spec

### Phase 3: Superior Validation
- QA bee (different instance) reviews
- Holdout-set methodology enforced

## Event Emissions

| Phase | Event Kind |
|-------|------------|
| Plan validated | TASK_PLAN_VALIDATED |
| Build complete | TASK_BUILD_COMPLETE |
| QA passed | TASK_QA_PASSED |
| QA failed | TASK_QA_FAILED |
```

---

## 4. .wiki/ Directory Convention

### 4.1 Repository Structure

```
shiftcenter/
├── .wiki/
│   ├── index.md                    # Repo overview, navigation
│   ├── architecture/
│   │   ├── index.md
│   │   ├── event-ledger.md
│   │   ├── three-currencies.md
│   │   └── hivenode.md
│   ├── processes/
│   │   ├── index.md
│   │   ├── PROCESS-13.md
│   │   └── clean-room-protocol.md
│   ├── decisions/
│   │   ├── index.md
│   │   ├── ADR-001.md
│   │   └── ADR-002.md
│   └── tutorials/
│       ├── getting-started.ipynb   # Notebooks live here too
│       └── api-walkthrough.ipynb
├── src/
│   ├── .wiki/
│   │   └── index.md                # "What's in src/"
│   ├── components/
│   │   ├── .wiki/
│   │   │   └── index.md            # "What's in components/"
│   │   └── HiveHostPanes.tsx
```

### 4.2 Index.md Convention

Every `.wiki/index.md` must contain:

```markdown
---
title: [Directory Name]
page_type: index
---

# [Directory Name]

## Purpose

[What this directory contains and why]

## Contents

- [[sub-page-1]] — Brief description
- [[sub-page-2]] — Brief description

## Navigation

- Parent: [[../index]]
- Related: [[other-relevant-section]]
```

### 4.3 LLM Navigation Pattern

When a bee needs to understand a directory:

1. Read `.wiki/index.md` first
2. Follow wikilinks to relevant pages
3. Only then examine actual code files

This replaces full-repo scans with targeted navigation.

---

## 5. Notebook System

### 5.1 NotebookPane Behavior

| Action | Behavior |
|--------|----------|
| **Open** | Parse `.ipynb`, render cells, outputs empty |
| **Run cell** | Execute, render output in pane (ephemeral) |
| **Save** | Write cells + code only, discard outputs |
| **Export** | User-triggered: .ipynb with outputs, .html, .py, .zip |
| **Close** | Prompt if cells modified. Outputs always discarded. |

### 5.2 Execution Environment

| Tier | Runtime | Use Case |
|------|---------|----------|
| **Browser** | Pyodide/JupyterLite | Light execution, no server |
| **Hivenode** | Python kernel | Heavy compute, full packages |
| **Hybrid** | Auto-detect | Simple → browser, complex → hivenode |

### 5.3 Notebook as Code Source

```yaml
# Build pipeline
steps:
  - name: Extract code from notebooks
    run: jupytext --to py notebooks/**/*.ipynb --output-dir src/
  
  - name: Test
    run: pytest src/
  
  - name: Package
    run: python -m build
```

Notebooks are source of truth. Extracted `.py` files are build artifacts.

---

## 6. Egg System (Local, Ungoverned)

V1 eggs are **local only** — no hodeia.me auth, no license enforcement.

### 6.1 Egg Structure

```
feature.egg/
├── manifest.yaml           # Metadata, dependencies
├── content/
│   ├── index.md           # Documentation
│   ├── main.ipynb         # Primary notebook
│   └── utils.ipynb        # Supporting code
└── extracted/             # (generated on inflate)
    ├── main.py
    └── utils.py
```

### 6.2 Manifest Schema

```yaml
egg_id: uuid
name: feature-name
version: 1.0.0
author: Q88N
created: 2026-04-06

description: |
  What this egg does.

dependencies:
  - numpy>=1.20
  - pandas>=2.0

extract_rules:
  - source: content/*.ipynb
    target: extracted/
    format: py

# V2 will add:
# auth_required: true
# permissions: [...]
# inflate_rules: [...]
```

### 6.3 CLI Commands

```bash
# Pack a directory into an egg
egg pack ./feature --output feature.egg

# Inflate an egg (extract code)
egg inflate feature.egg --target ./workspace

# List contents
egg list feature.egg

# Validate
egg validate feature.egg
```

---

## 7. WikiPane Component

### 7.1 Structure

```
primitives/wiki/
├── WikiPane.tsx            # Main container
├── WikiTree.tsx            # Directory tree
├── WikiEditor.tsx          # Markdown editor
├── WikiViewer.tsx          # Rendered markdown
├── NotebookPane.tsx        # Jupyter renderer
├── WikiBacklinks.tsx       # Inbound links panel
├── WikiSearch.tsx          # Search overlay
└── hooks/
    ├── useWikiPages.ts
    ├── useWikiLinks.ts
    └── useNotebook.ts
```

### 7.2 File Type Detection

```typescript
function getRenderer(path: string): 'markdown' | 'notebook' | 'prism' {
  if (path.endsWith('.ipynb')) return 'notebook';
  if (path.endsWith('.prism.md')) return 'prism';
  return 'markdown';
}
```

### 7.3 Wikilink Handling

```typescript
// Parse [[wikilinks]] from content
function parseWikilinks(content: string): string[] {
  const regex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
  const links: string[] = [];
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1].trim());
  }
  
  return [...new Set(links)];
}

// Transform for rendering
function transformWikilinks(content: string, onNavigate: (path: string) => void): ReactNode {
  // Convert [[link]] to clickable elements
}
```

---

## 8. API Endpoints

### 8.1 Wiki CRUD

```
GET    /api/wiki/pages                    # List pages
GET    /api/wiki/pages/{path}             # Get page + backlinks
POST   /api/wiki/pages                    # Create page
PUT    /api/wiki/pages/{path}             # Update page (new version)
DELETE /api/wiki/pages/{path}             # Soft delete

GET    /api/wiki/pages/{path}/history     # Version history
GET    /api/wiki/pages/{path}/backlinks   # Inbound links
GET    /api/wiki/search?q=...             # Full-text search
```

### 8.2 Notebook Execution

```
POST   /api/notebook/run                  # Execute cell(s)
POST   /api/notebook/export               # Generate export artifacts
GET    /api/notebook/kernel/status        # Kernel health
```

### 8.3 Egg Operations

```
POST   /api/egg/pack                      # Create egg from directory
POST   /api/egg/inflate                   # Extract egg contents
GET    /api/egg/validate                  # Check egg integrity
```

---

## 9. Event Emissions

All wiki operations emit to Event Ledger per SPEC-EVENT-LEDGER-GAMIFICATION.

| Operation | Event Kind | XP (per SPEC-GAMIFICATION-V1) |
|-----------|------------|-------------------------------|
| Create page | PAGE_CREATED | +15 |
| Update page | PAGE_UPDATED | +5 |
| Page gains backlink | PAGE_LINKED | +5 per link |
| Run notebook | NOTEBOOK_RUN | +2 |
| Export notebook | NOTEBOOK_EXPORTED | +10 |
| Pack egg | EGG_PACKED | +25 |
| Inflate egg | EGG_INFLATED | +5 |

---

## 10. Acceptance Criteria

### 10.1 Wiki Core

- [ ] WikiPane renders in HiveHostPanes
- [ ] Tree browser shows `.wiki/` structure
- [ ] Markdown editor with live preview
- [ ] Wikilinks `[[page_name]]` clickable
- [ ] Backlinks panel shows inbound links
- [ ] Version history viewable
- [ ] Search returns relevant pages

### 10.2 Notebooks

- [ ] NotebookPane renders `.ipynb` files
- [ ] Cell execution works (browser or hivenode)
- [ ] Outputs are ephemeral (not saved)
- [ ] Export generates .html, .py, .zip
- [ ] Notebooks extractable via jupytext

### 10.3 Eggs (Local)

- [ ] `egg pack` creates valid .egg
- [ ] `egg inflate` extracts to target
- [ ] `egg validate` checks integrity
- [ ] Manifest parsed correctly

### 10.4 Events

- [ ] All operations emit to Event Ledger
- [ ] Events contain required fields per SPEC-EVENT-LEDGER-GAMIFICATION
- [ ] Gamification receives and scores events

---

## 11. Migration Path

### Phase 1: Schema + Basic UI (Week 1)
- Create `wiki_pages`, `wiki_edit_log` tables
- WikiPane with tree + markdown editor
- No notebooks, no eggs

### Phase 2: Notebooks (Week 2)
- NotebookPane with Pyodide
- Ephemeral outputs
- Export functionality

### Phase 3: Eggs (Week 3)
- Pack/inflate CLI
- Local-only (no auth)
- Manifest validation

### Phase 4: Integration (Week 4)
- Event emissions wired
- Gamification consuming events
- `.wiki/` convention enforced

---

## 12. Out of Scope (V2+)

- hodeia.me auth integration
- License enforcement for eggs
- Time-locked/permission-gated inflation
- PHI tokenization
- Auto-compilation from external sources
- Graph view

These move to SPEC-WIKI-V2 after V1 ships and hodeia.me auth is wired.

---

**Spec Version:** 1.0
**Author:** Q88N × Claude
**Review Required:** Architecture approval before build
