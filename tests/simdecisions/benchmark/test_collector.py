"""
test_collector
==============

Tests for results collector and aggregation.

TASK-BENCH-003 - Tests for collector.py module.

Dependencies:
- import pytest
- import yaml
- import os
- import tempfile
- from pathlib import Path
- from simdecisions.benchmark.collector import ResultsCollector
- from simdecisions.benchmark.types import BenchmarkResult

Classes:
- TestResultsCollectorInit: Tests for ResultsCollector initialization.
- TestLoadResults: Tests for loading results from YAML files.
- TestAggregateByTrack: Tests for aggregating results by track.
- TestComputeStatistics: Tests for computing statistics from results.
- TestCompareTracks: Tests for comparing baseline and simdecisions tracks.
- TestGenerateSummaryTable: Tests for generating markdown summary table.
- TestExportAggregatedResults: Tests for exporting aggregated results to JSON.

Functions:
- temp_results_dir(): Create temporary results directory for testing.
- sample_results(): Create sample BenchmarkResult objects for testing.

SOURCE AVAILABLE ON REQUEST
Contact: Dave Eichler — linkedin.com/in/daaaave-atx
"""

# This file is a stub. See README.md for full source access.
