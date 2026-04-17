"""
test_relay_moderation
=====================

Tests for efemera moderation pipeline and routes.

Covers:
- PII scanner (email, phone, SSN, credit card)
- Toxicity scanner (harassment, threat keywords)
- Crisis detector (suicide, violence threats)
- Pipeline decision logic (BLOCK > FLAG > PASS)
- Moderation queue listing
- Review endpoint (approve/reject)
- Resubmit endpoint (re-run pipeline)
- Moderation logger (writes to system channels)

Dependencies:
- import pytest
- from hivenode.relay.store import (
- from hivenode.relay.moderation.pipeline import (

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
