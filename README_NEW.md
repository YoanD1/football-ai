# ⚽ Football Management System

## 📋 Overview

A comprehensive **Python-based Football Management Chatbot** with SQLite database backend. This system allows users to manage football clubs, players, and transfers through an intuitive Bulgarian-language command interface.

### Key Features

✅ **Club Management** - Add, view, update, and delete clubs  
✅ **Player Management** - Add players with validations (position, number, status)  
✅ **Transfer System** - Track player transfers with dates and fees  
✅ **Bulgarian Interface** - Natural language commands in Bulgarian  
✅ **Data Validation** - Comprehensive input validation and business rules  
✅ **Command Logging** - All commands logged with timestamps  
✅ **SQLite Database** - Persistent data storage with foreign keys

---

## 🏗️ Project Structure

```
football-ai/
├── src/
│   ├── main.py                 # Chatbot entry point
│   ├── db.py                   # Database connection & utilities
│   ├── chatbot.py              # Intent handler & command router
│   ├── clubs_service.py        # Club CRUD operations
│   ├── players_service.py      # Player CRUD operations
│   ├── transfers_service.py    # Transfer management
│   ├── intents.json            # Command definitions
│   └── football.db             # SQLite database
├── sql/
│   ├── schema.sql              # Database schema
│   ├── seed.sql                # Test data
│   └── football.db             # Alternative DB location
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── commands.log                # Command execution log
```

---

## 🗄️ Database Schema

### Tables

#### `clubs`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| name | TEXT | NOT NULL, UNIQUE |
| city | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### `players`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| full_name | TEXT | NOT NULL |
| birth_date | TEXT | NOT NULL (YYYY-MM-DD) |
| nationality | TEXT | NOT NULL |
| position | TEXT | NOT NULL, CHECK IN ('GK', 'DF', 'MF', 'FW') |
| number | INTEGER | NOT NULL, CHECK 1-99 |
| status | TEXT | DEFAULT 'active', CHECK IN ('active', 'injured', 'inactive') |
| club_id | INTEGER | NOT NULL, FOREIGN KEY → clubs.id |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### `transfers`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| player_id | INTEGER | NOT NULL, FOREIGN KEY → players.id |
| from_club_id | INTEGER | NULLABLE, FOREIGN KEY → clubs.id |
| to_club_id | INTEGER | NOT NULL, FOREIGN KEY → clubs.id |
| transfer_date | TEXT | NOT NULL (YYYY-MM-DD) |
| fee | REAL | NULLABLE |
| note | TEXT | NULLABLE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**Constraints:**
- `from_club_id != to_club_id` (cannot transfer to same club)
- Cascade delete on player deletion
- Restrict delete on club if transfers exist

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- SQLite3 (included in Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/football-ai.git
   cd football-ai
   ```

2. **No additional dependencies required!** (uses only Python stdlib)

3. **Run the application**
   ```bash
   cd src
   python main.py
   ```

The system will automatically:
- Initialize the SQLite database
- Create all tables with proper relationships
- Load seed data (5 clubs, 6 players, 5 transfers)

---

## ⚽ League Management System (Stage 5)

### Overview
The system now includes comprehensive league management with round-robin scheduling:
- Create and manage leagues by season
- Add/remove clubs to leagues
- Automatic round-robin schedule generation
- Match tracking and display
- Full validation and error handling

### Database Tables

#### `leagues`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| name | TEXT | NOT NULL |
| season | TEXT | NOT NULL (format: YYYY/YYYY) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| Unique | (name, season) | Composite unique constraint |

#### `league_teams`
| Column | Type | Constraints |
|--------|------|-------------|
| league_id | INTEGER | FK → leagues.id |
| club_id | INTEGER | FK → clubs.id |
| joined_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| Primary Key | (league_id, club_id) | Composite PK |

#### `matches`
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| league_id | INTEGER | FK → leagues.id |
| round_no | INTEGER | NOT NULL |
| home_club_id | INTEGER | FK → clubs.id |
| away_club_id | INTEGER | FK → clubs.id |
| match_date | TEXT | NULLABLE |
| home_goals | INTEGER | NULLABLE |
| away_goals | INTEGER | NULLABLE |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

**Constraints:**
- `home_club_id != away_club_id` (no team plays itself)
- No duplicate matches in same league/round
- Cascade delete on league deletion

### Round-Robin Algorithm

**For even number of teams (N):**
- Rounds: N - 1
- Matches per round: N / 2
- Total matches: N × (N-1) / 2
- Each team plays every other team exactly once

**For odd number of teams (N):**
- Rounds: N
- Matches per round: (N-1) / 2
- Total matches: N × (N-1) / 2
- One team has BYE (rest) per round
- Guaranteed: No team plays itself, no duplicates

---

## 📖 Commands Reference

### 🆘 General Commands

#### Help
```
помощ
help
```
Displays all available commands and usage examples.

#### Exit
```
изход
exit
quit
q
```
Gracefully exits the application.

---

### 🏢 Club Management

#### Add Club
```
Добави клуб "<ИМЕ>" "<ГРАД>"
```
**Example:**
```
Добави клуб "Левски" "София"
```

#### List All Clubs
```
Покажи всички клубове
покажи клубове
list clubs
```

#### Update Club
```
Обнови клуб "<ИМЕ>" в "<НОВ_ГРАД>"
```
**Example:**
```
Обнови клуб "Левски" в "Пловдив"
```

#### Delete Club
```
Изтрий клуб "<ИМЕ>"
```
**Example:**
```
Изтрий клуб "Левски"
```

---

### 👥 Player Management

#### Add Player
```
Добави играч "<ИМЕ>" в "<КЛУБ>" позиция <ПОЗА> номер <№> дата <ДАТА> [национална <НАЦИОНАЛ>]
```
**Valid positions:** GK, DF, MF, FW  
**Valid numbers:** 1-99  
**Date format:** YYYY-MM-DD  
**Default nationality:** Bulgaria

**Example:**
```
Добави играч "Иван Петров" в "Левски" позиция FW номер 9 дата 1999-05-12 национална България
```

#### List Players by Club
```
Покажи играчи на "<КЛУБ>"
```
**Example:**
```
Покажи играчи на "Левски"
```

#### Search Players
```
Търси играч "<КЛЮЧОВА_ДУМ>"
```
**Example:**
```
Търси играч "Петров"
```

#### Change Player Number
```
Смени номер на "<ИГРАЧ>" на <НОМЕР>
```
**Example:**
```
Смени номер на "Иван Петров" на 10
```

#### Change Player Status
```
Смени статус на "<ИГРАЧ>" на <СТАТУС>
```
**Valid statuses:** active, injured, inactive

**Example:**
```
Смени статус на "Иван Петров" на injured
```

#### Delete Player
```
Изтрий играч "<ИМЕ>"
```
**Example:**
```
Изтрий играч "Иван Петров"
```

---

### 🔄 Transfer Management

#### Transfer Player
```
Трансфер "<ИГРАЧ>" от "<ОТ_КЛУБ>" в "<ДО_КЛУБ>" <ДАТА> [сума <СУМА>]
```
**Date format:** YYYY-MM-DD  
**Fee:** Optional (numeric value)

**Business Rules:**
- Source club and destination club must be different
- Both clubs must exist
- Player must exist and belong to source club
- Creates transfer record and updates player's club

**Example:**
```
Трансфер "Иван Петров" от "Левски" в "ЦСКА" 2025-03-15 сума 500000
```

#### Show Player's Transfer History
```
Покажи трансфери на "<ИГРАЧ>"
```
**Example:**
```
Покажи трансфери на "Иван Петров"
```

#### Show Club's Transfers
```
Трансфери на клуб "<КЛУБ>"
```
**Example:**
```
Трансфери на клуб "Левски"
```

#### Show All Transfers
```
Покажи всички трансфери
```

---

### ⚽ League Management

#### Create League
```
Създай лига "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Създай лига "Първа лига" "2025/2026"
```

#### Add Club to League
```
Добави отбор "<КЛУБ>" в лига "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Добави отбор "Левски" в лига "Първа лига" "2025/2026"
```

#### Remove Club from League
```
Премахни отбор "<КЛУБ>" от лига "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Премахни отбор "Левски" от лига "Първа лига" "2025/2026"
```
**Note:** Only works if no schedule has been generated

#### Show Clubs in League
```
Покажи отбори в лига "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Покажи отбори в лига "Първа лига" "2025/2026"
```

#### Show All Leagues
```
Покажи всички лиги
```

#### Generate Round-Robin Schedule
```
Генерирай програма "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Генерирай програма "Първа лига" "2025/2026"
```

**Requirements:**
- Minimum 2 clubs in league
- No schedule already exists
- Season format must be YYYY/YYYY

**Output:**
- Creates all matches with round_no
- Returns: Total rounds, matches, and sample first round

#### Regenerate Schedule
```
Прегенерирай програма "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Прегенерирай програма "Първа лига" "2025/2026"
```
**Note:** Deletes existing schedule and generates new one

#### Show Schedule
```
Покажи програма "<ИМЕ>" "<СЕЗОН>" [кръг <НОМЕР>]
```
**Examples:**
```
Покажи програма "Първа лига" "2025/2026"
Покажи програма "Първа лига" "2025/2026" кръг 1
```

#### League Information
```
Инфо лига "<ИМЕ>" "<СЕЗОН>"
```
**Example:**
```
Инфо лига "Първа лига" "2025/2026"
```

---

## 📊 Sample Data

The system comes with pre-loaded seed data:

### Clubs
- Levski Sofia (Sofia)
- CSKA Sofia (Sofia)
- Ludogorets (Razgrad)
- Botev Plovdiv (Plovdiv)
- Lokomotiv Plovdiv (Plovdiv)

### Players
- Ivan Petrov (Levski) - FW #9
- Todor Markov (Levski) - MF #10
- Georgi Ivanov (CSKA) - DF #5
- Vasil Grozdev (CSKA) - GK #1
- Petar Dimitrov (Ludogorets) - DF #3
- Nikolay Stoyanov (Botev) - MF #8

### Transfers
- Ivan Petrov: Levski → Ludogorets (2025-01-15, €500,000)
- Todor Markov: CSKA → Levski (2025-02-01, €300,000)
- Georgi Ivanov: Ludogorets → CSKA (2025-01-20, €750,000)
- Nikolay Stoyanov: Botev → Levski (2025-02-10, €250,000)
- Petar Dimitrov: Ludogorets → Botev (2025-03-05, €100,000)

---

## 💾 Data Validation

### League Validation
- ✓ League name must be non-empty
- ✓ Season must be in YYYY/YYYY format
- ✓ Name + Season must be unique
- ✓ Minimum 2 clubs before schedule generation

### League Team Validation
- ✓ Club must exist in database
- ✓ Club cannot be added twice to same league
- ✓ Cannot remove club if schedule exists
- ✓ Cannot add club if schedule exists

### Schedule Validation
- ✓ No team plays itself (home != away)
- ✓ No duplicate matches in same round/league
- ✓ Even N teams: N-1 rounds, N/2 matches per round
- ✓ Odd N teams: N rounds, (N-1)/2 matches per round + BYE
- ✓ Total matches: N×(N-1)/2

---

## 💾 Data Validation (Original)

### Club Validation
- ✓ Name must be non-empty and unique
- ✓ City must be non-empty

### Player Validation
- ✓ Full name must be non-empty
- ✓ Position must be one of: GK, DF, MF, FW
- ✓ Number must be between 1 and 99
- ✓ Birth date must be in YYYY-MM-DD format
- ✓ Status must be one of: active, injured, inactive
- ✓ Club must exist before adding player
- ✓ Cannot add duplicate player to same club

### Transfer Validation
- ✓ Player must exist
- ✓ Source club and destination club must both exist
- ✓ Source club cannot equal destination club
- ✓ Transfer date must be in YYYY-MM-DD format
- ✓ Fee can be optional but must be numeric if provided

---

## 📝 Logging

All commands are logged to `commands.log` with:
- **Timestamp:** YYYY-MM-DD HH:MM:SS
- **Input:** User's exact input
- **Intent:** Detected command type
- **Result:** First 50 characters of result

**Example log entry:**
```
[2025-03-25 14:30:45] INPUT: Добави клуб "Левски" "София" | INTENT: add_club | RESULT: ✅ Club 'Левски' added successfully (ID: 1...
```

---

## 🔧 Development

### Adding New Commands

1. **Update `intents.json`** - Add command variations
2. **Create handler function** in `chatbot.py`
3. **Update `handle_input()`** - Add routing logic

### Project Architecture

- **Single Responsibility** - Each module has one purpose
- **Type Hints** - Functions have clear input/output types
- **Error Handling** - Comprehensive validation and error messages
- **Logging** - All operations logged for audit trail
- **Database Transactions** - Proper commit/rollback handling

---

## 🐛 Troubleshooting

### Database Not Found
```
Error: No such file or directory
```
**Solution:** Run from the `src/` directory where `football.db` is located.

### Foreign Key Constraint Failed
```
Error: FOREIGN KEY constraint failed
```
**Solution:** Ensure club/player exists before referencing in transfers.

### Cannot Delete Club
```
❌ Cannot delete club - it still has players
```
**Solution:** Delete all players from the club first.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

Created as a comprehensive Python & SQL demonstration project.

---

## 📞 Support

For issues or questions, please create an issue in the repository.

---

## 🎯 Future Enhancements

- [ ] Web interface (Flask/Django)
- [ ] Advanced transfer statistics
- [ ] Match management
- [ ] League standings
- [ ] CSV export functionality
- [ ] REST API
- [ ] User authentication
- [ ] Advanced search filters
- [ ] Data backup/restore
- [ ] Configuration file support

---

**Last Updated:** March 25, 2025  
**Version:** 1.0.0

