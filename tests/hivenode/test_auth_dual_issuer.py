"""
test_auth_dual_issuer
=====================

Tests for dual-issuer JWT validation (ra96it + hodeia).

Dependencies:
- import pytest
- import jwt
- from datetime import datetime, UTC, timedelta
- from hivenode.config import HivenodeConfig

Functions:
- _create_test_jwt(issuer: str, audience: str = "shiftcenter", expiry_hours: int = 1): Create a test JWT with specified issuer and audience.
- test_jwt_verification_with_ra96it_issuer(): Test that JWT with issuer='ra96it' is accepted.
- test_jwt_verification_with_hodeia_issuer(): Test that JWT with issuer='hodeia' is accepted.
- test_jwt_verification_rejects_wrong_issuer(): Test that JWT with unsupported issuer is rejected.
- test_jwt_verification_with_multiple_audiences(): Test that JWT is verified regardless of audience (as long as it's in list).
- test_config_fields_renamed(): Verify config fields are renamed to auth_* pattern.
- test_get_auth_public_key_method_exists(): Verify get_auth_public_key() method works.
- test_default_auth_jwks_url_is_hodeia(): Verify default auth_jwks_url points to api.hodeia.me.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
