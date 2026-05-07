"""
Standings Repository - Data access layer for league standings calculation.
"""

from db import fetch_all
from typing import List
import sqlite3


def get_league_teams(league_id: int) -> List[sqlite3.Row]:
    """Get all teams in a league with their basic info."""
    return fetch_all(
        """
        SELECT c.id, c.name, c.city
        FROM clubs c
        JOIN league_teams lt ON c.id = lt.club_id
        WHERE lt.league_id = ?
        ORDER BY c.name ASC
        """,
        (league_id,)
    )


def get_played_matches(league_id: int) -> List[sqlite3.Row]:
    """Get all played matches for a league with results."""
    return fetch_all(
        """
        SELECT m.id, m.home_club_id, m.away_club_id,
               m.home_goals, m.away_goals, m.status
        FROM matches m
        WHERE m.league_id = ? AND m.status = 'played'
        ORDER BY m.id ASC
        """,
        (league_id,)
    )


def get_direct_matches(league_id: int, team_ids: List[int]) -> List[sqlite3.Row]:
    """Get direct matches between specific teams for tiebreaker calculation."""
    if len(team_ids) < 2:
        return []

    # Build IN clause for team IDs
    placeholders = ','.join('?' * len(team_ids))
    return fetch_all(
        f"""
        SELECT m.home_club_id, m.away_club_id, m.home_goals, m.away_goals
        FROM matches m
        WHERE m.league_id = ? AND m.status = 'played'
        AND m.home_club_id IN ({placeholders}) AND m.away_club_id IN ({placeholders})
        """,
        [league_id] + team_ids + team_ids
    )
