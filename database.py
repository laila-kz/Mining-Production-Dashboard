import sqlite3
import pandas as pd

def get_connection():
    conn = sqlite3.connect('mining_db.sqlite')
    conn.row_factory = sqlite3.Row  # So you can access columns by name
    return conn
def fetch_data(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df