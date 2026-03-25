from db import fetch_one, fetch_all, execute_query, get_last_insert_id
from clubs_service import get_club_by_name
from players_service import get_player_by_name
from datetime import datetime
from typing import Optional


# =========================
# TRANSFERS CRUD & LOGIC
# =========================

def validate_transfer_date(date_str: str) -> bool:
    """Validate transfer date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def transfer_player(player_name: str, from_club_name: Optional[str], to_club_name: str, 
                   transfer_date: str, fee: Optional[float] = None, note: str = "") -> str:
    """Transfer a player from one club to another."""
    
    # Validation
    if not player_name or not player_name.strip():
        return "❌ Player name cannot be empty."
    
    if not to_club_name or not to_club_name.strip():
        return "❌ Destination club name cannot be empty."
    
    if not validate_transfer_date(transfer_date):
        return "❌ Invalid date format. Use YYYY-MM-DD."
    
    # Get player
    player = get_player_by_name(player_name.strip())
    if not player:
        return f"❌ Player '{player_name}' not found."
    
    from_club_id = player["club_id"]
    from_club = fetch_one("SELECT name FROM clubs WHERE id = ?", (from_club_id,))
    from_club_name_actual = from_club[0] if from_club else "Unknown"
    
    # Get destination club
    to_club = get_club_by_name(to_club_name.strip())
    if not to_club:
        return f"❌ Destination club '{to_club_name}' not found."
    
    # Business rule: source and destination must be different
    if from_club_id == to_club["id"]:
        return f"❌ Player is already in club '{to_club_name}'."
    
    # Create transfer record
    last_id = get_last_insert_id(
        """INSERT INTO transfers (player_id, from_club_id, to_club_id, transfer_date, fee, note)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (player["id"], from_club_id, to_club["id"], transfer_date, fee, note.strip())
    )
    
    if not last_id:
        return "❌ Failed to create transfer record."
    
    # Update player's club
    if not execute_query("UPDATE players SET club_id = ? WHERE id = ?", (to_club["id"], player["id"])):
        return "❌ Failed to update player's club."
    
    # Format fee for display
    fee_str = f" | Fee: ${fee:,.2f}" if fee else ""
    
    return (f"✅ Transfer successful!\n"
            f"   Player: {player['full_name']}\n"
            f"   From: {from_club_name_actual} → To: {to_club['name']}\n"
            f"   Date: {transfer_date}{fee_str}")


def get_transfers_by_player(player_name: str) -> str:
    """Get all transfers for a specific player."""
    if not player_name or not player_name.strip():
        return "❌ Player name cannot be empty."
    
    player = get_player_by_name(player_name.strip())
    if not player:
        return f"❌ Player '{player_name}' not found."
    
    transfers = fetch_all(
        """SELECT t.id, t.transfer_date, c1.name as from_club, c2.name as to_club, t.fee, t.note
           FROM transfers t
           LEFT JOIN clubs c1 ON t.from_club_id = c1.id
           JOIN clubs c2 ON t.to_club_id = c2.id
           WHERE t.player_id = ?
           ORDER BY t.transfer_date DESC""",
        (player["id"],)
    )
    
    if not transfers:
        return f"📋 No transfers found for player '{player_name}'."
    
    result = f"📋 **TRANSFER HISTORY - {player['full_name'].upper()}:**\n"
    result += "─" * 70 + "\n"
    for transfer in transfers:
        from_club = transfer[2] or "Free Agent"
        fee_str = f" | Fee: ${transfer[4]:,.2f}" if transfer[4] else ""
        note_str = f" | Note: {transfer[5]}" if transfer[5] else ""
        result += f"Date: {transfer[1]} | {from_club} → {transfer[3]}{fee_str}{note_str}\n"
    result += "─" * 70
    
    return result


def get_transfers_by_club(club_name: str) -> str:
    """Get all transfers involving a specific club."""
    if not club_name or not club_name.strip():
        return "❌ Club name cannot be empty."
    
    club = get_club_by_name(club_name.strip())
    if not club:
        return f"❌ Club '{club_name}' not found."
    
    # Get both incoming and outgoing transfers
    transfers = fetch_all(
        """SELECT t.id, t.transfer_date, p.full_name, c1.name as from_club, c2.name as to_club, t.fee
           FROM transfers t
           JOIN players p ON t.player_id = p.id
           LEFT JOIN clubs c1 ON t.from_club_id = c1.id
           JOIN clubs c2 ON t.to_club_id = c2.id
           WHERE t.from_club_id = ? OR t.to_club_id = ?
           ORDER BY t.transfer_date DESC""",
        (club["id"], club["id"])
    )
    
    if not transfers:
        return f"📋 No transfers found for club '{club_name}'."
    
    result = f"📋 **TRANSFERS - {club['name'].upper()}:**\n"
    result += "─" * 70 + "\n"
    
    incoming = []
    outgoing = []
    
    for transfer in transfers:
        fee_str = f" (${transfer[5]:,.2f})" if transfer[5] else ""
        
        if transfer[3] == club["name"]:  # from_club
            outgoing.append(f"  ⬅️  {transfer[1]} | {transfer[2]} → {transfer[4]}{fee_str}")
        else:  # to_club
            incoming.append(f"  ➡️  {transfer[1]} | {transfer[3]} → {transfer[2]}{fee_str}")
    
    if incoming:
        result += "**INCOMING TRANSFERS:**\n" + "\n".join(incoming) + "\n\n"
    
    if outgoing:
        result += "**OUTGOING TRANSFERS:**\n" + "\n".join(outgoing) + "\n"
    
    result += "─" * 70
    
    return result


def get_all_transfers() -> str:
    """Get all transfers in the system."""
    transfers = fetch_all(
        """SELECT t.id, t.transfer_date, p.full_name, c1.name as from_club, c2.name as to_club, t.fee
           FROM transfers t
           JOIN players p ON t.player_id = p.id
           LEFT JOIN clubs c1 ON t.from_club_id = c1.id
           JOIN clubs c2 ON t.to_club_id = c2.id
           ORDER BY t.transfer_date DESC"""
    )
    
    if not transfers:
        return "📋 No transfers found in the system."
    
    result = "📋 **ALL TRANSFERS:**\n"
    result += "─" * 70 + "\n"
    for transfer in transfers:
        from_club = transfer[3] or "Free Agent"
        fee_str = f" (${transfer[5]:,.2f})" if transfer[5] else ""
        result += f"{transfer[1]} | {transfer[2]} | {from_club} → {transfer[4]}{fee_str}\n"
    result += "─" * 70
    
    return result

