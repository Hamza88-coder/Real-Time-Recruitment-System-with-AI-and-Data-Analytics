-- 1. Insérer des titres
INSERT INTO title (title_name) VALUES 
    ('Data Scientist'),
    ('Data Engineer'),
    ('Data Analyst'),
    ('Machine Learning Engineer');

-- 2. Insérer des types de travail
INSERT INTO type_trav (trav_type) VALUES 
    ('Travail'),
    ('PFA'),
    ('PFE');

-- 3. Insérer des modes de travail
INSERT INTO mode_travail (mode_name) VALUES 
    ('Hybrid'),
    ('À distance'),
    ('Présentiel');

-- 4. Insérer des candidats
INSERT INTO candidates (first_name, last_name, full_name, title_id, date_of_birth, place_of_birth, gender, nationality, phone_number, type_trav_id, mode_travail_id)
VALUES
    ('Fatima Ezzahra', 'Kadiri', 'Fatima Ezzahra Kadiri', 2, '2002-05-15', 'Casablanca', 'Female', 'Moroccan', '0612345678', 3, 1),
    ('Hamza', 'Malyana', 'Hamza Malyana', 1, '2002-06-20', 'Rabat', 'Male', 'Moroccan', '0623456789', 3, 2),
    ('Ossama', 'Hafi', 'Ossama Hafi', 3, '2002-01-10', 'Fes', 'Male', 'Moroccan', '0634567890', 2, 3),
    ('Said', 'Khalid', 'Said Khalid', 4, '2002-09-25', 'Marrakech', 'Male', 'Moroccan', '0645678901', 1, 1),
    ('Sara', 'El Yousfi', 'Sara El Yousfi', NULL, '1998-03-15', 'Tangier', 'Female', 'Moroccan', '0656789012', 1, 2);

-- 5. Insérer des adresses
INSERT INTO addresses (candidate_id, formatted_location, city, region, country, postal_code) VALUES 
    (1, 'Route de l\'Université', 'Casablanca', 'Casablanca-Settat', 'Morocco', '20000'),
    (2, 'Avenue Mohammed V', 'Rabat', 'Rabat-Salé-Kénitra', 'Morocco', '10000'),
    (3, 'Quartier Atlas', 'Fes', 'Fes-Meknes', 'Morocco', '30000'),
    (4, 'Quartier Gueliz', 'Marrakech', 'Marrakech-Safi', 'Morocco', '40000'),
    (5, 'Avenue Pasteur', 'Tangier', 'Tanger-Tetouan-Al Hoceima', 'Morocco', '90000');

-- 6. Insérer des URLs
INSERT INTO urls (candidate_id, type, url) VALUES 
    (1, 'LinkedIn', 'https://linkedin.com/fatima_kadiri'),
    (2, 'GitHub', 'https://github.com/hamza_malyana'),
    (3, 'Portfolio', 'https://ossama-hafi.com'),
    (4, 'LinkedIn', 'https://linkedin.com/said_khalid'),
    (5, 'GitHub', 'https://github.com/sara_yousfi');

-- 7. Insérer des informations éducatives
INSERT INTO education_details (candidate_id, etude_title, etablissement_name, start_date, end_date, etude_city, etude_region, etude_country) VALUES 
    (1, 'BSc Computer Science', 'Université Hassan II', '2018-09-01', '2022-06-30', 'Casablanca', 'Casablanca-Settat', 'Morocco'),
    (2, 'MSc Data Science', 'Université Mohammed V', '2017-09-01', '2021-06-30', 'Rabat', 'Rabat-Salé-Kénitra', 'Morocco'),
    (3, 'Licence Informatique', 'Université Sidi Mohamed Ben Abdellah', '2016-09-01', '2020-06-30', 'Fes', 'Fes-Meknes', 'Morocco'),
    (4, 'Master Machine Learning', 'Université Cadi Ayyad', '2015-09-01', '2019-06-30', 'Marrakech', 'Marrakech-Safi', 'Morocco'),
    (5, 'BSc Software Engineering', 'Université Abdelmalek Essaadi', '2019-09-01', '2023-06-30', 'Tangier', 'Tanger-Tetouan-Al Hoceima', 'Morocco');

-- 8. Insérer des expériences professionnelles
INSERT INTO work_experience_details (candidate_id, job_title, company_name, city, region, sector_of_activity, start_date, end_date) VALUES 
    (1, 'Junior Data Engineer', 'OCP Group', 'Casablanca', 'Casablanca-Settat', 'Mining', '2022-07-01', '2023-07-01'),
    (2, 'Data Scientist Intern', 'Moroccan Agency for AI', 'Rabat', 'Rabat-Salé-Kénitra', 'AI Research', '2021-07-01', '2022-07-01'),
    (3, 'Data Analyst Intern', 'BMCE Bank', 'Fes', 'Fes-Meknes', 'Banking', '2020-07-01', '2021-07-01'),
    (4, 'Machine Learning Intern', 'Maroc Telecom', 'Marrakech', 'Marrakech-Safi', 'Telecommunications', '2019-07-01', '2020-07-01'),
    (5, 'Software Engineering Intern', 'Inwi', 'Tangier', 'Tanger-Tetouan-Al Hoceima', 'Telecommunications', '2022-07-01', '2023-07-01');

-- 9. Insérer des compétences
INSERT INTO skills (skill_name) VALUES 
    ('Python'), ('SQL'), ('Machine Learning'), ('Deep Learning'), ('Data Analysis');

INSERT INTO candidate_skills (candidate_id, skill_id) VALUES 
    (1, 1), (1, 2), (1, 3), 
    (2, 1), (2, 4), 
    (3, 2), (3, 5), 
    (4, 1), (4, 3), 
    (5, 2), (5, 5);

-- 10. Insérer des langues
INSERT INTO languages (language_name, proficiency_level) VALUES 
    ('English', 'Fluent'),
    ('French', 'Advanced'),
    ('Arabic', 'Native');

INSERT INTO candidate_languages (candidate_id, language_id) VALUES 
    (1, 1), (1, 3),
    (2, 2), (2, 3),
    (3, 1), 
    (4, 1), (4, 2), 
    (5, 3);

-- 11. Insérer des certifications
INSERT INTO certifications (certification_name, issuing_organization, date_obtained) VALUES 
    ('AWS Certified Solutions Architect', 'Amazon', '2022-01-15'),
    ('Google Data Analytics', 'Google', '2021-06-20'),
    ('Azure Data Engineer Associate', 'Microsoft', '2023-03-10');

INSERT INTO candidate_certifications (candidate_id, certification_id) VALUES 
    (1, 1), (1, 2),
    (2, 2), 
    (3, 3), 
    (4, 1), (4, 3),
    (5, 2);
