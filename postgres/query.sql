SELECT 
    c.full_name AS candidate_name,
    t.title_name AS title,
    COALESCE(SUM(EXTRACT(YEAR FROM we.end_date) - EXTRACT(YEAR FROM we.start_date)), 0) AS total_years_work_experience,
    COALESCE(SUM(EXTRACT(YEAR FROM ed.end_date) - EXTRACT(YEAR FROM ed.start_date)), 0) AS total_years_education,
    STRING_AGG(DISTINCT s.skill_name, ', ') AS skills,
    STRING_AGG(DISTINCT we.sector_of_activity, ', ') AS sector_of_activity,
    STRING_AGG(DISTINCT CONCAT(l.language_name, ' (', l.proficiency_level, ')'), ', ') AS language
FROM 
    candidates c
LEFT JOIN 
    title t ON c.title_id = t.id
LEFT JOIN 
    work_experience_details we ON c.id = we.candidate_id
LEFT JOIN 
    education_details ed ON c.id = ed.candidate_id
LEFT JOIN 
    candidate_skills cs ON c.id = cs.candidate_id
LEFT JOIN 
    skills s ON cs.skill_id = s.id
LEFT JOIN 
    candidate_languages cl ON c.id = cl.candidate_id
LEFT JOIN 
    languages l ON cl.language_id = l.id
GROUP BY 
    c.id, t.title_name;
