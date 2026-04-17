"""
embedder
========

Lazy singleton embedder for RAG system.

Uses sentence-transformers all-MiniLM-L6-v2 (384-dim).
Returns 503 if sentence-transformers is not installed.

Also provides TFIDFEmbedder for lightweight local embeddings.

Dependencies:
- import math
- import os
- import re
- from collections import Counter
- from typing import Any

Classes:
- TFIDFEmbedder: TF-IDF embedder for lightweight local embeddings without LLM API calls.

Functions:
- is_available(): Check if sentence-transformers is importable.
- get_model(): Get or create the singleton SentenceTransformer model.
- embed_texts(texts: list[str]): Embed a batch of texts into vectors.
- reset(): Reset the singleton (for testing).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
