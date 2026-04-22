"""Chatbot handlers for Match commands."""

import re
from services.matches_service import (
    select_league, get_current_league, select_match, get_current_match,
    show_round, record_result, add_goal_to_match, add_card_to_match, show_match_events
)


def handle_select_league(text: str) -> str:
    """Handle: Избери лига <name> <season>"""
    match = re.match(r'избери лига\s+"([^"]+)"\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return ('❌ Format: Избери лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Избери лига "Първа лига" "2025/2026"')
    
    name, season = match.groups()
    return select_league(name, season)


def handle_select_match(text: str) -> str:
    """Handle: Избери мач <match_id>"""
    match = re.match(r'избери мач\s+(\d+)', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Избери мач <MATCH_ID>\nExample: Избери мач 12'
    
    match_id = int(match.group(1))
    return select_match(match_id)


def handle_show_round(text: str) -> str:
    """Handle: Покажи кръг <round_no> <league> <season>"""
    # First try with league specified
    match = re.match(r'покажи кръг\s+(\d+)\s+"([^"]+)"\s+"([^"]+)"', text, re.IGNORECASE)
    if match:
        round_no, league_name, season = match.groups()
        round_no = int(round_no)
        # Select league first
        league_result = select_league(league_name, season)
        if "❌" in league_result:
            return league_result
        return show_round(round_no)
    
    # Try with current league
    match = re.match(r'покажи кръг\s+(\d+)', text, re.IGNORECASE)
    if match:
        round_no = int(match.group(1))
        return show_round(round_no)
    
    return ('❌ Format: Покажи кръг <НОМЕР> ["<ЛИГА>" "<СЕЗОН>"]\n'
            'Example: Покажи кръг 3 "Първа лига" "2025/2026"')


def handle_record_result(text: str) -> str:
    """Handle: Резултат <home>-<away> <home_goals>:<away_goals> запиши"""
    match = re.match(r'резултат\s+([^-]+)-([^\s]+)\s+(\d+):(\d+)\s+запиши', text, re.IGNORECASE)
    if not match:
        return ('❌ Format: Резултат <ДОМАКИН>-<ГОСТ> <X>:<Y> запиши\n'
                'Example: Резултат Левски-Ботев 3:0 запиши')
    
    home_club, away_club, home_goals, away_goals = match.groups()
    home_goals = int(home_goals)
    away_goals = int(away_goals)
    
    return record_result(home_club.strip(), away_club.strip(), home_goals, away_goals)


def handle_add_goal(text: str) -> str:
    """Handle: Гол <player> <club> <minute> минута"""
    match = re.match(r'гол\s+"([^"]+)"\s+"([^"]+)"\s+(\d+)\s+минута', text, re.IGNORECASE)
    if not match:
        return ('❌ Format: Гол "<ИГРАЧ>" "<ОТБОР>" <МИНУТА> минута\n'
                'Example: Гол "Иван Петров" "Левски" 23 минута')
    
    player_name, club_name, minute = match.groups()
    minute = int(minute)
    
    return add_goal_to_match(player_name, club_name, minute)


def handle_add_card(text: str) -> str:
    """Handle: Картон <player> <club> <Y/R> <minute>"""
    match = re.match(r'картон\s+"([^"]+)"\s+"([^"]+)"\s+([YR])\s+(\d+)', text, re.IGNORECASE)
    if not match:
        return ('❌ Format: Картон "<ИГРАЧ>" "<ОТБОР>" <Y/R> <МИНУТА>\n'
                'Example: Картон "Иван Петров" "Левски" Y 55')
    
    player_name, club_name, card_type, minute = match.groups()
    minute = int(minute)
    
    return add_card_to_match(player_name, club_name, card_type.upper(), minute)


def handle_show_events(text: str) -> str:
    """Handle: Покажи събития [match_id]"""
    match = re.match(r'покажи събития(?:\s+(\d+))?', text, re.IGNORECASE)
    if match:
        match_id = match.group(1)
        match_id = int(match_id) if match_id else None
        return show_match_events(match_id)
    
    return '❌ Format: Покажи събития [MATCH_ID]\nExample: Покажи събития 12'
