-- =========================
-- SCHEMA.SQL
-- =========================

CREATE TABLE Clubs (
    club_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    founded_year INTEGER NOT NULL
);

CREATE TABLE Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date TEXT,
    nationality TEXT,
    position TEXT NOT NULL,
    number INTEGER,
    club_id INTEGER NOT NULL,
    status TEXT,
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);

CREATE TABLE Leagues (
    league_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    season TEXT NOT NULL
);

CREATE TABLE League_Teams (
    league_team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    club_id INTEGER NOT NULL,
    FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
    FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
);

CREATE TABLE Matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    home_club_id INTEGER NOT NULL,
    away_club_id INTEGER NOT NULL,
    match_date TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    FOREIGN KEY (league_id) REFERENCES Leagues(league_id),
    FOREIGN KEY (home_club_id) REFERENCES Clubs(club_id),
    FOREIGN KEY (away_club_id) REFERENCES Clubs(club_id)
);

CREATE TABLE Transfers (
    transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    from_club_id INTEGER,
    to_club_id INTEGER,
    transfer_date TEXT,
    amount REAL,
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (from_club_id) REFERENCES Clubs(club_id),
    FOREIGN KEY (to_club_id) REFERENCES Clubs(club_id)
);

CREATE TABLE Goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);

CREATE TABLE Cards (
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- yellow/red
    minute INTEGER NOT NULL,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);