"""
Unit Tests for ETL Pipeline and Data Transformation Helpers
"""

import pytest
import pandas as pd
import tempfile
import os
import sqlite3

from init_db import create_schema
from import_csv import import_csv_data, parse_duration_to_minutes, align_foreign_keys


def test_parse_duration_to_minutes():
    """Tests string to minutes duration conversion."""
    assert parse_duration_to_minutes("0:34:00") == 34.0
    assert parse_duration_to_minutes("1:03:00") == 63.0
    assert parse_duration_to_minutes("0:15:30") == 15.5
    assert parse_duration_to_minutes(45) == 45.0
    assert parse_duration_to_minutes(None) == 0.0
    assert parse_duration_to_minutes("invalid") == 0.0


def test_align_foreign_keys():
    """Tests deterministic mapping of orphan foreign keys to parent IDs."""
    valid_parents = ["site_A", "site_B", "site_C"]
    s = pd.Series(["site_A", "orphan_1", "orphan_2", "site_B"])
    aligned = align_foreign_keys(s, valid_parents)

    assert aligned.iloc[0] == "site_A"
    assert aligned.iloc[3] == "site_B"
    assert aligned.iloc[1] in valid_parents
    assert aligned.iloc[2] in valid_parents


def test_full_etl_execution():
    """Tests that full ETL pipeline runs and populates tables with records."""
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    try:
        create_schema(path)
        import_csv_data(db_path=path)

        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        for table in ["site", "camion", "conducteur", "qualite", "voyage", "arret"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            assert count > 0, f"Table '{table}' has 0 rows after ETL import!"

        conn.close()
    finally:
        if os.path.exists(path):
            os.remove(path)
