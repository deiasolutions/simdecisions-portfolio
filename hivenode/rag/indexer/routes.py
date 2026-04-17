"""
routes
======

Indexer API routes for RAG system.

Dependencies:
- from fastapi import APIRouter, Depends, HTTPException, Query
- from pydantic import BaseModel
- from typing import Optional
- from pathlib import Path
- from hivenode.dependencies import verify_jwt_or_local
- from simdecisions.database import get_db
- from hivenode.rag.indexer.indexer_service import IndexerService
- from hivenode.rag.indexer.storage import IndexStorage
- from hivenode.rag.indexer.cloud_sync import CloudSyncService
- from hivenode.rag.indexer.sync_daemon import SyncDaemon

Classes:
- IndexRepoRequest: Request to index repository.
- IndexRepoResponse: Response from repository indexing.
- IndexFileRequest: Request to index single file.
- IndexFileResponse: Response from file indexing.
- SyncResponse: Response from sync operation.
- SyncStatusResponse: Sync daemon status.

Functions:
- get_storage(): Get IndexStorage instance.
- get_cloud_sync(storage: IndexStorage = Depends(get_storage): Get CloudSyncService instance.
- get_sync_daemon(): Get SyncDaemon singleton instance.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
