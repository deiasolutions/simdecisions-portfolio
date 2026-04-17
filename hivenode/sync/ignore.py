"""
ignore
======

Sync Ignore Patterns

Gitignore-style pattern matching for sync exclusions:
- Always skip: .git/, node_modules/, __pycache__/
- Custom patterns from sync_ignore file
- Supports glob patterns, directory anchoring, negation

Dependencies:
- import os
- from typing import Optional
- import pathspec

Functions:
- load_ignore_patterns(ignore_file_path: Optional[str]): Load ignore patterns from file.
- should_sync(path: str, patterns: pathspec.PathSpec): Check if a path should be synced.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
