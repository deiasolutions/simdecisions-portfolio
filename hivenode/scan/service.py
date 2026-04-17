"""
service
=======

SCAN service layer for fetching and processing external data.

Dependencies:
- from datetime import datetime, timedelta
- from typing import List, Optional
- from sqlalchemy.orm import Session
- from .models import ScanSource, ScanItem, ScanDigest
- from .adapters import SourceAdapter, RSSAdapter, ArxivAdapter, HackerNewsAdapter, GitHubTrendingAdapter
- from hivenode.ledger.emitter import emit_event
- from hivenode.config import settings

Classes:
- ScanService: Service for fetching and processing external data.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
