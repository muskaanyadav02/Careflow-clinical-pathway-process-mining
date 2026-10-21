import pandas as pd
import pm4py
from pathlib import Path

# Step 1: Load and validate the patient event log
file_path = Path("data/sample/sample_event_log.csv")

if not file_path.exists():
    raise FileNotFoundError(
        f"Patient event log not found: {file_path}"
    )

df = pd.read_csv(file_path)

if df.empty:
    raise ValueError("The patient event log is empty.")

# Step 2: Validate required columns
required_columns = {"Case_ID", "Activity_Name", "Timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

# Step 3: Validate event data
required_fields = ["Case_ID", "Activity_Name", "Timestamp"]

for column in required_fields:
    df[column] = df[column].replace(r"^\s*$", pd.NA, regex=True)

if df[required_fields].isna().any().any():
    raise ValueError(
        "The event log contains missing or blank required values."
    )

# Parse timestamps and reject invalid values
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

if df["Timestamp"].isna().any():
    raise ValueError(
        "The event log contains invalid timestamps."
    )

# Check for exact duplicate events
duplicate_columns = ["Case_ID", "Activity_Name", "Timestamp"]

duplicate_count = df.duplicated(
    subset=duplicate_columns
).sum()

if duplicate_count > 0:
    print(
        f"WARNING: Found {duplicate_count} duplicate event records. "
        "They will be retained for review."
    )

# Prepare the data for process mining
df = df.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

# Sort events by patient and timestamp
df = df.sort_values(
    ["case:concept:name", "time:timestamp"],
    kind="stable"
).reset_index(drop=True)

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