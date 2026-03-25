from db import fetch_one, fetch_all, execute_query, get_last_insert_id
from typing import Optional, List


# =========================
# CLUBS CRUD OPERATIONS
# =========================

def add_club(name: str, city: str) -> str:
    """Add a new club to the database."""
    # Validation
    if not name or not name.strip():
        return "❌ Club name cannot be empty."
    
    if not city or not city.strip():
        return "❌ City cannot be empty."
    
    name = name.strip()
    city = city.strip()

    # Check if club already exists
    if fetch_one("SELECT id FROM clubs WHERE name = ?", (name,)):
        return f"❌ Club '{name}' already exists."

    # Insert new club
    last_id = get_last_insert_id(
        "INSERT INTO clubs (name, city) VALUES (?, ?)",
        (name, city)
    )

    if last_id:
        return f"✅ Club '{name}' added successfully (ID: {last_id})."
    else:
        return "❌ Failed to add club."


def get_all_clubs() -> str:
    """Get all clubs from the database."""
    clubs = fetch_all("SELECT id, name, city FROM clubs ORDER BY name")

    if not clubs:
        return "📋 No clubs found in database."

    result = "📋 **ALL CLUBS:**\n"
    result += "─" * 50 + "\n"
    for club in clubs:
        result += f"ID: {club[0]} | Name: {club[1]} | City: {club[2]}\n"
    result += "─" * 50

    return result


def get_club_by_name(name: str) -> Optional[dict]:
    """Get a club by name."""
    club = fetch_one("SELECT id, name, city FROM clubs WHERE LOWER(name) = LOWER(?)", (name,))
    if club:
        return {"id": club[0], "name": club[1], "city": club[2]}
    return None


def get_club_by_id(club_id: int) -> Optional[dict]:
    """Get a club by ID."""
    club = fetch_one("SELECT id, name, city FROM clubs WHERE id = ?", (club_id,))
    if club:
        return {"id": club[0], "name": club[1], "city": club[2]}
    return None


def update_club(name: str, new_city: str) -> str:
    """Update a club's city."""
    if not name or not name.strip():
        return "❌ Club name cannot be empty."
    
    if not new_city or not new_city.strip():
        return "❌ City cannot be empty."

    club = get_club_by_name(name)
    if not club:
        return f"❌ Club '{name}' not found."

    if execute_query(
        "UPDATE clubs SET city = ? WHERE id = ?",
        (new_city.strip(), club["id"])
    ):
        return f"✅ Club '{name}' updated. New city: {new_city.strip()}"
    else:
        return "❌ Failed to update club."


def delete_club(name: str) -> str:
    """Delete a club by name."""
    if not name or not name.strip():
        return "❌ Club name cannot be empty."

    club = get_club_by_name(name)
    if not club:
        return f"❌ Club '{name}' not found."

    # Check if club has players
    players = fetch_all("SELECT COUNT(*) FROM players WHERE club_id = ?", (club["id"],))
    if players and players[0][0] > 0:
        return f"❌ Cannot delete club '{name}' - it still has players. Remove players first."

    if execute_query("DELETE FROM clubs WHERE id = ?", (club["id"],)):
        return f"✅ Club '{name}' deleted successfully."
    else:
        return "❌ Failed to delete club."


def get_club_players_count(club_name: str) -> int:
    """Get number of players in a club."""
    club = get_club_by_name(club_name)
    if not club:
        return 0
    
    result = fetch_one("SELECT COUNT(*) FROM players WHERE club_id = ?", (club["id"],))
    return result[0] if result else 0
