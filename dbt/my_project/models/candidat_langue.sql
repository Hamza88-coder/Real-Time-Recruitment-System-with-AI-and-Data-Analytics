-- models/candidat_langue.sql
WITH candidat_langue_details AS (
    SELECT
        cl.candidat_id,
        cf.first_name,
        cf.last_name,
        l.nom AS langue
    FROM
        {{ ref('langue_cand') }} cl
    JOIN {{ ref('candidat_fait') }} cf ON cl.candidat_id = cf.candidat_id
    JOIN {{ ref('langue') }} l ON cl.langue_id = l.langue_id
)
SELECT * FROM candidat_langue_details;
