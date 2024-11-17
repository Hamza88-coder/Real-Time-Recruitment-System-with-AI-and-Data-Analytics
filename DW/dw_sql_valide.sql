USE ROLE ACCOUNTADMIN;
CREATE WAREHOUSE projet_warehouse
WITH
WAREHOUSE_SIZE = 'XSMALL'  -- ou autre taille selon tes besoins
AUTO_SUSPEND = 60           -- temps d'inactivité avant la suspension (en secondes)
AUTO_RESUME = TRUE;         -- redémarre automatiquement si nécessaire

USE WAREHOUSE projet_warehouse;
CREATE DATABASE IF NOT EXISTS my_project_database;
CREATE SCHEMA IF NOT EXISTS my_project_database.my_project_schema;
USE DATABASE my_project_database;
USE SCHEMA my_project_database.my_project_schema;

USE ROLE ACCOUNTADMIN;
CREATE WAREHOUSE projet_warehouse
WITH
WAREHOUSE_SIZE = 'XSMALL'  -- ou autre taille selon tes besoins
AUTO_SUSPEND = 60           -- temps d'inactivité avant la suspension (en secondes)
AUTO_RESUME = TRUE;         -- redémarre automatiquement si nécessaire

USE WAREHOUSE projet_warehouse;
CREATE DATABASE IF NOT EXISTS my_project_database;
CREATE SCHEMA IF NOT EXISTS my_project_database.my_project_schema;
USE DATABASE my_project_database;
USE SCHEMA my_project_database.my_project_schema;

-- Création des tables principales

CREATE TABLE my_project_database.my_project_schema.langue (
    langue_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.formation (
    formation_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.competence (
    competence_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.certification (
    certificat_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.ecole (
    ecole_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.secteur (
    secteur_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.etat (
    etat_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.type_trav (
    typeTrav_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.type_stage (
    typeStag_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.ville (
    ville_id INT PRIMARY KEY,
    etat_id INT,
    nom VARCHAR(100),
    FOREIGN KEY (etat_id) REFERENCES etat(etat_id)
);

CREATE TABLE my_project_database.my_project_schema.entreprise (
    entreprise_id INT PRIMARY KEY,
    nom VARCHAR(100),
    email VARCHAR(100),
    URL VARCHAR(100),
    telephone VARCHAR(20),
    secteur_id INT,
    ville_id INT,
    FOREIGN KEY (secteur_id) REFERENCES secteur(secteur_id),
    FOREIGN KEY (ville_id) REFERENCES ville(ville_id)
);

CREATE TABLE my_project_database.my_project_schema.candidat_fait (
    candidat_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    ville_id INT,
    date_birth DATE,
    gender CHAR(1),
    formation_id INT,
    email VARCHAR(100),
    telephone VARCHAR(20),
    nbr_years_exp INT,
    ecole_id INT,
    FOREIGN KEY (ville_id) REFERENCES ville(ville_id),
    FOREIGN KEY (formation_id) REFERENCES formation(formation_id),
    FOREIGN KEY (ecole_id) REFERENCES ecole(ecole_id)
);

CREATE TABLE my_project_database.my_project_schema.contrat (
    contrat_id INT PRIMARY KEY,
    contrat_nom VARCHAR(100)
);

CREATE TABLE my_project_database.my_project_schema.offre_fait (
    offre_id INT PRIMARY KEY,
    contrat_id INT,
    entreprise_id INT,
    formation_id INT,
    experience_dur VARCHAR(100),
    salaire DECIMAL(10, 2),
    typeTrav_id INT,
    FOREIGN KEY (contrat_id) REFERENCES contrat(contrat_id),
    FOREIGN KEY (entreprise_id) REFERENCES entreprise(entreprise_id),
    FOREIGN KEY (formation_id) REFERENCES formation(formation_id),
    FOREIGN KEY (typeTrav_id) REFERENCES type_trav(typeTrav_id)
);

CREATE TABLE my_project_database.my_project_schema.stage_fait (
    stage_id INT PRIMARY KEY,
    entreprise_id INT,
    formation_id INT,
    typeStag_id INT,
    typeTrav_id INT,
    duree_stage VARCHAR(100),
    remunere BOOLEAN,
    FOREIGN KEY (entreprise_id) REFERENCES entreprise(entreprise_id),
    FOREIGN KEY (formation_id) REFERENCES formation(formation_id),
    FOREIGN KEY (typeStag_id) REFERENCES type_stage(typeStag_id),
    FOREIGN KEY (typeTrav_id) REFERENCES type_trav(typeTrav_id)
);

-- Tables pour les compétences et langues

CREATE TABLE my_project_database.my_project_schema.langue_offr (
    offre_id INT,
    langue_id INT,
    PRIMARY KEY (offre_id, langue_id),
    FOREIGN KEY (offre_id) REFERENCES offre_fait(offre_id),
    FOREIGN KEY (langue_id) REFERENCES langue(langue_id)
);

CREATE TABLE my_project_database.my_project_schema.langue_stag (
    offre_id INT,
    langue_id INT,
    PRIMARY KEY (offre_id, langue_id),
    FOREIGN KEY (offre_id) REFERENCES offre_fait(offre_id),
    FOREIGN KEY (langue_id) REFERENCES langue(langue_id)
);

CREATE TABLE my_project_database.my_project_schema.langue_cand (
    candidat_id INT,
    langue_id INT,
    PRIMARY KEY (candidat_id, langue_id),
    FOREIGN KEY (candidat_id) REFERENCES candidat_fait(candidat_id),
    FOREIGN KEY (langue_id) REFERENCES langue(langue_id)
);

CREATE TABLE my_project_database.my_project_schema.offre_comp (
    offre_id INT,
    competence_id INT,
    PRIMARY KEY (offre_id, competence_id),
    FOREIGN KEY (offre_id) REFERENCES offre_fait(offre_id),
    FOREIGN KEY (competence_id) REFERENCES competence(competence_id)
);

CREATE TABLE my_project_database.my_project_schema.stage_comp (
    stage_id INT,
    competence_id INT,
    PRIMARY KEY (stage_id, competence_id),
    FOREIGN KEY (stage_id) REFERENCES stage_fait(stage_id),
    FOREIGN KEY (competence_id) REFERENCES competence(competence_id)
);

CREATE TABLE my_project_database.my_project_schema.candidat_comp (
    candidat_id INT,
    competence_id INT,
    PRIMARY KEY (candidat_id, competence_id),
    FOREIGN KEY (candidat_id) REFERENCES candidat_fait(candidat_id),
    FOREIGN KEY (competence_id) REFERENCES competence(competence_id)
);

CREATE TABLE my_project_database.my_project_schema.certificat_cond (
    candidat_id INT,
    certificat_id INT,
    PRIMARY KEY (candidat_id, certificat_id),
    FOREIGN KEY (candidat_id) REFERENCES candidat_fait(candidat_id),
    FOREIGN KEY (certificat_id) REFERENCES certification(certificat_id)
);

SHOW TABLES IN my_project_database.my_project_schema;
--Pour suivre les modifications dans chacune de ces tables
CREATE OR REPLACE STREAM my_project_database.my_project_schema.offre_stream ON TABLE my_project_database.my_project_schema.offre_fait;
CREATE OR REPLACE STREAM my_project_database.my_project_schema.stage_stream ON TABLE my_project_database.my_project_schema.stage_fait;
CREATE OR REPLACE STREAM my_project_database.my_project_schema.candidat_stream ON TABLE my_project_database.my_project_schema.candidat_fait;
SELECT * FROM my_project_database.my_project_schema.candidat_stream;
--Ces deux lignes donnent toutes les permissions (ALL) sur toutes les tables existantes et futures dans le schéma test à dev_role. Cela inclut des permissions comme SELECT, INSERT, UPDATE, DELETE, etc.
CREATE OR REPLACE ROLE dev_role;
GRANT USAGE ON WAREHOUSE projet_warehouse TO ROLE dev_role;
GRANT USAGE ON DATABASE my_project_database TO ROLE dev_role;
GRANT USAGE ON SCHEMA my_project_database.my_project_schema TO ROLE dev_role;
GRANT ALL ON ALL TABLES IN SCHEMA my_project_database.my_project_schema  TO ROLE dev_role;
GRANT ALL ON FUTURE TABLES IN SCHEMA my_project_database.my_project_schema  TO ROLE dev_role;
SHOW GRANTS TO USER SAID;
GRANT ROLE dev_role TO USER SAID;






