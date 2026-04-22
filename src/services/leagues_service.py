"""
Leagues Service - Business logic for league management.
Includes round-robin algorithm, validation, and orchestration.
"""

import re
from typing import List, Tuple, Optional, Dict
from db import fetch_one
from repositories.leagues_repo import (
    create_league, get_league_by_name_and_season, get_league_by_id,
    get_all_leagues, delete_league, add_club_to_league, remove_club_from_league,
    get_clubs_in_league, is_club_in_league, create_match, get_matches_by_league,
    match_exists, get_match_count_by_league, get_round_count_by_league,
    delete_matches_by_league
)


# =========================
# VALIDATION HELPERS
# =========================

def validate_season_format(season: str) -> bool:
    """Validate season format (YYYY/YYYY)."""
    pattern = r'^\d{4}/\d{4}$'
    return bool(re.match(pattern, season))


def validate_club_exists(club_name: str) -> bool:
    """Check if club exists in database."""
    from clubs_service import get_club_by_name
    return get_club_by_name(club_name) is not None


def get_club_id(club_name: str) -> Optional[int]:
    """Get club ID by name."""
    from clubs_service import get_club_by_name
    club = get_club_by_name(club_name)
    return club["id"] if club else None


# =========================
# LEAGUE MANAGEMENT
# =========================

def create_new_league(name: str, season: str) -> str:
    """
    Create a new league with validation.
    """
    # Validation
    if not name or not name.strip():
        return "❌ League name cannot be empty."
    
    if not season or not season.strip():
        return "❌ Season cannot be empty."
    
    name = name.strip()
    season = season.strip()
    
    # Validate season format
    if not validate_season_format(season):
        return "❌ Invalid season format. Use format: YYYY/YYYY (e.g., 2025/2026)"
    
    # Check if league already exists
    if get_league_by_name_and_season(name, season):
        return f"❌ League '{name}' for season '{season}' already exists."
    
    # Create league
    league_id = create_league(name, season)
    if league_id:
        return f"✅ League '{name}' ({season}) created successfully (ID: {league_id})."
    else:
        return "❌ Failed to create league."


def add_club_to_league_cmd(club_name: str, league_name: str, season: str) -> str:
    """
    Add a club to a league.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    
    # Validate club exists
    if not validate_club_exists(club_name):
        return f"❌ Club '{club_name}' not found. Use: Покажи всички клубове"
    
    club_id = get_club_id(club_name)
    
    # Check if club is already in league
    if is_club_in_league(league_id, club_id):
        return f"❌ Club '{club_name}' is already in league '{league_name}'."
    
    # Check if league has matches - prevent adding after schedule generated
    if get_match_count_by_league(league_id) > 0:
        return "❌ Cannot add clubs after schedule has been generated. Delete schedule first or create a new league."
    
    # Add club to league
    if add_club_to_league(league_id, club_id):
        return f"✅ Club '{club_name}' added to league '{league_name}' successfully."
    else:
        return "❌ Failed to add club to league."


def remove_club_from_league_cmd(club_name: str, league_name: str, season: str) -> str:
    """
    Remove a club from a league.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    
    # Validate club exists
    if not validate_club_exists(club_name):
        return f"❌ Club '{club_name}' not found."
    
    club_id = get_club_id(club_name)
    
    # Check if league has matches - prevent removal after schedule generated
    if get_match_count_by_league(league_id) > 0:
        return "❌ Cannot remove clubs after schedule has been generated. Delete schedule first."
    
    # Remove club from league
    if remove_club_from_league(league_id, club_id):
        return f"✅ Club '{club_name}' removed from league '{league_name}' successfully."
    else:
        return "❌ Failed to remove club from league."


def show_clubs_in_league(league_name: str, season: str) -> str:
    """
    Show all clubs in a league.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    clubs = get_clubs_in_league(league_id)
    
    if not clubs:
        return f"📋 No clubs in league '{league_name}'. Add clubs first."
    
    result = f"📋 **CLUBS IN LEAGUE: {league_name} ({season})**\n"
    result += "─" * 60 + "\n"
    for i, club in enumerate(clubs, 1):
        result += f"{i}. ID: {club['id']} | Name: {club['name']} | City: {club['city']}\n"
    result += "─" * 60 + f"\nTotal: {len(clubs)} clubs"
    
    return result


def show_all_leagues() -> str:
    """Show all leagues in database."""
    leagues = get_all_leagues()
    
    if not leagues:
        return "📋 No leagues found in database."
    
    result = "📋 **ALL LEAGUES:**\n"
    result += "─" * 60 + "\n"
    for league in leagues:
        club_count = len(get_clubs_in_league(league["id"]))
        match_count = get_match_count_by_league(league["id"])
        result += f"ID: {league['id']} | {league['name']} | {league['season']} | {club_count} clubs | {match_count} matches\n"
    result += "─" * 60
    
    return result


# =========================
# ROUND-ROBIN ALGORITHM
# =========================

def generate_round_robin(clubs: List[Tuple]) -> List[List[Tuple[int, int]]]:
    """
    Generate round-robin schedule (single round) using Circle method.
    
    Input: List of (club_id, club_name) tuples
    Output: List of rounds, where each round is a list of (home_club_id, away_club_id) tuples
    
    Algorithm (Circle method - guaranteed no repeats):
    - For even N: N-1 rounds, N/2 matches per round
    - For odd N: N rounds, (N-1)/2 matches per round (1 BYE)
    """
    
    if len(clubs) < 2:
        return []
    
    # If odd number, add BYE
    is_odd = len(clubs) % 2 == 1
    if is_odd:
        clubs = list(clubs) + [(None, "BYE")]
    
    n = len(clubs)
    schedule = []
    
    # Arrange teams in a circle
    teams = list(range(len(clubs)))  # Use indices
    
    # Generate rounds using circle rotation
    for round_num in range(n - 1):
        matches = []
        
        # Pair teams
        for i in range(n // 2):
            home_idx = teams[i]
            away_idx = teams[n - 1 - i]
            
            # Get actual club info
            home_club = clubs[home_idx]
            away_club = clubs[away_idx]
            
            # Skip BYE
            if home_club[0] is not None and away_club[0] is not None:
                matches.append((home_club[0], away_club[0]))
        
        schedule.append(matches)
        
        # Rotate: keep first fixed, rotate rest clockwise
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    
    return schedule


def generate_schedule(league_name: str, season: str) -> str:
    """
    Generate round-robin schedule for a league.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    
    # Get clubs in league
    club_rows = get_clubs_in_league(league_id)
    
    if not club_rows:
        return "❌ No clubs in league. Add clubs first."
    
    if len(club_rows) < 2:
        return f"❌ League must have at least 2 clubs. Currently: {len(club_rows)}"
    
    # Check if schedule already exists
    if get_match_count_by_league(league_id) > 0:
        return "❌ Schedule already exists for this league. Use: Прегенерирай програма <име> <сезон> to regenerate or delete existing schedule first."
    
    # Prepare clubs data
    clubs = [(club["id"], club["name"]) for club in club_rows]
    
    # Generate schedule
    rounds = generate_round_robin(clubs)
    
    if not rounds:
        return "❌ Failed to generate schedule."
    
    # Save matches to database
    total_matches = 0
    for round_no, matches in enumerate(rounds, 1):
        for home_club_id, away_club_id in matches:
            match_id = create_match(league_id, round_no, home_club_id, away_club_id)
            if match_id:
                total_matches += 1
    
    # Build response with sample matches
    is_odd = len(clubs) % 2 == 1
    num_rounds = len(clubs) if is_odd else len(clubs) - 1
    expected_matches = (len(clubs) * (len(clubs) - 1)) // 2
    
    result = f"✅ Schedule generated successfully!\n"
    result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    result += f"League: {league_name} ({season})\n"
    result += f"Teams: {len(clubs)}\n"
    result += f"Rounds: {num_rounds}\n"
    result += f"Total Matches: {total_matches}\n"
    
    if is_odd:
        result += f"Note: Odd number of teams - BYE rounds included\n"
    
    result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    # Show first round as sample
    if rounds:
        result += f"\n📅 **ROUND 1 (Sample):**\n"
        for home_id, away_id in rounds[0]:
            home_name = next((c[1] for c in clubs if c[0] == home_id), "Unknown")
            away_name = next((c[1] for c in clubs if c[0] == away_id), "Unknown")
            result += f"  • {home_name} vs {away_name}\n"
    
    return result


def regenerate_schedule(league_name: str, season: str) -> str:
    """
    Delete existing schedule and generate new one.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    
    # Delete existing matches
    if not delete_matches_by_league(league_id):
        return "❌ Failed to delete existing schedule."
    
    # Generate new schedule
    return generate_schedule(league_name, season)


def show_schedule(league_name: str, season: str, round_no: Optional[int] = None) -> str:
    """
    Show schedule for a league or specific round.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    
    # Get matches
    matches = get_matches_by_league(league_id)
    
    if not matches:
        return f"❌ No schedule for league '{league_name}'. Generate schedule first."
    
    # Filter by round if specified
    if round_no:
        matches = [m for m in matches if m["round_no"] == round_no]
        if not matches:
            return f"❌ No matches in round {round_no}."
    
    # Build result
    result = f"📅 **SCHEDULE: {league_name} ({season})**\n"
    result += "━" * 70 + "\n"
    
    current_round = None
    for match in matches:
        if current_round != match["round_no"]:
            if current_round is not None:
                result += "\n"
            current_round = match["round_no"]
            result += f"\n**ROUND {current_round}:**\n"
        
        home = match["home_club_name"]
        away = match["away_club_name"]
        if match["home_goals"] is not None and match["away_goals"] is not None:
            result += f"  • {home} {match['home_goals']}:{match['away_goals']} {away}\n"
        else:
            result += f"  • {home} vs {away}\n"
    
    result += "\n" + "━" * 70
    return result


# =========================
# STATISTICS & INFO
# =========================

def get_league_info(league_name: str, season: str) -> str:
    """Get detailed league information."""
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."
    
    league_id = league["id"]
    clubs = get_clubs_in_league(league_id)
    match_count = get_match_count_by_league(league_id)
    round_count = get_round_count_by_league(league_id)
    
    result = f"ℹ️ **LEAGUE INFO: {league_name} ({season})**\n"
    result += "━" * 60 + "\n"
    result += f"Created: {league['created_at']}\n"
    result += f"Teams: {len(clubs)}\n"
    result += f"Matches: {match_count}\n"
    result += f"Rounds: {round_count}\n"
    result += "━" * 60
    
    return result

