"""
models
======

Data models for RAG indexer.

This module defines the complete data model for indexing artifacts in the RAG system.
Ported from platform/efemera/src/efemera/indexer/models.py.

Dependencies:
- from datetime import datetime
- from enum import Enum
- from typing import Optional
- from uuid import uuid4
- from pydantic import BaseModel, Field

Classes:
- ArtifactType: Type of artifact being indexed.
- StorageTier: Storage tier for artifact data.
- IRStatus: Status of intent-result pair verification.
- CCCMetadata: Clock, Coin, Carbon metadata per harness spec section 9.
- IRPair: Intent-Result pair for capability tracking.
- Chunk: A logical chunk of artifact content for indexing.
- IRSummary: Summary statistics for IR pairs in an artifact.
- ReliabilityMetadata: Load/failure tracking metadata for artifact reliability.
- ReliabilityMetrics: Reliability metrics for an artifact.
- RelevanceMetadata: Relevance metrics tracking artifact usage.
- RelevanceMetrics: Relevance metrics tracking artifact usage (legacy name).
- StalenessMetadata: Information about artifact freshness.
- StalenessInfo: Information about artifact freshness (legacy name).
- ProvenanceMetadata: Provenance tracking for artifact origin.
- ProvenanceInfo: Provenance tracking for artifact origin (legacy name).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
