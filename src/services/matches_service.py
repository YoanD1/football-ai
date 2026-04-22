"""
Matches Service - Business logic for match management.
Includes validation, context management, and orchestration.
"""

from typing import Optional, Dict, List
from repositories.matches_repo import (
    get_match_by_id, get_matches_by_round, get_match_by_clubs_and_league,
    update_match_result, is_match_played, add_goal, get_goals_by_match,
    add_card, get_cards_by_match, get_match_events, delete_all_match_events
)
from services.leagues_service import get_league_by_name_and_season, get_clubs_in_league
from players_service import get_player_by_name
from clubs_service import get_club_by_name


# =========================
# CONTEXT MANAGEMENT
# =========================

class MatchContext:
    """Global context for current league and match selection."""
    current_league_id: Optional[int] = None
    current_league_name: Optional[str] = None
    current_league_season: Optional[str] = None
    current_match_id: Optional[int] = None


# =========================
# VALIDATION HELPERS
# =========================

def validate_minute(minute: int) -> bool:
    """Validate minute is between 1 and 120."""
    return 1 <= minute <= 120


def validate_goals(home_goals: int, away_goals: int) -> bool:
    """Validate goals are non-negative integers."""
    return home_goals >= 0 and away_goals >= 0


def validate_player_in_match(player_id: int, match_id: int) -> bool:
    """Check if player belongs to one of the clubs in the match."""
    match = get_match_by_id(match_id)
    if not match:
        return False
    
    player = get_player_by_name("")  # We'll get player by name later
    # Actually, let's modify this
    from db import fetch_one
    player_club = fetch_one("SELECT club_id FROM players WHERE id = ?", (player_id,))
    if not player_club:
        return False
    
    return player_club["club_id"] in (match["home_club_id"], match["away_club_id"])


def get_player_id_by_name_and_club(player_name: str, club_name: str) -> Optional[int]:
    """Get player ID by name and club."""
    from db import fetch_one
    player = fetch_one(
        "SELECT id FROM players WHERE LOWER(full_name) = LOWER(?) AND club_id = (SELECT id FROM clubs WHERE LOWER(name) = LOWER(?))",
        (player_name, club_name)
    )
    return player["id"] if player else None


# =========================
# CONTEXT OPERATIONS
# =========================

def select_league(league_name: str, season: str) -> str:
    """Select current league for context."""
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    MatchContext.current_league_id = league["id"]
    MatchContext.current_league_name = league["name"]
    MatchContext.current_league_season = league["season"]
    MatchContext.current_match_id = None  # Reset match when changing league
    
    return f"✅ Current league set to: {league_name} ({season})"


def get_current_league() -> Optional[Dict]:
    """Get current league info."""
    if not MatchContext.current_league_id:
        return None
    
    return {
        "id": MatchContext.current_league_id,
        "name": MatchContext.current_league_name,
        "season": MatchContext.current_league_season
    }


def select_match(match_id: int) -> str:
    """Select current match for context."""
    if not MatchContext.current_league_id:
        return "❌ No league selected. Use: Избери лига <name> <season>"
    
    match = get_match_by_id(match_id)
    if not match:
        return f"❌ Match with ID {match_id} not found."
    
    if match["league_id"] != MatchContext.current_league_id:
        return f"❌ Match {match_id} is not in current league '{MatchContext.current_league_name}'."
    
    MatchContext.current_match_id = match_id
    return f"✅ Current match set to: {match['home_club_name']} vs {match['away_club_name']} (ID: {match_id})"


def get_current_match() -> Optional[Dict]:
    """Get current match info."""
    if not MatchContext.current_match_id:
        return None
    
    return get_match_by_id(MatchContext.current_match_id)


# =========================
# MATCH OPERATIONS
# =========================

def show_round(round_no: int) -> str:
    """Show matches for a specific round in current league."""
    if not MatchContext.current_league_id:
        return "❌ No league selected. Use: Избери лига <name> <season>"
    
    matches = get_matches_by_round(MatchContext.current_league_id, round_no)
    if not matches:
        return f"❌ No matches found for round {round_no} in league '{MatchContext.current_league_name}'."
    
    result = f"📅 **ROUND {round_no} - {MatchContext.current_league_name} ({MatchContext.current_league_season})**\n"
    result += "━" * 80 + "\n"
    
    for match in matches:
        status = "Played" if match["status"] == "played" else "Scheduled"
        score = f" {match['home_goals']}:{match['away_goals']} " if match["home_goals"] is not None else " vs "
        result += f"ID: {match['id']} | {match['home_club_name']}{score}{match['away_club_name']} | {status}\n"
    
    result += "━" * 80
    return result


def record_result(home_club: str, away_club: str, home_goals: int, away_goals: int) -> str:
    """Record match result."""
    if not MatchContext.current_league_id:
        return "❌ No league selected. Use: Избери лига <name> <season>"
    
    # Validate goals
    if not validate_goals(home_goals, away_goals):
        return "❌ Goals must be non-negative integers."
    
    # Find match between clubs
    home_club_obj = get_club_by_name(home_club)
    away_club_obj = get_club_by_name(away_club)
    if not home_club_obj or not away_club_obj:
        return f"❌ Club '{home_club}' or '{away_club}' not found."
    
    match = get_match_by_clubs_and_league(home_club_obj["id"], away_club_obj["id"], MatchContext.current_league_id)
    if not match:
        return f"❌ No match found between '{home_club}' and '{away_club}' in current league."
    
    # Check if already played
    if is_match_played(match["id"]):
        return f"❌ Match already played: {home_club} {match['home_goals']}:{match['away_goals']} {away_club}"
    
    # Update result
    if update_match_result(match["id"], home_goals, away_goals):
        return f"✅ Result recorded: {home_club} {home_goals}:{away_goals} {away_club} (Match #{match['id']})"
    else:
        return "❌ Failed to record result."


def add_goal_to_match(player_name: str, club_name: str, minute: int) -> str:
    """Add a goal to the current match."""
    if not MatchContext.current_match_id:
        return "❌ No match selected. Use: Избери мач <id>"
    
    # Validate minute
    if not validate_minute(minute):
        return "❌ Minute must be between 1 and 120."
    
    # Get player
    player_id = get_player_id_by_name_and_club(player_name, club_name)
    if not player_id:
        return f"❌ Player '{player_name}' not found in club '{club_name}'."
    
    # Get club
    club = get_club_by_name(club_name)
    if not club:
        return f"❌ Club '{club_name}' not found."
    
    # Validate player is in match
    match = get_current_match()
    if club["id"] not in (match["home_club_id"], match["away_club_id"]):
        return f"❌ Club '{club_name}' is not playing in current match."
    
    # Add goal
    goal_id = add_goal(MatchContext.current_match_id, player_id, club["id"], minute)
    if goal_id:
        return f"✅ Goal added: {player_name} ({club_name}) at {minute}' (Goal #{goal_id})"
    else:
        return "❌ Failed to add goal."


def add_card_to_match(player_name: str, club_name: str, card_type: str, minute: int) -> str:
    """Add a card to the current match."""
    if not MatchContext.current_match_id:
        return "❌ No match selected. Use: Избери мач <id>"
    
    # Validate card type
    if card_type.upper() not in ("Y", "R"):
        return "❌ Card type must be 'Y' (yellow) or 'R' (red)."
    
    # Validate minute
    if not validate_minute(minute):
        return "❌ Minute must be between 1 and 120."
    
    # Get player
    player_id = get_player_id_by_name_and_club(player_name, club_name)
    if not player_id:
        return f"❌ Player '{player_name}' not found in club '{club_name}'."
    
    # Get club
    club = get_club_by_name(club_name)
    if not club:
        return f"❌ Club '{club_name}' not found."
    
    # Validate player is in match
    match = get_current_match()
    if club["id"] not in (match["home_club_id"], match["away_club_id"]):
        return f"❌ Club '{club_name}' is not playing in current match."
    
    # For level 2 validation: check red cards and yellow cards
    from repositories.matches_repo import get_player_cards_in_match
    existing_cards = get_player_cards_in_match(MatchContext.current_match_id, player_id)
    
    if card_type.upper() == "R":
        if existing_cards["R"] > 0:
            return f"❌ Player '{player_name}' already has a red card in this match."
    elif card_type.upper() == "Y":
        if existing_cards["Y"] >= 2:
            return f"❌ Player '{player_name}' already has 2 yellow cards. Cannot add another yellow."
    
    # Add card
    card_id = add_card(MatchContext.current_match_id, player_id, club["id"], minute, card_type.upper())
    if card_id:
        return f"✅ {card_type.upper()} card added: {player_name} ({club_name}) at {minute}' (Card #{card_id})"
    else:
        return "❌ Failed to add card."


def show_match_events(match_id: Optional[int] = None) -> str:
    """Show events for a match."""
    target_match_id = match_id or MatchContext.current_match_id
    if not target_match_id:
        return "❌ No match specified. Use: Покажи събития <match_id> or select a match first."
    
    match = get_match_by_id(target_match_id)
    if not match:
        return f"❌ Match with ID {target_match_id} not found."
    
    events = get_match_events(target_match_id)
    
    result = f"⚽ **MATCH EVENTS: {match['home_club_name']} vs {match['away_club_name']}**\n"
    result += "━" * 80 + "\n"
    
    if not events["goals"] and not events["cards"]:
        result += "No events recorded for this match.\n"
    else:
        # Sort events by minute
        all_events = []
        for goal in events["goals"]:
            all_events.append({
                "type": "goal",
                "minute": goal["minute"],
                "player": goal["full_name"],
                "club": goal["club_name"],
                "detail": "GOAL" + (" (OG)" if goal["is_own_goal"] else "")
            })
        
        for card in events["cards"]:
            all_events.append({
                "type": "card",
                "minute": card["minute"],
                "player": card["full_name"],
                "club": card["club_name"],
                "detail": f"{card['card_type']} CARD"
            })
        
        all_events.sort(key=lambda x: x["minute"])
        
        for event in all_events:
            result += f"{event['minute']}' - {event['player']} ({event['club']}) - {event['detail']}\n"
    
    result += "━" * 80
    return result
