"""
embeddings
==========

Bot embedding system with drift detection.

This module provides:
- Bot profile embedding cache (SQLAlchemy ORM)
- Pi (preference) computation for domain + task alignment
- Drift detection (cosine similarity threshold)
- Bot profile registration

Dependencies:
- import hashlib
- import logging
- import pickle
- from datetime import datetime
- from typing import Optional
- from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
- from sqlalchemy.orm import Session
- from simdecisions.database import Base
- from hivenode.entities.voyage_embedding import get_embedding

Classes:
- BotEmbeddingStore: SQLAlchemy model for bot embedding cache.

Functions:
- cosine_similarity(vec1: list[float], vec2: list[float]): Compute cosine similarity between two vectors.
- get_or_compute_bot_embedding(entity_id: str, system_prompt: str, db: Session): Get cached bot embedding or compute new one.
- _get_domain_archetype_embedding(domain: str): Get domain archetype embedding (hardcoded for now).
- compute_pi_bot_full(entity_id: str,
    domain: str,
    system_prompt: str,
    task_text: Optional[str] = None,
    db: Optional[Session] = None,): Compute pi (bot preference) for domain + task alignment.
- check_bot_drift(entity_id: str,
    new_system_prompt: str,
    threshold: float = 0.3,
    db: Optional[Session] = None,): Check if bot prompt has drifted from cached baseline.
- register_bot_profile(entity_id: str,
    system_prompt: str,
    model_id: Optional[str] = None,
    db: Optional[Session] = None,): Register bot profile (cache embedding).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
