#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for league management"""

import sys
import os
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from db import initialize_database
from services.leagues_service import (
    create_new_league, add_club_to_league_cmd, 
    show_clubs_in_league, show_all_leagues,
    generate_schedule, show_schedule
)

# Initialize database
print("Initializing database...")
initialize_database()

print("\n" + "="*80)
print("⚽ TESTING LEAGUES MODULE")
print("="*80)

# Test 1: Create league
print("\n✓ TEST 1: Create league")
result = create_new_league("Първа лига", "2025/2026")
print(result)

# Test 2: Show all leagues
print("\n✓ TEST 2: Show all leagues")
result = show_all_leagues()
print(result)

# Test 3: Add club to league
print("\n✓ TEST 3: Add clubs to league")
result = add_club_to_league_cmd("Levski Sofia", "Първа лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("CSKA Sofia", "Първа лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Ludogorets", "Първа лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Botev Plovdiv", "Първа лига", "2025/2026")
print(result)

# Test 4: Show clubs in league
print("\n✓ TEST 4: Show clubs in league")
result = show_clubs_in_league("Първа лига", "2025/2026")
print(result)

# Test 5: Generate schedule
print("\n✓ TEST 5: Generate schedule (4 teams)")
result = generate_schedule("Първа лига", "2025/2026")
print(result)

# Test 6: Show schedule
print("\n✓ TEST 6: Show full schedule")
result = show_schedule("Първа лига", "2025/2026")
print(result)

# Test 7: Show schedule for round 1
print("\n✓ TEST 7: Show schedule for round 1")
result = show_schedule("Първа лига", "2025/2026", 1)
print(result)

# Test 8: Create league with odd number of teams
print("\n✓ TEST 8: Create league with 5 teams (odd)")
result = create_new_league("Втора лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Levski Sofia", "Втора лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("CSKA Sofia", "Втора лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Ludogorets", "Втора лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Botev Plovdiv", "Втора лига", "2025/2026")
print(result)

result = add_club_to_league_cmd("Lokomotiv Plovdiv", "Втора лига", "2025/2026")
print(result)

result = generate_schedule("Втора лига", "2025/2026")
print(result)

print("\n" + "="*80)
print("✅ ALL TESTS COMPLETED")
print("="*80)

