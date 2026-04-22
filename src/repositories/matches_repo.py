"""
Matches Repository - Data access layer for matches, goals, and cards
"""

from db import fetch_one, fetch_all, execute_query, get_last_insert_id
from typing import Optional, List
import sqlite3


# =========================
# MATCHES OPERATIONS
# =========================

def get_match_by_id(match_id: int) -> Optional[sqlite3.Row]:
    """Get match by ID with club details."""
    return fetch_one(
        """
        SELECT m.id, m.league_id, m.round_no, 
               m.home_club_id, h.name as home_club_name,
               m.away_club_id, a.name as away_club_name,
               m.match_date, m.home_goals, m.away_goals, m.status
        FROM matches m
        JOIN clubs h ON m.home_club_id = h.id
        JOIN clubs a ON m.away_club_id = a.id
        WHERE m.id = ?
        """,
        (match_id,)
    )


def get_matches_by_round(league_id: int, round_no: int) -> List[sqlite3.Row]:
    """Get all matches for a specific round in a league."""
    return fetch_all(
        """
        SELECT m.id, m.league_id, m.round_no,
               m.home_club_id, h.name as home_club_name,
               m.away_club_id, a.name as away_club_name,
               m.match_date, m.home_goals, m.away_goals, m.status
        FROM matches m
        JOIN clubs h ON m.home_club_id = h.id
        JOIN clubs a ON m.away_club_id = a.id
        WHERE m.league_id = ? AND m.round_no = ?
        ORDER BY m.id ASC
        """,
        (league_id, round_no)
    )


def get_match_by_clubs_and_league(home_id: int, away_id: int, league_id: int) -> Optional[sqlite3.Row]:
    """Get match between two clubs in a league."""
    return fetch_one(
        """
        SELECT m.id, m.league_id, m.round_no,
               m.home_club_id, h.name as home_club_name,
               m.away_club_id, a.name as away_club_name,
               m.match_date, m.home_goals, m.away_goals, m.status
        FROM matches m
        JOIN clubs h ON m.home_club_id = h.id
        JOIN clubs a ON m.away_club_id = a.id
        WHERE m.home_club_id = ? AND m.away_club_id = ? AND m.league_id = ?
        """,
        (home_id, away_id, league_id)
    )


def update_match_result(match_id: int, home_goals: int, away_goals: int) -> bool:
    """Update match result and mark as played."""
    return execute_query(
        """
        UPDATE matches 
        SET home_goals = ?, away_goals = ?, status = 'played', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (home_goals, away_goals, match_id)
    )


def is_match_played(match_id: int) -> bool:
    """Check if match has been played."""
    result = fetch_one(
        "SELECT status FROM matches WHERE id = ?",
        (match_id,)
    )
    return result and result["status"] == "played"


# =========================
# GOALS OPERATIONS
# =========================

def add_goal(match_id: int, player_id: int, club_id: int, minute: int, is_own_goal: int = 0) -> Optional[int]:
    """Add a goal record."""
    try:
        goal_id = get_last_insert_id(
            """
            INSERT INTO goals (match_id, player_id, club_id, minute, is_own_goal)
            VALUES (?, ?, ?, ?, ?)
            """,
            (match_id, player_id, club_id, minute, is_own_goal)
        )
        return goal_id
    except Exception as e:
        print(f"❌ Error adding goal: {e}")
        return None


def get_goals_by_match(match_id: int) -> List[sqlite3.Row]:
    """Get all goals for a match, ordered by minute."""
    return fetch_all(
        """
        SELECT g.id, g.match_id, g.player_id, p.full_name,
               g.club_id, c.name as club_name, g.minute, g.is_own_goal
        FROM goals g
        JOIN players p ON g.player_id = p.id
        JOIN clubs c ON g.club_id = c.id
        WHERE g.match_id = ?
        ORDER BY g.minute ASC
        """,
        (match_id,)
    )


def get_player_goals_in_match(match_id: int, player_id: int) -> int:
    """Get goal count for a player in a match."""
    result = fetch_one(
        """
        SELECT COUNT(*) as count FROM goals
        WHERE match_id = ? AND player_id = ? AND is_own_goal = 0
        """,
        (match_id, player_id)
    )
    return result["count"] if result else 0


def delete_goal(goal_id: int) -> bool:
    """Delete a goal record."""
    return execute_query(
        "DELETE FROM goals WHERE id = ?",
        (goal_id,)
    )


# =========================
# CARDS OPERATIONS
# =========================

def add_card(match_id: int, player_id: int, club_id: int, minute: int, card_type: str) -> Optional[int]:
    """Add a card record (Y=yellow, R=red)."""
    try:
        card_id = get_last_insert_id(
            """
            INSERT INTO cards (match_id, player_id, club_id, minute, card_type)
            VALUES (?, ?, ?, ?, ?)
            """,
            (match_id, player_id, club_id, minute, card_type)
        )
        return card_id
    except Exception as e:
        print(f"❌ Error adding card: {e}")
        return None


def get_cards_by_match(match_id: int) -> List[sqlite3.Row]:
    """Get all cards for a match, ordered by minute."""
    return fetch_all(
        """
        SELECT c.id, c.match_id, c.player_id, p.full_name,
               c.club_id, cl.name as club_name, c.minute, c.card_type
        FROM cards c
        JOIN players p ON c.player_id = p.id
        JOIN clubs cl ON c.club_id = cl.id
        WHERE c.match_id = ?
        ORDER BY c.minute ASC
        """,
        (match_id,)
    )


def get_player_cards_in_match(match_id: int, player_id: int) -> dict:
    """Get yellow and red cards for a player in a match."""
    result = fetch_all(
        """
        SELECT card_type, COUNT(*) as count FROM cards
        WHERE match_id = ? AND player_id = ?
        GROUP BY card_type
        """,
        (match_id, player_id)
    )
    
    cards = {"Y": 0, "R": 0}
    if result:
        for row in result:
            cards[row["card_type"]] = row["count"]
    
    return cards


def get_player_red_cards_in_match(match_id: int, player_id: int) -> int:
    """Get red card count for a player in a match."""
    result = fetch_one(
        """
        SELECT COUNT(*) as count FROM cards
        WHERE match_id = ? AND player_id = ? AND card_type = 'R'
        """,
        (match_id, player_id)
    )
    return result["count"] if result else 0


def delete_card(card_id: int) -> bool:
    """Delete a card record."""
    return execute_query(
        "DELETE FROM cards WHERE id = ?",
        (card_id,)
    )


# =========================
# COMBINED OPERATIONS
# =========================

def get_match_events(match_id: int) -> dict:
    """Get all events (goals + cards) for a match."""
    goals = get_goals_by_match(match_id)
    cards = get_cards_by_match(match_id)
    
    return {
        "goals": goals,
        "cards": cards
    }


def delete_all_match_events(match_id: int) -> bool:
    """Delete all goals and cards for a match."""
    try:
        execute_query("DELETE FROM goals WHERE match_id = ?", (match_id,))
        execute_query("DELETE FROM cards WHERE match_id = ?", (match_id,))
        return True
    except Exception as e:
        print(f"❌ Error deleting match events: {e}")
        return False

