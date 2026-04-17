"""
test_ethics_loader
==================

Tests for ethics_loader module.

Dependencies:
- import time
- from hivenode.governance.gate_enforcer.ethics_loader import EthicsLoader

Functions:
- test_load_ethics_from_file(temp_deia_root, write_ethics_file, sample_ethics_dict): Load ethics from .deia/agents/{id}/ethics.yml.
- test_cache_hit_within_ttl(temp_deia_root, write_ethics_file, sample_ethics_dict): Cache hit within TTL returns cached ethics without reloading.
- test_cache_miss_after_ttl_expires(temp_deia_root, write_ethics_file, sample_ethics_dict): Cache miss after TTL expires reloads ethics.
- test_inheritance_from_default(temp_deia_root, write_ethics_file, write_default_ethics): Inheritance from default template works correctly.
- test_merge_logic_lists_replaced(temp_deia_root, write_ethics_file, write_default_ethics): Merge logic: lists are replaced, not appended.
- test_merge_logic_scalars_overridden(temp_deia_root, write_ethics_file, write_default_ethics): Merge logic: scalars are overridden.
- test_missing_ethics_yml_returns_none(temp_deia_root): Missing ethics.yml returns None.
- test_invalid_yaml_returns_none(temp_deia_root): Invalid YAML returns None and logs error.
- test_scan_all_agents(temp_deia_root, write_ethics_file, sample_ethics_dict): scan_all_agents walks directory and loads all ethics.
- test_invalidate_clears_cache(temp_deia_root, write_ethics_file, sample_ethics_dict): invalidate() clears cache for specific agent.
- test_invalidate_all_clears_all_caches(temp_deia_root, write_ethics_file, sample_ethics_dict): invalidate() with no agent_id clears all caches.
- test_grace_config_loaded_from_file(temp_deia_root, write_grace_config, sample_grace_config_dict): Grace config loaded from .deia/config/grace.yml.
- test_grace_config_defaults_when_file_missing(temp_deia_root): Grace config defaults when file missing.
- test_agent_id_with_agent_prefix_handled(temp_deia_root, write_ethics_file, sample_ethics_dict): Agent ID with 'agent:' prefix is handled correctly.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
