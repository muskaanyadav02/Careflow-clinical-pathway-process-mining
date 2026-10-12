-- CareFlow: Transition-Time Analysis
-- Database: careflow_db
-- Table: patient_events
-- Validation: Results matched the Python analysis.

USE careflow_db;

WITH ordered_events AS (
    SELECT
        Case_ID,
        Activity_Name,
        Timestamp,

        LEAD(Activity_Name) OVER (
            PARTITION BY Case_ID
            ORDER BY Timestamp
        ) AS Next_Activity,

        LEAD(Timestamp) OVER (
            PARTITION BY Case_ID
            ORDER BY Timestamp
        ) AS Next_Timestamp

    FROM patient_events
)

SELECT
    Activity_Name AS Previous_Activity,
    Next_Activity,
    COUNT(*) AS Occurrences,

    ROUND(
        AVG(
            TIMESTAMPDIFF(
                MINUTE,
                Timestamp,
                Next_Timestamp
            )
        ),
        2
    ) AS Average_Interval_Minutes,

    MAX(
        TIMESTAMPDIFF(
            MINUTE,
            Timestamp,
            Next_Timestamp
        )
    ) AS Maximum_Interval_Minutes

FROM ordered_events

WHERE Next_Activity IS NOT NULL

GROUP BY Activity_Name, Next_Activity

ORDER BY Average_Interval_Minutes DESC;