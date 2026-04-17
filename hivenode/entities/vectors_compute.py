"""
vectors_compute
===============

Entity vector computation - alpha, sigma, rho, pi_bot, pi_human.

This module provides:
- compute_alpha: Autonomy score (internal vs external signals)
- compute_sigma: Quality score (outcome × (1 - rework))
- compute_rho: Reliability score (SLA adherence)
- compute_pi_bot: Bot preference (cosine similarity to domain archetype)
- compute_pi_human: Human preference (observed claim rate or declared)
- recalculate_entity: Full recalculation of all vectors

Dependencies:
- import logging
- from datetime import datetime
- from typing import Tuple, Dict, Any
- from collections import defaultdict
- from sqlalchemy.orm import Session
- from hivenode.entities.vectors_core import (
- from hivenode.entities.embeddings import compute_pi_bot_full

Functions:
- compute_alpha(entity_id: str, domain: str, db: Session): Compute alpha (autonomy score).
- compute_sigma(entity_id: str, domain: str, db: Session): Compute sigma (quality score).
- compute_rho(entity_id: str, domain: str, db: Session): Compute rho (reliability score).
- compute_pi_bot(entity_id: str, domain: str, db: Session): Compute pi_bot (bot preference).
- compute_pi_human(entity_id: str, domain: str, db: Session): Compute pi_human (human preference).
- recalculate_entity(entity_id: str, domain: str, db: Session): Recalculate all vectors for entity in domain.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
