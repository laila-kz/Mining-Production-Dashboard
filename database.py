"""
Database Connector and Query Utilities for Mining Production Dashboard.
Provides thread-safe connection context managers, parameterized query execution,
and pandas DataFrame converters.
"""

import sqlite3
from contextlib import contextmanager
import pandas as pd
import os
from typing import Any, Dict, List, Optional, Tuple, Union

DB_NAME = os.getenv("MINING_DB_PATH", "mining_db.sqlite")
ALLOWED_TABLES = {"site", "camion", "conducteur", "qualite", "voyage", "arret"}


def get_connection(db_path: str = DB_NAME) -> sqlite3.Connection:
    """Returns a raw SQLite connection with Foreign Keys enabled and Row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db_connection(db_path: str = DB_NAME):
    """Context manager for safe, leak-free SQLite connections."""
    conn = get_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()


def query_df(
    query: str,
    params: Optional[Union[Tuple[Any, ...], Dict[str, Any], List[Any]]] = None,
    db_path: str = DB_NAME,
) -> pd.DataFrame:
    """
    Executes a SQL query with parameters and returns a pandas DataFrame.
    Guarantees connection closure via context management.
    """
    with get_db_connection(db_path) as conn:
        if params is None:
            return pd.read_sql_query(query, conn)
        return pd.read_sql_query(query, conn, params=params)


def execute_non_query(
    query: str,
    params: Optional[Union[Tuple[Any, ...], Dict[str, Any], List[Any]]] = None,
    db_path: str = DB_NAME,
) -> int:
    """Executes an INSERT, UPDATE, or DELETE query and commits changes."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount


def fetch_data(table_name: str, db_path: str = DB_NAME) -> pd.DataFrame:
    """
    Safely fetches all rows from a whitelisted table name.
    Preserved for backwards compatibility.
    """
    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"Unauthorized table name '{table_name}'. Must be one of: {sorted(ALLOWED_TABLES)}"
        )
    return query_df(f"SELECT * FROM {table_name}", db_path=db_path)