from pathlib import Path
import pandas as pd
import pm4py

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "sample" / "sample_event_log.csv"

print("Project root:", PROJECT_ROOT)
print("CSV path:", DATA_FILE)
print("File exists:", DATA_FILE.exists())

if DATA_FILE.exists():
    print("File size:", DATA_FILE.stat().st_size, "bytes")
    df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nMissing values:")
print(df.isnull().sum())

import pandas as pd
import pm4py

# Create a separate working copy
event_log = df.copy()

# Convert timestamps
event_log["Timestamp"] = pd.to_datetime(
    event_log["Timestamp"],
    errors="coerce"
)

# Remove records missing essential process information
event_log = event_log.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
).copy()

# Standardize column names for PM4Py
event_log = event_log.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

# Sort events in chronological order within each case
event_log = event_log.sort_values(
    ["case:concept:name", "time:timestamp"]
).reset_index(drop=True)

print("Raw records:", len(df))
print("Valid event records:", len(event_log))
print("Records excluded:", len(df) - len(event_log))

print(event_log.head())

activity_counts = (
    event_log["concept:name"]
    .value_counts()
    .rename_axis("Activity")
    .reset_index(name="Event_Count")
)

print(activity_counts)



# Patient activities order
# ==========================================
# DAY 2: PROCESS DISCOVERY
# ==========================================

print("\n========== DAY 2: PROCESS DISCOVERY ==========")

print("\nPatient activities ka order:")

# arrnage the patient activities to  time order 
for patient_id, patient_data in event_log.groupby("case:concept:name"):

    activities = patient_data["concept:name"].tolist()

    print(patient_id, "->", " -> ".join(activities))


# Which activities is Hapenning  more

print("\nWhich activities is Hapenning  more:")

activity_count = event_log["concept:name"].value_counts()

print(activity_count)




# Where the paitent goes to after one activity

print("\nActivity after next activity:")


for patient_id, patient_data in event_log.groupby("case:concept:name"):

    # Patient activities  order
    activities = patient_data["concept:name"].tolist()

    # Ativity after one activity 
    for i in range(len(activities) - 1):
        print(activities[i], "->", activities[i + 1])



print("\nMost common activity connections:")

transitions = []

for patient_id, patient_data in event_log.groupby("case:concept:name"):
    activities = patient_data["concept:name"].tolist()

    for i in range(len(activities) - 1):
        transitions.append((activities[i], activities[i + 1]))

transition_count = pd.Series(transitions).value_counts()

print(transition_count.head(10))




# Calculate time between activities
event_log = event_log.sort_values(
    ["case:concept:name", "time:timestamp"]
).copy()

# Find the next activity and its timestamp for each patient
event_log["Next_Activity"] = (
    event_log.groupby("case:concept:name")["concept:name"].shift(-1)
)

event_log["Next_Timestamp"] = (
    event_log.groupby("case:concept:name")["time:timestamp"].shift(-1)
)

# Calculate time taken in minutes
event_log["Transition_Time_Minutes"] = (
    event_log["Next_Timestamp"] - event_log["time:timestamp"]
).dt.total_seconds() / 60

# Remove the last activity of each patient
transitions_df = event_log.dropna(
    subset=["Next_Activity", "Next_Timestamp"]
).copy()

print("Transition time calculated successfully!")
print(
    transitions_df[
        [
            "case:concept:name",
            "concept:name",
            "Next_Activity",
            "Transition_Time_Minutes"
        ]
    ].head(10)
)



# Calculate time between two activities

event_log["Next_Timestamp"] = (
    event_log.groupby("case:concept:name")["time:timestamp"].shift(-1)
)

event_log["Waiting_Time_Minutes"] = (
    event_log["Next_Timestamp"] - event_log["time:timestamp"]
).dt.total_seconds() / 60

print(event_log[[
    "case:concept:name",
    "concept:name",
    "time:timestamp",
    "Next_Timestamp",
    "Waiting_Time_Minutes"]].head(10))


    

print("\n--- Average Time Between Activities ---")

average_times = (
    transitions_df.groupby(
        ["concept:name", "Next_Activity"]
    )["Transition_Time_Minutes"]
    .mean()
    .reset_index()
)

average_times = average_times.sort_values(
    "Transition_Time_Minutes",
    ascending=False
)

print(average_times.to_string(index=False))




# Day 4: Patient Process Map using PM4Py

print("\nCreating Patient Process Map...")

# Convert data into PM4Py format
event_log["time:timestamp"] = pd.to_datetime(
    event_log["time:timestamp"]
)




# Create Event Log

import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

pm_log = pm4py.convert_to_event_log(event_log)

# Discover process map
dfg, start_activities, end_activities = pm4py.discover_dfg(pm_log)

print("\nStart Activities:")
print(start_activities)

print("\nEnd Activities:")
print(end_activities)

print("\nProcess Map Connections:")
print(dfg)

# Show Process Map
pm4py.view_dfg(
    dfg,
    start_activities,
    end_activities
) 
