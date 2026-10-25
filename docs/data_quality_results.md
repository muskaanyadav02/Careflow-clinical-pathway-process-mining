# BigQuery Data Quality Results

## Overview
The simulated hospital event log was checked in BigQuery to verify data completeness, uniqueness, timestamp ordering, and activity consistency.

## Dataset Summary
- Total events: 10,263
- Unique patient cases: 1,500
- Unique activities: 8

## Validation Results

| Check | Result |
|---|---|
| Missing Case IDs | 0 |
| Missing activity names | 0 |
| Missing timestamps | 0 |
| Duplicate event groups | 0 |
| Out-of-order events | 0 |
| Equal consecutive timestamps | 0 |
| Unexpected activity names | 0 |

## Conclusion
All checks returned the expected results. The dataset passed these BigQuery data-quality checks and is ready for further process-mining and transition-time analysis.

**Note:** These checks validate data quality, not clinical correctness or compliance with an expected patient pathway.
