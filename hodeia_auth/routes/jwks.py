"""
jwks
====

JWKS (JSON Web Key Set) endpoint for hodeia_auth.

TASK-136: Port GitHub OAuth + JWKS
Bee: BEE-2026-03-15-TASK-136-ra96it-git

Dependencies:
- import hashlib
- from fastapi import APIRouter
- from fastapi.responses import JSONResponse
- from cryptography.hazmat.primitives.serialization import load_pem_public_key
- from cryptography.hazmat.backends import default_backend
- from hodeia_auth.config import settings

Functions:
- _public_key_to_jwk(public_key_pem: str): Convert RSA public key PEM to JWK (JSON Web Key) format.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
