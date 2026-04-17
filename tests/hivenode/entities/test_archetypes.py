"""
test_archetypes
===============

TDD Tests for Domain Archetype Tribunal — ADR-003 TASK-043

Tests cover:
1.  DomainArchetype ORM CRUD
2.  hash_embedding produces consistent results
3.  cosine_similarity of identical vectors = 1.0
4.  cosine_similarity of orthogonal vectors ~ 0
5.  consensus_method_a picks most representative
6.  consensus_method_b averages embeddings
7.  consensus_method_d selects by index
8.  generate_archetype saves to DB and marks current
9.  generate_archetype marks previous as non-current
10. get_current_archetype returns latest
11. check_drift detects deviation above threshold
12. check_drift returns false for similar embedding
13. POST /api/domains/{domain}/archetype/refresh creates archetype
14. GET /api/domains/{domain}/archetype returns current
15. GET /api/domains/{domain}/archetype/history returns history
16. serialize/deserialize embedding round-trip

Dependencies:
- import pytest
- from fastapi.testclient import TestClient
- from hivenode.main import app
- from simdecisions.database import SessionLocal
- from hivenode.entities.archetypes import (

Functions:
- db_session(): Provide a clean database session with domain_archetypes table emptied.
- client(): FastAPI test client with domain_archetypes cleaned before/after.
- _make_candidates(texts: list[str], provider: str = "stub"): Helper to build ArchetypeCandidate list from texts.
- test_domain_archetype_crud(db_session): Create, read, update, delete a DomainArchetype row.
- test_hash_embedding_consistent(): Same text always produces the same embedding.
- test_cosine_similarity_identical(): Identical vectors have cosine similarity of 1.0.
- test_cosine_similarity_orthogonal(): Orthogonal vectors have cosine similarity of 0.
- test_consensus_method_a_picks_most_representative(): Method A selects the candidate with highest avg similarity to others.
- test_consensus_method_a_single_candidate(): Method A with single candidate returns it with confidence=1.0.
- test_consensus_method_b_averages_embeddings(): Method B produces an averaged embedding and picks nearest text.
- test_consensus_method_b_single_candidate(): Method B with single candidate returns it directly.
- test_consensus_method_d_selects_by_index(): Method D returns the candidate at the selected index.
- test_consensus_method_d_out_of_range(): Method D raises IndexError for invalid index.
- test_generate_archetype_saves_to_db(db_session): generate_archetype creates a record in the database.
- test_generate_archetype_marks_previous_non_current(db_session): When generating a new archetype, previous ones become is_current=0.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
