import sqlite3
from sqlite3 import Error

DB_NAME = "football.db"


# =========================
# CONNECTION
# =========================
def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        print("Connected to SQLite database.")
        return conn
    except Error as e:
        print("Connection error:", e)
        return None


# =========================
# INITIALIZE DATABASE
# =========================
def initialize_database():
    conn = create_connection()
    if conn is None:
        return

    try:
        with open("schema.sql", "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Database schema created.")
    except Exception as e:
        print("Schema error:", e)

    conn.close()


# =========================
# CRUD OPERATIONS – CLUBS
# =========================

# CREATE
def add_club(name, city, founded_year):
    conn = create_connection()
    try:
        sql = """INSERT INTO Clubs (name, city, founded_year)
                 VALUES (?, ?, ?)"""
        conn.execute(sql, (name, city, founded_year))
        conn.commit()
        print("Club added successfully.")
    except Exception as e:
        print("Insert error:", e)
    finally:
        conn.close()


# READ (ALL)
def get_all_clubs():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clubs")
        rows = cursor.fetchall()

        print("\n--- Clubs ---")
        for row in rows:
            print(row)

    except Exception as e:
        print("Read error:", e)
    finally:
        conn.close()


# READ (BY ID)
def get_club_by_id(club_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clubs WHERE club_id = ?", (club_id,))
        club = cursor.fetchone()
        print(club)
    except Exception as e:
        print("Read error:", e)
    finally:
        conn.close()


# UPDATE
def update_club(club_id, name, city, founded_year):
    conn = create_connection()
    try:
        sql = """UPDATE Clubs
                 SET name = ?, city = ?, founded_year = ?
                 WHERE club_id = ?"""
        conn.execute(sql, (name, city, founded_year, club_id))
        conn.commit()
        print("Club updated.")
    except Exception as e:
        print("Update error:", e)
    finally:
        conn.close()


# DELETE
def delete_club(club_id):
    conn = create_connection()
    try:
        conn.execute("DELETE FROM Clubs WHERE club_id = ?", (club_id,))
        conn.commit()
        print("Club deleted.")
    except Exception as e:
        print("Delete error:", e)
    finally:
        conn.close()
