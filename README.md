# CareFlow – Clinical Pathway Process Mining

## Project Overview

CareFlow is a clinical pathway process-mining project that analyzes simulated hospital event logs to understand patient journeys, discover process bottlenecks, and investigate delays between hospital activities.

Traditional dashboards often show average waiting times but may not reveal the sequence of activities responsible for delays. CareFlow aims to provide a process-oriented view of hospital workflows to support better analysis and decision-making.

## Objectives

- Reconstruct patient journeys from timestamped event logs.
- Discover actual activity sequences and process variations.
- Analyze elapsed time between consecutive activities.
- Identify potential bottlenecks in hospital workflows.
- Check process conformance against an expected pathway.
- Present findings through analytical dashboards and reports.

## Dataset

The project uses a simulated hospital event log generated in Python.

| Property | Details |
|---|---|
| Patient cases | 1,500 |
| Total events | 10,263 |
| Unique activities | 8 |
| Required fields | `Case_ID`, `Activity_Name`, `Timestamp` |
| Full dataset | `data/raw/hospital_event_log_full.csv` |

The dataset includes activities such as Patient Registration, Triage, Doctor Consultation, Lab Test, Lab Results Review, Treatment, and Discharge. Some simulated journeys include repeat tests and additional consultations.

**Data disclaimer:** All patient journeys are simulated for educational and analytical purposes. No real patient records are used.

## Technology Stack

- **Python and Pandas:** Data generation, preparation, validation, and analysis.
- **SQL and Google BigQuery:** Data storage, quality checks, transition-time analysis, and bottleneck summaries.
- **PM4Py:** Process discovery and process-mining analysis.
- **Power BI:** Interactive dashboard and visualization development.

## Project Workflow

1. Generate simulated hospital event logs.
2. Validate and prepare the event data.
3. Store and analyze the dataset using SQL and BigQuery.
4. Discover process flows and analyze activity transitions.
5. Investigate potential bottlenecks and process conformance.
6. Develop dashboards and consolidate findings into project documentation.

## Repository Structure

- `data/` – Sample, raw, and processed datasets.
- `scripts/` – Data generation and validation scripts.
- `sql/` – Table definitions, quality checks, transition-time queries, and bottleneck summaries.
- `process_mining/` – Process discovery, bottleneck, and conformance analysis scripts.
- `dashboard/` – Dashboard-related files and documentation.
- `docs/` – Project overview, architecture, data dictionary, and analysis documentation.
- `tests/` – Automated tests for data validation and other project components.
- `dbt/` – dbt-related project documentation and development.



## Team Collaboration

The project is developed collaboratively using Git and GitHub. Team members contribute through individual branches so their work can be reviewed and integrated according to the team's prescribed workflow.

## Disclaimer

The results are based on simulated data and should not be interpreted as evidence of actual hospital performance or clinical outcomes.
