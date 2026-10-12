# CareFlow: Clinical Pathway Process Mining

## Project Overview
CareFlow analyzes patient event logs to understand clinical
process flows, measure activity transition times, and identify
potential process bottlenecks.

## My Role
Role 4: Process Compliance & Analytics Engineer

## Technologies Used
- Python
- Pandas
- PM4Py
- SQL
- Git and GitHub

## Dataset
Sample event log: `data/sample/sample_event_log.csv`

The dataset contains 676 event records for 100 patients.

Columns:
- Case_ID
- Activity_Name
- Timestamp

## Work Completed

1. Transition-time analysis using Pandas.
2. Process discovery using PM4Py.
3. Basic patient pathway comparison.
4. Preliminary findings documented in `docs/role4_transition_analysis.md`.

## Preliminary Findings

The longest average activity transition intervals identified were:

| Transition | Occurrences | Average Interval |
|---|---:|---:|
| Triage -> Doctor Consultation | 100 | 49.82 minutes |
| Lab Test -> Repeat Lab Test | 6 | 44.83 minutes |
| Lab Results Review -> Doctor Consultation | 24 | 40.42 minutes |

These are preliminary results from a sample dataset.
Long intervals do not automatically indicate clinical errors.

## Important Note
The expected clinical pathway must be validated with the project
team before confirming process deviations.

## How to Run

Install dependencies:

```bash
py -m pip install -r requirements.txt