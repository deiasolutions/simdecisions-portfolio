"""
test_gitignore
==============

Tests for gitignore parser.

Dependencies:
- import pytest
- from hivenode.repo.gitignore import GitignoreParser

Functions:
- simple_repo(tmp_path): Create a simple test repo with .gitignore.
- nested_repo(tmp_path): Create repo with nested .gitignore files.
- negation_repo(tmp_path): Create repo with negation patterns.
- test_parse_simple_patterns(simple_repo): Test parsing standard gitignore patterns.
- test_nested_gitignore_files(nested_repo): Test combining rules from root and nested .gitignore files.
- test_negation_patterns(negation_repo): Test negation patterns (! prefix).
- test_wildcard_patterns(simple_repo): Test wildcard pattern matching.
- test_empty_gitignore(tmp_path): Test repo with no .gitignore file.
- test_directory_slash_pattern(tmp_path): Test directory-specific patterns (trailing slash).
- test_absolute_path_pattern(tmp_path): Test patterns with leading slash (root-relative).

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
