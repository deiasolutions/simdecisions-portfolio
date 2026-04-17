"""
test_routes
===========

Integration tests for hodeia_auth API routes.

Dependencies:
- from hodeia_auth.models import User
- from hodeia_auth.services.password import hash_password
- from hodeia_auth.services.token import issue_refresh_token

Functions:
- test_health_endpoint(client): Test /health endpoint.
- test_root_endpoint(client): Test / endpoint.
- test_register_success(client): Test successful user registration.
- test_register_duplicate_email(client): Test that registering duplicate email fails.
- test_register_sms_without_phone(client): Test that SMS MFA without phone fails.
- test_login_success(client, db_session): Test successful login flow.
- test_login_wrong_email(client): Test login with non-existent email.
- test_login_wrong_password(client, db_session): Test login with wrong password.
- test_mfa_verify_invalid_session(client): Test MFA verify with non-existent session.
- test_token_refresh_invalid(client): Test token refresh with invalid token.
- test_token_refresh_success(client, db_session, mock_jwt_keys): Test successful token refresh.
- test_token_revoke_success(client, db_session): Test token revoke (idempotent).
- test_profile_without_auth(client): Test profile access without authentication.
- test_profile_with_invalid_token(client): Test profile access with invalid token.
- test_profile_with_valid_token(client, db_session, mock_jwt_keys): Test profile access with valid token.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
