-- Question 1: List all currently open job postings with recruiter names.
SELECT
    jp.id,
    jp.title,
    r.name AS recruiter_name
FROM job_postings AS jp
JOIN recruiters AS r
    ON r.id = jp.recruiter_id
WHERE jp.status = 'open'
ORDER BY jp.id;

-- Question 2: For each job posting, how many applicants reached the Final interview stage?
SELECT
    jp.id,
    jp.title,
    COUNT(DISTINCT i.applicant_id) AS final_stage_applicants
FROM job_postings AS jp
LEFT JOIN interviews AS i
    ON i.job_posting_id = jp.id
   AND i.stage = 'Final'
GROUP BY jp.id, jp.title
ORDER BY jp.id;

-- Question 3: Find every person who effectively applied to more than one job posting.
SELECT
    LOWER(TRIM(a.full_name)) AS person_name,
    COUNT(DISTINCT i.job_posting_id) AS jobs_applied
FROM applicants AS a
JOIN interviews AS i
    ON i.applicant_id = a.id
GROUP BY LOWER(TRIM(a.full_name))
HAVING COUNT(DISTINCT i.job_posting_id) > 1
ORDER BY person_name;

-- Question 4: For each recruiter, compute the Final-stage conversion rate (passed / total Final-stage interviews),
-- but only include recruiters with at least 3 Final-stage interviews.
SELECT
    r.id,
    r.name,
    CAST(
        SUM(CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END) AS REAL
    ) / COUNT(i.id) AS final_conversion_rate
FROM recruiters AS r
JOIN job_postings AS jp
    ON jp.recruiter_id = r.id
JOIN interviews AS i
    ON i.job_posting_id = jp.id
   AND i.stage = 'Final'
GROUP BY r.id, r.name
HAVING COUNT(i.id) >= 3
ORDER BY final_conversion_rate DESC, r.name;

-- Question 5 (Bonus): Using a window function, find the recruiter with the most successful placements (passed at Final stage)
-- per department.
WITH recruiter_success AS (
    SELECT
        jp.department,
        r.name AS recruiter_name,
        COUNT(*) AS successful_placements,
        ROW_NUMBER() OVER (
            PARTITION BY jp.department
            ORDER BY COUNT(*) DESC, r.name
        ) AS placement_rank
    FROM interviews AS i
    JOIN job_postings AS jp
        ON jp.id = i.job_posting_id
    JOIN recruiters AS r
        ON r.id = jp.recruiter_id
    WHERE i.stage = 'Final'
      AND i.outcome = 'passed'
    GROUP BY jp.department, r.id, r.name
)
SELECT
    department,
    recruiter_name,
    successful_placements
FROM recruiter_success
WHERE placement_rank = 1
ORDER BY department;
