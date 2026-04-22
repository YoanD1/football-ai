"""
Repositories module for Leagues management.
Handles all SQL operations for leagues, league_teams, and matches.
"""

from db import fetch_one, fetch_all, execute_query, get_last_insert_id
from typing import Optional, List, Tuple
import sqlite3


# =========================
# LEAGUES REPOSITORY
# =========================

def create_league(name: str, season: str) -> Optional[int]:
    """
    Create a new league.
    Returns: league_id on success, None on failure.
    """
    try:
        league_id = get_last_insert_id(
            "INSERT INTO leagues (name, season) VALUES (?, ?)",
            (name, season)
        )
        return league_id
    except Exception as e:
        print(f"❌ Error creating league: {e}")
        return None


def get_league_by_name_and_season(name: str, season: str) -> Optional[sqlite3.Row]:
    """Get league by name and season."""
    return fetch_one(
        "SELECT id, name, season, created_at FROM leagues WHERE name = ? AND season = ?",
        (name, season)
    )


def get_league_by_id(league_id: int) -> Optional[sqlite3.Row]:
    """Get league by ID."""
    return fetch_one(
        "SELECT id, name, season, created_at FROM leagues WHERE id = ?",
        (league_id,)
    )


def get_all_leagues() -> List[sqlite3.Row]:
    """Get all leagues."""
    return fetch_all(
        "SELECT id, name, season, created_at FROM leagues ORDER BY season DESC, name ASC"
    )


def delete_league(league_id: int) -> bool:
    """Delete a league (cascades to league_teams and matches)."""
    return execute_query(
        "DELETE FROM leagues WHERE id = ?",
        (league_id,)
    )


# =========================
# LEAGUE_TEAMS REPOSITORY
# =========================

def add_club_to_league(league_id: int, club_id: int) -> bool:
    """Add a club to a league."""
    try:
        return execute_query(
            "INSERT INTO league_teams (league_id, club_id) VALUES (?, ?)",
            (league_id, club_id)
        )
    except Exception as e:
        print(f"❌ Error adding club to league: {e}")
        return False


def remove_club_from_league(league_id: int, club_id: int) -> bool:
    """Remove a club from a league."""
    return execute_query(
        "DELETE FROM league_teams WHERE league_id = ? AND club_id = ?",
        (league_id, club_id)
    )


def get_clubs_in_league(league_id: int) -> List[sqlite3.Row]:
    """Get all clubs in a league."""
    return fetch_all(
        """
        SELECT c.id, c.name, c.city, lt.joined_at
        FROM clubs c
        JOIN league_teams lt ON c.id = lt.club_id
        WHERE lt.league_id = ?
        ORDER BY c.name ASC
        """,
        (league_id,)
    )


def is_club_in_league(league_id: int, club_id: int) -> bool:
    """Check if a club is already in a league."""
    result = fetch_one(
        "SELECT 1 FROM league_teams WHERE league_id = ? AND club_id = ?",
        (league_id, club_id)
    )
    return result is not None


# =========================
# MATCHES REPOSITORY
# =========================

def create_match(
    league_id: int,
    round_no: int,
    home_club_id: int,
    away_club_id: int,
    match_date: Optional[str] = None
) -> Optional[int]:
    """
    Create a new match.
    Returns: match_id on success, None on failure.
    """
    try:
        match_id = get_last_insert_id(
            """
            INSERT INTO matches (league_id, round_no, home_club_id, away_club_id, match_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (league_id, round_no, home_club_id, away_club_id, match_date)
        )
        return match_id
    except Exception as e:
        print(f"❌ Error creating match: {e}")
        return None


def get_matches_by_league(league_id: int) -> List[sqlite3.Row]:
    """Get all matches for a league."""
    return fetch_all(
        """
        SELECT m.id, m.league_id, m.round_no, 
               m.home_club_id, h.name as home_club_name,
               m.away_club_id, a.name as away_club_name,
               m.match_date, m.home_goals, m.away_goals
        FROM matches m
        JOIN clubs h ON m.home_club_id = h.id
        JOIN clubs a ON m.away_club_id = a.id
        WHERE m.league_id = ?
        ORDER BY m.round_no ASC, m.id ASC
        """,
        (league_id,)
    )


def get_matches_by_league_and_round(league_id: int, round_no: int) -> List[sqlite3.Row]:
    """Get all matches for a specific round in a league."""
    return fetch_all(
        """
        SELECT m.id, m.league_id, m.round_no, 
               m.home_club_id, h.name as home_club_name,
               m.away_club_id, a.name as away_club_name,
               m.match_date, m.home_goals, m.away_goals
        FROM matches m
        JOIN clubs h ON m.home_club_id = h.id
        JOIN clubs a ON m.away_club_id = a.id
        WHERE m.league_id = ? AND m.round_no = ?
        ORDER BY m.id ASC
        """,
        (league_id, round_no)
    )


def match_exists(league_id: int, round_no: int, home_id: int, away_id: int) -> bool:
    """Check if a match already exists in a league and round."""
    result = fetch_one(
        """
        SELECT 1 FROM matches
        WHERE league_id = ? AND round_no = ? AND home_club_id = ? AND away_club_id = ?
        """,
        (league_id, round_no, home_id, away_id)
    )
    return result is not None


def get_match_count_by_league(league_id: int) -> int:
    """Get total number of matches in a league."""
    result = fetch_one(
        "SELECT COUNT(*) as count FROM matches WHERE league_id = ?",
        (league_id,)
    )
    return result["count"] if result else 0


def get_round_count_by_league(league_id: int) -> int:
    """Get number of rounds in a league."""
    result = fetch_one(
        "SELECT MAX(round_no) as max_round FROM matches WHERE league_id = ?",
        (league_id,)
    )
    return result["max_round"] if result and result["max_round"] else 0


def delete_matches_by_league(league_id: int) -> bool:
    """Delete all matches for a league."""
    return execute_query(
        "DELETE FROM matches WHERE league_id = ?",
        (league_id,)
    )


def update_match_result(match_id: int, home_goals: int, away_goals: int) -> bool:
    """Update match result (goals)."""
    return execute_query(
        "UPDATE matches SET home_goals = ?, away_goals = ? WHERE id = ?",
        (home_goals, away_goals, match_id)
    )

