"""
routes
======

Terminal API routes.

Dependencies:
- from pathlib import Path
- from typing import List, Optional
- from fastapi import APIRouter, HTTPException, status, Depends
- from pydantic import BaseModel, Field
- from hivenode.terminal import store
- from hivenode.terminal.tfidf_index import TFIDFIndex
- from hivenode.dependencies import verify_jwt_or_local

Classes:
- SuggestRequest: Runtime context for context-aware weighting.
- SuggestWeightedRequest: Request for context-weighted suggestions.

Functions:
- get_index(): Get or create TF-IDF index.
- init_index(data_dir: Path): Initialize index and set persistence path.
- save_index(): Save index to disk.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
