from db import get_connection


def create_club():
    name = input("Club name: ")
    city = input("City: ")
    founded_year = input("Founded year: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Clubs (name, city, founded_year) VALUES (?, ?, ?)",
        (name, city, founded_year)
    )

    conn.commit()
    conn.close()
    print("Club created successfully!")


def read_clubs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clubs")
    clubs = cursor.fetchall()

    conn.close()

    print("\n--- CLUBS ---")
    for club in clubs:
        print(club)

def update_club():
    club_id = input("Club ID to update: ")
    new_name = input("New name: ")
    new_city = input("New city: ")
    new_year = input("New founded year: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Clubs SET name = ?, city = ?, founded_year = ? WHERE id = ?",
        (new_name, new_city, new_year, club_id)
    )

    conn.commit()
    conn.close()
    print("Club updated successfully!")



def delete_club():
    club_id = input("Club ID to delete: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM clubs WHERE id = ?",
        (club_id,)
    )

    conn.commit()
    conn.close()
    print("Club deleted successfully!")


def menu():
    while True:
        print("""
1. Create club
2. Read clubs
3. Update club
4. Delete club
5. Exit
        """)

        choice = input("Choose option: ")

        if choice == "1":
            create_club()
        elif choice == "2":
            read_clubs()
        elif choice == "3":
            update_club()
        elif choice == "4":
            delete_club()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()
