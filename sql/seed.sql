-- =========================
-- SEED DATA FOR FOOTBALL MANAGEMENT SYSTEM
-- =========================

-- =========================
-- CLUBS
-- =========================
INSERT INTO clubs (name, city) VALUES
('Levski Sofia', 'Sofia'),
('CSKA Sofia', 'Sofia'),
('Ludogorets', 'Razgrad'),
('Botev Plovdiv', 'Plovdiv'),
('Lokomotiv Plovdiv', 'Plovdiv');

-- =========================
-- PLAYERS (distributed across clubs)
-- =========================
-- Levski Sofia (id=1)
INSERT INTO players (full_name, birth_date, nationality, position, number, status, club_id) VALUES
('Ivan Petrov', '1999-05-12', 'Bulgaria', 'FW', 9, 'active', 1),
('Todor Markov', '1998-03-20', 'Bulgaria', 'MF', 10, 'active', 1);

-- CSKA Sofia (id=2)
INSERT INTO players (full_name, birth_date, nationality, position, number, status, club_id) VALUES
('Georgi Ivanov', '1995-08-20', 'Bulgaria', 'DF', 5, 'active', 2),
('Vasil Grozdev', '2000-11-15', 'Bulgaria', 'GK', 1, 'active', 2);

-- Ludogorets (id=3)
INSERT INTO players (full_name, birth_date, nationality, position, number, status, club_id) VALUES
('Petar Dimitrov', '2000-02-15', 'Bulgaria', 'DF', 3, 'active', 3);

-- Botev Plovdiv (id=4)
INSERT INTO players (full_name, birth_date, nationality, position, number, status, club_id) VALUES
('Nikolay Stoyanov', '1993-11-01', 'Bulgaria', 'MF', 8, 'active', 4);

-- =========================
-- TRANSFERS
-- =========================
INSERT INTO transfers (player_id, from_club_id, to_club_id, transfer_date, fee, note) VALUES
(1, 1, 3, '2025-01-15', 500000.00, 'Summer transfer'),
(2, 2, 1, '2025-02-01', 300000.00, 'Mid-season transfer'),
(3, 3, 2, '2025-01-20', 750000.00, 'Strategic acquisition'),
(4, 4, 1, '2025-02-10', 250000.00, 'Youth development'),
(5, 3, 4, '2025-03-05', 100000.00, 'Loan with purchase option');

-- =========================
-- LEAGUES (Sample data for testing)
-- =========================
INSERT INTO leagues (name, season) VALUES
('Primeira Liga', '2025/2026'),
('Premier League', '2025/2026');

-- =========================
-- LEAGUE_TEAMS (Add clubs to leagues)
-- =========================
-- Primeira Liga: Levski, CSKA, Ludogorets, Botev
INSERT INTO league_teams (league_id, club_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4);

-- Premier League: Levski, CSKA, Ludogorets, Lokomotiv
INSERT INTO league_teams (league_id, club_id) VALUES
(2, 1),
(2, 2),
(2, 3),
(2, 5);

