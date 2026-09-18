"""
Unified Database Setup Script for Mining Production Dashboard
Initializes the SQLite schema with relational integrity and ingests all CSV data.
Usage: python setup_db.py
"""

import sys
import os
from init_db import create_schema, DB_NAME
from import_csv import import_csv_data, DATA_DIR


def setup(db_path: str = DB_NAME, data_dir: str = DATA_DIR):
    """Orchestrates database creation and initial data loading."""
    print("=" * 60)
    print(" Mining Production Dashboard - Database Setup")
    print("=" * 60)

    # 1. Initialize schema
    print("\n[Step 1/2] Initializing SQLite schema...")
    create_schema(db_path)

    # 2. Ingest CSV data
    print("\n[Step 2/2] Loading raw CSV dataset...")
    import_csv_data(db_path, data_dir)

    print("\n" + "=" * 60)
    print("[SUCCESS] Database setup complete and ready for Streamlit!")
    print("=" * 60)


if __name__ == "__main__":
    setup()
