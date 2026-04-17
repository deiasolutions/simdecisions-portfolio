"""
dependencies
============

FastAPI dependency injection for hivenode.

Dependencies:
- from typing import Optional
- from fastapi import Header, HTTPException, status
- import jwt
- from hivenode.config import settings
- from hivenode.ledger.reader import LedgerReader
- from hivenode.ledger.writer import LedgerWriter
- from hivenode.storage.registry import VolumeRegistry
- from hivenode.storage.transport import FileTransport
- from hivenode.node_store import NodeStore
- from hivenode.services.jwks_cache import JWKSCache

Functions:
- set_ledger_writer(writer: LedgerWriter): Set global ledger writer.
- set_ledger_reader(reader: LedgerReader): Set global ledger reader.
- set_transport(transport: FileTransport): Set global file transport.
- set_volume_registry(registry: VolumeRegistry): Set global volume registry.
- set_node_store(store: NodeStore): Set global node store.
- set_repo_indexer(indexer: "RepoIndexer"): Set global JWKS cache.
- set_preferences_store(store: PreferencesStore): Set global preferences store.
- set_early_access_store(store: EarlyAccessStore): Set global early access store.
- get_ledger_writer(): Dependency: Get ledger writer.
- get_ledger_reader(): Dependency: Get ledger reader.
- get_transport(): Dependency: Get file transport.
- get_volume_registry(): Dependency: Get volume registry.
- get_node_store(): Dependency: Get node store (only in cloud mode).
- get_repo_indexer(): Dependency: Get preferences store.
- get_early_access_store(): Dependency: Get early access store.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
