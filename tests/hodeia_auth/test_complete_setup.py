"""
test_complete_setup
===================

Tests for complete-setup endpoint and needs_setup JWT claim.

Dependencies:
- import pytest
- from hodeia_auth.models import User
- from hodeia_auth.services.password import hash_password
- from hodeia_auth.services.jwt import create_access_token, decode_access_token

Functions:
- user_and_token(test_db, rsa_key_pair): Token with needs_setup=True contains the claim.
- test_no_needs_setup_claim_when_false(rsa_key_pair): Token with needs_setup=False omits the claim.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
