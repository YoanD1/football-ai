#!/usr/bin/env python3
"""
Sample Interactive Session for Football Management System
Demonstrates real-world usage patterns
"""

import sys
import io

# Fix Unicode output in Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chatbot import handle_input

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def demo_session():
    """Run an interactive demo session"""
    
    print_section("⚽ FOOTBALL MANAGEMENT SYSTEM - INTERACTIVE DEMO ⚽")
    
    # Demo 1: View all clubs
    print("👉 Demo 1: View all clubs in the system")
    print("   Command: Покажи всички клубове\n")
    result = handle_input("Покажи всички клубове")
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 2: View players in a club
    print_section("👉 Demo 2: View all players in Levski Sofia")
    print("   Command: Покажи играчи на \"Levski Sofia\"\n")
    result = handle_input('Покажи играчи на "Levski Sofia"')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 3: Search for a player
    print_section("👉 Demo 3: Search for players named 'Petrov'")
    print("   Command: Търси играч \"Petrov\"\n")
    result = handle_input('Търси играч "Petrov"')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 4: View player's transfer history
    print_section("👉 Demo 4: View transfer history for Ivan Petrov")
    print("   Command: Покажи трансфери на \"Ivan Petrov\"\n")
    result = handle_input('Покажи трансфери на "Ivan Petrov"')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 5: View club's transfers
    print_section("👉 Demo 5: View all transfers involving Levski Sofia")
    print("   Command: Трансфери на клуб \"Levski Sofia\"\n")
    result = handle_input('Трансфери на клуб "Levski Sofia"')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 6: View all transfers
    print_section("👉 Demo 6: View all transfers in the system")
    print("   Command: Покажи всички трансфери\n")
    result = handle_input("Покажи всички трансфери")
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 7: Add a new club
    print_section("👉 Demo 7: Add a new club to the system")
    print("   Command: Добави клуб \"Slaviya Sofia\" \"Sofia\"\n")
    result = handle_input('Добави клуб "Slaviya Sofia" "Sofia"')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 8: Add a player to the new club
    print_section("👉 Demo 8: Add a new player to Slaviya Sofia")
    print('   Command: Добави играч "Dimitar Kitov" в "Slaviya Sofia" позиция FW номер 10 дата 1990-07-15 национална България\n')
    result = handle_input('Добави играч "Dimitar Kitov" в "Slaviya Sofia" позиция FW номер 10 дата 1990-07-15 национална България')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 9: Change player status
    print_section("👉 Demo 9: Mark a player as injured")
    print('   Command: Смени статус на "Ivan Petrov" на injured\n')
    result = handle_input('Смени статус на "Ivan Petrov" на injured')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 10: Change player number
    print_section("👉 Demo 10: Change player's jersey number")
    print('   Command: Смени номер на "Ivan Petrov" на 12\n')
    result = handle_input('Смени номер на "Ivan Petrov" на 12')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 11: Transfer a player
    print_section("👉 Demo 11: Transfer Dimitar Kitov to Ludogorets")
    print('   Command: Трансфер "Dimitar Kitov" от "Slaviya Sofia" в "Ludogorets" 2025-03-25 сума 150000\n')
    result = handle_input('Трансфер "Dimitar Kitov" от "Slaviya Sofia" в "Ludogorets" 2025-03-25 сума 150000')
    print(result)
    
    input("\n   Press Enter to continue...\n")
    
    # Demo 12: View updated transfers
    print_section("👉 Demo 12: View updated transfers for Dimitar Kitov")
    print('   Command: Покажи трансфери на "Dimitar Kitov"\n')
    result = handle_input('Покажи трансфери на "Dimitar Kitov"')
    print(result)
    
    print_section("✅ DEMO COMPLETED")
    print("All major features have been demonstrated!")
    print("The system is ready for use.\n")

if __name__ == "__main__":
    try:
        demo_session()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

