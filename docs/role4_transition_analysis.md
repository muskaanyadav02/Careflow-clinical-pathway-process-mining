# CareFlow – Role 4 Transition Time Analysis

## 1. Objective
To analyze patient activity transitions and identify potential bottlenecks
using Python and the sample event log.

## 2. Dataset
- File: sample_event_log.csv
- Total records: 676
- Columns: Case_ID, Activity_Name, Timestamp
- Missing values: None found in the three columns.

## 3. Methodology
1. Loaded the event log using Pandas.
2. Converted timestamps into datetime format.
3. Sorted activities by patient ID and timestamp.
4. Calculated the time between consecutive activities.
5. Grouped exact activity-to-activity transitions.
6. Ranked transitions by average interval.

## 4. Preliminary Findings

| Transition | Occurrences | Average Interval (minutes) | Maximum Interval (minutes) |
|---|---:|---:|---:|
| Triage -> Doctor Consultation | 100 | 49.82 | 147 |
| Lab Test -> Repeat Lab Test | 6 | 44.83 | 57 |
| Lab Results Review -> Doctor Consultation | 24 | 40.42 | 75 |

## 5. Interpretation
- Triage -> Doctor Consultation has the highest average interval
  among the three transitions analyzed.
- Lab Test -> Repeat Lab Test has only six occurrences,
  so the result should be interpreted cautiously.
- Lab Results Review -> Doctor Consultation is another
  transition that may need further investigation.

These intervals represent the time between recorded activities.
They are not necessarily pure waiting times.

## 6. Limitations
- The analysis uses a sample dataset.
- Long intervals alone do not prove that a clinical bottleneck exists.
- Clinical context and the expected treatment pathway are needed
  before confirming process deviations.

## 7. Next Steps
- Implement SQL transition-time queries.
- Perform conformance checks against the expected pathway.
- Validate findings and document potential process deviations.
## 8. Preliminary Conformance Check

- Total patients analyzed: 100
- Exact matches to the illustrative pathway: 27 (27%)
- Different from the illustrative pathway: 73 (73%)

### Interpretation
The basic exact-sequence comparison identified 27 patient journeys
that matched the proposed pathway and 73 that differed from it.

These results are preliminary because the expected pathway has not
yet been validated against an approved clinical standard.
Differences may reflect legitimate variations in patient care.

### Next Steps
Validate the expected pathway with the project team and perform
more detailed conformance checking before reporting clinical deviations.