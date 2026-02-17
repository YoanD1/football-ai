import db

# Създаване на таблиците (само първия път)
db.initialize_database()

# CREATE
db.add_club("Levski Sofia", "Sofia", 1914)

# READ
db.get_all_clubs()

# UPDATE
db.update_club(1, "Levski Sofia Updated", "Sofia", 1914)

# DELETE
# db.delete_club(1)
