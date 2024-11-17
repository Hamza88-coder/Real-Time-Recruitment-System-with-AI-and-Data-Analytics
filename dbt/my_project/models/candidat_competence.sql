-- models/candidat_competence.sql
WITH candidat_competence_details AS (
    SELECT
        cc.candidat_id,
        cf.first_name,
        cf.last_name,
        c.nom AS competence
    FROM
        {{ ref('candidat_comp') }} cc
    JOIN {{ ref('candidat_fait') }} cf ON cc.candidat_id = cf.candidat_id
    JOIN {{ ref('competence') }} c ON cc.competence_id = c.competence_id
)
SELECT * FROM candidat_competence_details;
