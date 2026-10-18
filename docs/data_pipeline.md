
# CareFlow Data Pipeline

## 1. Overview

The CareFlow data pipeline generates simulated hospital event-log data, validates its quality, and creates a machine-readable quality report for downstream process-mining analysis.

## 2. Input Data

The dataset is simulated and contains the following columns:

- `Case_ID`: Identifier for a simulated patient journey.
- `Activity_Name`: Hospital activity performed during the journey.
- `Timestamp`: Date and time when the activity occurred.

The dataset does not contain real patient records.

## 3. Generate the Dataset

Run the following command from the project root:

```powershell
python scripts/generate_data.py --cases 1500 --output data/raw/hospital_event_log_full.csv
```

This generates 1,500 simulated patient cases.

## 4. Validate the Dataset

Run:

```powershell
python scripts/validate_data.py data/raw/hospital_event_log_full.csv
```

The validator checks required fields, timestamps, duplicate events, and event chronology, among other data-quality rules.

## 5. Generate the Quality Report

Run:

```powershell
python scripts/generate_quality_report.py
```

The report is saved to:

`data/processed/data_quality_report.json`

It includes event and case counts, activity counts, missing values, duplicate events, invalid timestamps, chronological violations, and an overall status.

## 6. Run Automated Tests

Run the data-generation tests:

```powershell
python -m pytest tests/test_data_generation.py -v
```

Run the validation tests:

```powershell
python -m pytest tests/test_validation.py -v
```

## 7. Downstream Analysis

The validated event log can be loaded into BigQuery and used for transition-time analysis, bottleneck investigation, process discovery, and dashboard development.

## 8. Limitations

The dataset is simulated. Time differences between activities are not necessarily confirmed clinical waiting times and should be interpreted as process-analysis indicators.
