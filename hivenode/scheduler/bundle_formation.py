"""
bundle_formation
================

Bundle formation with context window guard.

Forms bundles of related specs for efficient dispatch, with hard guard that
no bundle exceeds the target operator's context window.

Per PRISM-IR v1.1 Section 5.1-5.2:
- Bundles are ephemeral dispatch-time groupings (not tree nodes)
- Three bundling reasons: GRANULARITY_FIT, OPERATOR_FIT, VENDOR_FIT
- Context window guard: sum(estimated_tokens) <= max_context_tokens * buffer_ratio
- Bundle success → all specs marked BUILT
- Bundle failure → unbundle and retry individually

Dependencies:
- import re
- from dataclasses import dataclass, field
- from datetime import datetime, timezone
- from enum import Enum
- from pathlib import Path
- from typing import Optional
- from uuid import uuid4

Classes:
- BundleReason: Why this bundle was formed.
- Bundle: Ephemeral bundle of specs for dispatch.

Functions:
- estimate_tokens(spec, prompt_overhead: int = 100): Estimate input tokens for a spec.
- _semantic_prefix(spec_id: str): Extract semantic prefix from spec ID for grouping.
- _group_by_prefix(specs: list): Group specs by semantic prefix.
- form_bundles(ready_specs: list,
    operator,
    token_buffer_ratio: float = 0.8,
    bundle_reason: Optional[BundleReason] = None,): Form bundles of specs respecting context window constraints.
- _bundle_group(specs: list,
    operator,
    max_tokens: int,
    bundle_reason: BundleReason,): Bundle a group of specs, respecting context window.
- _generate_bundle_id(): Generate unique bundle ID.
- load_bundle_config(config_path: Optional[Path] = None): Load bundle configuration from queue.yml.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
