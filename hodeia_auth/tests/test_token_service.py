"""
test_token_service
==================

Unit tests for refresh token service.

Dependencies:
- from datetime import datetime, UTC, timedelta
- from hodeia_auth.services.token import (
- from hodeia_auth.models import RefreshToken, User
- from hodeia_auth.services.password import hash_password

Functions:
- test_generate_token_returns_string(): Test that generate_token returns a string.
- test_generate_token_unique(): Test that generate_token produces unique tokens.
- test_hash_token_consistent(): Test that hash_token produces consistent hashes.
- test_hash_token_different_for_different_tokens(): Test that different tokens produce different hashes.
- test_issue_refresh_token(db_session): Test issuing a refresh token.
- test_get_refresh_token(db_session): Test retrieving a refresh token by raw value.
- test_get_refresh_token_not_found(db_session): Test that get_refresh_token returns None for non-existent token.
- test_is_token_valid_fresh_token(db_session): Test that is_token_valid returns True for fresh token.
- test_is_token_valid_expired(db_session): Test that is_token_valid returns False for expired token.
- test_is_token_valid_consumed(db_session): Test that is_token_valid returns False for consumed token.
- test_is_token_valid_revoked(db_session): Test that is_token_valid returns False for revoked token.
- test_rotate_refresh_token(db_session): Test token rotation (consume old, issue new).
- test_rotate_refresh_token_invalid(db_session): Test that rotating an invalid token returns None.
- test_detect_replay_attack(db_session): Test replay attack detection.
- test_revoke_refresh_token(db_session): Test revoking a single refresh token.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
