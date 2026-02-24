-- =========================
-- SEED DATA FOR ALL TABLES
-- =========================

-- Clubs
INSERT INTO Clubs (name, city, founded_year) VALUES
('Levski Sofia', 'Sofia', 1914),
('CSKA Sofia', 'Sofia', 1948),
('Ludogorets', 'Razgrad', 2001),
('Botev Plovdiv', 'Plovdiv', 1912),
('Lokomotiv Plovdiv', 'Plovdiv', 1926);

-- Players
INSERT INTO Players (name, birth_date, nationality, position, number, club_id, status) VALUES
('Ivan Petrov', '1999-05-12', 'BG', 'FW', 9, 1, 'active'),
('Georgi Ivanov', '1995-08-20', 'BG', 'MF', 10, 2, 'active'),
('Petar Dimitrov', '2000-02-15', 'BG', 'DF', 5, 3, 'active'),
('Nikolay Stoyanov', '1993-11-01', 'BG', 'GK', 1, 4, 'active'),
('Dimitar Kolev', '1997-07-30', 'BG', 'FW', 11, 5, 'active');

-- Leagues
INSERT INTO Leagues (name, season) VALUES
('First League', '2025/2026');

-- League Teams
INSERT INTO League_Teams (league_id, club_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5);

-- Matches
INSERT INTO Matches (league_id, home_club_id, away_club_id, match_date, home_score, away_score) VALUES
(1, 1, 2, '2025-03-01', 2, 1),
(1, 3, 4, '2025-03-05', 3, 0),
(1, 5, 1, '2025-03-10', 1, 1);

-- Transfers
INSERT INTO Transfers (player_id, from_club_id, to_club_id, transfer_date, amount) VALUES
(1, 1, 3, '2025-01-15', 500000),
(2, 2, 1, '2025-02-01', 300000);

-- Goals
INSERT INTO Goals (match_id, player_id, minute) VALUES
(1, 1, 23),
(1, 2, 45),
(2, 3, 10);

-- Cards
INSERT INTO Cards (match_id, player_id, type, minute) VALUES
(1, 2, 'yellow', 33),
(2, 3, 'red', 77);