"""
schemas
=======

Pydantic schemas for hodeia_auth API request/response models.

Dependencies:
- from typing import Literal
- from pydantic import BaseModel, EmailStr, Field

Classes:
- RegisterRequest: Request body for POST /register.
- RegisterResponse: Response body for POST /register.
- LoginRequest: Request body for POST /login.
- LoginResponse: Response body for POST /login.
- MFAVerifyRequest: Request body for POST /mfa/verify.
- MFAVerifyResponse: Response body for POST /mfa/verify.
- TokenRefreshRequest: Request body for POST /token/refresh.
- TokenRefreshResponse: Response body for POST /token/refresh.
- TokenRevokeRequest: Request body for POST /token/revoke.
- TokenRevokeResponse: Response body for POST /token/revoke.
- OAuthCallbackRequest: Request parameters for GET /oauth/github/callback.
- OAuthExchangeRequest: Request body for POST /oauth/github/exchange.
- OAuthUserResponse: User data in OAuth response.
- OAuthTokenResponse: Response body for POST /oauth/{provider}/exchange.
- DevLoginAvailableResponse: Response body for GET /dev-login/available.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
