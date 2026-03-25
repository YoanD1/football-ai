import sys
import io

# Fix Unicode output in Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from chatbot import handle_input
from db import initialize_database


def main():
    """Main chatbot entry point."""
    # Initialize database with schema and seed data
    print("\n" + "="*80)
    print("⚽ FOOTBALL MANAGEMENT SYSTEM ⚽")
    print("="*80 + "\n")
    
    print("📊 Initializing database...")
    if not initialize_database():
        print("❌ Failed to initialize database. Exiting.")
        return
    
    print("\n✅ System ready!")
    print("Type 'помощ' (help) for available commands.\n")
    print("-" * 80 + "\n")

    while True:
        try:
            user_input = input("⚽ >> ").strip()
            
            # Skip empty input
            if not user_input:
                continue

            # Handle input and get result
            result = handle_input(user_input)

            # Check if user wants to exit
            if result == "exit":
                print("\n" + "="*80)
                print("👋 Thank you for using Football Management System!")
                print("="*80 + "\n")
                break

            # Display result
            print("\n" + result + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
