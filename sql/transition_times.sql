
-- CareFlow: Calculate time between consecutive hospital activities
-- Data source: Simulated hospital event log in BigQuery

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
        Case_ID,
        Activity_Name AS from_activity,
        next_activity AS to_activity,
        Timestamp AS from_timestamp,
        next_timestamp AS to_timestamp,

        TIMESTAMP_DIFF(
            next_timestamp,
            Timestamp,
            MINUTE
        ) AS transition_time_minutes

    FROM ordered_events
    WHERE next_activity IS NOT NULL
)

SELECT
    Case_ID,
    from_activity,
    to_activity,
    from_timestamp,
    to_timestamp,
    transition_time_minutes

FROM transition_times
ORDER BY
    Case_ID,
    from_timestamp;
