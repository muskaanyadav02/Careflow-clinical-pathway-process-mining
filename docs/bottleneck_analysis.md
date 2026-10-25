# Initial Bottleneck Analysis

## Objective
Analyze the time between consecutive hospital activities using the simulated CareFlow event log stored in BigQuery.

## Initial Finding
The transition from **Triage → Doctor Consultation** had the highest average elapsed time among the results reviewed so far.

- **Average elapsed time:** 46.37 minutes
- **Median elapsed time:** 31 minutes
- **Number of transitions:** 1,500

## Interpretation
This transition is a priority for further investigation because it has a relatively high average elapsed time. These measurements represent the time between recorded activities and do not, by themselves, confirm the actual waiting time.

## Next Steps
- Compare the SQL findings with the team's Python process-mining analysis.
- Investigate other transitions with high elapsed times.
- Use the findings to support the CareFlow dashboard and recommendations.