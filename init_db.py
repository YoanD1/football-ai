# init_db.py
import sqlite3
import os

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "src", "clubs.db")           # database file
schema_path = os.path.join(base_dir, "sql", "schema.sql")     # schema.sql file

# Connect to database (will create clubs.db if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read and execute schema
with open(schema_path, "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Database initialized successfully!")