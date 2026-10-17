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
## 9. SQL Testing and Validation

### Database Setup
- Database: careflow_db
- Table: patient_events
- Total event records: 676

### Testing Performed
1. Imported the sample event log into MySQL.
2. Verified the event count using COUNT(*).
3. Executed the SQL transition-time analysis.
4. Compared the SQL results with the Python analysis.

### Validation Result
The SQL output matched the Python results for the
three longest-average transitions checked.

| Transition | Occurrences | Average Interval |
|---|---:|---:|
| Triage -> Doctor Consultation | 100 | 49.82 minutes |
| Lab Test -> Repeat Lab Test | 6 | 44.83 minutes |
| Lab Results Review -> Doctor Consultation | 24 | 40.42 minutes |

### Limitations
The results are based on a sample dataset.
Long intervals identify transitions for further investigation,
but do not independently prove clinical bottlenecks.
## 10. Patient Pathway Conformance Analysis

### Objective
The purpose of this analysis is to compare each patient's recorded activity sequence with an illustrative expected pathway and identify differences.

### Illustrative Expected Pathway
Patient Registration -> Triage -> Doctor Consultation -> Treatment -> Discharge

Note: This pathway is used for demonstration only. It has not been confirmed as an approved clinical standard.

### Methodology
1. Load the patient event log using Python and pandas.
2. Convert event timestamps into datetime format.
3. Sort events by patient ID and timestamp.
4. Group activities into individual patient journeys.
5. Compare each journey with the illustrative expected pathway.
6. Identify missing expected activities, additional activities, and the first sequence difference.
7. Export patient-level results to a CSV file.

### Results
The analysis processed 100 patient journeys.

- Exact pathway matches: 27
- Journeys differing from the expected pathway: 73
- Exact pathway match percentage: 27.00%

### Output
The patient-level results are saved to:

`data/processed/conformance_results.csv`

The output includes the patient ID, actual journey, exact-match status, missing activities, additional activities, and first identified difference.

### Limitations
The expected pathway is illustrative and has not been clinically validated. A difference does not automatically indicate a clinical error or poor-quality care. Some activities may be optional, repeated, or appropriate for particular patients.

The current analysis performs an exact sequence comparison. It does not implement formal process-mining conformance metrics or determine whether deviations are clinically appropriate.

### How to Run
From the project root directory, run:

`py process_mining/conformance_check.py`
## 11. Process Deviation Summary

### Objective
The objective of this analysis is to summarize differences between recorded patient journeys and the illustrative expected pathway.

### Methodology
1. Load the existing patient-level conformance results.
2. Calculate the total number of patient journeys.
3. Count exact pathway matches and differing journeys.
4. Count the additional activities recorded in the results.
5. Summarize missing activities.
6. Count the reported first-difference patterns.
7. Export the summary to a separate CSV file.

### Results

The analysis summarized 100 patient journeys.

- Exact pathway matches: 27
- Journeys differing from the illustrative pathway: 73
- Exact-match percentage: 27.00%

Additional activities reported:

- Lab Test: 73 patient journeys
- Lab Results Review: 73 patient journeys
- Repeat Lab Test: 6 patient journeys

No missing activities were recorded in the existing conformance results.

The most frequent first-difference pattern was:

Position 4: expected 'Treatment', found 'Lab Test'

This pattern was reported for 73 patient journeys.

### Output Files

Input:
`data/processed/conformance_results.csv`

Python script:
`process_mining/deviation_summary.py`

Generated summary:
`data/processed/deviation_summary.csv`

### Limitations

The summary is based on the existing conformance results and an illustrative expected pathway that has not been clinically validated.

Additional activities are activities that do not appear in the illustrative pathway. Their presence does not establish that they are unnecessary or inappropriate.

The first-difference pattern identifies a difference in sequence, not a confirmed operational or clinical problem.

Further investigation and an approved clinical pathway would be required to assess the significance of these differences.
## 12. Validation of Conformance Results

### Objective
Validate the patient-level conformance results against the deviation summary.

### Validation Checks
- Total patient records: 100
- Exact pathway matches: 27
- Journeys differing from the reference pathway: 73
- Duplicate patient IDs: 0
- Missing patient IDs: 0

### Validation Outcome
The patient-level record count and exact-match counts agree with
the deviation summary. No duplicate or missing patient IDs were
found in the checked results.

### Limitation
This validation checks record counts and patient ID quality.
Activity-level deviation counts require separate validation.
The reference pathway is illustrative and is not a clinically
approved standard. Differences do not automatically indicate
clinical errors.
### Validation Results

The patient-level conformance results were checked for record counts
and patient ID quality.

- Total patient journeys: 100
- Exact pathway matches: 27
- Journeys differing from the reference pathway: 73
- Duplicate patient IDs: 0
- Missing patient IDs: 0

Additional activity counts were independently checked against the
patient-level conformance results:

- Lab Test: 73 patient journeys
- Lab Results Review: 73 patient journeys
- Repeat Lab Test: 6 patient journeys
- Missing activities recorded: None

These checks support the consistency of the reported counts.
The results describe differences from an illustrative reference
pathway and do not establish clinical errors.
## 13. Deviation Summary Validation

### Objective
Validate that the deviation summary accurately represents the patient-level conformance results.

### Validation Checks
The validation script checks:
- Required columns and patient identifiers.
- Duplicate patient IDs.
- Exact-match and differing-journey counts.
- Overall summary counts against patient-level results.
- Additional-activity counts.
- First-difference counts.
- Missing-activity counts.
- Consistency of journeys marked as exact matches.

### Results
Validation was performed on 100 patient journeys.

- Exact pathway matches: 27
- Journeys differing from the illustrative pathway: 73
- Journeys with a first difference: 73
- Journeys with missing activities: 0

All validation checks passed on the current sample results.

### How to Run
From the project root directory, run:

`py process_mining/validate_deviation_summary.py`

### Limitations
The validation checks data consistency and summary accuracy.
They do not establish whether a pathway difference is a clinical
error. The expected pathway remains illustrative and requires
validation against an approved clinical standard.