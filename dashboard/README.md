
# CareFlow Streamlit Dashboard

## Overview
The CareFlow dashboard provides a visual interface for exploring
clinical pathway event data, process activities, transition times,
bottlenecks, and data quality.

## Dashboard Pages
- Executive Overview: Summary metrics and activity insights.
- Activity Explorer: Explore activity counts and distributions.
- Pathway Explorer: Visualize transitions between activities.
- Bottleneck Intelligence: Analyze transition counts and elapsed times.
- Data Quality: Review data validation results.

## Requirements
Install the project dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Ensure the processed data files and data quality report
are available in `data/processed/`.

## Run the Dashboard
From the repository root, execute:

```bash
python -m streamlit run dashboard/app.py
```

## Run Tests
Run the project test suite from the repository root:

```bash
python -m pytest -q
```

## Data Interpretation
Transition durations represent elapsed time between consecutive
recorded activities. They should not automatically be interpreted
as confirmed clinical waiting times.

## Integration
The dashboard is a backup UI for the CareFlow project.
It should be tested alongside the process-mining and analytics
components on the integration branch before the review.
