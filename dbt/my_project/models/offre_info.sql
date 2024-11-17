-- models/offre_info.sql
WITH offre_details AS (
    SELECT
        ofr.offre_id,
        ofr.salaire,
        ofr.experience_dur,
        tt.nom AS type_trav,
        e.nom AS entreprise,
        f.nom AS formation
    FROM
        {{ ref('offre_fait') }} ofr
    JOIN {{ ref('type_trav') }} tt ON ofr.typeTrav_id = tt.typeTrav_id
    JOIN {{ ref('entreprise') }} e ON ofr.entreprise_id = e.entreprise_id
    JOIN {{ ref('formation') }} f ON ofr.formation_id = f.formation_id
)
SELECT * FROM offre_details;
