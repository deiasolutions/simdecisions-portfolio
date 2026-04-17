"""
test_allowlist
==============

Tests for shell allowlist/denylist validation.

Dependencies:
- from hivenode.shell.allowlist import is_allowed

Functions:
- test_allowed_command(): Test that allowed command passes.
- test_denied_command_in_denylist(): Test that format matches denylist regex.
- test_not_in_allowlist(): Test that command not in allowlist fails.
- test_denylist_pattern_match(): Test that denylist regex matches full command string.
- test_fork_bomb_denied(): Test that fork bomb pattern is denied.
- test_sudo_denied(): Test that sudo is caught by denylist.
- test_command_substitution_denied(): Test that $(cmd) in args is blocked.
- test_pipe_in_args_denied(): Test that pipe character in args is blocked.
- test_semicolon_in_args_denied(): Test that semicolon in args is blocked.
- test_backtick_in_args_denied(): Test that backticks in args are blocked.
- test_ampersand_in_args_denied(): Test that & in args is blocked.
- test_path_traversal_denied(): Test that ../ path traversal in args is blocked.
- test_clean_args_pass(): Test that normal arguments are allowed.
- test_grep_with_rm_in_filename_not_false_positive(): Test that grep with 'rm' in a filename is NOT falsely denied.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
