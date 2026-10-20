import pandas as pd
from pathlib import Path

# Load and validate the event log
input_file = Path("data/sample/sample_event_log.csv")

if not input_file.exists():
    raise FileNotFoundError(
        f"Event log not found: {input_file}"
    )

df = pd.read_csv(input_file)

if df.empty:
    raise ValueError("The event log contains no records.")

required_columns = {"Case_ID", "Activity_Name", "Timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

if df[["Case_ID", "Activity_Name", "Timestamp"]].isna().any().any():
    raise ValueError(
        "The event log contains missing case IDs, activities, or timestamps."
    )

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="raise"
)

# Identify previous and next activities
df["Previous_Activity"] = df.groupby("Case_ID")["Activity_Name"].shift(1)

# Calculate time between consecutive activities
df["Transition_Time_Minutes"] = (
    df.groupby("Case_ID")["Timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Remove first activities, which have no previous activity
transitions = df.dropna(subset=["Previous_Activity"]).copy()

# Create exact activity-to-activity transitions
transitions["Transition"] = (
    transitions["Previous_Activity"]
    + " -> "
    + transitions["Activity_Name"]
)

# Calculate transition statistics
results = (
    transitions.groupby("Transition")["Transition_Time_Minutes"]
    .agg(["count", "mean", "max"])
    .sort_values("mean", ascending=False)
)

results.columns = [
    "Occurrences",
    "Average_Minutes",
    "Maximum_Minutes"
]

print("\n===== CAREFLOW: TOP 3 LONGEST TRANSITIONS =====\n")
print(results.head(3).round(2).to_string())

print("\n===== ANALYSIS COMPLETED =====")