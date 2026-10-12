
-- CareFlow: Event Log Data Quality Checks
-- Table: hospital_event_log

-- 1. Check for missing required values
SELECT
    COUNTIF(Case_ID IS NULL OR TRIM(CAST(Case_ID AS STRING)) = '') AS missing_case_ids,
    COUNTIF(Activity_Name IS NULL OR TRIM(Activity_Name) = '') AS missing_activity_names,
    COUNTIF(Timestamp IS NULL) AS missing_timestamps
FROM hospital_event_log;


-- 2. Check for duplicate events
SELECT
    Case_ID,
    Activity_Name,
    Timestamp,
    COUNT(*) AS duplicate_count
FROM hospital_event_log
GROUP BY Case_ID, Activity_Name, Timestamp
HAVING COUNT(*) > 1;


-- 3. Check for unexpected activity names
SELECT
    Activity_Name,
    COUNT(*) AS event_count
FROM hospital_event_log
WHERE Activity_Name NOT IN (
    'Patient Registration',
    'Triage',
    'Doctor Consultation',
    'Lab Test',
    'Repeat Lab Test',
    'Lab Results Review',
    'Treatment',
    'Discharge'
)
GROUP BY Activity_Name;
