-- 1. Incidents by Sport
SELECT sport_type, COUNT(*) AS incident_count
FROM incident_report_export
GROUP BY sport_type;

-- 2. Diagnosed vs Not Diagnosed by Age Group
SELECT age_group, diagnosed_concussion, COUNT(*) AS count
FROM incident_report_export
GROUP BY age_group, diagnosed_concussion;

-- 3. Incidents Over Time (Last 90 Days)
SELECT CAST(injury_date AS DATE) AS date, COUNT(*) AS incident_count
FROM incident_report_export
WHERE injury_date >= DATEADD(day, -90, GETDATE())
GROUP BY CAST(injury_date AS DATE)
ORDER BY date;

-- 4. Cleared vs Still Symptomatic
SELECT cleared_to_play, COUNT(*) AS count
FROM incident_report_export
GROUP BY cleared_to_play;

-- 5. KPI – Average Days to Clearance (for diagnosed cases only)
SELECT AVG(DATEDIFF(day, injury_date, timestamp)) AS avg_days_to_clear
FROM incident_report_export
WHERE diagnosed_concussion = 1 AND cleared_to_play = 1;