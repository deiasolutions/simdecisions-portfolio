"""
model_capabilities
==================

Model capabilities loader for bundle formation.

Loads model context window sizes and batch preferences from model_rates.yml.
Used by scheduler to make bundling decisions.

Dependencies:
- from dataclasses import dataclass
- from pathlib import Path
- from typing import Optional

Classes:
- ModelCapabilities: Model capabilities for bundling decisions.

Functions:
- load_model_capabilities(model_id: str,
    rates_path: Optional[Path] = None,): Load model capabilities from model_rates.yml.
- load_all_model_capabilities(rates_path: Optional[Path] = None,): Load all model capabilities from model_rates.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
