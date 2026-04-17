"""
test_publisher
==============

Tests for benchmark results publisher.

TASK-BENCH-004 - Tests for Publisher class that generates markdown summaries,
raw JSON exports, and trend CSV data for benchmark results.

Dependencies:
- from __future__ import annotations
- import json
- import pytest
- import tempfile
- import csv
- from pathlib import Path
- from datetime import datetime
- from simdecisions.benchmark.publisher import Publisher
- from simdecisions.benchmark.collector import ResultsCollector
- from simdecisions.benchmark.types import BenchmarkResult

Functions:
- temp_results_dir(): Create temporary results directory.
- sample_results(): Create sample benchmark results for testing.
- sample_comparison(): Create sample comparison data from ResultsCollector.
- test_publisher_initialization(temp_results_dir): Test Publisher initialization sets results directory.
- test_publish_summary_creates_file(temp_results_dir, sample_comparison): Test publish_summary() creates a markdown file.
- test_publish_summary_valid_markdown(temp_results_dir, sample_comparison): Test publish_summary() creates valid markdown with required sections.
- test_publish_summary_includes_statistics(temp_results_dir, sample_comparison): Test markdown includes statistical comparison table.
- test_publish_raw_json_creates_file(temp_results_dir, sample_results): Test publish_raw_json() creates a JSON file.
- test_publish_raw_json_valid_format(temp_results_dir, sample_results): Test publish_raw_json() writes valid parseable JSON.
- test_publish_raw_json_contains_all_results(temp_results_dir, sample_results): Test raw JSON contains all result objects.
- test_publish_trend_data_creates_csv(temp_results_dir): Test publish_trend_data() creates a CSV file.
- test_publish_trend_data_correct_columns(temp_results_dir): Test CSV has correct columns.
- test_publish_trend_data_parseable_by_csv_reader(temp_results_dir): Test CSV format is parseable by standard CSV readers.
- test_publish_all_creates_all_files(temp_results_dir, sample_results, sample_comparison): Test publish_all() creates all three output files.
- test_publish_all_creates_versioned_subdirectory(temp_results_dir, sample_results, sample_comparison): Test publish_all() creates versioned subdirectory structure.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
