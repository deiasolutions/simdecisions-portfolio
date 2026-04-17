"""
ir_validator
============

PRISM-IR Validator

Validates PRISM-IR JSON objects against the mobile_ir_schema.json schema.

Dependencies:
- import json
- from dataclasses import dataclass, field
- from pathlib import Path
- from typing import Any
- import jsonschema
- from jsonschema import Draft7Validator

Classes:
- ValidationResult: Result of IR validation.

Functions:
- _load_schema(): Load the PRISM-IR JSON schema.
- validate_ir(ir: dict[str, Any]): Validate a PRISM-IR object against the mobile IR schema.
- validate_ir_strict(ir: dict[str, Any]): Validate IR with stricter rules (warnings become errors).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
