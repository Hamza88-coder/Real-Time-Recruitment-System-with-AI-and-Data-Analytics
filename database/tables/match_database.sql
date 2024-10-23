-- Connexion à la base de données "football" (faire lors de la connexion au serveur)

-- Table des pays
CREATE TABLE countries (
    country_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table des compétitions
CREATE TABLE Competitions (
    competition_id INT PRIMARY KEY,
    competition_name VARCHAR(255),
    country_name VARCHAR(255)
    
);

-- Table des saisons
CREATE TABLE Seasons (
    season_id INT PRIMARY KEY,
    season_name VARCHAR(50)
);

-- Table des équipes
CREATE TABLE Teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(255),
    team_gender VARCHAR(10),
    country_id INT NOT NULL, -- Ajout de la colonne country_id
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Table des managers
CREATE TABLE managers (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255),
    dob DATE NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Table des stades
CREATE TABLE stadiums (
    stadium_id INT PRIMARY KEY,
    stadium_name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Table des arbitres
CREATE TABLE referee (
    referee_id INT PRIMARY KEY,
    referee_name VARCHAR(255) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- Table des phases de compétition
CREATE TABLE competition_stage (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table des matchs
CREATE TABLE Matches (
    match_id INT PRIMARY KEY,
    match_date DATE,
    kick_off TIME,
    competition_id INT,
    manager_id INT,  -- Correction du nom ici
    season_id INT,
    home_team_id INT,
    away_team_id INT,
    home_score INT,
    away_score INT,
    match_status VARCHAR(50),
    match_status_360 VARCHAR(50),
    last_updated TIMESTAMP,
    match_week INT,
    competition_stage_id INT,
    stadium_id INT,
    referee_id INT,
    FOREIGN KEY (competition_id) REFERENCES Competitions(competition_id),
    FOREIGN KEY (manager_id) REFERENCES managers(id),  -- Correction ici
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (stadium_id) REFERENCES stadiums(stadium_id),
    FOREIGN KEY (referee_id) REFERENCES referee(referee_id)
);
