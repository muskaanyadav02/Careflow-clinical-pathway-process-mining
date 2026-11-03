CareFlow – Role 4: Process Compliance and Analytics

1. Project Overview

The objective of Role 4 is to analyse patient journeys, identify potential waiting-time bottlenecks and compare actual patient journeys with an illustrative expected clinical pathway.

2. Dataset Information

- Dataset: "hospital_event_log_full.csv"
- Total event records: 676
- Total patients: 100
- Data columns: Case_ID, Activity_Name, Timestamp

3. Transition-Time and Bottleneck Analysis

Python and Pandas were used to calculate the time between consecutive patient activities.

Top three potential bottlenecks:

Activity Transition| Average Time| Occurrences
Triage → Doctor Consultation| 49.82 minutes| 100
Lab Test → Repeat Lab Test| 44.83 minutes| 6
Lab Results Review → Doctor Consultation| 40.42 minutes| 24

The Triage-to-Doctor Consultation transition had the highest average waiting time.

Output files:

- "data/processed/bottleneck_summary.csv"
- "data/processed/top_bottlenecks.png"

4. Conformance Checking

The actual patient journeys were compared with this illustrative expected pathway:

Patient Registration → Triage → Doctor Consultation → Treatment → Discharge

Results:

- Total patients analysed: 100
- Exact pathway matches: 27
- Different pathways: 73
- Exact match percentage: 27%

Output file:
"data/processed/conformance_results.csv"

Note: The expected pathway is illustrative and is not a clinically validated standard. Differences do not automatically indicate clinical errors.

5. Tools and Technologies

- Python
- Pandas
- SQL
- PM4Py
- Matplotlib
- Git and GitHub

6. Conclusion

Through this analysis, I examined 676 event records from 100 patients, identified potential waiting-time bottlenecks and evaluated variations in patient journeys. These results help understand the workflow and highlight areas for further investigation.