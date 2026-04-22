#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final comprehensive test for Stage 5 Leagues Module"""

import sys
import os
import io

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chatbot import handle_input
from db import initialize_database

# Initialize database
print("Initializing database...")
initialize_database()

print("\n" + "="*80)
print("STAGE 5: LEAGUES MODULE - COMPREHENSIVE TEST")
print("="*80 + "\n")

# Test scenarios grouped by functionality
test_groups = [
    ("LEAGUE CREATION", [
        ('Покажи всички лиги', "Show initial leagues"),
        ('Създай лига "Първа лига" "2025/2026"', "Create new league"),
        ('Покажи всички лиги', "Show leagues after creation"),
    ]),
    ("CLUB MANAGEMENT IN LEAGUES", [
        ('Добави отбор "Levski Sofia" в лига "Първа лига" "2025/2026"', "Add Levski"),
        ('Добави отбор "CSKA Sofia" в лига "Първа лига" "2025/2026"', "Add CSKA"),
        ('Добави отбор "Ludogorets" в лига "Първа лига" "2025/2026"', "Add Ludogorets"),
        ('Добави отбор "Botev Plovdiv" в лига "Първа лига" "2025/2026"', "Add Botev"),
        ('Покажи отбори в лига "Първа лига" "2025/2026"', "Show clubs in league"),
    ]),
    ("SCHEDULE GENERATION (EVEN TEAMS)", [
        ('Генерирай програма "Първа лига" "2025/2026"', "Generate round-robin schedule"),
        ('Покажи програма "Първа лига" "2025/2026"', "Show full schedule"),
        ('Покажи програма "Първа лига" "2025/2026" кръг 1', "Show round 1"),
        ('Покажи програма "Първа лига" "2025/2026" кръг 2', "Show round 2"),
        ('Покажи програма "Първа лига" "2025/2026" кръг 3', "Show round 3"),
    ]),
    ("LEAGUE INFORMATION", [
        ('Инфо лига "Първа лига" "2025/2026"', "Show league info"),
    ]),
    ("ODD TEAMS TEST", [
        ('Създай лига "Втора лига" "2025/2026"', "Create second league"),
        ('Добави отбор "Levski Sofia" в лига "Втора лига" "2025/2026"', "Add Levski to 2nd league"),
        ('Добави отбор "CSKA Sofia" в лига "Втора лига" "2025/2026"', "Add CSKA to 2nd league"),
        ('Добави отбор "Ludogorets" в лига "Втора лига" "2025/2026"', "Add Ludogorets to 2nd league"),
        ('Добави отбор "Botev Plovdiv" в лига "Втора лига" "2025/2026"', "Add Botev to 2nd league"),
        ('Добави отбор "Lokomotiv Plovdiv" в лига "Втора лига" "2025/2026"', "Add Lokomotiv (5th team)"),
        ('Генерирай програма "Втора лига" "2025/2026"', "Generate schedule for 5 teams"),
        ('Покажи програма "Втора лига" "2025/2026"', "Show schedule for odd number"),
    ]),
]

test_counter = 1

for group_name, tests in test_groups:
    print(f"\n{'='*80}")
    print(f"GROUP: {group_name}")
    print(f"{'='*80}\n")
    
    for command, description in tests:
        print(f"[TEST {test_counter}] {description}")
        print(f"Command: {command}")
        print("-" * 80)
        result = handle_input(command)
        # Show first 500 chars
        if len(result) > 500:
            print(result[:500] + "\n...\n[Output truncated, showing first 500 chars]\n")
        else:
            print(result)
        print()
        test_counter += 1

print("\n" + "="*80)
print("✅ COMPREHENSIVE TEST COMPLETED")
print("="*80)

# Show commands log
if os.path.exists("commands.log"):
    print("\n📋 COMMANDS.LOG (all entries):")
    print("-" * 80)
    with open("commands.log", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
    
    # Statistics
    lines = content.strip().split('\n')
    print("\n" + "="*80)
    print(f"📊 LOG STATISTICS: {len(lines)} commands logged")
    print("="*80)

