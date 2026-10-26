import pandas as pd
from pathlib import Path

from event_log_validation import load_and_validate_event_log


# Load and validate the event log
input_file = Path("data/sample/sample_event_log.csv")
df = load_and_validate_event_log(input_file)


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
    "Maximum_Minutes",
]


# Save all transition statistics
output_file = Path("data/processed/bottleneck_summary.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

results.round(2).to_csv(output_file)


# Display the three longest transitions
print("\n===== CAREFLOW: TOP 3 LONGEST TRANSITIONS =====\n")
print(results.head(3).round(2).to_string())

print(f"\nFull bottleneck report saved to: {output_file}")
print("\n===== ANALYSIS COMPLETED =====")
