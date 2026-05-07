"""
Standings Service - Business logic for league standings calculation.
"""

from typing import List, Dict, Optional, Tuple
from repositories.standings_repo import get_league_teams, get_played_matches, get_direct_matches
from repositories.leagues_repo import get_league_by_name_and_season
from db import fetch_all
import sqlite3


class TeamStanding:
    """Represents a team's standing in the league."""
    def __init__(self, team_id: int, team_name: str, team_city: str):
        self.team_id = team_id
        self.team_name = team_name
        self.team_city = team_city
        self.mp = 0  # Matches Played
        self.w = 0   # Wins
        self.d = 0   # Draws
        self.l = 0   # Losses
        self.gf = 0  # Goals For
        self.ga = 0  # Goals Against
        self.gd = 0  # Goal Difference
        self.pts = 0 # Points

    def add_match(self, goals_for: int, goals_against: int):
        """Add a match result to this team's standing."""
        self.mp += 1
        self.gf += goals_for
        self.ga += goals_against
        self.gd = self.gf - self.ga

        if goals_for > goals_against:
            self.w += 1
            self.pts += 3
        elif goals_for == goals_against:
            self.d += 1
            self.pts += 1
        else:
            self.l += 1
            # pts += 0

    def to_dict(self) -> Dict:
        """Convert to dictionary for display."""
        return {
            'team_id': self.team_id,
            'team_name': self.team_name,
            'team_city': self.team_city,
            'mp': self.mp,
            'w': self.w,
            'd': self.d,
            'l': self.l,
            'gf': self.gf,
            'ga': self.ga,
            'gd': self.gd,
            'pts': self.pts
        }


def calculate_standings(league_name: str, season: str) -> str:
    """
    Calculate and display league standings.
    """
    # Validate league exists
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."

    league_id = league["id"]

    # Get teams and matches
    teams_data = get_league_teams(league_id)
    matches = get_played_matches(league_id)

    if not teams_data:
        return f"❌ No teams found in league '{league_name}'."

    # Initialize standings
    standings = {}
    for team in teams_data:
        standings[team["id"]] = TeamStanding(
            team["id"], team["name"], team["city"]
        )

    # Process matches
    for match in matches:
        home_id = match["home_club_id"]
        away_id = match["away_club_id"]
        home_goals = match["home_goals"]
        away_goals = match["away_goals"]

        # Skip matches with null results
        if home_goals is None or away_goals is None:
            continue

        # Add results to both teams
        if home_id in standings:
            standings[home_id].add_match(home_goals, away_goals)
        if away_id in standings:
            standings[away_id].add_match(away_goals, home_goals)

    # Convert to list and sort
    standings_list = list(standings.values())
    standings_list.sort(key=lambda x: (-x.pts, -x.gd, -x.gf, x.team_name))

    # Build result
    result = f"🏆 **LEAGUE STANDINGS: {league_name} ({season})**\n"
    result += "━" * 85 + "\n"
    result += f"{'#':<2} {'Team':<20} {'MP':<2} {'W':<2} {'D':<2} {'L':<2} {'GF':<2} {'GA':<2} {'GD':<3} {'PTS':<3}\n"
    result += "━" * 85 + "\n"

    for position, standing in enumerate(standings_list, 1):
        team = standing.team_name
        if len(team) > 18:  # Truncate long names
            team = team[:15] + "..."

        gd_str = f"{standing.gd:+d}" if standing.gd != 0 else "0"

        result += f"{position:<2} {team:<20} {standing.mp:<2} {standing.w:<2} {standing.d:<2} {standing.l:<2} "
        result += f"{standing.gf:<2} {standing.ga:<2} {gd_str:<3} {standing.pts:<3}\n"

    result += "━" * 85

    # Add summary
    total_matches = len(matches)
    played_matches = sum(s.mp for s in standings_list) // 2  # Each match counted twice
    result += f"\n\n📊 Total matches played: {played_matches}"
    if total_matches > played_matches:
        result += f" (out of {total_matches} scheduled)"

    return result


def calculate_standings_with_tiebreakers(league_name: str, season: str) -> str:
    """
    Calculate standings with advanced tiebreakers (direct matches).
    For excellent grade.
    """
    # Basic calculation first
    basic_result = calculate_standings(league_name, season)
    if "❌" in basic_result:
        return basic_result

    # For now, return basic result - tiebreakers would require more complex sorting
    # TODO: Implement direct match tiebreakers for teams with equal points
    return basic_result


def validate_league_data(league_name: str, season: str) -> str:
    """
    Validate league data consistency.
    """
    league = get_league_by_name_and_season(league_name, season)
    if not league:
        return f"❌ League '{league_name}' ({season}) not found."

    league_id = league["id"]

    # Check for matches with teams not in league
    invalid_matches = fetch_all(
        """
        SELECT COUNT(*) as count FROM matches m
        WHERE m.league_id = ?
        AND (m.home_club_id NOT IN (SELECT club_id FROM league_teams WHERE league_id = ?)
             OR m.away_club_id NOT IN (SELECT club_id FROM league_teams WHERE league_id = ?))
        """,
        (league_id, league_id, league_id)
    )

    if invalid_matches and invalid_matches[0]["count"] > 0:
        return f"⚠️ Warning: Found {invalid_matches[0]['count']} matches with teams not in league."

    return "✅ League data is consistent."
