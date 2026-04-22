import re
import os
import json
from datetime import datetime
from typing import Tuple, Optional

# Import all service modules
from clubs_service import (
    add_club, get_all_clubs, update_club, delete_club, 
    get_club_by_name
)
from players_service import (
    add_player, get_players_by_club, update_player_number,
    update_player_status, delete_player, search_players,
    get_player_by_name
)
from transfers_service import (
    transfer_player, get_transfers_by_player,
    get_transfers_by_club, get_all_transfers
)
from handlers.handlers_leagues import (
    handle_create_league, handle_add_club_to_league,
    handle_remove_club_from_league, handle_show_clubs_in_league,
    handle_show_all_leagues, handle_generate_schedule,
    handle_regenerate_schedule, handle_show_schedule,
    handle_league_info
)
from handlers.handlers_matches import (
    handle_select_league, handle_select_match, handle_show_round,
    handle_record_result, handle_add_goal, handle_add_card, handle_show_events
)


# =========================
# LOGGING
# =========================
def log_command(user_input: str, intent: str, result: str) -> None:
    """Log user commands with timestamp, intent, and result."""
    try:
        with open("commands.log", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] INPUT: {user_input} | INTENT: {intent} | RESULT: {result[:50]}...\n")
    except Exception as e:
        print(f"❌ Logging error: {e}")


# =========================
# INTENT LOADING
# =========================
def load_intents() -> dict:
    """Load intents from intents.json."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    intents_path = os.path.join(base_dir, "intents.json")

    try:
        with open(intents_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading intents: {e}")
        return {"intents": {}}


intents = load_intents()


# =========================
# HELP MENU
# =========================
def show_help() -> str:
    """Display help menu with all available commands."""
    help_text = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    ⚽ FOOTBALL MANAGEMENT CHATBOT ⚽                       ║
║                             Available Commands                             ║
╚════════════════════════════════════════════════════════════════════════════╝

📋 CLUB MANAGEMENT:
  • Добави клуб <ИМЕ> <ГРАД>
    Example: Добави клуб "Левски" "София"
  
  • Покажи всички клубове
  
  • Обнови клуб <ИМЕ> в <НОВ_ГРАД>
    Example: Обнови клуб "Левски" в "Пловдив"
  
  • Изтрий клуб <ИМЕ>
    Example: Изтрий клуб "Левски"

👥 PLAYER MANAGEMENT:
  • Добави играч <ИМЕ> в <КЛУБ> позиция <POS> номер <НОМЕР> дата <ДАТА> [национална <НАЦ>]
    Example: Добави играч "Иван Петров" в "Левски" позиция FW номер 9 дата 1999-05-12 национална България
  
  • Покажи играчи на <КЛУБ>
    Example: Покажи играчи на "Левски"
  
  • Търси играч <КЛЮЧОВА_ДУМ>
    Example: Търси играч "Петров"
  
  • Смени номер на <ИГРАЧ> на <НОВ_НОМЕР>
    Example: Смени номер на "Иван Петров" на 10
  
  • Смени статус на <ИГРАЧ> на <СТАТУС>
    Example: Смени статус на "Иван Петров" на injured
    Valid statuses: active, injured, inactive
  
  • Изтрий играч <ИМЕ>
    Example: Изтрий играч "Иван Петров"

🔄 TRANSFER MANAGEMENT:
  • Трансфер <ИГРАЧ> от <ОТ_КЛУБ> в <ДО_КЛУБ> <ДАТА> [сума <СУМА>]
    Example: Трансфер "Иван Петров" от "Левски" в "Юнайтед" 2025-03-15 сума 500000
  
  • Покажи трансфери на <ИГРАЧ>
    Example: Покажи трансфери на "Иван Петров"
  
  • Трансфери на клуб <КЛУБ>
    Example: Трансфери на клуб "Левски"
  
   • Покажи всички трансфери

⚽ LEAGUE MANAGEMENT:
   • Създай лига "<ИМЕ>" "<СЕЗОН>"
     Example: Създай лига "Първа лига" "2025/2026"
   
   • Добави отбор "<КЛУБ>" в лига "<ИМЕ>" "<СЕЗОН>"
     Example: Добави отбор "Левски" в лига "Първа лига" "2025/2026"
   
   • Премахни отбор "<КЛУБ>" от лига "<ИМЕ>" "<СЕЗОН>"
     Example: Премахни отбор "Левски" от лига "Първа лига" "2025/2026"
   
   • Покажи отбори в лига "<ИМЕ>" "<СЕЗОН>"
     Example: Покажи отбори в лига "Първа лига" "2025/2026"
   
   • Покажи всички лиги
   
   • Генерирай програма "<ИМЕ>" "<СЕЗОН>"
     Example: Генерирай програма "Първа лига" "2025/2026"
   
   • Прегенерирай програма "<ИМЕ>" "<СЕЗОН>"
     Example: Прегенерирай програма "Първа лига" "2025/2026"
   
   • Покажи програма "<ИМЕ>" "<СЕЗОН>" [кръг <НОМЕР>]
     Example: Покажи програма "Първа лига" "2025/2026"
     Example: Покажи програма "Първа лига" "2025/2026" кръг 1
   
   • Инфо лига "<ИМЕ>" "<СЕЗОН>"
     Example: Инфо лига "Първа лига" "2025/2026"

🏆 MATCH MANAGEMENT:
   • Избери лига "<ИМЕ>" "<СЕЗОН>"
     Example: Избери лига "Първа лига" "2025/2026"
   
   • Избери мач <ИД_НА_МАЧА>
     Example: Избери мач 12
   
   • Покажи кръг <НОМЕР> ["<ЛИГА>" "<СЕЗОН>"]
     Example: Покажи кръг 3 "Първа лига" "2025/2026"
   
   • Резултат <ДОМАКИН>-<ГОСТ> <X>:<Y> запиши
     Example: Резултат Левски-Ботев 3:0 запиши
   
   • Гол "<ИГРАЧ>" "<ОТБОР>" <МИНУТА> минута
     Example: Гол "Иван Петров" "Левски" 23 минута
   
   • Картон "<ИГРАЧ>" "<ОТБОР>" <Y/R> <МИНУТА>
     Example: Картон "Иван Петров" "Левски" Y 55
   
   • Покажи събития [MATCH_ID]
     Example: Покажи събития 12

❓ GENERAL:
   • помощ / help - Show this help menu
   • изход / exit - Exit the program

╔════════════════════════════════════════════════════════════════════════════╗
"""
    return help_text


# =========================
# COMMAND HANDLERS
# =========================

def handle_add_club(text: str) -> str:
    """Handle: Добави клуб <ИМЕ> <ГРАД>"""
    match = re.match(r'добави клуб\s+"([^"]+)"\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Добави клуб "<ИМЕ>" "<ГРАД>"\nExample: Добави клуб "Левски" "София"'
    
    name, city = match.groups()
    return add_club(name, city)


def handle_list_clubs() -> str:
    """Handle: Покажи всички клубове"""
    return get_all_clubs()


def handle_update_club(text: str) -> str:
    """Handle: Обнови клуб <ИМЕ> в <НОВ_ГРАД>"""
    match = re.match(r'обнови клуб\s+"([^"]+)"\s+в\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Обнови клуб "<ИМЕ>" в "<НОВ_ГРАД>"\nExample: Обнови клуб "Левски" в "Пловдив"'
    
    name, city = match.groups()
    return update_club(name, city)


def handle_delete_club(text: str) -> str:
    """Handle: Изтрий клуб <ИМЕ>"""
    match = re.match(r'изтрий клуб\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Изтрий клуб "<ИМЕ>"\nExample: Изтрий клуб "Левски"'
    
    name = match.group(1)
    return delete_club(name)


def handle_add_player(text: str) -> str:
    """Handle: Добави играч <ИМЕ> в <КЛУБ> позиция <POS> номер <НОМЕР> дата <ДАТА> [национална <НАЦ>]"""
    # Pattern: добави играч "ИМЕ" в "КЛУБ" позиция POS номер НОМЕР дата ДАТА [национална НАЦ]
    match = re.match(
        r'добави играч\s+"([^"]+)"\s+в\s+"([^"]+)"\s+позиция\s+(\w+)\s+номер\s+(\d+)\s+дата\s+(\d{4}-\d{2}-\d{2})(?:\s+национална\s+(.+))?',
        text, re.IGNORECASE
    )
    
    if not match:
        return ('❌ Format: Добави играч "<ИМЕ>" в "<КЛУБ>" позиция <POS> номер <НОМЕР> дата <ДАТА> [национална <НАЦ>]\n'
                'Example: Добави играч "Иван Петров" в "Левски" позиция FW номер 9 дата 1999-05-12 национална България')
    
    name, club, position, number, birth_date, nationality = match.groups()
    nationality = nationality or "Bulgaria"
    
    try:
        number = int(number)
    except ValueError:
        return "❌ Player number must be a valid integer."
    
    return add_player(name, club, birth_date, nationality, position, number)


def handle_list_players_by_club(text: str) -> str:
    """Handle: Покажи играчи на <КЛУБ>"""
    match = re.match(r'покажи играчи на\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Покажи играчи на "<КЛУБ>"\nExample: Покажи играчи на "Левски"'
    
    club = match.group(1)
    return get_players_by_club(club)


def handle_search_players(text: str) -> str:
    """Handle: Търси играч <КЛЮЧОВА_ДУМ>"""
    match = re.match(r'търси играч\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Търси играч "<КЛЮЧОВА_ДУМ>"\nExample: Търси играч "Петров"'
    
    keyword = match.group(1)
    return search_players(keyword)


def handle_update_player_number(text: str) -> str:
    """Handle: Смени номер на <ИГРАЧ> на <НОВ_НОМЕР>"""
    match = re.match(r'смени номер на\s+"([^"]+)"\s+на\s+(\d+)', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Смени номер на "<ИГРАЧ>" на <НОМЕР>\nExample: Смени номер на "Иван Петров" на 10'
    
    player, number = match.groups()
    try:
        number = int(number)
    except ValueError:
        return "❌ Player number must be a valid integer."
    
    return update_player_number(player, number)


def handle_update_player_status(text: str) -> str:
    """Handle: Смени статус на <ИГРАЧ> на <СТАТУС>"""
    match = re.match(r'смени статус на\s+"([^"]+)"\s+на\s+(\w+)', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Смени статус на "<ИГРАЧ>" на <СТАТУС>\nExample: Смени статус на "Иван Петров" на injured'
    
    player, status = match.groups()
    return update_player_status(player, status)


def handle_delete_player(text: str) -> str:
    """Handle: Изтрий играч <ИМЕ>"""
    match = re.match(r'изтрий играч\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Изтрий играч "<ИМЕ>"\nExample: Изтрий играч "Иван Петров"'
    
    player = match.group(1)
    return delete_player(player)


def handle_transfer_player(text: str) -> str:
    """Handle: Трансфер <ИГРАЧ> от <ОТ_КЛУБ> в <ДО_КЛУБ> <ДАТА> [сума <СУМА>]"""
    # Pattern: трансфер "ИГРАЧ" от "ОТ" в "ДО" ДАТА [сума СУМА]
    match = re.match(
        r'трансфер\s+"([^"]+)"\s+от\s+"([^"]+)"\s+в\s+"([^"]+)"\s+(\d{4}-\d{2}-\d{2})(?:\s+сума\s+([\d.]+))?',
        text, re.IGNORECASE
    )
    
    if not match:
        return ('❌ Format: Трансфер "<ИГРАЧ>" от "<ОТ_КЛУБ>" в "<ДО_КЛУБ>" <ДАТА> [сума <СУМА>]\n'
                'Example: Трансфер "Иван Петров" от "Левски" в "ЦСКА" 2025-03-15 сума 500000')
    
    player, from_club, to_club, date, fee = match.groups()
    fee = float(fee) if fee else None
    
    return transfer_player(player, from_club, to_club, date, fee)


def handle_list_transfers_by_player(text: str) -> str:
    """Handle: Покажи трансфери на <ИГРАЧ>"""
    match = re.match(r'покажи трансфери на\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Покажи трансфери на "<ИГРАЧ>"\nExample: Покажи трансфери на "Иван Петров"'
    
    player = match.group(1)
    return get_transfers_by_player(player)


def handle_list_transfers_by_club(text: str) -> str:
    """Handle: Трансфери на клуб <КЛУБ>"""
    match = re.match(r'трансфери на клуб\s+"([^"]+)"', text, re.IGNORECASE)
    if not match:
        return '❌ Format: Трансфери на клуб "<КЛУБ>"\nExample: Трансфери на клуб "Левски"'
    
    club = match.group(1)
    return get_transfers_by_club(club)


# =========================
# MAIN INPUT HANDLER
# =========================
def handle_input(user_input: str) -> str:
    """
    Main input handler that routes to appropriate intent handler.
    """
    text = user_input.lower().strip()
    
    # HELP
    if text in intents["intents"]["help"]:
        log_command(user_input, "help", "help menu displayed")
        return show_help()
    
    # EXIT
    if text in intents["intents"]["exit"]:
        log_command(user_input, "exit", "exit command")
        return "exit"
    
    # CLUB COMMANDS
    if any(text.startswith(cmd) for cmd in intents["intents"]["add_club"]):
        result = handle_add_club(text)
        log_command(user_input, "add_club", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["list_clubs"]):
        result = handle_list_clubs()
        log_command(user_input, "list_clubs", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["update_club"]):
        result = handle_update_club(text)
        log_command(user_input, "update_club", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["delete_club"]):
        result = handle_delete_club(text)
        log_command(user_input, "delete_club", result)
        return result
    
    # PLAYER COMMANDS
    if any(text.startswith(cmd) for cmd in intents["intents"]["add_player"]):
        result = handle_add_player(text)
        log_command(user_input, "add_player", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["list_players_by_club"]):
        result = handle_list_players_by_club(text)
        log_command(user_input, "list_players", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["search_players"]):
        result = handle_search_players(text)
        log_command(user_input, "search_players", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["update_player_number"]):
        result = handle_update_player_number(text)
        log_command(user_input, "update_player_number", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["update_player_status"]):
        result = handle_update_player_status(text)
        log_command(user_input, "update_player_status", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["delete_player"]):
        result = handle_delete_player(text)
        log_command(user_input, "delete_player", result)
        return result
    
    # TRANSFER COMMANDS
    # Check longer/more specific patterns FIRST
    if any(text.startswith(cmd) for cmd in intents["intents"]["list_transfers_by_club"]):
        result = handle_list_transfers_by_club(text)
        log_command(user_input, "list_transfers_by_club", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["list_transfers_by_player"]):
        result = handle_list_transfers_by_player(text)
        log_command(user_input, "list_transfers_by_player", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["list_all_transfers"]):
        result = get_all_transfers()
        log_command(user_input, "list_all_transfers", result)
        return result
    
    # Check shorter pattern AFTER longer patterns
    if any(text.startswith(cmd) for cmd in intents["intents"]["transfer_player"]):
        result = handle_transfer_player(text)
        log_command(user_input, "transfer_player", result)
        return result
    
    # LEAGUE COMMANDS
    if any(text.startswith(cmd) for cmd in intents["intents"]["create_league"]):
        result = handle_create_league(text)
        log_command(user_input, "create_league", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["add_club_to_league"]):
        result = handle_add_club_to_league(text)
        log_command(user_input, "add_club_to_league", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["remove_club_from_league"]):
        result = handle_remove_club_from_league(text)
        log_command(user_input, "remove_club_from_league", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["show_clubs_in_league"]):
        result = handle_show_clubs_in_league(text)
        log_command(user_input, "show_clubs_in_league", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["show_all_leagues"]):
        result = handle_show_all_leagues()
        log_command(user_input, "show_all_leagues", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["regenerate_schedule"]):
        result = handle_regenerate_schedule(text)
        log_command(user_input, "regenerate_schedule", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["generate_schedule"]):
        result = handle_generate_schedule(text)
        log_command(user_input, "generate_schedule", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["show_schedule"]):
        result = handle_show_schedule(text)
        log_command(user_input, "show_schedule", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["league_info"]):
        result = handle_league_info(text)
        log_command(user_input, "league_info", result)
        return result
    
    # MATCH COMMANDS
    if any(text.startswith(cmd) for cmd in intents["intents"]["select_league"]):
        result = handle_select_league(text)
        log_command(user_input, "select_league", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["select_match"]):
        result = handle_select_match(text)
        log_command(user_input, "select_match", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["show_round"]):
        result = handle_show_round(text)
        log_command(user_input, "show_round", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["record_result"]):
        result = handle_record_result(text)
        log_command(user_input, "record_result", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["add_goal"]):
        result = handle_add_goal(text)
        log_command(user_input, "add_goal", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["add_card"]):
        result = handle_add_card(text)
        log_command(user_input, "add_card", result)
        return result
    
    if any(text.startswith(cmd) for cmd in intents["intents"]["show_events"]):
        result = handle_show_events(text)
        log_command(user_input, "show_events", result)
        return result
    
    # UNKNOWN COMMAND
    result = "❌ Unknown command. Type 'помощ' or 'help' for available commands."
    log_command(user_input, "unknown", result)
    return result

