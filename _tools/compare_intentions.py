"""
compare_intentions
==================

Compare platform vs shiftcenter intentions to find gaps.

Finds functionalities documented or built in platform that are
missing from shiftcenter. Groups by source area and category.

Dependencies:
- import json
- import re
- from collections import defaultdict
- from pathlib import Path

Functions:
- normalize(text: str): Lowercase, strip markdown noise, collapse whitespace.
- extract_keywords(text: str): Pull meaningful words (4+ chars) from normalized text.
- source_area(sources: list): Extract the top-level source directory from first source file.
- functional_area(sources: list): Get a deeper path for grouping — first 2-3 meaningful segments.
- is_noise(item: dict): Filter out process noise, warnings, and trivial items.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
