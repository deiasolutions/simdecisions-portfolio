"""
indexer
=======

Repository file indexer with SQLite backend.

Dependencies:
- import hashlib
- import sqlite3
- import time
- import base64
- from pathlib import Path
- from datetime import datetime, timezone
- from hivenode.repo.gitignore import GitignoreParser
- from hivenode.repo.schemas import (

Classes:
- RepoIndexer: Indexes repository files into SQLite database.

Functions:
- _find_repo_root(start_path: Path | None = None): Walk up from current file until .git/ is found.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
