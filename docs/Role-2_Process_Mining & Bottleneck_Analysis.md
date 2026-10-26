# CareFlow – Role 2 Process Mining & Bottleneck Analysis

## 1. Objective
To discover the actual patient flows, visualize the clinical pathways using PM4Py, and identify the top system bottlenecks causing delays in patient care.

## 2. Dataset & Scope
- **Input File:** `data/raw/hospital_event_log_full.csv` (Switched to full raw dataset for the mid-review demo)
- **Target Fields:** `Case_ID` (renamed to `case:concept:name`), `Activity_Name` (renamed to `concept:name`), and `Timestamp` (renamed to `time:timestamp`).
- **Data Quality:** Cleaned missing rows and sorted records chronologically within each patient case.

## 3. Methodology & Core Deliverables

### A. Process Discovery (`discover_process.py`)
- Standardized the core event data frame for **PM4Py** compliance.
- Generated the **Directly-Followed Graph (DFG)** to map the complete flow of patients between various clinical activities.
- Handled Graphviz backend dependencies locally (`DejaVu Sans` font engine mapping).

### B. Bottleneck Analysis (`analyze_bottlenecks.py`)
- Implemented automated look-ahead logic via Pandas `.shift(-1)` grouping to isolate subsequent patient hops and compute explicit elapsed times in minutes.
- Grouped identical activity-to-activity transitions to compute the **Average Transition Time** and total **Patient Transitions**.

## 4. Mid-Review Metrics & Findings

### Top 3 Potential Bottlenecks (Identified from Full Dataset)

| Rank | From Activity | To Activity | Average Time (Minutes) | Total Patient Transitions |
| :---: | :--- | :--- | :---: | :---: |
| **1** | Triage | Doctor Consultation | 49.82 | 100 |
| **2** | Lab Test | Repeat Lab Test | 44.83 | 6 |
| **3** | Lab Results Review | Doctor Consultation | 40.42 | 24 |

### Interpretation
- **Triage to Doctor Consultation** stands out as the most critical bottleneck with a significant waiting window of **49.82 minutes** affecting all 100 tracked cases. 
- **Lab Test to Repeat Lab Test** takes an average of **44.83 minutes** but features low frequency (6 cases), requiring closer clinical review rather than structural resizing.

## 5. Output Artifacts Generated
The pipeline automatically overwrites and maintains the following artifacts inside `data/processed/`:
1. **`transition_analysis.csv`**: Structured spreadsheet mapping the summary metrics for all identified process loops.
2. **`top_bottlenecks.png`**: An optimized vertical bar chart visualization embedded with automated text data labels, explicit axis rotations, and tailored safe bottom subplots padding to prevent edge text clippings during rendering.

## 6. How to Run
From the repository root directory, execute:
```bash
python process_mining/discover_process.py
python process_mining/analyze_bottlenecks.py
```
