"""
vectors_core
============

Entity vector core - data model and helper functions.

This module provides:
- Helper functions for event queries, SLA lookups, profile upserts
- Cold-start cascade for entity vectors
- Confidence computation
- Global vector aggregation across domains

Dependencies:
- import logging
- import math
- from datetime import datetime, timedelta
- from typing import Optional, Tuple, List, Dict, Any
- from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, text
- from sqlalchemy.orm import Session
- from simdecisions.database import Base

Classes:
- EntityProfile: SQLAlchemy model for entity profile vectors.
- EntityComponent: SQLAlchemy model for entity components.
- EntitySLAConfig: SQLAlchemy model for SLA targets per domain.
- EntityVectorHistory: SQLAlchemy model for entity vector history.

Functions:
- _fetch_events(entity_id: str,
    event_types: List[str],
    db: Session,
    days: int = 30,
    domain: Optional[str] = None): Fetch events from Event Ledger with 30-day decay window.
- _get_sla_target(domain: str, db: Session): Get SLA target for domain.
- _get_entity_prompt(entity_id: str, db: Session): Get entity system prompt.
- _upsert_profile(entity_id: str,
    domain: str,
    vector_name: str,
    value: float,
    confidence: float,
    source: str,
    db: Session): Upsert EntityProfile record.
- _upsert_component(entity_id: str,
    component_type: str,
    system_prompt: Optional[str],
    metadata: Dict[str, Any],
    db: Session): Upsert EntityComponent record.
- get_entity_vector(entity_id: str,
    domain: str,
    vector_name: str,
    db: Session): Get entity vector with cold-start cascade.
- compute_global_vector(entity_id: str,
    vector_name: str,
    db: Session): Compute global vector (confidence-weighted average across domains).
- compute_confidence(sample_size: int, source: str): Compute confidence score from sample size and source.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
