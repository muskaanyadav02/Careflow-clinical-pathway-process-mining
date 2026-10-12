import pandas as pd
import pm4py
import os

# Step 1: Load the patient event log
file_path = "data/sample/sample_event_log.csv"
df = pd.read_csv(file_path)

# Step 2: Prepare the data for process mining
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

df = df.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

# Step 3: Sort events by patient and time
df = df.sort_values(["case:concept:name", "time:timestamp"])

# Step 4: Discover the process model
event_log = pm4py.format_dataframe(
    df,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

process_tree = pm4py.discover_process_tree_inductive(event_log)

# Step 5: Display the results
print("\n===== CAREFLOW PROCESS DISCOVERY =====")
print("Total patient records:", len(df))
print("Unique patients:", df["case:concept:name"].nunique())
print("Unique activities:", df["concept:name"].nunique())

print("\nDiscovered Process Tree:")
print(process_tree)

print("\n===== PROCESS DISCOVERY COMPLETED =====")