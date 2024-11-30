-- Insérer 30 candidats supplémentaires
INSERT INTO candidates (first_name, last_name, full_name, title_id, date_of_birth, place_of_birth, gender, nationality, phone_number, type_trav_id, mode_travail_id)
VALUES
    ('Ahmed', 'Bensalah', 'Ahmed Bensalah', 1, '1998-02-15', 'Rabat', 'Male', 'Moroccan', '0661234567', 1, 3),
    ('Asmae', 'El Amrani', 'Asmae El Amrani', 2, '1995-08-20', 'Casablanca', 'Female', 'Moroccan', '0662234567', 2, 2),
    ('Mehdi', 'Kabbaj', 'Mehdi Kabbaj', 3, '1997-04-18', 'Marrakech', 'Male', 'Moroccan', '0663234567', 3, 1),
    ('Noura', 'Fakhreddine', 'Noura Fakhreddine', 4, '1996-11-25', 'Tangier', 'Female', 'Moroccan', '0664234567', 1, 1),
    ('Samir', 'Hammani', 'Samir Hammani', 1, '1999-03-30', 'Fes', 'Male', 'Moroccan', '0665234567', 2, 2),
    ('Zineb', 'Chaoui', 'Zineb Chaoui', 2, '1995-05-15', 'Agadir', 'Female', 'Moroccan', '0666234567', 3, 3),
    ('Karim', 'Jebli', 'Karim Jebli', 3, '1998-12-10', 'Casablanca', 'Male', 'Moroccan', '0667234567', 1, 2),
    ('Hajar', 'Lahlou', 'Hajar Lahlou', 4, '1994-06-25', 'Rabat', 'Female', 'Moroccan', '0668234567', 2, 1),
    ('Yassir', 'El Ouafi', 'Yassir El Ouafi', 2, '1997-01-12', 'Fes', 'Male', 'Moroccan', '0669234567', 3, 3),
    ('Malak', 'Belghiti', 'Malak Belghiti', 1, '1996-09-07', 'Marrakech', 'Female', 'Moroccan', '0671234567', 2, 1),
    ('Imane', 'El Idrissi', 'Imane El Idrissi', 3, '1999-05-21', 'Tangier', 'Female', 'Moroccan', '0672234567', 1, 2),
    ('Rachid', 'Toumi', 'Rachid Toumi', 4, '1998-02-18', 'Agadir', 'Male', 'Moroccan', '0673234567', 2, 3),
    ('Leila', 'Bouhaddou', 'Leila Bouhaddou', 2, '1995-07-30', 'Casablanca', 'Female', 'Moroccan', '0674234567', 3, 1),
    ('Anas', 'Filali', 'Anas Filali', 1, '1997-03-10', 'Rabat', 'Male', 'Moroccan', '0675234567', 1, 2),
    ('Salma', 'El Oufir', 'Salma El Oufir', 4, '1999-08-22', 'Fes', 'Female', 'Moroccan', '0676234567', 2, 3),
    ('Younes', 'Benjelloun', 'Younes Benjelloun', 3, '1995-10-05', 'Marrakech', 'Male', 'Moroccan', '0677234567', 1, 1),
    ('Hanane', 'Tazi', 'Hanane Tazi', 2, '1996-12-15', 'Tangier', 'Female', 'Moroccan', '0678234567', 3, 2),
    ('Ibrahim', 'Rahmouni', 'Ibrahim Rahmouni', 1, '1998-01-01', 'Casablanca', 'Male', 'Moroccan', '0679234567', 2, 3),
    ('Amina', 'Jadidi', 'Amina Jadidi', 4, '1997-02-14', 'Rabat', 'Female', 'Moroccan', '0681234567', 1, 2),
    ('Tarik', 'Moujahid', 'Tarik Moujahid', 2, '1996-09-27', 'Fes', 'Male', 'Moroccan', '0682234567', 3, 1),
    ('Mouna', 'El Karimi', 'Mouna El Karimi', 3, '1999-04-30', 'Marrakech', 'Female', 'Moroccan', '0683234567', 1, 2),
    ('Ali', 'Bouazza', 'Ali Bouazza', 1, '1998-12-12', 'Tangier', 'Male', 'Moroccan', '0684234567', 2, 3),
    ('Sofia', 'Alaoui', 'Sofia Alaoui', 4, '1995-06-16', 'Agadir', 'Female', 'Moroccan', '0685234567', 3, 1),
    ('Hamid', 'Bennani', 'Hamid Bennani', 2, '1997-11-20', 'Casablanca', 'Male', 'Moroccan', '0686234567', 1, 2),
    ('Nadia', 'Zouiten', 'Nadia Zouiten', 3, '1996-03-05', 'Rabat', 'Female', 'Moroccan', '0687234567', 2, 3),
    ('Khalil', 'El Bassir', 'Khalil El Bassir', 1, '1999-07-19', 'Fes', 'Male', 'Moroccan', '0688234567', 3, 1),
    ('Nada', 'Chaib', 'Nada Chaib', 2, '1995-02-25', 'Marrakech', 'Female', 'Moroccan', '0689234567', 1, 2),
    ('Ziad', 'Harroun', 'Ziad Harroun', 4, '1997-09-09', 'Tangier', 'Male', 'Moroccan', '0691234567', 2, 3),
    ('Laila', 'Fassi', 'Laila Fassi', 3, '1998-11-11', 'Agadir', 'Female', 'Moroccan', '0692234567', 3, 1);


-- Adresses supplémentaires
INSERT INTO addresses (candidate_id, formatted_location, city, region, country, postal_code)
VALUES
    (6, 'Rue des fleurs', 'Marrakech', 'Marrakech-Safi', 'Morocco', '40000'),
    (7, 'Quartier Yacoub', 'Casablanca', 'Casablanca-Settat', 'Morocco', '20000'),
    (8, 'Avenue Al Qods', 'Tangier', 'Tanger-Tetouan-Al Hoceima', 'Morocco', '90000'),
    (9, 'Boulevard Hassan II', 'Fes', 'Fes-Meknes', 'Morocco', '30000'),
    (10, 'Cité Universitaire', 'Agadir', 'Souss-Massa', 'Morocco', '80000');

-- Compétences supplémentaires
INSERT INTO skills (skill_name)
VALUES
    ('R'), ('Java'), ('Power BI'), ('Tableau'), ('Data Cleaning');

-- Attribuer des compétences aux candidats supplémentaires
INSERT INTO candidate_skills (candidate_id, skill_id)
VALUES
    (6, 6), (6, 7), (7, 8), (8, 9), (9, 10),
    (10, 1), (10, 2), (11, 3), (12, 4), (13, 5);

-- Langues supplémentaires
INSERT INTO languages (language_name, proficiency_level)
VALUES
    ('Spanish', 'Intermediate'), ('German', 'Basic');

-- Attribuer des langues aux candidats supplémentaires
INSERT INTO candidate_languages (candidate_id, language_id)
VALUES
    (6, 4), (7, 5), (8, 1), (9, 2), (10, 3);

-- Certifications supplémentaires
INSERT INTO certifications (certification_name, issuing_organization, date_obtained)
VALUES
    ('Certified Data Scientist', 'IBM', '2023-05-10'),
    ('Certified Tableau Specialist', 'Tableau', '2022-08-15');

-- Attribuer des certifications aux candidats supplémentaires
INSERT INTO candidate_certifications (candidate_id, certification_id)
VALUES
    (6, 4), (7, 5), (8, 1), (9, 2), (10, 3);


