"""
test_jwt
========

Tests for JWT service.

Dependencies:
- import pytest
- from datetime import datetime, UTC, timedelta
- import jwt
- from hodeia_auth.services.jwt import create_access_token, decode_access_token

Functions:
- test_create_access_token(rsa_key_pair): Test creating an access token.
- test_decode_access_token(rsa_key_pair): Test decoding a valid access token.
- test_decode_expired_token(rsa_key_pair): Test that expired tokens are rejected.
- test_decode_wrong_signature(rsa_key_pair): Test that tokens with wrong signature are rejected.
- test_decode_invalid_audience(rsa_key_pair): Test that tokens with wrong audience are rejected.
- test_decode_invalid_issuer(rsa_key_pair): Test that tokens with wrong issuer are rejected.
- test_decode_malformed_token(rsa_key_pair): Test that malformed tokens are rejected.
- test_token_expiry_time(rsa_key_pair): Test that token expires in 15 minutes.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
