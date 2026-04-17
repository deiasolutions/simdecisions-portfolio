"""
pipeline
========

Privacy-preserving training pipeline.

Process documents through full privacy pipeline:
1. Hash original (before any processing)
2. Redact PII
3. Generate embeddings (from redacted text only)
4. Store embeddings for training (anonymized)
5. Purge original and redacted text
6. Generate audit receipt

Dependencies:
- from dataclasses import dataclass
- from datetime import datetime
- from typing import List, Optional
- import hashlib
- from .hasher import DocumentHasher
- from .redactor import PIIRedactor
- from .purger import SecurePurger
- from .audit_trail import AuditTrail
- from .consent import ConsentManager
- from .training_store import TrainingStore

Classes:
- PrivacyReceipt: Proof of privacy-preserving processing.
- EmbeddingService: Pluggable embedding service.
- PrivacyPipeline: Main privacy-preserving training pipeline.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
