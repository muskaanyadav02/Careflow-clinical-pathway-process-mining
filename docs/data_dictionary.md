# CareFlow Data Dictionary

## 1. Overview

This document defines the structure of the simulated hospital event log used in the CareFlow Clinical Pathway Process Mining project.

The dataset represents patient journeys through hospital activities and is intended for process discovery, transition-time analysis, bottleneck identification, and conformance checking.

**Data source:** Simulated data generated using Python. It does not contain real patient records.

## 2. Dataset Details

| Property | Description |
|---|---|
| Dataset file | `hospital_event_log_full.csv` |
| BigQuery table | `eastern-concord-511514-t3.careflow.hospital_event_log` |
| Number of cases | 1,500 |
| Number of events | 10,263 |
| Number of unique activities | 8 |
| Required columns | 3 |

## 3. Column Definitions

| Column | Data type | Description |
|---|---|---|
| `Case_ID` | STRING | Unique identifier for a simulated patient journey. |
| `Activity_Name` | STRING | Name of the hospital activity recorded in an event. |
| `Timestamp` | TIMESTAMP | Date and time when the activity occurred. |

## 4. Activities in the Dataset

The simulated event log includes these activities:

- Patient Registration
- Triage
- Doctor Consultation
- Lab Test
- Repeat Lab Test
- Lab Results Review
- Treatment
- Discharge

Some journeys include optional laboratory activities, repeat tests, or another doctor consultation.

## 5. Data Quality Rules

- All required columns must be present.
- Case IDs, activity names, and timestamps must not be blank.
- Timestamps must be valid.
- Duplicate events must be identified.
- Events within each case must follow chronological order.
- Activity names should match the expected activity list.

## 6. Important Notes

- The dataset is simulated for project development and demonstration.
- Time between consecutive events represents elapsed time, not necessarily confirmed waiting time.
- The event log supports process mining and exploratory analysis; findings should not be interpreted as evidence about a real hospital.
