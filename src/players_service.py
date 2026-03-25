from db import fetch_one, fetch_all, execute_query, get_last_insert_id
from clubs_service import get_club_by_name
from datetime import datetime
from typing import Optional, List


# =========================
# CONSTANTS
# =========================
VALID_POSITIONS = {'GK', 'DF', 'MF', 'FW'}
VALID_STATUS = {'active', 'injured', 'inactive'}


# =========================
# PLAYERS CRUD OPERATIONS
# =========================

def validate_player_data(position: str, number: int, birth_date: str) -> str:
    """Validate player data."""
    if position.upper() not in VALID_POSITIONS:
        return f"❌ Invalid position '{position}'. Valid positions: {', '.join(VALID_POSITIONS)}"
    
    if not (1 <= number <= 99):
        return "❌ Player number must be between 1 and 99."
    
    # Validate date format (YYYY-MM-DD)
    try:
        datetime.strptime(birth_date, "%Y-%m-%d")
    except ValueError:
        return "❌ Invalid date format. Use YYYY-MM-DD."
    
    return ""  # No errors


def add_player(full_name: str, club_name: str, birth_date: str, nationality: str, 
               position: str, number: int) -> str:
    """Add a new player to the database."""
    
    # Validation
    if not full_name or not full_name.strip():
        return "❌ Player name cannot be empty."
    
    if not club_name or not club_name.strip():
        return "❌ Club name cannot be empty."
    
    # Validate position and number
    error = validate_player_data(position, number, birth_date)
    if error:
        return error
    
    # Check if club exists
    club = get_club_by_name(club_name.strip())
    if not club:
        return f"❌ Club '{club_name}' not found."
    
    # Check if player already exists in the club
    existing = fetch_one(
        "SELECT id FROM players WHERE full_name = ? AND club_id = ?",
        (full_name.strip(), club["id"])
    )
    if existing:
        return f"❌ Player '{full_name}' already exists in club '{club_name}'."
    
    # Insert player
    last_id = get_last_insert_id(
        """INSERT INTO players (full_name, birth_date, nationality, position, number, club_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (full_name.strip(), birth_date, nationality.strip(), position.upper(), number, club["id"])
    )
    
    if last_id:
        return f"✅ Player '{full_name}' added to club '{club_name}' (ID: {last_id}, Position: {position.upper()}, Number: {number})."
    else:
        return "❌ Failed to add player."


def get_players_by_club(club_name: str) -> str:
    """Get all players in a specific club."""
    if not club_name or not club_name.strip():
        return "❌ Club name cannot be empty."
    
    club = get_club_by_name(club_name.strip())
    if not club:
        return f"❌ Club '{club_name}' not found."
    
    players = fetch_all(
        """SELECT id, full_name, birth_date, nationality, position, number, status 
           FROM players WHERE club_id = ? ORDER BY number""",
        (club["id"],)
    )
    
    if not players:
        return f"📋 No players found in club '{club_name}'."
    
    result = f"📋 **PLAYERS IN {club['name'].upper()}:**\n"
    result += "─" * 70 + "\n"
    for player in players:
        result += f"ID: {player[0]} | Name: {player[1]}\n"
        result += f"   Position: {player[4]} | Number: {player[5]} | DOB: {player[2]} | Status: {player[6]}\n"
    result += "─" * 70
    
    return result


def get_player_by_name(full_name: str) -> Optional[dict]:
    """Get a player by full name (first match)."""
    player = fetch_one(
        "SELECT id, full_name, birth_date, nationality, position, number, status, club_id FROM players WHERE LOWER(full_name) = LOWER(?)",
        (full_name,)
    )
    
    if player:
        return {
            "id": player[0],
            "full_name": player[1],
            "birth_date": player[2],
            "nationality": player[3],
            "position": player[4],
            "number": player[5],
            "status": player[6],
            "club_id": player[7]
        }
    return None


def get_player_by_id(player_id: int) -> Optional[dict]:
    """Get a player by ID."""
    player = fetch_one(
        "SELECT id, full_name, birth_date, nationality, position, number, status, club_id FROM players WHERE id = ?",
        (player_id,)
    )
    
    if player:
        return {
            "id": player[0],
            "full_name": player[1],
            "birth_date": player[2],
            "nationality": player[3],
            "position": player[4],
            "number": player[5],
            "status": player[6],
            "club_id": player[7]
        }
    return None


def update_player_number(full_name: str, new_number: int) -> str:
    """Update a player's jersey number."""
    if not (1 <= new_number <= 99):
        return "❌ Player number must be between 1 and 99."
    
    player = get_player_by_name(full_name.strip())
    if not player:
        return f"❌ Player '{full_name}' not found."
    
    # Check if number is already taken in same club
    existing = fetch_one(
        "SELECT id FROM players WHERE number = ? AND club_id = ? AND id != ?",
        (new_number, player["club_id"], player["id"])
    )
    if existing:
        return f"❌ Number {new_number} is already taken in this club."
    
    if execute_query("UPDATE players SET number = ? WHERE id = ?", (new_number, player["id"])):
        return f"✅ Player '{full_name}' number updated to {new_number}."
    else:
        return "❌ Failed to update player number."


def update_player_status(full_name: str, new_status: str) -> str:
    """Update a player's status (active, injured, inactive)."""
    if new_status.lower() not in VALID_STATUS:
        return f"❌ Invalid status '{new_status}'. Valid statuses: {', '.join(VALID_STATUS)}"
    
    player = get_player_by_name(full_name.strip())
    if not player:
        return f"❌ Player '{full_name}' not found."
    
    if execute_query("UPDATE players SET status = ? WHERE id = ?", (new_status.lower(), player["id"])):
        return f"✅ Player '{full_name}' status updated to '{new_status.lower()}'."
    else:
        return "❌ Failed to update player status."


def delete_player(full_name: str) -> str:
    """Delete a player."""
    player = get_player_by_name(full_name.strip())
    if not player:
        return f"❌ Player '{full_name}' not found."
    
    if execute_query("DELETE FROM players WHERE id = ?", (player["id"],)):
        return f"✅ Player '{full_name}' deleted successfully."
    else:
        return "❌ Failed to delete player."


def search_players(keyword: str) -> str:
    """Search for players by name or club."""
    if not keyword or not keyword.strip():
        return "❌ Search keyword cannot be empty."
    
    search_term = f"%{keyword.strip()}%"
    
    results = fetch_all(
        """SELECT p.id, p.full_name, p.position, p.number, c.name, p.status
           FROM players p
           JOIN clubs c ON p.club_id = c.id
           WHERE p.full_name LIKE ? OR c.name LIKE ?
           ORDER BY p.full_name""",
        (search_term, search_term)
    )
    
    if not results:
        return f"🔍 No players found matching '{keyword}'."
    
    result = f"🔍 **SEARCH RESULTS FOR '{keyword}':**\n"
    result += "─" * 70 + "\n"
    for player in results:
        result += f"{player[1]} | Position: {player[2]} | Number: {player[3]} | Club: {player[4]} | Status: {player[5]}\n"
    result += "─" * 70
    
    return result

