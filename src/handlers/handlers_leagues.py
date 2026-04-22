"""Chatbot handlers for League commands."""

import re
from services.leagues_service import (
    create_new_league, add_club_to_league_cmd, remove_club_from_league_cmd,
    show_clubs_in_league, show_all_leagues, generate_schedule,
    regenerate_schedule, show_schedule, get_league_info
)


def handle_create_league(text: str) -> str:
    """Handle: Създай лига <име> <сезон>"""
    match = re.match(r'създай лига\s+"([^"]+)"\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return ('❌ Format: Създай лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Създай лига "Първа лига" "2025/2026"')
    
    name, season = match.groups()
    return create_new_league(name, season)


def handle_add_club_to_league(text: str) -> str:
    """Handle: Добави отбор <клуб> в лига <име> <сезон>"""
    match = re.match(
        r'добави отбор\s+"([^"]+)"\s+в лига\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Добави отбор "<КЛУБ>" в лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Добави отбор "Левски" в лига "Първа лига" "2025/2026"')
    
    club_name, league_name, season = match.groups()
    return add_club_to_league_cmd(club_name, league_name, season)


def handle_remove_club_from_league(text: str) -> str:
    """Handle: Премахни отбор <клуб> от лига <име> <сезон>"""
    match = re.match(
        r'премахни отбор\s+"([^"]+)"\s+от лига\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Премахни отбор "<КЛУБ>" от лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Премахни отбор "Левски" от лига "Първа лига" "2025/2026"')
    
    club_name, league_name, season = match.groups()
    return remove_club_from_league_cmd(club_name, league_name, season)


def handle_show_clubs_in_league(text: str) -> str:
    """Handle: Покажи отбори в лига <име> <сезон>"""
    match = re.match(
        r'покажи отбори в лига\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Покажи отбори в лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Покажи отбори в лига "Първа лига" "2025/2026"')
    
    league_name, season = match.groups()
    return show_clubs_in_league(league_name, season)


def handle_show_all_leagues() -> str:
    """Handle: Покажи всички лиги"""
    return show_all_leagues()


def handle_generate_schedule(text: str) -> str:
    """Handle: Генерирай програма <име> <сезон>"""
    match = re.match(
        r'генерирай програма\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Генерирай програма "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Генерирай програма "Първа лига" "2025/2026"')
    
    league_name, season = match.groups()
    return generate_schedule(league_name, season)


def handle_regenerate_schedule(text: str) -> str:
    """Handle: Прегенерирай програма <име> <сезон>"""
    match = re.match(
        r'прегенерирай програма\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Прегенерирай програма "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Прегенерирай програма "Първа лига" "2025/2026"')
    
    league_name, season = match.groups()
    return regenerate_schedule(league_name, season)


def handle_show_schedule(text: str) -> str:
    """Handle: Покажи програма <име> <сезон> [кръг <номер>]"""
    match = re.match(
        r'покажи програма\s+"([^"]+)"\s+"([^"]+)"(?:\s+кръг\s+(\d+))?',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Покажи програма "<ИМЕ>" "<СЕЗОН>" [кръг <НОМЕР>]\n'
                'Example: Покажи програма "Първа лига" "2025/2026"')
    
    league_name, season, round_no = match.groups()
    round_no = int(round_no) if round_no else None
    return show_schedule(league_name, season, round_no)


def handle_league_info(text: str) -> str:
    """Handle: Инфо лига <име> <сезон>"""
    match = re.match(
        r'инфо лига\s+"([^"]+)"\s+"([^"]+)"',
        text, re.IGNORECASE
    )
    if not match:
        return ('❌ Format: Инфо лига "<ИМЕ>" "<СЕЗОН>"\n'
                'Example: Инфо лига "Първа лига" "2025/2026"')
    
    league_name, season = match.groups()
    return get_league_info(league_name, season)
