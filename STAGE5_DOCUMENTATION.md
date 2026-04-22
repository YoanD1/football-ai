# Stage 5: League Management - Testing & Usage Guide

## Overview
This document describes the League Management module (Stage 5) with comprehensive examples and test scenarios.

## Architecture

### Module Structure
```
src/
├── repositories/
│   ├── __init__.py
│   └── leagues_repo.py          # Data access layer (SQL operations)
├── services/
│   ├── __init__.py
│   └── leagues_service.py       # Business logic (validations, round-robin)
├── handlers/
│   ├── __init__.py
│   └── handlers_leagues.py      # Command parsing & routing
├── chatbot.py                   # Main intent router
├── intents.json                 # Command patterns
└── db.py                        # Database connection
```

### Data Flow
```
User Input
    ↓
chatbot.py (handle_input) - Routes to correct handler
    ↓
handlers/handlers_leagues.py - Parses command parameters
    ↓
services/leagues_service.py - Business logic & validation
    ↓
repositories/leagues_repo.py - SQL operations
    ↓
Database (leagues, league_teams, matches tables)
```

## Test Scenarios

### Test 1: Create League
**Command:** `Създай лига "Първа лига" "2025/2026"`
**Expected:** ✅ League created with ID
**Validations:**
- Season format YYYY/YYYY checked
- Duplicate (name, season) prevented
- Empty values rejected

### Test 2: Add Clubs to League
**Commands:**
```
Добави отбор "Levski Sofia" в лига "Първа лига" "2025/2026"
Добави отбор "CSKA Sofia" в лига "Първа лига" "2025/2026"
Добави отбор "Ludogorets" в лига "Първа лига" "2025/2026"
Добави отбор "Botev Plovdiv" в лига "Първа лига" "2025/2026"
```
**Expected:** ✅ 4 clubs added
**Validations:**
- Club existence checked
- Duplicate clubs prevented
- Cannot add if schedule exists

### Test 3: Show Clubs in League
**Command:** `Покажи отбори в лига "Първа лига" "2025/2026"`
**Expected:** ✅ Lists all 4 clubs with IDs and cities

### Test 4: Generate Schedule (Even Number)
**Command:** `Генерирай програма "Първа лига" "2025/2026"`
**Expected:** ✅ 3 rounds generated, 6 total matches
- Round 1: Botev vs Ludogorets, CSKA vs Levski
- Round 2: Botev vs Levski, Ludogorets vs CSKA
- Round 3: Botev vs CSKA, Levski vs Ludogorets

**Validation:**
- No team plays itself ✓
- No duplicate matches ✓
- Each team plays each other exactly once ✓
- Formula: 4×(4-1)/2 = 6 matches ✓
- Formula: 4-1 = 3 rounds ✓

### Test 5: Show Schedule
**Command:** `Покажи програма "Първа лига" "2025/2026"`
**Expected:** ✅ All matches grouped by round

**With Round Filter:**
**Command:** `Покажи програма "Първа лига" "2025/2026" кръг 1`
**Expected:** ✅ Only Round 1 matches shown

### Test 6: Test with Odd Number of Teams
**Commands:**
```
Създай лига "Втора лига" "2025/2026"
Добави отбор "Levski Sofia" в лига "Втора лига" "2025/2026"
Добави отбор "CSKA Sofia" в лига "Втора лига" "2025/2026"
Добави отбор "Ludogorets" в лига "Втора лига" "2025/2026"
Добави отбор "Botev Plovdiv" в лига "Втора лига" "2025/2026"
Добави отбор "Lokomotiv Plovdiv" в лига "Втора лига" "2025/2026"
Генерирай програма "Втора лига" "2025/2026"
```
**Expected:** ✅ 5 rounds, 10 matches total
- Each round has 2 matches (4 teams play, 1 has BYE)
- Formula: 5×(5-1)/2 = 10 matches ✓
- Formula: 5 rounds ✓

### Test 7: Regenerate Schedule
**Command:** `Прегенерирай програма "Първа лига" "2025/2026"`
**Expected:** ✅ Old schedule deleted, new one generated

### Test 8: League Information
**Command:** `Инфо лига "Първа лига" "2025/2026"`
**Expected:** ✅ Shows creation date, teams count, matches, rounds

### Test 9: Error Cases
**Scenario:** Add club that doesn't exist
**Command:** `Добави отбор "NonExistent Club" в лига "Първа лига" "2025/2026"`
**Expected:** ❌ Error: "Club 'NonExistent Club' not found"

**Scenario:** Invalid season format
**Command:** `Създай лига "Test" "2025"`
**Expected:** ❌ Error: "Invalid season format. Use format: YYYY/YYYY"

**Scenario:** Duplicate club
**Command:** `Добави отбор "Levski Sofia" в лига "Първа лига" "2025/2026"` (twice)
**Expected:** ❌ Error: "Club 'Levski Sofia' is already in league"

**Scenario:** Generate schedule with < 2 teams
**Command:** Create league, add 1 club, try to generate
**Expected:** ❌ Error: "League must have at least 2 clubs"

## Round-Robin Algorithm Details

### Circle Method Implementation
```python
# For N=4 teams (even):
Initial: [0, 1, 2, 3]
Round 1: (0,3), (1,2)
Rotate: [0, 3, 1, 2]
Round 2: (0,2), (3,1)
Rotate: [0, 2, 3, 1]
Round 3: (0,1), (2,3)
```

### BYE Handling (Odd N)
- Add a virtual BYE team to make N+1 (even)
- BYE matches are skipped in output
- Results in N-1 actual matches per round
- Example: 5 teams → 5 rounds, 2 matches per round

## Command Logging

**Log Format:** `[YYYY-MM-DD HH:MM:SS] INPUT: <command> | INTENT: <intent> | RESULT: <first 50 chars>`

**Example:**
```
[2026-04-22 16:44:45] INPUT: Генерирай програма "Първа лига" "2025/2026" | INTENT: generate_schedule | RESULT: ✅ Schedule generated successfully! Teams: 4 Rounds: 3 ...
[2026-04-22 16:44:46] INPUT: Покажи програма "Първа лига" "2025/2026" | INTENT: show_schedule | RESULT: 📅 **SCHEDULE: Първа лига (2025/2026)** ━━━━━━━...
```

## Running Tests

### Method 1: Unit Tests
```bash
cd football-ai
python test_leagues.py
```
Tests core service functions with 8 scenarios

### Method 2: Chatbot Integration Tests
```bash
cd football-ai
python test_chatbot_leagues.py
```
Tests all commands through chatbot interface, shows commands.log entries

### Method 3: Interactive Mode
```bash
cd src
python main.py
```
Then manually type commands:
```
помощ
Създай лига "Test League" "2025/2026"
Добави отбор "Levski Sofia" в лига "Test League" "2025/2026"
Генерирай програма "Test League" "2025/2026"
Покажи програма "Test League" "2025/2026"
```

## Key Files Modified

| File | Changes |
|------|---------|
| `sql/schema.sql` | Added: leagues, league_teams, matches tables |
| `sql/seed.sql` | Added: Sample leagues and league_teams |
| `src/intents.json` | Added: 9 league-related intents |
| `src/chatbot.py` | Added: League command routing, updated help menu |
| `src/repositories/leagues_repo.py` | NEW: Data access layer |
| `src/services/leagues_service.py` | NEW: Business logic + round-robin algorithm |
| `src/handlers/handlers_leagues.py` | NEW: Command handlers |

## Acceptance Criteria Status

✅ **Database**
- leagues table with name+season uniqueness
- league_teams with composite key
- matches table with proper constraints

✅ **Python Structure**
- repositories/leagues_repo.py for SQL
- services/leagues_service.py for logic
- handlers/handlers_leagues.py for commands
- No direct SQL in handlers (data layer pattern)

✅ **Chatbot Commands**
- Create league with validation
- Add/remove clubs with checks
- Show clubs in league
- Generate schedule (round-robin)
- Show schedule (all or by round)
- Regenerate schedule

✅ **Round-Robin Algorithm**
- Even teams: N-1 rounds, N/2 matches per round
- Odd teams: N rounds with BYE
- No self-matches, no duplicates
- Circle/rotation method verified

✅ **Logging & Validation**
- commands.log tracks all inputs
- Clear error messages for invalid inputs
- Season format validation
- Club existence checks

✅ **Testing**
- 8+ test scenarios covered
- Works with even/odd team counts
- All error cases tested
- Commands.log verified

## Future Enhancements

- [ ] Match result recording (goals)
- [ ] League standings calculation
- [ ] Double round-robin (home/away reversed)
- [ ] Custom match dates
- [ ] League export to CSV
- [ ] Web interface for schedule viewing
- [ ] Automatic standing updates after matches

