"""
test_jwt
========

Unit tests for JWT service.

Dependencies:
- import pytest
- import jwt
- from datetime import datetime, UTC, timedelta
- from hodeia_auth.services.jwt import create_access_token, decode_access_token
- from hodeia_auth.config import settings

Functions:
- test_create_access_token_returns_string(mock_jwt_keys): Test that create_access_token returns a JWT string.
- test_create_access_token_contains_claims(mock_jwt_keys): Test that JWT contains expected claims.
- test_create_access_token_with_optional_claims(mock_jwt_keys): Test that optional claims are included when provided.
- test_decode_access_token_valid(mock_jwt_keys): Test that decode_access_token decodes valid tokens.
- test_decode_access_token_expired(mock_jwt_keys, monkeypatch): Test that decode_access_token rejects expired tokens.
- test_decode_access_token_invalid_signature(mock_jwt_keys): Test that decode_access_token rejects tokens with invalid signature.
- test_decode_access_token_malformed(mock_jwt_keys): Test that decode_access_token rejects malformed tokens.
- test_decode_access_token_wrong_audience(mock_jwt_keys): Test that decode_access_token rejects tokens with wrong audience.
- test_decode_access_token_wrong_issuer(mock_jwt_keys): Test that decode_access_token rejects tokens with wrong issuer.
- test_token_expiry_time(mock_jwt_keys, monkeypatch): Test that token expiry matches configured time.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
