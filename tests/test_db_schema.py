"""
Unit Tests for Database Schema & Relational Integrity
"""

import sqlite3
import pytest
import os
import tempfile
from init_db import create_schema


@pytest.fixture
def temp_db():
    """Creates a temporary SQLite database with the full schema for testing."""
    fd, path = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    create_schema(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_schema_tables_exist(temp_db):
    """Verifies that all 6 core tables are properly created."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()

    expected_tables = {"site", "camion", "conducteur", "qualite", "voyage", "arret"}
    assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"


def test_foreign_key_enforcement(temp_db):
    """Verifies that foreign key constraints reject orphan child records."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Attempting to insert a voyage with non-existent driver/truck should fail
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("""
        INSERT INTO voyage (id_voyage, date, id_conducteur, id_camion)
        VALUES ('test_voyage_1', '2025-01-01', 'non_existent_driver', 99999);
        """)
        conn.commit()

    conn.close()


def test_indexes_created(temp_db):
    """Verifies that performance indexes are registered in SQLite."""
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = {row[0] for row in cursor.fetchall()}
    conn.close()

    assert "idx_voyage_date" in indexes
    assert "idx_voyage_camion" in indexes
    assert "idx_arret_camion" in indexes
