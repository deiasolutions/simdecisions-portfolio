"""
__init__
========

Privacy-preserving training pipeline.

Train on embeddings, not text. Customer data contributes to model improvement
without exposing secrets.

Privacy Guarantees:
- No PII in training (redacted before embedding)
- No text reconstruction (embeddings are one-way)
- Verifiable deletion (hash chain audit trail)
- Customer control (opt-in/opt-out)
- Data isolation (embeddings anonymized)

Dependencies:
- from .pipeline import PrivacyPipeline, PrivacyReceipt
- from .hasher import DocumentHasher
- from .redactor import PIIRedactor, PIIMatch
- from .purger import SecurePurger
- from .audit_trail import AuditTrail, AuditEvent
- from .consent import ConsentManager, ConsentToken
- from .training_store import TrainingStore

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
