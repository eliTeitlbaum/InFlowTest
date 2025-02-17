query_2 = """
SELECT 
    w.worker_id,
    w.first_name,
    w.last_name,
    COUNT(c.candidate_id) AS total_candidates,
    COUNT(r.recruitment_id) / COUNT(c.candidate_id) * 100 AS success_rate_percentage,
    SUM(b.bonus_amount) AS monthly_bonus
FROM 
    dim_workers w
JOIN 
    fact_recruitment r ON w.worker_id = r.worker_id
JOIN 
    dim_candidate c ON r.candidate_id = c.candidate_id
JOIN 
    fact_bonus b ON w.worker_id = b.worker_id AND r.month_id = b.month_id
GROUP BY 
    w.worker_id, w.first_name, w.last_name;
"""


query_3 = """
SELECT 
    w.worker_id,
    w.first_name,
    w.last_name,
    w.address,
    COUNT(c.candidate_id) AS total_candidates,
    COUNT(r.recruitment_id) / COUNT(c.candidate_id) * 100 AS success_rate_percentage,
    SUM(b.bonus_amount) AS monthly_bonus
FROM 
    dim_workers w
JOIN 
    fact_recruitment r ON w.worker_id = r.worker_id
JOIN 
    dim_candidate c ON r.candidate_id = c.candidate_id
JOIN 
    fact_bonus b ON w.worker_id = b.worker_id AND r.month_id = b.month_id
GROUP BY 
    w.worker_id, w.first_name, w.last_name, w.address;
"""


query_4 = """
SELECT 
    r.department_id,
    r.month_id,
    w.worker_id,
    w.first_name,
    w.last_name,
    COUNT(r.recruitment_id) AS total_recruited
FROM 
    fact_recruitment r
JOIN 
    dim_workers w ON r.worker_id = w.worker_id
GROUP BY 
    r.department_id, r.month_id, w.worker_id, w.first_name, w.last_name
ORDER BY 
    r.department_id, r.month_id, total_recruited DESC
LIMIT 2;
"""


query_5 = """
SELECT 
    r.department_id,
    r.month_id,
    c.candidate_id,
    c.name,
    c.submission_date
FROM 
    fact_recruitment r
JOIN 
    dim_candidate c ON r.candidate_id = c.candidate_id
WHERE 
    (r.department_id, r.month_id, c.submission_date) IN (
        SELECT 
            r.department_id,
            r.month_id,
            MIN(c.submission_date) AS first_submission_date
        FROM 
            fact_recruitment r
        JOIN 
            dim_candidate c ON r.candidate_id = c.candidate_id
        GROUP BY 
            r.department_id, r.month_id
        ORDER BY 
            r.department_id, r.month_id
    )
ORDER BY 
    r.department_id, r.month_id, c.submission_date
LIMIT 2;
"""