
-- CareFlow: Bottleneck Summary Analysis
-- Calculates elapsed time between consecutive activities.

WITH ordered_events AS (
    SELECT
        Case_ID,
        Activity_Name,
        Timestamp,

        LEAD(Activity_Name) OVER (
            PARTITION BY Case_ID
            ORDER BY Timestamp
        ) AS next_activity,

        LEAD(Timestamp) OVER (
            PARTITION BY Case_ID
            ORDER BY Timestamp
        ) AS next_timestamp

    FROM
        `eastern-concord-511514-t3.careflow.hospital_event_log`
),

transition_times AS (
    SELECT
        Activity_Name AS from_activity,
        next_activity AS to_activity,

        TIMESTAMP_DIFF(
            next_timestamp,
            Timestamp,
            MINUTE
        ) AS transition_time_minutes

    FROM ordered_events
    WHERE next_activity IS NOT NULL
)

SELECT
    from_activity,
    to_activity,

    COUNT(*) AS transition_count,

    ROUND(
        AVG(transition_time_minutes), 2
    ) AS average_time_minutes,

    APPROX_QUANTILES(
        transition_time_minutes, 100
    )[OFFSET(50)] AS median_time_minutes,

    MAX(transition_time_minutes)
        AS maximum_time_minutes

FROM transition_times

GROUP BY
    from_activity,
    to_activity

ORDER BY
    average_time_minutes DESC;
