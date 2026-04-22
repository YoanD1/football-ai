#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interactive test script for chatbot league commands"""

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
print("⚽ CHATBOT LEAGUES INTEGRATION TEST")
print("="*80 + "\n")

# Define test commands
test_commands = [
    ("помощ", "Show help menu"),
    ('Покажи всички лиги', "Show all leagues"),
    ('Създай лига "Първа лига" "2025/2026"', "Create new league"),
    ('Добави отбор "Levski Sofia" в лига "Първа лига" "2025/2026"', "Add club 1"),
    ('Добави отбор "CSKA Sofia" в лига "Първа лига" "2025/2026"', "Add club 2"),
    ('Добави отбор "Ludogorets" в лига "Първа лига" "2025/2026"', "Add club 3"),
    ('Добави отбор "Botev Plovdiv" в лига "Първа лига" "2025/2026"', "Add club 4"),
    ('Покажи отбори в лига "Първа лига" "2025/2026"', "Show clubs in league"),
    ('Генерирай програма "Първа лига" "2025/2026"', "Generate schedule"),
    ('Покажи програма "Първа лига" "2025/2026"', "Show full schedule"),
    ('Покажи програма "Първа лига" "2025/2026" кръг 1', "Show round 1"),
    ('Инфо лига "Първа лига" "2025/2026"', "Show league info"),
]

# Run tests
for i, (command, description) in enumerate(test_commands, 1):
    print(f"{'='*80}")
    print(f"TEST {i}: {description}")
    print(f"{'='*80}")
    print(f"⚽ >> {command}\n")
    
    result = handle_input(command)
    print(result)
    print()

print("\n" + "="*80)
print("✅ CHATBOT INTEGRATION TEST COMPLETED")
print("="*80)

# Check command log
if os.path.exists("commands.log"):
    print("\n📋 COMMANDS LOG (last 10 entries):")
    print("-" * 80)
    with open("commands.log", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[-10:]:
            print(line.strip())

