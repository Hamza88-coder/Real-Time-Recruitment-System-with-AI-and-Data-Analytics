-- models/stage_info.sql
WITH stage_details AS (
    SELECT
        sf.stage_id,
        sf.duree_stage,
        sf.remunere,
        ts.nom AS type_stage,
        tt.nom AS type_trav,
        e.nom AS entreprise,
        f.nom AS formation
    FROM
        {{ ref('stage_fait') }} sf
    JOIN {{ ref('type_stage') }} ts ON sf.typeStag_id = ts.typeStag_id
    JOIN {{ ref('type_trav') }} tt ON sf.typeTrav_id = tt.typeTrav_id
    JOIN {{ ref('entreprise') }} e ON sf.entreprise_id = e.entreprise_id
    JOIN {{ ref('formation') }} f ON sf.formation_id = f.formation_id
)
SELECT * FROM stage_details;
