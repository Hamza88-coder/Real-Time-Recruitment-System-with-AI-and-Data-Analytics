-- Créer la base de données
--CREATE DATABASE cond_db;

-- Table des titres
CREATE TABLE title (
    id SERIAL PRIMARY KEY,
    title_name VARCHAR(100) NOT NULL UNIQUE  
);

-- Table des types de contrats avec contrainte CHECK
CREATE TABLE type_trav (
    id SERIAL PRIMARY KEY,
    trav_type VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT chk_trav_type CHECK (trav_type IN ('Travail', 'PFA', 'PFE')) -- Valeurs autorisées
);

-- Table des modes de travail avec contrainte CHECK
CREATE TABLE mode_travail (
    id SERIAL PRIMARY KEY,
    mode_name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT chk_mode_name CHECK (mode_name IN ('Hybrid', 'À distance', 'Présentiel')) -- Valeurs autorisées
);

-- Table principale : candidats
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    title_id INT REFERENCES title(id) ON DELETE SET NULL,  
    date_of_birth DATE,
    place_of_birth VARCHAR(200),
    gender VARCHAR(50),
    nationality VARCHAR(100),
    phone_number VARCHAR(15),
    type_trav_id INT REFERENCES type_trav(id) ON DELETE SET NULL,  
    mode_travail_id INT REFERENCES mode_travail(id) ON DELETE SET NULL  
);

-- Table des adresses
CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    formatted_location TEXT,
    city VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20)
);

-- Table des URLs (GitHub, LinkedIn, etc.)
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    type VARCHAR(50),
    url TEXT NOT NULL
);

-- Table des informations éducatives
CREATE TABLE education_details (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    etude_title VARCHAR(200),
    etablissement_name VARCHAR(200),
    start_date DATE,
    end_date DATE,
    etude_city VARCHAR(100),
    etude_region VARCHAR(100),
    etude_country VARCHAR(100)
);

-- Table des expériences professionnelles
CREATE TABLE work_experience_details (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_title VARCHAR(200),
    company_name VARCHAR(200),
    city VARCHAR(100),
    region VARCHAR(100),
    sector_of_activity VARCHAR(200),
    start_date DATE,
    end_date DATE
);

-- Table des compétences avec une relation N,N
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE   
);

CREATE TABLE candidate_skills (
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    skill_id INT NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (candidate_id, skill_id)  
);

-- Table des langues avec une relation N,N
CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    language_name VARCHAR(100) NOT NULL,
    proficiency_level VARCHAR(100) -- Niveau de compétence
);

CREATE TABLE candidate_languages (
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    language_id INT NOT NULL REFERENCES languages(id) ON DELETE CASCADE,
    PRIMARY KEY (candidate_id, language_id)  
);

-- Table des certifications avec une relation N,N
CREATE TABLE certifications (
    id SERIAL PRIMARY KEY,
    certification_name VARCHAR(200),
    issuing_organization VARCHAR(200),
    date_obtained DATE
);

CREATE TABLE candidate_certifications (
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    certification_id INT NOT NULL REFERENCES certifications(id) ON DELETE CASCADE,
    PRIMARY KEY (candidate_id, certification_id)  
);
