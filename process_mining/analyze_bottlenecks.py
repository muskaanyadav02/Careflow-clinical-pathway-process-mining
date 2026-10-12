import pandas as pd

# Load the dataset
df = pd.read_csv("data/sample/sample_event_log.csv")

# Convert timestamps
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort activities for each patient
df = df.sort_values(["Case_ID", "Timestamp"])

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