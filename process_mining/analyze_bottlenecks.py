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

# Validate required columns
required_columns = {"Case_ID", "Activity_Name", "Timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {sorted(missing_columns)}"
    )

# Validate missing values
if df[list(required_columns)].isna().any().any():
    raise ValueError(
        "The event log contains missing case IDs, activities, or timestamps."
    )

# Validate blank values
for column in ["Case_ID", "Activity_Name", "Timestamp"]:
    df[column] = df[column].replace(r"^\s*$", pd.NA, regex=True)

if df[["Case_ID", "Activity_Name", "Timestamp"]].isna().any().any():
    raise ValueError(
        "The event log contains blank required values."
    )

# Convert timestamps and order events
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="raise"
)

df = df.sort_values(
    ["Case_ID", "Timestamp"]
).reset_index(drop=True)

# Identify previous activities
df["Previous_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(1)
)

# Calculate time between consecutive activities
df["Transition_Time_Minutes"] = (
    df.groupby("Case_ID")["Timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Keep activities that have a previous activity
transitions = df.dropna(
    subset=["Previous_Activity"]
).copy()

# Validate transition times
if (transitions["Transition_Time_Minutes"] < 0).any():
    raise ValueError(
        "Negative transition times detected. Check event ordering."
    )

# Create activity-to-activity transitions
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

# Rename result columns
results.columns = [
    "Occurrences",
    "Average_Minutes",
    "Maximum_Minutes"
]

# Display the three longest transitions
print("\n===== CAREFLOW: TOP 3 LONGEST TRANSITIONS =====\n")
print(results.head(3).round(2).to_string())

print("\n===== ANALYSIS COMPLETED =====")