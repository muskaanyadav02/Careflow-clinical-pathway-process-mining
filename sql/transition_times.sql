-- CareFlow: Transition-Time Analysis
-- Database: careflow_db
-- Table: patient_events
-- Purpose: Summarize valid transition intervals between activities.

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
),

transition_intervals AS (
    SELECT
        Activity_Name AS Previous_Activity,
        Next_Activity,

        TIMESTAMPDIFF(
            SECOND,
            Timestamp,
            Next_Timestamp
        ) / 60.0 AS Interval_Minutes

    FROM ordered_events
    WHERE Next_Activity IS NOT NULL
)

SELECT
    Previous_Activity,
    Next_Activity,

    COUNT(*) AS Total_Transitions,

    SUM(
        CASE
            WHEN Interval_Minutes >= 0 THEN 1
            ELSE 0
        END
    ) AS Valid_Transitions,

    ROUND(
        AVG(
            CASE
                WHEN Interval_Minutes >= 0
                THEN Interval_Minutes
                ELSE NULL
            END
        ),
        2
    ) AS Average_Interval_Minutes,

    MAX(
        CASE
            WHEN Interval_Minutes >= 0
            THEN Interval_Minutes
            ELSE NULL
        END
    ) AS Maximum_Interval_Minutes

FROM transition_intervals

GROUP BY Previous_Activity, Next_Activity

ORDER BY Average_Interval_Minutes DESC;