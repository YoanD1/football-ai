"""Chatbot handlers for Standings commands."""

import re
from services.standings_service import calculate_standings


def handle_show_standings(text: str) -> str:
    """Handle: Покажи класиране <league> <season>"""
    match = re.match(
        r'покажи класиране\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Покажи класиране "<ЛИГА>" "<СЕЗОН>"\n'
                'Example: Покажи класиране "Първа лига" "2025/2026"')

    league_name, season = match.groups()
    return calculate_standings(league_name, season)
