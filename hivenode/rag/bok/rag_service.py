"""
rag_service
===========

RAG service for BOK keyword search and prompt enrichment.

Dependencies:
- from typing import List, Tuple
- from sqlalchemy.orm import Session

Functions:
- search_bok(query: str, db: Session, limit: int = 5): Search BOK entries using keyword matching.
- format_bok_for_prompt(entries: List): Format BOK entries as markdown for inclusion in prompts.
- enrich_prompt(base_prompt: str,
    query: str,
    db: Session,
    max_entries: int = 3): Enrich a base prompt with relevant BOK entries.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
