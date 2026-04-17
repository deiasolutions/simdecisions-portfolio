# SPEC-AUDIT-FIX-001: Capability Activation & SCAN Pillar Build

**Spec ID:** SPEC-AUDIT-FIX-001
**Created:** 2026-04-14
**Status:** READY
**Priority:** P0
**Depends On:** None (quick wins are standalone)
**Audit Source:** AUDIT-CAPABILITY-2026-04-14.md

---

## Executive Summary

This spec addresses all findings from the 2026-04-14 capability audit:

1. **Wave 0:** Activate built capabilities (1-line changes, wiring)
2. **Wave 1:** SCAN pillar — external data ingestion (RSS, arXiv, HackerNews, GitHub)
3. **Wave 2:** Daily Briefing automation

Total estimate: 3-5 days across all waves.

---

## Wave 0: Quick Wins (Same Day)

### 0.1 Mount RAG Routes

**File:** `hivenode/main.py`

**Change:**
```python
# Add import
from hivenode.rag.routes import router as rag_router

# Add to router includes (after wiki_router)
app.include_router(rag_router, prefix="/api/rag", tags=["rag"])
```

**Acceptance:**
- [ ] `GET /api/rag/search?q=test` returns 200 (empty or results)
- [ ] `GET /api/rag/status` returns index stats

---

### 0.2 Deploy WikiPane

**File:** `browser/sets/wiki.set.md` (new)

```markdown
---
id: wiki
name: Wiki
description: Knowledge base viewer and editor
layout: single
---

panes:
  - id: wiki-main
    appType: wiki
    position: { x: 0, y: 0, w: 12, h: 12 }
    config:
      showBacklinks: true
      showHistory: true
```

**Acceptance:**
- [ ] WikiPane renders at route `/set/wiki`
- [ ] Can view existing pages (core, intro, advanced)
- [ ] Backlinks panel shows inbound links

---

### 0.3 Wire Wiki Event Emission

**File:** `hivenode/wiki/routes.py`

**Changes:**

```python
# Add import at top
from hivenode.ledger.writer import emit_event

# In create_page() after successful insert:
await emit_event(
    kind="PAGE_CREATED",
    actor={"id": "system", "type": "system"},
    target={"id": str(page.id), "type": "wiki_page", "path": page.path},
    context={
        "title": page.title,
        "workspace_id": str(page.workspace_id),
        "page_type": page.page_type
    }
)

# In update_page() after successful update:
await emit_event(
    kind="PAGE_UPDATED",
    actor={"id": "system", "type": "system"},
    target={"id": str(page.id), "type": "wiki_page", "path": page.path},
    context={
        "title": page.title,
        "version": page.version,
        "changes": "content_updated"
    }
)

# In delete_page() after soft delete:
await emit_event(
    kind="PAGE_DELETED",
    actor={"id": "system", "type": "system"},
    target={"id": str(page.id), "type": "wiki_page", "path": page.path},
    context={}
)
```

**Acceptance:**
- [ ] Create page → `PAGE_CREATED` event in ledger
- [ ] Update page → `PAGE_UPDATED` event in ledger
- [ ] Delete page → `PAGE_DELETED` event in ledger

---

### 0.4 Populate Wiki Edit Log

**File:** `hivenode/wiki/routes.py`

**Changes:**

```python
# In update_page() after version increment:
edit_log = WikiEditLog(
    page_id=page.id,
    version=page.version,
    edited_by=None,  # TODO: wire to auth
    edit_type="update",
    diff_summary=f"Updated content ({len(content)} chars)"
)
db.add(edit_log)
```

**Acceptance:**
- [ ] Update page → row in `wiki_edit_log` table
- [ ] `GET /api/wiki/pages/{id}/history` returns edit log entries

---

## Wave 1: SCAN Pillar — External Data Ingestion

### 1.1 Database Schema

**File:** `hivenode/scan/models.py` (new)

```python
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import JSONB
from hivenode.database import Base
from datetime import datetime

class ScanSource(Base):
    """External data source configuration."""
    __tablename__ = "scan_sources"
    
    id = Column(String(50), primary_key=True)  # rss-techcrunch, arxiv-cs-ai, hn-top, gh-trending
    source_type = Column(String(20), nullable=False)  # rss, arxiv, hackernews, github
    name = Column(String(100), nullable=False)
    url = Column(String(500))  # Feed URL or API endpoint
    config = Column(JSON, default={})  # Source-specific config
    
    is_active = Column(Boolean, default=True)
    poll_interval_minutes = Column(Integer, default=60)
    last_polled_at = Column(DateTime)
    last_error = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanItem(Base):
    """Individual item from an external source."""
    __tablename__ = "scan_items"
    
    id = Column(String(100), primary_key=True)  # source_id + item_id hash
    source_id = Column(String(50), nullable=False)
    
    # Content
    title = Column(String(500), nullable=False)
    url = Column(String(1000))
    content = Column(Text)  # Summary or full text
    author = Column(String(200))
    
    # Metadata
    external_id = Column(String(200))  # Original ID from source
    published_at = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    
    # Processing
    is_processed = Column(Boolean, default=False)
    is_relevant = Column(Boolean)  # LLM relevance score
    relevance_score = Column(Integer)  # 0-100
    relevance_reason = Column(Text)
    tags = Column(JSON, default=[])
    
    # Embedding
    content_embedding = Column(JSON)  # Vector for search (or use pgvector)


class ScanDigest(Base):
    """Daily/periodic digest of scan items."""
    __tablename__ = "scan_digests"
    
    id = Column(String(50), primary_key=True)  # YYYY-MM-DD or YYYY-MM-DD-HH
    digest_type = Column(String(20), default="daily")  # daily, weekly, adhoc
    
    # Content
    summary = Column(Text)  # LLM-generated summary
    top_items = Column(JSON, default=[])  # List of item IDs
    item_count = Column(Integer, default=0)
    
    # Delivery
    delivered_at = Column(DateTime)
    delivered_via = Column(String(50))  # efemera, email, wiki
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Migration:**
```sql
CREATE TABLE scan_sources (
    id VARCHAR(50) PRIMARY KEY,
    source_type VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(500),
    config JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    poll_interval_minutes INTEGER DEFAULT 60,
    last_polled_at TIMESTAMPTZ,
    last_error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE scan_items (
    id VARCHAR(100) PRIMARY KEY,
    source_id VARCHAR(50) NOT NULL REFERENCES scan_sources(id),
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000),
    content TEXT,
    author VARCHAR(200),
    external_id VARCHAR(200),
    published_at TIMESTAMPTZ,
    fetched_at TIMESTAMPTZ DEFAULT NOW(),
    is_processed BOOLEAN DEFAULT FALSE,
    is_relevant BOOLEAN,
    relevance_score INTEGER,
    relevance_reason TEXT,
    tags JSONB DEFAULT '[]',
    content_embedding JSONB
);

CREATE INDEX idx_scan_items_source ON scan_items(source_id);
CREATE INDEX idx_scan_items_published ON scan_items(published_at DESC);
CREATE INDEX idx_scan_items_relevant ON scan_items(is_relevant) WHERE is_relevant = TRUE;

CREATE TABLE scan_digests (
    id VARCHAR(50) PRIMARY KEY,
    digest_type VARCHAR(20) DEFAULT 'daily',
    summary TEXT,
    top_items JSONB DEFAULT '[]',
    item_count INTEGER DEFAULT 0,
    delivered_at TIMESTAMPTZ,
    delivered_via VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

### 1.2 Source Adapters

**File:** `hivenode/scan/adapters/__init__.py`

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class ScanResult:
    external_id: str
    title: str
    url: Optional[str]
    content: Optional[str]
    author: Optional[str]
    published_at: Optional[datetime]
    metadata: dict = None

class SourceAdapter(ABC):
    """Base adapter for external data sources."""
    
    @abstractmethod
    async def fetch(self, since: datetime = None) -> List[ScanResult]:
        """Fetch items from source, optionally since a timestamp."""
        ...
    
    @abstractmethod
    def source_type(self) -> str:
        """Return source type identifier."""
        ...
```

**File:** `hivenode/scan/adapters/rss.py`

```python
import feedparser
from datetime import datetime
from typing import List
from .base import SourceAdapter, ScanResult

class RSSAdapter(SourceAdapter):
    """Adapter for RSS/Atom feeds."""
    
    def __init__(self, feed_url: str, config: dict = None):
        self.feed_url = feed_url
        self.config = config or {}
    
    def source_type(self) -> str:
        return "rss"
    
    async def fetch(self, since: datetime = None) -> List[ScanResult]:
        feed = feedparser.parse(self.feed_url)
        
        results = []
        for entry in feed.entries:
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            
            if since and published and published < since:
                continue
            
            results.append(ScanResult(
                external_id=entry.get('id', entry.link),
                title=entry.title,
                url=entry.link,
                content=entry.get('summary', ''),
                author=entry.get('author', ''),
                published_at=published,
                metadata={"feed_title": feed.feed.get('title', '')}
            ))
        
        return results
```

**File:** `hivenode/scan/adapters/arxiv.py`

```python
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
from .base import SourceAdapter, ScanResult

class ArxivAdapter(SourceAdapter):
    """Adapter for arXiv API."""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, categories: List[str], max_results: int = 50, config: dict = None):
        self.categories = categories  # e.g., ["cs.AI", "cs.LG", "cs.CL"]
        self.max_results = max_results
        self.config = config or {}
    
    def source_type(self) -> str:
        return "arxiv"
    
    async def fetch(self, since: datetime = None) -> List[ScanResult]:
        # Build query
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
        
        params = {
            "search_query": cat_query,
            "start": 0,
            "max_results": self.max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
        
        # Parse Atom XML
        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
        
        results = []
        for entry in root.findall("atom:entry", ns):
            published_str = entry.find("atom:published", ns).text
            published = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            
            if since and published < since:
                continue
            
            # Get authors
            authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
            
            # Get categories
            categories = [c.get("term") for c in entry.findall("atom:category", ns)]
            
            results.append(ScanResult(
                external_id=entry.find("atom:id", ns).text,
                title=entry.find("atom:title", ns).text.strip(),
                url=entry.find("atom:id", ns).text.replace("abs", "pdf"),
                content=entry.find("atom:summary", ns).text.strip(),
                author=", ".join(authors[:3]) + ("..." if len(authors) > 3 else ""),
                published_at=published,
                metadata={"categories": categories, "all_authors": authors}
            ))
        
        return results
```

**File:** `hivenode/scan/adapters/hackernews.py`

```python
import httpx
from datetime import datetime
from typing import List
from .base import SourceAdapter, ScanResult

class HackerNewsAdapter(SourceAdapter):
    """Adapter for HackerNews API."""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self, story_type: str = "top", max_results: int = 30, config: dict = None):
        self.story_type = story_type  # top, new, best
        self.max_results = max_results
        self.config = config or {}
    
    def source_type(self) -> str:
        return "hackernews"
    
    async def fetch(self, since: datetime = None) -> List[ScanResult]:
        async with httpx.AsyncClient() as client:
            # Get story IDs
            response = await client.get(f"{self.BASE_URL}/{self.story_type}stories.json")
            story_ids = response.json()[:self.max_results]
            
            results = []
            for story_id in story_ids:
                story_response = await client.get(f"{self.BASE_URL}/item/{story_id}.json")
                story = story_response.json()
                
                if not story or story.get("type") != "story":
                    continue
                
                published = datetime.fromtimestamp(story.get("time", 0))
                
                if since and published < since:
                    continue
                
                results.append(ScanResult(
                    external_id=str(story_id),
                    title=story.get("title", ""),
                    url=story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    content=story.get("text", ""),  # For Ask HN, Show HN
                    author=story.get("by", ""),
                    published_at=published,
                    metadata={
                        "score": story.get("score", 0),
                        "comments": story.get("descendants", 0),
                        "hn_url": f"https://news.ycombinator.com/item?id={story_id}"
                    }
                ))
        
        return results
```

**File:** `hivenode/scan/adapters/github.py`

```python
import httpx
from datetime import datetime
from typing import List
from .base import SourceAdapter, ScanResult

class GitHubTrendingAdapter(SourceAdapter):
    """Adapter for GitHub trending repos (unofficial API)."""
    
    # Using github-trending-api or scraping
    TRENDING_URL = "https://api.gitterapp.com/repositories"  # Example unofficial API
    
    def __init__(self, language: str = None, since: str = "daily", config: dict = None):
        self.language = language  # python, typescript, etc.
        self.since = since  # daily, weekly, monthly
        self.config = config or {}
    
    def source_type(self) -> str:
        return "github"
    
    async def fetch(self, since_dt: datetime = None) -> List[ScanResult]:
        params = {"since": self.since}
        if self.language:
            params["language"] = self.language
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.TRENDING_URL, params=params)
            repos = response.json()
        
        results = []
        for repo in repos[:30]:
            results.append(ScanResult(
                external_id=repo.get("url", ""),
                title=f"{repo.get('author')}/{repo.get('name')}",
                url=repo.get("url"),
                content=repo.get("description", ""),
                author=repo.get("author", ""),
                published_at=None,  # Trending doesn't have publish date
                metadata={
                    "stars": repo.get("stars", 0),
                    "forks": repo.get("forks", 0),
                    "language": repo.get("language", ""),
                    "stars_today": repo.get("currentPeriodStars", 0)
                }
            ))
        
        return results
```

---

### 1.3 SCAN Service

**File:** `hivenode/scan/service.py`

```python
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from .models import ScanSource, ScanItem, ScanDigest
from .adapters import SourceAdapter, RSSAdapter, ArxivAdapter, HackerNewsAdapter, GitHubTrendingAdapter
from hivenode.ledger.writer import emit_event

ADAPTER_MAP = {
    "rss": RSSAdapter,
    "arxiv": ArxivAdapter,
    "hackernews": HackerNewsAdapter,
    "github": GitHubTrendingAdapter
}

class ScanService:
    """Service for fetching and processing external data."""
    
    def __init__(self, db: Session, llm_adapter=None):
        self.db = db
        self.llm_adapter = llm_adapter
    
    def get_adapter(self, source: ScanSource) -> SourceAdapter:
        """Create adapter for a source."""
        adapter_class = ADAPTER_MAP.get(source.source_type)
        if not adapter_class:
            raise ValueError(f"Unknown source type: {source.source_type}")
        
        if source.source_type == "rss":
            return RSSAdapter(source.url, source.config)
        elif source.source_type == "arxiv":
            return ArxivAdapter(
                categories=source.config.get("categories", ["cs.AI"]),
                max_results=source.config.get("max_results", 50),
                config=source.config
            )
        elif source.source_type == "hackernews":
            return HackerNewsAdapter(
                story_type=source.config.get("story_type", "top"),
                max_results=source.config.get("max_results", 30),
                config=source.config
            )
        elif source.source_type == "github":
            return GitHubTrendingAdapter(
                language=source.config.get("language"),
                since=source.config.get("since", "daily"),
                config=source.config
            )
    
    async def poll_source(self, source_id: str) -> int:
        """Poll a single source, return count of new items."""
        source = self.db.query(ScanSource).get(source_id)
        if not source or not source.is_active:
            return 0
        
        adapter = self.get_adapter(source)
        since = source.last_polled_at
        
        try:
            results = await adapter.fetch(since=since)
            
            new_count = 0
            for result in results:
                item_id = f"{source_id}:{result.external_id}"
                
                # Skip if exists
                if self.db.query(ScanItem).get(item_id):
                    continue
                
                item = ScanItem(
                    id=item_id,
                    source_id=source_id,
                    title=result.title,
                    url=result.url,
                    content=result.content,
                    author=result.author,
                    external_id=result.external_id,
                    published_at=result.published_at
                )
                self.db.add(item)
                new_count += 1
            
            source.last_polled_at = datetime.utcnow()
            source.last_error = None
            self.db.commit()
            
            await emit_event(
                kind="SCAN_POLL_COMPLETE",
                target={"id": source_id, "type": "scan_source"},
                context={"new_items": new_count, "total_fetched": len(results)}
            )
            
            return new_count
            
        except Exception as e:
            source.last_error = str(e)
            self.db.commit()
            raise
    
    async def poll_all_sources(self) -> dict:
        """Poll all active sources."""
        sources = self.db.query(ScanSource).filter(ScanSource.is_active == True).all()
        
        results = {}
        for source in sources:
            # Check if poll interval has passed
            if source.last_polled_at:
                next_poll = source.last_polled_at + timedelta(minutes=source.poll_interval_minutes)
                if datetime.utcnow() < next_poll:
                    continue
            
            try:
                count = await self.poll_source(source.id)
                results[source.id] = {"status": "ok", "new_items": count}
            except Exception as e:
                results[source.id] = {"status": "error", "error": str(e)}
        
        return results
    
    async def score_relevance(self, item_id: str) -> int:
        """Use LLM to score item relevance to Q88N's interests."""
        if not self.llm_adapter:
            return 50  # Default neutral score
        
        item = self.db.query(ScanItem).get(item_id)
        if not item:
            return 0
        
        prompt = f"""Score the relevance of this item to someone interested in:
- AI/ML infrastructure and governance
- Process simulation and execution engines
- Enterprise software architecture
- Startup building and product development
- Developer tools and productivity

Title: {item.title}
Content: {item.content[:1000] if item.content else 'No content'}
Source: {item.source_id}

Return a JSON object:
{{"score": 0-100, "reason": "brief explanation", "tags": ["tag1", "tag2"]}}
"""
        
        response = await self.llm_adapter.call(
            prompt=prompt,
            model="haiku",
            max_tokens=200
        )
        
        import json
        try:
            result = json.loads(response.content)
            item.relevance_score = result.get("score", 50)
            item.relevance_reason = result.get("reason", "")
            item.tags = result.get("tags", [])
            item.is_relevant = item.relevance_score >= 60
            item.is_processed = True
            self.db.commit()
            return item.relevance_score
        except:
            item.is_processed = True
            item.relevance_score = 50
            self.db.commit()
            return 50
    
    async def generate_digest(self, digest_type: str = "daily") -> ScanDigest:
        """Generate a digest of recent relevant items."""
        if digest_type == "daily":
            since = datetime.utcnow() - timedelta(days=1)
            digest_id = datetime.utcnow().strftime("%Y-%m-%d")
        elif digest_type == "weekly":
            since = datetime.utcnow() - timedelta(days=7)
            digest_id = datetime.utcnow().strftime("%Y-W%W")
        else:
            since = datetime.utcnow() - timedelta(hours=4)
            digest_id = datetime.utcnow().strftime("%Y-%m-%d-%H")
        
        # Get relevant items
        items = self.db.query(ScanItem).filter(
            ScanItem.fetched_at >= since,
            ScanItem.is_relevant == True
        ).order_by(ScanItem.relevance_score.desc()).limit(20).all()
        
        if not items:
            return None
        
        # Generate summary with LLM
        items_text = "\n".join([
            f"- [{item.title}]({item.url}) (score: {item.relevance_score}, source: {item.source_id})"
            for item in items
        ])
        
        summary = ""
        if self.llm_adapter:
            prompt = f"""Summarize these items for a daily briefing. Group by theme. Be concise.

Items:
{items_text}

Write a 3-5 paragraph summary highlighting the most important developments."""
            
            response = await self.llm_adapter.call(
                prompt=prompt,
                model="sonnet",
                max_tokens=500
            )
            summary = response.content
        
        digest = ScanDigest(
            id=digest_id,
            digest_type=digest_type,
            summary=summary,
            top_items=[item.id for item in items],
            item_count=len(items)
        )
        
        self.db.merge(digest)
        self.db.commit()
        
        await emit_event(
            kind="SCAN_DIGEST_GENERATED",
            target={"id": digest_id, "type": "scan_digest"},
            context={"item_count": len(items), "digest_type": digest_type}
        )
        
        return digest
```

---

### 1.4 SCAN Routes

**File:** `hivenode/scan/routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from hivenode.database import get_db
from .models import ScanSource, ScanItem, ScanDigest
from .service import ScanService

router = APIRouter()

# --- Sources ---

@router.get("/sources")
async def list_sources(db: Session = Depends(get_db)):
    """List all scan sources."""
    sources = db.query(ScanSource).all()
    return {"sources": [
        {
            "id": s.id,
            "name": s.name,
            "source_type": s.source_type,
            "is_active": s.is_active,
            "last_polled_at": s.last_polled_at,
            "last_error": s.last_error
        }
        for s in sources
    ]}

@router.post("/sources")
async def create_source(
    id: str,
    name: str,
    source_type: str,
    url: str = None,
    config: dict = None,
    db: Session = Depends(get_db)
):
    """Create a new scan source."""
    source = ScanSource(
        id=id,
        name=name,
        source_type=source_type,
        url=url,
        config=config or {}
    )
    db.add(source)
    db.commit()
    return {"created": id}

@router.post("/sources/{source_id}/poll")
async def poll_source(source_id: str, db: Session = Depends(get_db)):
    """Manually trigger poll for a source."""
    service = ScanService(db)
    try:
        count = await service.poll_source(source_id)
        return {"polled": source_id, "new_items": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/poll-all")
async def poll_all_sources(db: Session = Depends(get_db)):
    """Poll all active sources."""
    service = ScanService(db)
    results = await service.poll_all_sources()
    return {"results": results}

# --- Items ---

@router.get("/items")
async def list_items(
    source_id: Optional[str] = None,
    is_relevant: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List scan items with filters."""
    query = db.query(ScanItem)
    
    if source_id:
        query = query.filter(ScanItem.source_id == source_id)
    if is_relevant is not None:
        query = query.filter(ScanItem.is_relevant == is_relevant)
    
    items = query.order_by(ScanItem.fetched_at.desc()).offset(offset).limit(limit).all()
    
    return {"items": [
        {
            "id": item.id,
            "source_id": item.source_id,
            "title": item.title,
            "url": item.url,
            "author": item.author,
            "published_at": item.published_at,
            "relevance_score": item.relevance_score,
            "tags": item.tags
        }
        for item in items
    ]}

@router.get("/items/{item_id}")
async def get_item(item_id: str, db: Session = Depends(get_db)):
    """Get a single item with full content."""
    item = db.query(ScanItem).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/{item_id}/score")
async def score_item(item_id: str, db: Session = Depends(get_db)):
    """Score item relevance using LLM."""
    service = ScanService(db)  # TODO: inject LLM adapter
    score = await service.score_relevance(item_id)
    return {"item_id": item_id, "score": score}

# --- Digests ---

@router.get("/digests")
async def list_digests(limit: int = 10, db: Session = Depends(get_db)):
    """List recent digests."""
    digests = db.query(ScanDigest).order_by(ScanDigest.created_at.desc()).limit(limit).all()
    return {"digests": [
        {
            "id": d.id,
            "digest_type": d.digest_type,
            "item_count": d.item_count,
            "created_at": d.created_at,
            "delivered_at": d.delivered_at
        }
        for d in digests
    ]}

@router.get("/digests/{digest_id}")
async def get_digest(digest_id: str, db: Session = Depends(get_db)):
    """Get a digest with summary."""
    digest = db.query(ScanDigest).get(digest_id)
    if not digest:
        raise HTTPException(status_code=404, detail="Digest not found")
    return digest

@router.post("/digests/generate")
async def generate_digest(digest_type: str = "daily", db: Session = Depends(get_db)):
    """Generate a new digest."""
    service = ScanService(db)  # TODO: inject LLM adapter
    digest = await service.generate_digest(digest_type)
    if not digest:
        return {"status": "no_items", "message": "No relevant items found"}
    return {"generated": digest.id, "item_count": digest.item_count}
```

---

### 1.5 Default Sources

**File:** `hivenode/scan/defaults.py`

```python
"""Default scan sources for DEIA hive."""

DEFAULT_SOURCES = [
    {
        "id": "arxiv-cs-ai",
        "name": "arXiv CS.AI",
        "source_type": "arxiv",
        "config": {
            "categories": ["cs.AI", "cs.LG", "cs.CL", "cs.MA"],
            "max_results": 50
        },
        "poll_interval_minutes": 360  # 6 hours
    },
    {
        "id": "hn-top",
        "name": "HackerNews Top",
        "source_type": "hackernews",
        "config": {
            "story_type": "top",
            "max_results": 30
        },
        "poll_interval_minutes": 60
    },
    {
        "id": "gh-trending-python",
        "name": "GitHub Trending Python",
        "source_type": "github",
        "config": {
            "language": "python",
            "since": "daily"
        },
        "poll_interval_minutes": 360
    },
    {
        "id": "gh-trending-typescript",
        "name": "GitHub Trending TypeScript",
        "source_type": "github",
        "config": {
            "language": "typescript",
            "since": "daily"
        },
        "poll_interval_minutes": 360
    },
    {
        "id": "rss-anthropic",
        "name": "Anthropic Blog",
        "source_type": "rss",
        "url": "https://www.anthropic.com/feed.xml",
        "poll_interval_minutes": 360
    },
    {
        "id": "rss-openai",
        "name": "OpenAI Blog",
        "source_type": "rss",
        "url": "https://openai.com/blog/rss.xml",
        "poll_interval_minutes": 360
    },
    {
        "id": "rss-deepmind",
        "name": "DeepMind Blog",
        "source_type": "rss",
        "url": "https://deepmind.com/blog/feed/basic/",
        "poll_interval_minutes": 360
    }
]
```

---

### 1.6 SCAN Daemon

**File:** `hivenode/scan/daemon.py`

```python
"""Background daemon for SCAN polling."""

import asyncio
from datetime import datetime
from sqlalchemy.orm import Session

from hivenode.database import SessionLocal
from .service import ScanService
from .defaults import DEFAULT_SOURCES
from .models import ScanSource

async def init_default_sources(db: Session):
    """Initialize default sources if not present."""
    for source_config in DEFAULT_SOURCES:
        if not db.query(ScanSource).get(source_config["id"]):
            source = ScanSource(**source_config)
            db.add(source)
    db.commit()

async def poll_loop(interval_minutes: int = 15):
    """Main polling loop."""
    db = SessionLocal()
    
    # Init defaults
    await init_default_sources(db)
    
    service = ScanService(db)
    
    while True:
        print(f"[SCAN] Polling all sources at {datetime.utcnow()}")
        try:
            results = await service.poll_all_sources()
            print(f"[SCAN] Poll complete: {results}")
        except Exception as e:
            print(f"[SCAN] Poll error: {e}")
        
        await asyncio.sleep(interval_minutes * 60)

async def scoring_loop(interval_minutes: int = 30):
    """Background loop to score unprocessed items."""
    db = SessionLocal()
    service = ScanService(db)  # TODO: inject LLM adapter
    
    while True:
        # Get unprocessed items
        items = db.query(ScanItem).filter(
            ScanItem.is_processed == False
        ).limit(20).all()
        
        for item in items:
            try:
                await service.score_relevance(item.id)
            except Exception as e:
                print(f"[SCAN] Scoring error for {item.id}: {e}")
        
        await asyncio.sleep(interval_minutes * 60)

async def digest_loop():
    """Generate daily digest at 6 AM."""
    db = SessionLocal()
    service = ScanService(db)
    
    while True:
        now = datetime.utcnow()
        # Wait until 6 AM
        if now.hour == 6 and now.minute < 5:
            try:
                digest = await service.generate_digest("daily")
                if digest:
                    print(f"[SCAN] Generated daily digest: {digest.id}")
            except Exception as e:
                print(f"[SCAN] Digest error: {e}")
        
        await asyncio.sleep(300)  # Check every 5 minutes

def start_scan_daemon():
    """Start all SCAN background loops."""
    loop = asyncio.get_event_loop()
    loop.create_task(poll_loop())
    loop.create_task(scoring_loop())
    loop.create_task(digest_loop())
```

---

### 1.7 Mount SCAN Routes

**File:** `hivenode/main.py` (addition)

```python
# Add import
from hivenode.scan.routes import router as scan_router
from hivenode.scan.daemon import start_scan_daemon

# Add to router includes
app.include_router(scan_router, prefix="/api/scan", tags=["scan"])

# In startup event
@app.on_event("startup")
async def startup():
    # ... existing startup code ...
    start_scan_daemon()
```

---

## Wave 2: Daily Briefing Automation

### 2.1 Briefing Template

**File:** `.wiki/templates/daily-briefing.md`

```markdown
---
title: Daily Briefing - {{date}}
page_type: briefing
generated_at: {{timestamp}}
---

# Daily Briefing: {{date}}

## SCAN Digest

{{scan_summary}}

### Top Items

{{#each top_items}}
- [{{title}}]({{url}}) — {{source}} (relevance: {{score}})
{{/each}}

## Hive Status

- **Tasks Completed:** {{tasks_completed}}
- **Tasks In Progress:** {{tasks_in_progress}}
- **Specs Queued:** {{specs_queued}}

## Event Ledger Highlights

{{#each ledger_highlights}}
- {{kind}}: {{summary}}
{{/each}}

## Action Items

{{action_items}}

---

*Generated by SCAN daemon at {{timestamp}}*
```

### 2.2 Briefing Generator

**File:** `hivenode/briefing/generator.py`

```python
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from hivenode.scan.models import ScanDigest, ScanItem
from hivenode.wiki.store import WikiPage
from hivenode.ledger.reader import LedgerReader

class BriefingGenerator:
    """Generate daily briefings combining SCAN, hive status, and ledger."""
    
    def __init__(self, db: Session, ledger: LedgerReader, llm_adapter=None):
        self.db = db
        self.ledger = ledger
        self.llm_adapter = llm_adapter
    
    async def generate(self) -> str:
        """Generate today's briefing."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Get SCAN digest
        digest = self.db.query(ScanDigest).get(today)
        scan_summary = digest.summary if digest else "No SCAN digest available."
        
        # Get top items
        top_items = []
        if digest and digest.top_items:
            items = self.db.query(ScanItem).filter(
                ScanItem.id.in_(digest.top_items[:10])
            ).all()
            top_items = [
                {"title": i.title, "url": i.url, "source": i.source_id, "score": i.relevance_score}
                for i in items
            ]
        
        # Get hive status from ledger
        since = datetime.utcnow() - timedelta(days=1)
        events = await self.ledger.query(since=since)
        
        tasks_completed = len([e for e in events if e["kind"] == "TASK_COMPLETED"])
        tasks_in_progress = len([e for e in events if e["kind"] == "TASK_STARTED"]) - tasks_completed
        specs_queued = len([e for e in events if e["kind"] == "SPEC_QUEUED"])
        
        # Get ledger highlights
        highlights = []
        important_kinds = ["BUILD_COMPLETE", "DEPLOY_COMPLETE", "ERROR", "ESCALATION"]
        for event in events:
            if event["kind"] in important_kinds:
                highlights.append({"kind": event["kind"], "summary": event.get("context", {}).get("summary", "")})
        
        # Generate action items with LLM
        action_items = ""
        if self.llm_adapter:
            prompt = f"""Based on this briefing data, suggest 3-5 action items for today:

SCAN Summary: {scan_summary}
Tasks Completed: {tasks_completed}
Tasks In Progress: {tasks_in_progress}
Specs Queued: {specs_queued}

Be specific and actionable."""
            
            response = await self.llm_adapter.call(prompt=prompt, model="haiku", max_tokens=300)
            action_items = response.content
        
        # Render template
        briefing = f"""# Daily Briefing: {today}

## SCAN Digest

{scan_summary}

### Top Items

"""
        for item in top_items:
            briefing += f"- [{item['title']}]({item['url']}) — {item['source']} (relevance: {item['score']})\n"
        
        briefing += f"""
## Hive Status

- **Tasks Completed:** {tasks_completed}
- **Tasks In Progress:** {tasks_in_progress}
- **Specs Queued:** {specs_queued}

## Event Ledger Highlights

"""
        for h in highlights:
            briefing += f"- {h['kind']}: {h['summary']}\n"
        
        briefing += f"""
## Action Items

{action_items}

---

*Generated at {datetime.utcnow().isoformat()}*
"""
        
        return briefing
    
    async def save_to_wiki(self, content: str) -> WikiPage:
        """Save briefing as wiki page."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        page = WikiPage(
            path=f"briefings/{today}",
            title=f"Daily Briefing - {today}",
            content=content,
            page_type="briefing"
        )
        
        self.db.merge(page)
        self.db.commit()
        return page
    
    async def deliver_via_efemera(self, content: str):
        """Send briefing via efemera channel."""
        # TODO: wire to efemera relay
        pass
```

### 2.3 Briefing Route

**File:** `hivenode/briefing/routes.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from hivenode.database import get_db
from .generator import BriefingGenerator

router = APIRouter()

@router.get("/today")
async def get_today_briefing(db: Session = Depends(get_db)):
    """Get or generate today's briefing."""
    generator = BriefingGenerator(db, None)  # TODO: inject ledger, LLM
    content = await generator.generate()
    return {"briefing": content}

@router.post("/generate")
async def generate_briefing(save_to_wiki: bool = True, db: Session = Depends(get_db)):
    """Generate and optionally save briefing."""
    generator = BriefingGenerator(db, None)
    content = await generator.generate()
    
    if save_to_wiki:
        page = await generator.save_to_wiki(content)
        return {"generated": True, "wiki_path": page.path}
    
    return {"generated": True, "content": content}
```

---

## Acceptance Criteria

### Wave 0 (Quick Wins)
- [ ] `GET /api/rag/search` returns 200
- [ ] WikiPane renders at `/set/wiki`
- [ ] Wiki CRUD emits PAGE_* events to ledger
- [ ] `wiki_edit_log` populated on updates

### Wave 1 (SCAN Pillar)
- [ ] 7 default sources configured
- [ ] `POST /api/scan/poll-all` fetches from all sources
- [ ] Items stored in `scan_items` table
- [ ] Relevance scoring with LLM works
- [ ] `GET /api/scan/digests/today` returns daily digest
- [ ] SCAN daemon runs on hivenode startup

### Wave 2 (Daily Briefing)
- [ ] `GET /api/briefing/today` returns combined briefing
- [ ] Briefing saved to wiki at `briefings/YYYY-MM-DD`
- [ ] Briefing includes SCAN + hive status + action items

---

## Dependencies

```
# requirements.txt additions
feedparser>=6.0.0
httpx>=0.24.0
```

---

## Estimated Effort

| Wave | Tasks | Hours |
|------|-------|-------|
| Wave 0 | 4 quick wins | 2-4 |
| Wave 1 | SCAN pillar | 16-24 |
| Wave 2 | Daily briefing | 8-12 |
| **Total** | | **26-40** |

---

## Migration Path

1. **Deploy Wave 0** — Same day, minimal risk
2. **Deploy Wave 1** — Run migrations, mount routes, start daemon
3. **Deploy Wave 2** — After SCAN is producing digests

---

**Spec Version:** 1.0
**Author:** Q88N × Q33NR
