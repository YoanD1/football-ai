#!/usr/bin/env python3
"""
Test script for Football Management System
Demonstrates all major functionality
"""

import sys
import io

# Fix Unicode output in Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chatbot import handle_input

def test_system():
    """Run a series of test commands"""
    
    test_commands = [
        # Show help
        ("help", "Show help menu"),
        
        # List initial clubs
        ("Покажи всички клубове", "List all clubs"),
        
        # List players by club
        ('Покажи играчи на "Levski Sofia"', "List players in Levski Sofia"),
        
        # Search for a player
        ('Търси играч "Petrov"', "Search for players named Petrov"),
        
        # Show transfers by player
        ('Покажи трансфери на "Ivan Petrov"', "Show transfers for Ivan Petrov"),
        
        # Show transfers by club
        ('Трансфери на клуб "Levski Sofia"', "Show transfers for Levski Sofia"),
        
        # Show all transfers
        ("Покажи всички трансфери", "Show all transfers"),
        
        # Add a new club
        ('Добави клуб "Spartak Sofia" "Sofia"', "Add new club Spartak Sofia"),
        
        # Add a new player
        ('Добави играч "Alexander Aleksandrov" в "Spartak Sofia" позиция MF номер 7 дата 2000-01-10 национална България', "Add new player"),
        
        # Update player number
        ('Смени номер на "Ivan Petrov" на 11', "Change player number"),
        
        # Update player status
        ('Смени статус на "Ivan Petrov" на injured', "Change player status"),
        
        # Transfer player
        ('Трансфер "Alexander Aleksandrov" от "Spartak Sofia" в "CSKA Sofia" 2025-03-25 сума 250000', "Transfer a player"),
    ]
    
    print("\n" + "="*80)
    print("⚽ FOOTBALL MANAGEMENT SYSTEM - TEST SUITE ⚽")
    print("="*80 + "\n")
    
    for command, description in test_commands:
        print(f"📋 TEST: {description}")
        print(f"   Command: {command}\n")
        
        result = handle_input(command)
        
        if result != "exit":
            print(result)
        
        print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    test_system()
    print("✅ All tests completed!")

