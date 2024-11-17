-- models/candidat_stage_competence_langue.sql
WITH candidat_stage_details AS (
    SELECT
        cf.candidat_id,
        cf.first_name,
        cf.last_name,
        sf.stage_id,
        ts.nom AS type_stage,
        tt.nom AS type_trav,
        e.nom AS entreprise,
        f.nom AS formation,
        c.nom AS competence,
        l.nom AS langue
    FROM
        {{ ref('candidat_fait') }} cf
    JOIN {{ ref('stage_fait') }} sf ON sf.formation_id = cf.formation_id
    JOIN {{ ref('type_stage') }} ts ON sf.typeStag_id = ts.typeStag_id
    JOIN {{ ref('type_trav') }} tt ON sf.typeTrav_id = tt.typeTrav_id
    JOIN {{ ref('entreprise') }} e ON sf.entreprise_id = e.entreprise_id
    JOIN {{ ref('formation') }} f ON sf.formation_id = f.formation_id
    LEFT JOIN {{ ref('stage_comp') }} sc ON sf.stage_id = sc.stage_id
    LEFT JOIN {{ ref('competence') }} c ON sc.competence_id = c.competence_id
    LEFT JOIN {{ ref('langue_stag') }} ls ON sf.stage_id = ls.offre_id
    LEFT JOIN {{ ref('langue') }} l ON ls.langue_id = l.langue_id
)
SELECT * FROM candidat_stage_details;
