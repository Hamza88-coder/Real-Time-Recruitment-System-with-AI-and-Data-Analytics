-- models/candidat_info.sql
WITH candidat_details AS (
    SELECT
        cf.candidat_id,
        cf.first_name,
        cf.last_name,
        cf.email,
        cf.telephone,
        cf.date_birth,
        cf.gender,
        f.nom AS formation,
        e.nom AS ecole,
        v.nom AS ville,
        cf.nbr_years_exp
    FROM
        {{ ref('candidat_fait') }} cf
    JOIN {{ ref('formation') }} f ON cf.formation_id = f.formation_id
    JOIN {{ ref('ecole') }} e ON cf.ecole_id = e.ecole_id
    JOIN {{ ref('ville') }} v ON cf.ville_id = v.ville_id
)
SELECT * FROM candidat_details;
