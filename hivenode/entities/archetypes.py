"""
archetypes
==========

Domain Archetype Model + Tribunal Logic — ADR-003 TASK-043

Provides:
- DomainArchetype ORM model (SQLite-compatible)
- ArchetypeCandidate and ConsensusResult dataclasses
- Four consensus methods (A: majority, B: weighted avg, C: LLM synthesis, D: human select)
- hash_embedding for deterministic test embeddings (no external service needed)
- cosine_similarity, serialize/deserialize helpers
- generate_archetype, get_current_archetype, check_drift management functions

Method C uses a real LLM provider (claude by default) to synthesize a unified archetype
from all candidate texts.  Falls back to concatenation when no API key is configured.

Dependencies:
- from all candidate texts.  Falls back to concatenation when no API key is configured.
- import hashlib
- import json
- import logging
- import math
- from dataclasses import dataclass
- from typing import Optional
- from sqlalchemy import Column, String, Float, Integer, DateTime, LargeBinary, func
- from sqlalchemy.orm import Session
- from pydantic import BaseModel, ConfigDict

Classes:
- DomainArchetype: Generate deterministic embedding from text hash. For testing only.

Functions:
- hash_embedding(text: str, dim: int = 64): Generate deterministic embedding from text hash. For testing only.
- cosine_similarity(a: list[float], b: list[float]): Cosine similarity between two vectors. Returns value in [-1, 1].
- serialize_embedding(embedding: list[float]): Serialize float list to bytes for DB storage.
- deserialize_embedding(data: bytes): Deserialize bytes to float list.
- consensus_method_a(candidates: list[ArchetypeCandidate]): Majority text selection: pick the candidate whose embedding has
- consensus_method_b(candidates: list[ArchetypeCandidate]): Weighted average of embeddings.
- _synthesize_archetype_stub(candidates: list[ArchetypeCandidate]): Fallback synthesis: concatenate all candidate texts separated by ' | '.
- consensus_method_c(candidates: list[ArchetypeCandidate]): LLM synthesis: calls Claude to synthesize a unified archetype from all candidate texts.
- consensus_method_d(candidates: list[ArchetypeCandidate], selected_index: int = 0): Human selects candidate by index.
- generate_archetype(domain: str,
    candidates: list[ArchetypeCandidate],
    method: str = "A",
    db: Optional[Session] = None,): Run consensus on candidates, save to DB, mark as current.
- get_current_archetype(domain: str, db: Optional[Session] = None): Get the current archetype for a domain.
- check_drift(domain: str,
    new_embedding: list[float],
    threshold: float = 0.3,
    db: Optional[Session] = None,): Check if new embedding deviates from current archetype beyond threshold.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
