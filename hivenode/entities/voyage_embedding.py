"""
voyage_embedding
================

Voyage AI embedding client with fallback to hash-based embeddings.

This module provides a production embedding client for Voyage AI with:
- In-memory LRU cache (maxsize=1000)
- Automatic fallback to hash-based embeddings when API key not set
- Robust error handling (timeout, connection errors, HTTP errors)

Dependencies:
- import hashlib
- import logging
- import os
- from functools import lru_cache
- from typing import Optional
- import requests

Functions:
- hash_embedding(text: str, dimension: int = 1024): Generate hash-based embedding as fallback.
- _get_cache_key(text: str, model: str): Generate cache key for LRU cache.
- _get_embedding_cached(cache_key: str, text: str, model: str): Cached embedding function (internal).
- get_embedding(text: str, model: Optional[str] = None): Get embedding for text from Voyage AI or fallback.
- clear_cache(): Clear LRU cache.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
