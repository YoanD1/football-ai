-- =========================
-- FOOTBALL MANAGEMENT SYSTEM
-- DATABASE SCHEMA
-- =========================

-- Drop existing tables (for clean initialization)
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS league_teams;
DROP TABLE IF EXISTS leagues;
DROP TABLE IF EXISTS transfers;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS clubs;

-- =========================
-- CLUBS TABLE
-- =========================
CREATE TABLE clubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- PLAYERS TABLE
-- =========================
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    nationality TEXT NOT NULL,
    position TEXT NOT NULL CHECK(position IN ('GK', 'DF', 'MF', 'FW')),
    number INTEGER NOT NULL CHECK(number >= 1 AND number <= 99),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'injured', 'inactive')),
    club_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE RESTRICT
);

-- =========================
-- TRANSFERS TABLE
-- =========================
CREATE TABLE transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    from_club_id INTEGER,
    to_club_id INTEGER NOT NULL,
    transfer_date TEXT NOT NULL,
    fee REAL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (from_club_id) REFERENCES clubs(id) ON DELETE SET NULL,
    FOREIGN KEY (to_club_id) REFERENCES clubs(id) ON DELETE RESTRICT,
    CHECK(from_club_id IS NULL OR from_club_id != to_club_id)
);

-- =========================
-- INDEXES FOR PERFORMANCE
-- =========================
CREATE INDEX idx_players_club_id ON players(club_id);
CREATE INDEX idx_players_full_name ON players(full_name);
CREATE INDEX idx_transfers_player_id ON transfers(player_id);
CREATE INDEX idx_transfers_transfer_date ON transfers(transfer_date);

-- =========================
-- LEAGUES TABLE
-- =========================
CREATE TABLE leagues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    season TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, season)
);

-- =========================
-- LEAGUE_TEAMS TABLE
-- =========================
CREATE TABLE league_teams (
    league_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (league_id, club_id),
    FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
);

-- =========================
-- MATCHES TABLE
-- =========================
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    round_no INTEGER NOT NULL,
    home_club_id INTEGER NOT NULL,
    away_club_id INTEGER NOT NULL,
    match_date TEXT,
    home_goals INTEGER DEFAULT 0,
    away_goals INTEGER DEFAULT 0,
    status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'played')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE,
    FOREIGN KEY (home_club_id) REFERENCES clubs(id) ON DELETE RESTRICT,
    FOREIGN KEY (away_club_id) REFERENCES clubs(id) ON DELETE RESTRICT,
    CHECK(home_club_id != away_club_id)
);

-- =========================
-- GOALS TABLE
-- =========================
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    minute INTEGER NOT NULL CHECK(minute >= 1 AND minute <= 120),
    is_own_goal INTEGER DEFAULT 0 CHECK(is_own_goal IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE RESTRICT,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE RESTRICT
);

-- =========================
-- CARDS TABLE
-- =========================
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    minute INTEGER NOT NULL CHECK(minute >= 1 AND minute <= 120),
    card_type TEXT NOT NULL CHECK(card_type IN ('Y', 'R')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE RESTRICT,
    FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE RESTRICT
);

-- =========================
-- INDEXES FOR LEAGUES
-- =========================
CREATE INDEX idx_league_teams_league_id ON league_teams(league_id);
CREATE INDEX idx_league_teams_club_id ON league_teams(club_id);
CREATE INDEX idx_matches_league_id ON matches(league_id);
CREATE INDEX idx_matches_round_no ON matches(round_no);
CREATE INDEX idx_matches_home_club ON matches(home_club_id);
CREATE INDEX idx_matches_away_club ON matches(away_club_id);
CREATE INDEX idx_matches_status ON matches(status);

-- =========================
-- INDEXES FOR MATCHES EVENTS
-- =========================
CREATE INDEX idx_goals_match_id ON goals(match_id);
CREATE INDEX idx_goals_player_id ON goals(player_id);
CREATE INDEX idx_goals_minute ON goals(minute);
CREATE INDEX idx_cards_match_id ON cards(match_id);
CREATE INDEX idx_cards_player_id ON cards(player_id);
CREATE INDEX idx_cards_minute ON cards(minute);

