import sqlite3
import os
from sqlite3 import Error
from typing import Optional, List, Tuple

# =========================
# DATABASE CONFIGURATION
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = "football.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


# =========================
# CONNECTION MANAGEMENT
# =========================
def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Error as e:
        print(f"❌ Connection error: {e}")
        return None


def close_connection(conn: sqlite3.Connection) -> None:
    """Safely close database connection."""
    if conn:
        conn.close()


# =========================
# DATABASE INITIALIZATION
# =========================
def initialize_database() -> bool:
    """Initialize database with schema and seed data."""
    try:
        conn = get_connection()
        if conn is None:
            return False

        cursor = conn.cursor()

        # Read and execute schema
        schema_path = os.path.join(os.path.dirname(BASE_DIR), "sql", "schema.sql")
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

        # Read and execute seed data
        seed_path = os.path.join(os.path.dirname(BASE_DIR), "sql", "seed.sql")
        with open(seed_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
        return True

    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False


# =========================
# HELPER METHODS
# =========================
def execute_query(query: str, params: Tuple = ()) -> bool:
    """Execute a write query (INSERT, UPDATE, DELETE)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        print(f"❌ Query error: {e}")
        return False


def fetch_one(query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
    """Fetch a single row from database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result
    except Error as e:
        print(f"❌ Fetch error: {e}")
        return None


def fetch_all(query: str, params: Tuple = ()) -> List[sqlite3.Row]:
    """Fetch all rows from database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    except Error as e:
        print(f"❌ Fetch error: {e}")
        return []


def get_last_insert_id(query: str, params: Tuple = ()) -> Optional[int]:
    """Execute query and return last inserted row ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    except Error as e:
        print(f"❌ Insert error: {e}")
        return None
