# FBB Wiki System Specification

**Spec ID:** SPEC-WIKI-SYSTEM
**Created:** 2026-04-06
**Status:** DRAFT - Ready for review
**Depends On:** 01-SCHEMA-ADDITIONS.md, 02-CONTENT-ENTITY-SYSTEM.md
**Replaces:** Content entity RAG system (partial — wiki augments, doesn't fully replace)
**Priority:** P3

---

## Acceptance Criteria

- [ ] Clinical Wiki stores and retrieves trainer-maintained knowledge
- [ ] Family Wiki auto-compiles per-family context
- [ ] Both wikis use shared storage schema
- [ ] Wiki retrieval service returns structured results
- [ ] API endpoints for wiki CRUD operations
- [ ] Frontend WikiPane component renders wiki content

---

## Executive Summary

This spec defines a **dual-wiki architecture** for FamilyBondBot:

1. **Clinical Wiki** — Trainer-maintained knowledge base replacing/augmenting RAG content entities
2. **Family Wiki** — Auto-compiled per-family context replacing chat history mining

Both wikis use the same storage schema, same editor UI, and same retrieval patterns. The wiki system also powers **intelligent gamification** by tracking user patterns in structured, queryable form.

### Why Wiki Over RAG?

| RAG Approach | Wiki Approach |
|--------------|---------------|
| Chunk → embed → retrieve by similarity | Compile once → maintain → retrieve by structure |
| Clinical terms match poorly to user language | Wiki written in natural language patterns |
| No accumulation across queries | Knowledge compounds with each interaction |
| Black box retrieval | Human-readable, editable pages |
| Amy's chapters → lossy chunking | Amy's chapters → interlinked concept pages |

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              RAW SOURCES                                 │
├─────────────────────────────────┬───────────────────────────────────────┤
│  Clinical (trainer uploads)     │  Family (auto-captured)               │
│  • Amy's book chapters          │  • Chat transcripts (tokenized)       │
│  • Research papers              │  • Family History chat                │
│  • Clinical notes               │  • Intake form responses              │
│  • Training materials           │  • Interaction debriefs               │
└─────────────────────────────────┴───────────────────────────────────────┘
                │                                    │
                ▼                                    ▼
┌─────────────────────────────────┐  ┌───────────────────────────────────┐
│  CLINICAL WIKI                  │  │  FAMILY WIKI (per folder)         │
│  Maintained by: Trainers + Amy  │  │  Maintained by: Frank (auto)      │
│  corpus_id: 'clinical-v1'       │  │  folder_id: <uuid>                │
│                                 │  │                                   │
│  wiki/                          │  │  wiki/                            │
│  ├── index.md                   │  │  ├── index.md                     │
│  ├── concepts/                  │  │  ├── members/                     │
│  │   ├── loyalty_binds.md       │  │  │   ├── DS001.md                 │
│  │   ├── coercive_control.md    │  │  │   ├── DD001.md                 │
│  │   └── parental_alienation.md │  │  │   └── CP001.md                 │
│  ├── techniques/                │  │  ├── patterns/                    │
│  │   ├── biff_response.md       │  │  │   ├── communication.md         │
│  │   ├── gray_rock.md           │  │  │   ├── custody.md               │
│  │   └── validation_first.md    │  │  │   └── triggers.md              │
│  ├── guardrails/                │  │  ├── history/                     │
│  │   ├── never_diagnose.md      │  │  │   └── timeline.md              │
│  │   ├── crisis_response.md     │  │  └── meta/                        │
│  │   └── court_safe_language.md │  │      ├── clinical_formulation.md  │
│  └── scripts/                   │  │      └── progression.md           │
│      └── rejection_response.md  │  │                                   │
└─────────────────────────────────┘  └───────────────────────────────────┘
                │                                    │
                └──────────────┬─────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  WIKI RETRIEVAL SERVICE                                                  │
│                                                                          │
│  1. Read index.md for relevant page paths                               │
│  2. Load specific pages based on:                                        │
│     - Chat type (Co-Parent → custody patterns, techniques/biff)         │
│     - Message content (semantic match to page summaries)                │
│     - Family context (member pages for mentioned tokens)                │
│  3. Inject into prompt assembly                                         │
└─────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PROMPT ASSEMBLY                                                         │
│                                                                          │
│  [PERSONA] + [GUARDRAILS] + [CLINICAL WIKI PAGES] + [FAMILY WIKI PAGES] │
│  + [CONVERSATION HISTORY] + [USER CONTEXT + PROGRESSION]                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema

### 2.1 Wiki Pages Table

```sql
CREATE TABLE wiki_pages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Scoping (one of these will be set, not both)
    corpus_id VARCHAR(50),                              -- 'clinical-v1', 'clinical-v2' (NULL for family wikis)
    folder_id UUID REFERENCES folders(id) ON DELETE CASCADE,  -- NULL for clinical wiki
    
    -- Identity
    path VARCHAR(500) NOT NULL,                         -- 'concepts/loyalty_binds' (no .md extension)
    title VARCHAR(255) NOT NULL,                        -- 'Loyalty Binds'
    slug VARCHAR(255) GENERATED ALWAYS AS (
        LOWER(REGEXP_REPLACE(title, '[^a-zA-Z0-9]+', '_', 'g'))
    ) STORED,
    
    -- Content
    content TEXT NOT NULL,                              -- Markdown with [[wikilinks]]
    summary VARCHAR(500),                               -- One-line summary for index
    
    -- Optional embedding for hybrid retrieval
    content_embedding VECTOR(1024),                     -- Voyage AI embedding
    
    -- Classification
    page_type VARCHAR(50) NOT NULL,                     -- See enum below
    tags JSONB DEFAULT '[]',                            -- Freeform tags for filtering
    
    -- Frontmatter (parsed YAML from content header)
    frontmatter JSONB DEFAULT '{}',                     -- priority, chat_types, audience_types, etc.
    
    -- Links (computed on save)
    outbound_links JSONB DEFAULT '[]',                  -- ['concepts/coercive_control', 'techniques/biff']
    
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
    
    -- Constraints
    CONSTRAINT wiki_pages_scope_check CHECK (
        (corpus_id IS NOT NULL AND folder_id IS NULL) OR
        (corpus_id IS NULL AND folder_id IS NOT NULL)
    ),
    CONSTRAINT wiki_pages_unique_path UNIQUE (corpus_id, folder_id, path, version)
);

-- Indexes
CREATE INDEX idx_wiki_pages_corpus ON wiki_pages(corpus_id) 
    WHERE corpus_id IS NOT NULL AND is_current = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_wiki_pages_folder ON wiki_pages(folder_id) 
    WHERE folder_id IS NOT NULL AND is_current = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_wiki_pages_path ON wiki_pages(path);
CREATE INDEX idx_wiki_pages_type ON wiki_pages(page_type);
CREATE INDEX idx_wiki_pages_tags ON wiki_pages USING GIN(tags);
CREATE INDEX idx_wiki_pages_links ON wiki_pages USING GIN(outbound_links);
CREATE INDEX idx_wiki_pages_embedding ON wiki_pages 
    USING ivfflat (content_embedding vector_cosine_ops) WITH (lists = 100)
    WHERE content_embedding IS NOT NULL;
```

### 2.2 Page Types Enum

```sql
-- Clinical Wiki page types
CREATE TYPE clinical_page_type AS ENUM (
    'concept',           -- Educational concepts (loyalty binds, coercive control)
    'technique',         -- Actionable skills (BIFF, gray rock)
    'guardrail',         -- Hard rules (never diagnose, crisis response)
    'script',            -- Response templates
    'decision_rule',     -- If-then logic
    'training_material', -- Background knowledge
    'index'              -- Navigation/overview pages
);

-- Family Wiki page types
CREATE TYPE family_page_type AS ENUM (
    'member',            -- Person pages (DS001, CP001)
    'pattern',           -- Observed patterns (communication, triggers)
    'history',           -- Timeline, events
    'meta',              -- Clinical formulation, progression
    'index'              -- Navigation/overview pages
);

-- Combined for the page_type column
-- Use VARCHAR(50) to allow both types
```

### 2.3 Wiki Compilation Log

```sql
CREATE TABLE wiki_compilation_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Scope
    folder_id UUID REFERENCES folders(id) ON DELETE CASCADE,  -- NULL for clinical
    corpus_id VARCHAR(50),                                     -- NULL for family
    
    -- Operation
    operation VARCHAR(50) NOT NULL,      -- 'ingest', 'compile', 'lint', 'manual_edit'
    source_type VARCHAR(50),             -- 'chat', 'upload', 'trainer', 'system'
    source_id UUID,                      -- chat_id, upload_id, etc.
    
    -- Changes
    pages_created JSONB DEFAULT '[]',    -- ['members/DS001', 'patterns/communication']
    pages_updated JSONB DEFAULT '[]',
    pages_deleted JSONB DEFAULT '[]',
    
    -- Metadata
    compiled_by UUID REFERENCES users(id),  -- NULL if system/Frank
    compiled_at TIMESTAMPTZ DEFAULT NOW(),
    token_cost INTEGER,                     -- LLM tokens used for compilation
    
    -- Summary
    summary TEXT                            -- Human-readable change summary
);

CREATE INDEX idx_wiki_log_folder ON wiki_compilation_log(folder_id);
CREATE INDEX idx_wiki_log_corpus ON wiki_compilation_log(corpus_id);
CREATE INDEX idx_wiki_log_time ON wiki_compilation_log(compiled_at DESC);
```

### 2.4 Raw Sources Table (for Clinical Wiki)

```sql
CREATE TABLE wiki_raw_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    corpus_id VARCHAR(50) NOT NULL,
    
    -- File info
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,       -- 'docx', 'pdf', 'md', 'txt'
    file_size_bytes INTEGER,
    
    -- Content
    content_text TEXT,                     -- Extracted text
    content_hash VARCHAR(64) NOT NULL,    -- SHA-256 for change detection
    
    -- Processing status
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'compiled', 'failed'
    compiled_at TIMESTAMPTZ,
    error_message TEXT,
    
    -- Links to generated pages
    generated_pages JSONB DEFAULT '[]',   -- Page paths created from this source
    
    -- Audit
    uploaded_by UUID REFERENCES users(id),
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(corpus_id, content_hash)
);
```

---

## 3. Page Schema (Markdown + Frontmatter)

### 3.1 Clinical Wiki Page Example

```markdown
---
title: Loyalty Binds
page_type: concept
priority: 80
chat_types: [PARENT_CHILD, CO_PARENT, GENERAL]
audience_types: [parent, clinician]
triggers:
  - "child says they hate me"
  - "child doesn't want to come"
  - "child is rejecting me"
  - "child chose the other parent"
related: [parental_alienation, triangulation, enmeshment]
source: amy_chapter_7
last_reviewed: 2026-03-15
---

# Loyalty Binds

A loyalty bind occurs when a child feels they must choose between parents, often resulting in rejection of one parent to maintain peace with the other. This is not a reflection of the child's true feelings, but a survival strategy.

## Recognition Signs

The child may:
- Use language that mirrors the other parent's complaints
- Express absolute rejection ("I never want to see you again")
- Show anxiety around transitions
- Seem relieved when visits are cancelled

## What This Means

The child is not choosing sides — they are managing an impossible situation. Their rejection is often proportional to the pressure they feel, not their actual attachment to you.

## Frank's Approach

When a parent describes rejection:
1. Validate the pain without amplifying it
2. Reframe: "That sounds like a loyalty bind, not a true rejection"
3. Reassure: "Your relationship is still there, even when it's hard to see"
4. Guide toward patience, not pursuit

## See Also

- [[parental_alienation]] — When loyalty binds become systematic
- [[triangulation]] — The communication pattern that creates binds
- [[techniques/validation_first]] — How to respond in the moment

## References

- Dr. Amy Eichler, "Chapter 7: Treatment with the Child"
- Baker, A.J.L. (2007). Adult Children of Parental Alienation Syndrome
```

### 3.2 Family Wiki Page Example (Member)

```markdown
---
title: DS001
page_type: member
token: DS001
relationship: son
age_bracket: preteen
last_updated: 2026-04-05
compiled_from: [chat_abc123, chat_def456]
---

# DS001 (Son, Preteen)

## Summary

User's son, currently in middle school. Described as sensitive and creative. Shows signs of loyalty bind behavior since custody dispute began.

## Communication Style

- Prefers one-on-one time over group activities
- Opens up more during car rides (parallel attention)
- Shuts down when pressed for answers
- Uses art and games to express feelings indirectly

## Observed Patterns

### With User
- Affectionate when alone, withdrawn when sister present
- Asks about CP001's activities (checking for safety?)
- Has started using phrases that echo CP001's complaints (2026-03)

### With CP001
- User reports DS001 seems anxious before returns to CP001
- Has told user "I can't talk about that" regarding CP001's house

## Triggers

- Schedule changes without warning
- Being asked to choose activities
- Discussions about the divorce

## Strengths

- Creative problem solver
- Empathetic with younger children
- Strong reader, loves fantasy books

## User's Concerns

- Loyalty bind deepening
- Academic performance slipping
- Pulling away emotionally

## Key Moments

- **2026-02-15**: First time DS001 said "I don't want to come" (user devastated, worked through with Frank)
- **2026-03-20**: User used validation-first approach, DS001 opened up about pressure
- **2026-04-01**: Successful handoff despite CP001's late arrival

## See Also

- [[patterns/communication]] — How DS001 factors into co-parent exchanges
- [[patterns/custody]] — Current schedule and transition patterns
- [[DD001]] — Relationship with sibling
```

### 3.3 Family Wiki Meta Page (Clinical Formulation)

```markdown
---
title: Clinical Formulation
page_type: meta
auto_generated: true
last_updated: 2026-04-05
---

# Clinical Formulation

This page is auto-generated based on observed patterns. It biases Frank's responses without being visible to the user.

## Current Assessment

### Conflict Level: HIGH
- 4 hostile exchanges logged this month
- CP001 pattern: escalation around schedule changes
- Recent court filing has increased tension

### Safety Concerns: MODERATE
- No physical violence indicators
- Possible financial coercion (see chat_xyz789)
- No child safety concerns currently

### Coercive Control Indicators
- [x] Uses children as messengers
- [x] Makes unilateral schedule changes
- [x] Criticizes user's parenting to children
- [ ] Monitors user's communications
- [ ] Controls finances post-separation

### Child Development Context
- DS001: preteen, loyalty bind indicators PRESENT
- DD001: elementary, appears buffered from conflict

### Legal Status
- Court date: 2026-05-15
- GAL involvement: YES
- Current order: 50/50, week-on/week-off

## Recommended Response Biases

- **Tone**: Containment > Solutions
- **Techniques**: Prioritize gray rock, BIFF for co-parent chat
- **Cautions**: User may be over-documenting; watch for rumination
- **Strengths to reinforce**: Consistent presence, patience with DS001

## Progression Status

- **Days Active**: 67
- **Engagement**: Consistent (logged 5 of last 7 days)
- **Skills Practiced**: BIFF (12x), validation_first (8x), gray_rock (3x)
- **Current Level**: "Steady Navigator"
- **Next Unlock**: Court Prep chat (pending 5 more logins)
```

---

## 4. Wiki Compilation Service

### 4.1 Clinical Wiki Compilation (Trainer-Triggered)

```python
# services/wiki/clinical_compiler.py

class ClinicalWikiCompiler:
    """
    Compiles raw source documents into clinical wiki pages.
    Triggered by trainer upload or manual request.
    """
    
    def __init__(
        self,
        db: Session,
        llm_service: LLMService,
        embedding_service: EmbeddingService
    ):
        self.db = db
        self.llm = llm_service
        self.embeddings = embedding_service
    
    async def ingest_source(
        self,
        corpus_id: str,
        file_path: str,
        file_content: bytes,
        uploaded_by: UUID
    ) -> CompilationResult:
        """
        Process a new source document:
        1. Extract text
        2. Hash for deduplication
        3. Send to LLM for analysis
        4. Create/update wiki pages
        5. Log compilation
        """
        
        # 1. Extract text based on file type
        text = await self._extract_text(file_path, file_content)
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        
        # 2. Check for duplicate
        existing = self.db.query(WikiRawSource).filter(
            WikiRawSource.corpus_id == corpus_id,
            WikiRawSource.content_hash == content_hash
        ).first()
        
        if existing:
            return CompilationResult(
                status="skipped",
                message="Document already processed",
                source_id=existing.id
            )
        
        # 3. Store raw source
        source = WikiRawSource(
            corpus_id=corpus_id,
            filename=Path(file_path).name,
            file_type=Path(file_path).suffix.lstrip('.'),
            content_text=text,
            content_hash=content_hash,
            uploaded_by=uploaded_by,
            status="processing"
        )
        self.db.add(source)
        self.db.commit()
        
        # 4. Send to LLM for compilation
        try:
            pages = await self._compile_with_llm(corpus_id, text, source.id)
            source.status = "compiled"
            source.compiled_at = datetime.utcnow()
            source.generated_pages = [p.path for p in pages]
        except Exception as e:
            source.status = "failed"
            source.error_message = str(e)
            self.db.commit()
            raise
        
        # 5. Log compilation
        self._log_compilation(
            corpus_id=corpus_id,
            operation="ingest",
            source_id=source.id,
            pages_created=[p.path for p in pages if p.is_new],
            pages_updated=[p.path for p in pages if not p.is_new]
        )
        
        self.db.commit()
        
        return CompilationResult(
            status="success",
            source_id=source.id,
            pages_created=len([p for p in pages if p.is_new]),
            pages_updated=len([p for p in pages if not p.is_new])
        )
    
    async def _compile_with_llm(
        self,
        corpus_id: str,
        source_text: str,
        source_id: UUID
    ) -> List[WikiPage]:
        """
        Use LLM to extract wiki pages from source text.
        """
        
        # Load existing index to provide context
        existing_index = await self._get_index(corpus_id)
        
        prompt = f"""You are a clinical knowledge curator for FamilyBondBot.

Analyze this source document and extract wiki pages. For each distinct concept, 
technique, guardrail, or script you identify, create a wiki page.

## Existing Pages (for cross-referencing)
{existing_index}

## Source Document
{source_text}

## Instructions

1. Identify distinct knowledge units (concepts, techniques, guardrails, scripts)
2. For each unit, output a complete wiki page in markdown with YAML frontmatter
3. Use [[wikilinks]] to reference existing pages or new pages you're creating
4. Include triggers (phrases users might say that should surface this content)
5. Write in FBB's voice: warm, practical, non-clinical language

## Output Format

For each page, output:
```wiki
---
path: concepts/loyalty_binds
title: Loyalty Binds
page_type: concept
priority: 80
triggers: ["child says they hate me", "child doesn't want to come"]
---

[Page content in markdown]
```

Separate pages with `---PAGE_BREAK---`
"""
        
        response = await self.llm.generate(
            prompt=prompt,
            model="claude-sonnet-4-20250514",
            max_tokens=8000
        )
        
        # Parse response into pages
        pages = self._parse_pages(response.content, corpus_id, source_id)
        
        # Save pages and generate embeddings
        for page in pages:
            await self._save_page(page)
        
        return pages
```

### 4.2 Family Wiki Compilation (Frank-Triggered)

```python
# services/wiki/family_compiler.py

class FamilyWikiCompiler:
    """
    Compiles family context from chat history into wiki pages.
    Triggered after significant chat exchanges or on schedule.
    """
    
    COMPILATION_TRIGGERS = [
        "family_history_chat_complete",
        "significant_disclosure",
        "new_family_member_mentioned",
        "pattern_observed",
        "milestone_reached",
        "scheduled_daily"
    ]
    
    async def compile_after_chat(
        self,
        folder_id: UUID,
        chat_id: UUID,
        trigger: str
    ) -> CompilationResult:
        """
        Update family wiki based on recent chat.
        """
        
        # 1. Load current wiki state
        current_wiki = await self._load_wiki(folder_id)
        
        # 2. Load recent chat (tokenized)
        chat_content = await self._get_chat_transcript(chat_id)
        
        # 3. Send to Frank for wiki updates
        updates = await self._compile_with_frank(
            folder_id=folder_id,
            current_wiki=current_wiki,
            new_content=chat_content,
            trigger=trigger
        )
        
        # 4. Apply updates
        pages_created = []
        pages_updated = []
        
        for update in updates:
            if update.operation == "create":
                await self._create_page(folder_id, update.page)
                pages_created.append(update.page.path)
            elif update.operation == "update":
                await self._update_page(folder_id, update.page)
                pages_updated.append(update.page.path)
        
        # 5. Update meta/clinical_formulation.md
        await self._update_clinical_formulation(folder_id)
        
        # 6. Update meta/progression.md
        await self._update_progression(folder_id)
        
        # 7. Log
        self._log_compilation(
            folder_id=folder_id,
            operation="compile",
            source_type="chat",
            source_id=chat_id,
            pages_created=pages_created,
            pages_updated=pages_updated
        )
        
        return CompilationResult(
            status="success",
            pages_created=len(pages_created),
            pages_updated=len(pages_updated)
        )
    
    async def _compile_with_frank(
        self,
        folder_id: UUID,
        current_wiki: WikiState,
        new_content: str,
        trigger: str
    ) -> List[WikiUpdate]:
        """
        Frank analyzes new content and suggests wiki updates.
        """
        
        prompt = f"""You are Frank, maintaining a family wiki for this user.

## Current Wiki State
{current_wiki.to_summary()}

## New Content to Incorporate
{new_content}

## Trigger
This compilation was triggered by: {trigger}

## Instructions

Analyze the new content and determine what should be added or updated in the wiki.

For MEMBER pages (DS001, CP001, etc.):
- Update observed patterns
- Note new communication insights
- Record key moments
- Track triggers and strengths

For PATTERN pages:
- Identify recurring dynamics
- Note communication patterns
- Track custody/schedule patterns

For META pages:
- Update clinical formulation if risk levels change
- Update progression tracking

## Output Format

For each update:
```wiki_update
operation: create|update
path: members/DS001
reason: User disclosed new information about DS001's school anxiety
---
[Full page content or merged content]
```

Only output pages that need changes. If nothing needs updating, output:
```wiki_update
operation: none
reason: No significant updates needed
```
"""
        
        response = await self.llm.generate(
            prompt=prompt,
            model="claude-haiku-4-20250414",  # Haiku for efficiency
            max_tokens=4000
        )
        
        return self._parse_updates(response.content)
```

---

## 5. Wiki Retrieval Service

### 5.1 Retrieval for Prompt Assembly

```python
# services/wiki/retrieval_service.py

class WikiRetrievalService:
    """
    Retrieves relevant wiki pages for prompt assembly.
    Supports both clinical and family wikis.
    """
    
    async def get_context_for_message(
        self,
        message: str,
        folder_id: UUID,
        chat_type: str,
        corpus_id: str = "clinical-v1",
        max_clinical_pages: int = 5,
        max_family_pages: int = 4
    ) -> WikiContext:
        """
        Retrieve relevant wiki pages for a user message.
        
        Returns:
            WikiContext with clinical_pages, family_pages, and meta
        """
        
        # 1. Get clinical wiki pages
        clinical_pages = await self._get_clinical_pages(
            message=message,
            chat_type=chat_type,
            corpus_id=corpus_id,
            max_pages=max_clinical_pages
        )
        
        # 2. Get family wiki pages
        family_pages = await self._get_family_pages(
            message=message,
            folder_id=folder_id,
            max_pages=max_family_pages
        )
        
        # 3. Always include clinical formulation (meta)
        clinical_formulation = await self._get_page(
            folder_id=folder_id,
            path="meta/clinical_formulation"
        )
        
        # 4. Get progression status
        progression = await self._get_page(
            folder_id=folder_id,
            path="meta/progression"
        )
        
        return WikiContext(
            clinical_pages=clinical_pages,
            family_pages=family_pages,
            clinical_formulation=clinical_formulation,
            progression=progression
        )
    
    async def _get_clinical_pages(
        self,
        message: str,
        chat_type: str,
        corpus_id: str,
        max_pages: int
    ) -> List[WikiPage]:
        """
        Retrieve clinical wiki pages using hybrid approach:
        1. Always include guardrails for this chat type
        2. Semantic search over concepts/techniques
        3. Trigger matching
        """
        
        pages = []
        
        # 1. Guardrails (always included)
        guardrails = await self._get_guardrails(corpus_id, chat_type)
        pages.extend(guardrails)
        
        # 2. Trigger matching (exact phrase matches in frontmatter.triggers)
        trigger_matches = await self._match_triggers(
            message=message,
            corpus_id=corpus_id,
            chat_type=chat_type
        )
        pages.extend(trigger_matches)
        
        # 3. Semantic search if we have room
        remaining_slots = max_pages - len(pages)
        if remaining_slots > 0:
            message_embedding = await self.embedding_service.embed(message)
            semantic_matches = await self._semantic_search(
                embedding=message_embedding,
                corpus_id=corpus_id,
                chat_type=chat_type,
                exclude_paths=[p.path for p in pages],
                limit=remaining_slots
            )
            pages.extend(semantic_matches)
        
        # Deduplicate and sort by priority
        pages = self._dedupe_and_sort(pages)
        
        return pages[:max_pages]
    
    async def _get_family_pages(
        self,
        message: str,
        folder_id: UUID,
        max_pages: int
    ) -> List[WikiPage]:
        """
        Retrieve family wiki pages:
        1. Member pages for any tokens mentioned
        2. Pattern pages relevant to message
        3. Recent history entries
        """
        
        pages = []
        
        # 1. Extract tokens from message (DS001, CP001, etc.)
        tokens = self._extract_tokens(message)
        for token in tokens:
            member_page = await self._get_page(
                folder_id=folder_id,
                path=f"members/{token}"
            )
            if member_page:
                pages.append(member_page)
        
        # 2. Semantic match to pattern pages
        remaining_slots = max_pages - len(pages)
        if remaining_slots > 0:
            message_embedding = await self.embedding_service.embed(message)
            pattern_matches = await self._semantic_search_family(
                embedding=message_embedding,
                folder_id=folder_id,
                page_types=["pattern", "history"],
                limit=remaining_slots
            )
            pages.extend(pattern_matches)
        
        return pages[:max_pages]
```

### 5.2 Prompt Injection Format

```python
# services/wiki/prompt_formatter.py

class WikiPromptFormatter:
    """
    Formats wiki pages for injection into Frank's prompt.
    """
    
    def format_for_prompt(self, context: WikiContext) -> str:
        """
        Format wiki context for prompt assembly.
        """
        
        sections = []
        
        # 1. Clinical formulation (hidden from user, biases response)
        if context.clinical_formulation:
            sections.append(self._format_meta(context.clinical_formulation))
        
        # 2. Family context
        if context.family_pages:
            sections.append(self._format_family(context.family_pages))
        
        # 3. Clinical guardrails
        guardrails = [p for p in context.clinical_pages if p.page_type == 'guardrail']
        if guardrails:
            sections.append(self._format_guardrails(guardrails))
        
        # 4. Relevant concepts/techniques
        knowledge = [p for p in context.clinical_pages if p.page_type in ('concept', 'technique', 'script')]
        if knowledge:
            sections.append(self._format_knowledge(knowledge))
        
        # 5. Progression context
        if context.progression:
            sections.append(self._format_progression(context.progression))
        
        return "\n\n".join(sections)
    
    def _format_meta(self, page: WikiPage) -> str:
        return f"""=== INTERNAL CLINICAL CONTEXT (not visible to user) ===
{page.content}
"""
    
    def _format_family(self, pages: List[WikiPage]) -> str:
        content = "\n\n---\n\n".join([
            f"### {p.title}\n{self._extract_summary(p.content)}"
            for p in pages
        ])
        return f"""=== FAMILY CONTEXT ===
{content}
"""
    
    def _format_guardrails(self, pages: List[WikiPage]) -> str:
        rules = []
        for p in pages:
            # Extract just the key rules, not full content
            rules.extend(self._extract_rules(p.content))
        return f"""=== GUARDRAILS ===
{chr(10).join(f"- {r}" for r in rules)}
"""
    
    def _format_knowledge(self, pages: List[WikiPage]) -> str:
        content = "\n\n---\n\n".join([
            f"### {p.title}\n{self._extract_summary(p.content)}"
            for p in pages
        ])
        return f"""=== RELEVANT KNOWLEDGE ===
{content}
"""
    
    def _format_progression(self, page: WikiPage) -> str:
        # Extract just the key stats
        stats = self._extract_progression_stats(page.content)
        return f"""=== USER PROGRESSION ===
Days Active: {stats.get('days_active', 'unknown')}
Current Level: {stats.get('level', 'unknown')}
Recent Skills: {', '.join(stats.get('recent_skills', []))}
"""
```

---

## 6. API Endpoints

### 6.1 Wiki CRUD

```python
# api/wiki.py

router = APIRouter(prefix="/api/wiki", tags=["wiki"])

# ============ Clinical Wiki (Trainer Access) ============

@router.get("/clinical/{corpus_id}/pages")
async def list_clinical_pages(
    corpus_id: str,
    page_type: Optional[str] = None,
    current_user: User = Depends(get_current_trainer)
) -> List[WikiPageSummary]:
    """List all pages in clinical wiki."""
    pass

@router.get("/clinical/{corpus_id}/pages/{path:path}")
async def get_clinical_page(
    corpus_id: str,
    path: str,
    current_user: User = Depends(get_current_trainer)
) -> WikiPageDetail:
    """Get a single clinical wiki page with backlinks."""
    pass

@router.post("/clinical/{corpus_id}/pages")
async def create_clinical_page(
    corpus_id: str,
    page: WikiPageCreate,
    current_user: User = Depends(get_current_trainer)
) -> WikiPageDetail:
    """Create a new clinical wiki page."""
    pass

@router.put("/clinical/{corpus_id}/pages/{path:path}")
async def update_clinical_page(
    corpus_id: str,
    path: str,
    page: WikiPageUpdate,
    current_user: User = Depends(get_current_trainer)
) -> WikiPageDetail:
    """Update a clinical wiki page (creates new version)."""
    pass

@router.delete("/clinical/{corpus_id}/pages/{path:path}")
async def delete_clinical_page(
    corpus_id: str,
    path: str,
    current_user: User = Depends(get_current_trainer)
) -> dict:
    """Soft delete a clinical wiki page."""
    pass

@router.get("/clinical/{corpus_id}/pages/{path:path}/history")
async def get_page_history(
    corpus_id: str,
    path: str,
    current_user: User = Depends(get_current_trainer)
) -> List[WikiPageVersion]:
    """Get version history for a page."""
    pass

@router.get("/clinical/{corpus_id}/pages/{path:path}/backlinks")
async def get_page_backlinks(
    corpus_id: str,
    path: str,
    current_user: User = Depends(get_current_trainer)
) -> List[WikiPageSummary]:
    """Get pages that link to this page."""
    pass

# ============ Source Ingestion ============

@router.post("/clinical/{corpus_id}/ingest")
async def ingest_source(
    corpus_id: str,
    file: UploadFile,
    current_user: User = Depends(get_current_trainer)
) -> CompilationResult:
    """Upload and compile a source document."""
    pass

@router.get("/clinical/{corpus_id}/sources")
async def list_sources(
    corpus_id: str,
    current_user: User = Depends(get_current_trainer)
) -> List[WikiRawSourceSummary]:
    """List all ingested source documents."""
    pass

# ============ Search ============

@router.get("/clinical/{corpus_id}/search")
async def search_clinical_wiki(
    corpus_id: str,
    q: str,
    page_type: Optional[str] = None,
    limit: int = 20,
    current_user: User = Depends(get_current_trainer)
) -> List[WikiSearchResult]:
    """Full-text search over clinical wiki."""
    pass

# ============ Family Wiki (Admin View) ============

@router.get("/family/{folder_id}/pages")
async def list_family_pages(
    folder_id: UUID,
    current_user: User = Depends(get_current_admin)
) -> List[WikiPageSummary]:
    """List all pages in a family wiki (admin only)."""
    pass

@router.get("/family/{folder_id}/pages/{path:path}")
async def get_family_page(
    folder_id: UUID,
    path: str,
    current_user: User = Depends(get_current_admin)
) -> WikiPageDetail:
    """Get a single family wiki page (admin only)."""
    pass

# ============ Lint/Health Check ============

@router.post("/clinical/{corpus_id}/lint")
async def lint_wiki(
    corpus_id: str,
    current_user: User = Depends(get_current_trainer)
) -> LintResult:
    """Run health check on wiki: find contradictions, orphans, gaps."""
    pass
```

### 6.2 API Models

```python
# api/models/wiki.py

class WikiPageSummary(BaseModel):
    id: UUID
    path: str
    title: str
    page_type: str
    summary: Optional[str]
    updated_at: datetime
    
class WikiPageDetail(BaseModel):
    id: UUID
    path: str
    title: str
    page_type: str
    content: str
    frontmatter: dict
    outbound_links: List[str]
    backlinks: List[WikiPageSummary]
    version: int
    created_at: datetime
    updated_at: datetime
    updated_by: Optional[UUID]

class WikiPageCreate(BaseModel):
    path: str
    title: str
    page_type: str
    content: str
    
class WikiPageUpdate(BaseModel):
    title: Optional[str]
    content: str
    
class WikiSearchResult(BaseModel):
    page: WikiPageSummary
    snippet: str
    score: float

class CompilationResult(BaseModel):
    status: str  # 'success', 'skipped', 'failed'
    source_id: Optional[UUID]
    pages_created: int = 0
    pages_updated: int = 0
    message: Optional[str]

class LintResult(BaseModel):
    contradictions: List[dict]  # Pages with conflicting info
    orphans: List[str]          # Pages with no inbound links
    broken_links: List[dict]    # Links to non-existent pages
    gaps: List[str]             # Suggested pages to create
    stale: List[str]            # Pages not updated in 90+ days
```

---

## 7. Frontend: Wiki Explorer Component

### 7.1 Component Structure

```
components/wiki/
├── WikiExplorer.tsx        # Main layout (sidebar + editor)
├── WikiTree.tsx            # Folder tree navigation
├── WikiEditor.tsx          # Monaco editor + preview
├── WikiPage.tsx            # Page display (read mode)
├── WikiBacklinks.tsx       # "Referenced By" panel
├── WikiSearch.tsx          # Search overlay
├── WikiGraph.tsx           # Optional d3 graph view
├── WikiIngest.tsx          # Source upload dialog
└── hooks/
    ├── useWikiPages.ts     # Data fetching
    ├── useWikiLinks.ts     # Wikilink parsing
    └── useWikiSearch.ts    # Search functionality
```

### 7.2 Main Explorer Component

```tsx
// components/wiki/WikiExplorer.tsx

import React, { useState, useCallback } from 'react';
import { Box, Drawer, AppBar, Toolbar, IconButton, Typography } from '@mui/material';
import { Menu as MenuIcon, Add as AddIcon, Search as SearchIcon } from '@mui/icons-material';
import { WikiTree } from './WikiTree';
import { WikiEditor } from './WikiEditor';
import { WikiBacklinks } from './WikiBacklinks';
import { WikiSearch } from './WikiSearch';
import { useWikiPages } from './hooks/useWikiPages';

interface WikiExplorerProps {
  corpusId?: string;      // For clinical wiki
  folderId?: string;      // For family wiki
  readOnly?: boolean;     // Family wikis are read-only for admins
}

export const WikiExplorer: React.FC<WikiExplorerProps> = ({
  corpusId,
  folderId,
  readOnly = false
}) => {
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(true);
  
  const { pages, loading, refetch } = useWikiPages({ corpusId, folderId });
  
  const handlePageSelect = useCallback((path: string) => {
    setSelectedPath(path);
    setIsEditing(false);
  }, []);
  
  const handleWikiLink = useCallback((link: string) => {
    // Navigate to linked page
    const targetPath = resolveWikiLink(link, selectedPath);
    setSelectedPath(targetPath);
    setIsEditing(false);
  }, [selectedPath]);
  
  const handleSave = useCallback(async (content: string) => {
    if (!selectedPath) return;
    
    await updatePage(corpusId || folderId, selectedPath, content);
    setIsEditing(false);
    refetch();
  }, [selectedPath, corpusId, folderId, refetch]);
  
  const drawerWidth = 280;
  
  return (
    <Box sx={{ display: 'flex', height: '100%' }}>
      {/* Sidebar */}
      <Drawer
        variant="persistent"
        anchor="left"
        open={drawerOpen}
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            position: 'relative'
          }
        }}
      >
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="subtitle1" fontWeight={600}>
            {corpusId ? 'Clinical Wiki' : 'Family Wiki'}
          </Typography>
          <Box>
            <IconButton size="small" onClick={() => setSearchOpen(true)}>
              <SearchIcon />
            </IconButton>
            {!readOnly && (
              <IconButton size="small" onClick={() => handleCreatePage()}>
                <AddIcon />
              </IconButton>
            )}
          </Box>
        </Toolbar>
        
        <WikiTree
          pages={pages}
          selectedPath={selectedPath}
          onSelect={handlePageSelect}
          loading={loading}
        />
      </Drawer>
      
      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          height: '100%',
          overflow: 'hidden'
        }}
      >
        {selectedPath ? (
          <WikiEditor
            corpusId={corpusId}
            folderId={folderId}
            path={selectedPath}
            isEditing={isEditing}
            readOnly={readOnly}
            onEdit={() => setIsEditing(true)}
            onSave={handleSave}
            onCancel={() => setIsEditing(false)}
            onWikiLink={handleWikiLink}
          />
        ) : (
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            height: '100%',
            color: 'text.secondary'
          }}>
            <Typography>Select a page to view</Typography>
          </Box>
        )}
      </Box>
      
      {/* Backlinks Panel (collapsible) */}
      {selectedPath && (
        <WikiBacklinks
          corpusId={corpusId}
          folderId={folderId}
          path={selectedPath}
          onNavigate={handlePageSelect}
        />
      )}
      
      {/* Search Dialog */}
      <WikiSearch
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        corpusId={corpusId}
        folderId={folderId}
        onSelect={(path) => {
          handlePageSelect(path);
          setSearchOpen(false);
        }}
      />
    </Box>
  );
};
```

### 7.3 Wiki Editor with Wikilinks

```tsx
// components/wiki/WikiEditor.tsx

import React, { useState, useEffect, useCallback } from 'react';
import { Box, Button, Tabs, Tab, CircularProgress } from '@mui/material';
import Editor from '@monaco-editor/react';
import ReactMarkdown from 'react-markdown';
import { useWikiPage } from './hooks/useWikiPages';

interface WikiEditorProps {
  corpusId?: string;
  folderId?: string;
  path: string;
  isEditing: boolean;
  readOnly: boolean;
  onEdit: () => void;
  onSave: (content: string) => Promise<void>;
  onCancel: () => void;
  onWikiLink: (link: string) => void;
}

export const WikiEditor: React.FC<WikiEditorProps> = ({
  corpusId,
  folderId,
  path,
  isEditing,
  readOnly,
  onEdit,
  onSave,
  onCancel,
  onWikiLink
}) => {
  const { page, loading } = useWikiPage({ corpusId, folderId, path });
  const [content, setContent] = useState('');
  const [viewMode, setViewMode] = useState<'preview' | 'source'>('preview');
  const [saving, setSaving] = useState(false);
  
  useEffect(() => {
    if (page) {
      setContent(page.content);
    }
  }, [page]);
  
  const handleSave = useCallback(async () => {
    setSaving(true);
    try {
      await onSave(content);
    } finally {
      setSaving(false);
    }
  }, [content, onSave]);
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }
  
  if (!page) {
    return <Box sx={{ p: 2 }}>Page not found</Box>;
  }
  
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Toolbar */}
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        p: 1,
        borderBottom: 1,
        borderColor: 'divider'
      }}>
        <Tabs 
          value={viewMode} 
          onChange={(_, v) => setViewMode(v)}
          size="small"
        >
          <Tab value="preview" label="Preview" />
          <Tab value="source" label="Source" />
        </Tabs>
        
        <Box>
          {isEditing ? (
            <>
              <Button onClick={onCancel} sx={{ mr: 1 }}>
                Cancel
              </Button>
              <Button 
                variant="contained" 
                onClick={handleSave}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save'}
              </Button>
            </>
          ) : !readOnly && (
            <Button variant="outlined" onClick={onEdit}>
              Edit
            </Button>
          )}
        </Box>
      </Box>
      
      {/* Content */}
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        {isEditing || viewMode === 'source' ? (
          <Editor
            height="100%"
            language="markdown"
            value={content}
            onChange={(value) => setContent(value || '')}
            options={{
              readOnly: !isEditing,
              minimap: { enabled: false },
              wordWrap: 'on',
              lineNumbers: 'off',
              fontSize: 14,
              padding: { top: 16 }
            }}
          />
        ) : (
          <Box sx={{ p: 3, maxWidth: 800 }}>
            <WikiMarkdown 
              content={content}
              onWikiLink={onWikiLink}
            />
          </Box>
        )}
      </Box>
    </Box>
  );
};

// Custom markdown renderer with wikilink support
const WikiMarkdown: React.FC<{
  content: string;
  onWikiLink: (link: string) => void;
}> = ({ content, onWikiLink }) => {
  // Transform [[wikilinks]] to clickable elements
  const transformedContent = content.replace(
    /\[\[([^\]]+)\]\]/g,
    (_, link) => `[${link}](wiki:${link})`
  );
  
  return (
    <ReactMarkdown
      components={{
        a: ({ href, children }) => {
          if (href?.startsWith('wiki:')) {
            const link = href.replace('wiki:', '');
            return (
              <a
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  onWikiLink(link);
                }}
                style={{ 
                  color: '#3C6BFF',
                  textDecoration: 'none',
                  borderBottom: '1px dashed #3C6BFF'
                }}
              >
                {children}
              </a>
            );
          }
          return <a href={href}>{children}</a>;
        }
      }}
    >
      {transformedContent}
    </ReactMarkdown>
  );
};
```

### 7.4 Wiki Tree Component

```tsx
// components/wiki/WikiTree.tsx

import React, { useMemo } from 'react';
import { Box, List, ListItemButton, ListItemIcon, ListItemText, Collapse, Skeleton } from '@mui/material';
import { 
  Folder as FolderIcon, 
  FolderOpen as FolderOpenIcon,
  Description as PageIcon,
  ExpandMore,
  ChevronRight
} from '@mui/icons-material';

interface WikiTreeProps {
  pages: WikiPageSummary[];
  selectedPath: string | null;
  onSelect: (path: string) => void;
  loading: boolean;
}

interface TreeNode {
  name: string;
  path: string;
  isFolder: boolean;
  children: TreeNode[];
  page?: WikiPageSummary;
}

export const WikiTree: React.FC<WikiTreeProps> = ({
  pages,
  selectedPath,
  onSelect,
  loading
}) => {
  const [expanded, setExpanded] = React.useState<Set<string>>(new Set(['concepts', 'techniques', 'members', 'patterns']));
  
  // Build tree structure from flat page list
  const tree = useMemo(() => {
    const root: TreeNode[] = [];
    const folders: Record<string, TreeNode> = {};
    
    // Sort pages by path
    const sortedPages = [...pages].sort((a, b) => a.path.localeCompare(b.path));
    
    for (const page of sortedPages) {
      const parts = page.path.split('/');
      
      if (parts.length === 1) {
        // Root level page
        root.push({
          name: page.title,
          path: page.path,
          isFolder: false,
          children: [],
          page
        });
      } else {
        // Nested page - ensure folder exists
        const folderPath = parts.slice(0, -1).join('/');
        
        if (!folders[folderPath]) {
          folders[folderPath] = {
            name: parts[parts.length - 2],
            path: folderPath,
            isFolder: true,
            children: []
          };
          root.push(folders[folderPath]);
        }
        
        folders[folderPath].children.push({
          name: page.title,
          path: page.path,
          isFolder: false,
          children: [],
          page
        });
      }
    }
    
    return root;
  }, [pages]);
  
  const toggleFolder = (path: string) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };
  
  if (loading) {
    return (
      <Box sx={{ p: 2 }}>
        {[1, 2, 3, 4, 5].map(i => (
          <Skeleton key={i} height={36} sx={{ my: 0.5 }} />
        ))}
      </Box>
    );
  }
  
  const renderNode = (node: TreeNode, depth: number = 0) => {
    const isExpanded = expanded.has(node.path);
    const isSelected = selectedPath === node.path;
    
    if (node.isFolder) {
      return (
        <React.Fragment key={node.path}>
          <ListItemButton
            onClick={() => toggleFolder(node.path)}
            sx={{ pl: 2 + depth * 2 }}
          >
            <ListItemIcon sx={{ minWidth: 32 }}>
              {isExpanded ? <FolderOpenIcon fontSize="small" /> : <FolderIcon fontSize="small" />}
            </ListItemIcon>
            <ListItemText 
              primary={node.name}
              primaryTypographyProps={{ 
                variant: 'body2',
                fontWeight: 500,
                textTransform: 'capitalize'
              }}
            />
            {isExpanded ? <ExpandMore fontSize="small" /> : <ChevronRight fontSize="small" />}
          </ListItemButton>
          
          <Collapse in={isExpanded}>
            <List disablePadding>
              {node.children.map(child => renderNode(child, depth + 1))}
            </List>
          </Collapse>
        </React.Fragment>
      );
    }
    
    return (
      <ListItemButton
        key={node.path}
        selected={isSelected}
        onClick={() => onSelect(node.path)}
        sx={{ pl: 2 + depth * 2 }}
      >
        <ListItemIcon sx={{ minWidth: 32 }}>
          <PageIcon fontSize="small" color={isSelected ? 'primary' : 'action'} />
        </ListItemIcon>
        <ListItemText 
          primary={node.name}
          primaryTypographyProps={{ 
            variant: 'body2',
            noWrap: true
          }}
        />
      </ListItemButton>
    );
  };
  
  return (
    <List sx={{ overflow: 'auto', flexGrow: 1 }}>
      {tree.map(node => renderNode(node))}
    </List>
  );
};
```

---

## 8. Gamification Integration

### 8.1 Progression Page (Auto-Generated)

The `meta/progression.md` page in each family wiki tracks gamification state:

```markdown
---
title: Progression
page_type: meta
auto_generated: true
last_updated: 2026-04-06
---

# User Progression

## Current Status

- **Days Active**: 67
- **Current Level**: Steady Navigator (Level 2)
- **XP Total**: 1,340
- **Current Streak**: 5 days

## Skills Practiced

| Skill | Times Used | Last Used | Proficiency |
|-------|------------|-----------|-------------|
| BIFF Response | 12 | 2026-04-05 | ⭐⭐⭐ |
| Validation First | 8 | 2026-04-04 | ⭐⭐ |
| Gray Rock | 3 | 2026-03-28 | ⭐ |
| Reframe Rejection | 2 | 2026-04-01 | ⭐ |

## Badges Earned

- 🏅 **First Boundary** (2026-02-20): Set first clear limit with CP001
- 🏅 **Steady Presence** (2026-03-15): 30 consecutive days active
- 🏅 **Reframe Artist** (2026-04-01): Recognized loyalty bind unprompted

## Chat Types Unlocked

- [x] General
- [x] Family History
- [x] Co-Parent
- [x] Parent-Child
- [ ] Court Prep (unlock: 5 more logins)
- [ ] Interaction Debrief (unlock: log 3 interactions)

## Hidden Features Available

Based on wiki content, these features are now relevant:
- **Faith & Spirituality**: User mentioned church pressure (patterns/triggers.md)

## XP Log (Last 7 Days)

| Date | Action | XP |
|------|--------|-----|
| 2026-04-06 | Daily check-in | +10 |
| 2026-04-05 | Completed Co-Parent chat | +25 |
| 2026-04-05 | Used BIFF technique | +15 |
| 2026-04-04 | Logged interaction | +20 |
| ... | ... | ... |
```

### 8.2 Progression Service

```python
# services/gamification/progression_service.py

class ProgressionService:
    """
    Manages user progression based on wiki state.
    """
    
    LEVELS = [
        {"name": "Emerging Co-Parent", "xp": 0},
        {"name": "Steady Navigator", "xp": 500},
        {"name": "Conflict Alchemist", "xp": 2000},
        {"name": "Family Guardian", "xp": 5000}
    ]
    
    BADGES = {
        "first_boundary": {
            "name": "First Boundary",
            "description": "Set first clear limit with co-parent",
            "wiki_trigger": "patterns/communication.md contains 'set.*boundary|limit'"
        },
        "steady_presence": {
            "name": "Steady Presence", 
            "description": "30 consecutive days active",
            "condition": "streak >= 30"
        },
        "reframe_artist": {
            "name": "Reframe Artist",
            "description": "Recognized loyalty bind without prompting",
            "wiki_trigger": "user message contains 'loyalty bind' before Frank mentions it"
        },
        "gray_rock_graduate": {
            "name": "Gray Rock Graduate",
            "description": "3+ non-reactive responses to baiting",
            "wiki_trigger": "patterns/communication.md shows 3+ gray rock successes"
        }
    }
    
    CHAT_UNLOCKS = {
        "GENERAL": {"default": True},
        "FAMILY_HISTORY": {"default": True},
        "CO_PARENT": {"days_active": 3},
        "PARENT_CHILD": {"days_active": 3},
        "COURT_PREP": {"days_active": 14, "xp": 500},
        "INTERACTION_DEBRIEF": {"interactions_logged": 3}
    }
    
    async def calculate_progression(self, folder_id: UUID) -> ProgressionState:
        """
        Calculate current progression state from wiki.
        """
        
        # Load family wiki
        wiki = await self.wiki_service.load_wiki(folder_id)
        
        # Calculate XP
        xp = await self._calculate_xp(folder_id)
        
        # Determine level
        level = self._get_level(xp)
        
        # Check badges
        earned_badges = await self._check_badges(wiki, folder_id)
        
        # Check unlocks
        unlocked_chats = await self._check_unlocks(folder_id, xp)
        
        # Check hidden features
        available_features = await self._check_hidden_features(wiki)
        
        return ProgressionState(
            xp=xp,
            level=level,
            badges=earned_badges,
            unlocked_chats=unlocked_chats,
            available_features=available_features
        )
    
    async def update_progression_page(self, folder_id: UUID):
        """
        Update meta/progression.md with current state.
        """
        
        state = await self.calculate_progression(folder_id)
        
        content = self._render_progression_page(state)
        
        await self.wiki_service.update_page(
            folder_id=folder_id,
            path="meta/progression",
            content=content,
            auto_generated=True
        )
    
    async def _check_badges(
        self, 
        wiki: WikiState, 
        folder_id: UUID
    ) -> List[Badge]:
        """
        Check wiki content for badge triggers.
        """
        
        earned = []
        
        for badge_id, badge_def in self.BADGES.items():
            if "wiki_trigger" in badge_def:
                if self._check_wiki_trigger(wiki, badge_def["wiki_trigger"]):
                    earned.append(Badge(
                        id=badge_id,
                        name=badge_def["name"],
                        earned_at=await self._get_badge_earned_date(folder_id, badge_id)
                    ))
            elif "condition" in badge_def:
                if await self._check_condition(folder_id, badge_def["condition"]):
                    earned.append(Badge(
                        id=badge_id,
                        name=badge_def["name"],
                        earned_at=await self._get_badge_earned_date(folder_id, badge_id)
                    ))
        
        return earned
    
    async def _check_hidden_features(self, wiki: WikiState) -> List[str]:
        """
        Check wiki for triggers that should surface hidden features.
        """
        
        features = []
        
        # Faith & Spirituality
        if self._wiki_mentions(wiki, ["church", "faith", "pray", "forgive", "God"]):
            features.append("faith_spirituality")
        
        # LGBTQIA+
        if self._wiki_mentions(wiki, ["gender identity", "transition", "same-sex", "LGBTQ"]):
            features.append("lgbtqia")
        
        # Safety & Abuse
        if self._wiki_mentions(wiki, ["abuse", "violence", "threatened", "afraid", "safety"]):
            features.append("safety_abuse")
        
        return features
```

---

## 9. Migration Path

### 9.1 Phase 1: Schema + API (Week 1)

1. Create `wiki_pages`, `wiki_compilation_log`, `wiki_raw_sources` tables
2. Implement CRUD API endpoints
3. Basic WikiExplorer component (tree + editor, no backlinks)

### 9.2 Phase 2: Clinical Wiki Seeding (Week 2)

1. Migrate existing content entities to wiki pages
2. Build source ingestion flow (Amy's chapters)
3. Trainer can view/edit clinical wiki
4. Wire retrieval service to use wiki instead of/alongside RAG

### 9.3 Phase 3: Family Wiki Compilation (Week 3)

1. Build FamilyWikiCompiler service
2. Post-chat compilation hook
3. Admin view for family wikis (read-only)
4. Wire family wiki into prompt assembly

### 9.4 Phase 4: Gamification Integration (Week 4)

1. Progression page auto-generation
2. Badge trigger system
3. Chat type unlock logic
4. Hidden feature surfacing

### 9.5 Phase 5: Polish (Week 5)

1. Graph view (optional)
2. Search improvements
3. Version history UI
4. Lint/health check UI

---

## 10. Acceptance Criteria

### 10.1 Clinical Wiki

- [ ] Trainer can view all clinical wiki pages in tree view
- [ ] Trainer can create new pages with path, title, content
- [ ] Trainer can edit existing pages (creates new version)
- [ ] Wikilinks `[[page_name]]` render as clickable links
- [ ] Backlinks panel shows "Referenced By" pages
- [ ] Source upload compiles document into wiki pages
- [ ] Search returns relevant pages with snippets
- [ ] Version history shows previous versions with diffs

### 10.2 Family Wiki

- [ ] Family wiki auto-created on first chat
- [ ] Member pages created when family members mentioned
- [ ] Pattern pages updated based on observed behaviors
- [ ] Clinical formulation page reflects current assessment
- [ ] Progression page tracks XP, badges, unlocks
- [ ] Admin can view (read-only) any family wiki

### 10.3 Retrieval

- [ ] Wiki pages injected into Frank's prompt
- [ ] Guardrails always included for chat type
- [ ] Relevant concepts/techniques retrieved by trigger match
- [ ] Family context included from member/pattern pages
- [ ] Token budget respected (wiki content truncated if needed)

### 10.4 Gamification

- [ ] XP calculated from engagement metrics
- [ ] Level determined by XP thresholds
- [ ] Badges awarded based on wiki triggers
- [ ] Chat types unlock based on progression
- [ ] Hidden features surface based on wiki content

---

## 11. Open Questions

1. **Embedding strategy**: Generate embeddings for all wiki pages, or rely on index + trigger matching?
2. **Token budget allocation**: How many tokens for clinical wiki vs family wiki vs history?
3. **Compilation frequency**: After every chat, or batch nightly?
4. **Version retention**: Keep all versions forever, or prune after N versions?
5. **Graph view priority**: V1 or defer to V2?

---

## 12. Appendix: Wikilink Resolution

```typescript
// utils/wikilinks.ts

/**
 * Parse wikilinks from markdown content.
 * Returns array of link targets.
 */
export function parseWikilinks(content: string): string[] {
  const regex = /\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g;
  const links: string[] = [];
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1].trim());
  }
  
  return [...new Set(links)]; // Dedupe
}

/**
 * Resolve a wikilink to a full path.
 * Handles relative links and aliases.
 */
export function resolveWikiLink(link: string, currentPath: string): string {
  // If link contains /, treat as absolute path
  if (link.includes('/')) {
    return link.toLowerCase().replace(/\s+/g, '_');
  }
  
  // Otherwise, try to find matching page
  // This would query the API in practice
  return link.toLowerCase().replace(/\s+/g, '_');
}

/**
 * Transform wikilinks to markdown links for rendering.
 */
export function transformWikilinks(
  content: string, 
  linkPrefix: string = 'wiki:'
): string {
  return content.replace(
    /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,
    (_, target, display) => {
      const text = display || target;
      const href = `${linkPrefix}${target.trim().toLowerCase().replace(/\s+/g, '_')}`;
      return `[${text}](${href})`;
    }
  );
}
```

---

**Spec Version:** 1.0
**Author:** Claude (with Dave)
**Review Required:** Amy (clinical page schema), Dave (architecture approval)
