-- =========================
-- FOOTBALL MANAGEMENT SYSTEM
-- DATABASE SCHEMA
-- =========================

-- Drop existing tables (for clean initialization)
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
