"""
models
======

SCAN database models - external data source ingestion.

Dependencies:
- from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean
- from sqlalchemy.dialects.postgresql import JSONB
- from sqlalchemy.types import JSON
- from sqlalchemy.ext.declarative import declarative_base
- from datetime import datetime

Classes:
- ScanSource: External data source configuration.
- ScanItem: Individual item from an external source.
- ScanDigest: Daily/periodic digest of scan items.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
