from pathlib import Path
import pandas as pd

# Project path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "sample" / "sample_event_log.csv"

# Load data
df = pd.read_csv(DATA_FILE)

# Prepare event log
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
).copy()

df = df.sort_values(
    ["Case_ID", "Timestamp"]
).copy()

# Find next activity and timestamp
df["Next_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(-1)
)

df["Next_Timestamp"] = (
    df.groupby("Case_ID")["Timestamp"].shift(-1)
)

# Calculate time between activities in minutes
df["Transition_Time_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

# Remove last activity of each patient
transitions = df.dropna(
    subset=["Next_Activity", "Next_Timestamp"]
).copy()

# Calculate average transition time
average_times = (
    transitions.groupby(
        ["Activity_Name", "Next_Activity"]
    )["Transition_Time_Minutes"]
    .agg(["mean", "count"])
    .reset_index()
)

average_times.columns = [
    "From_Activity",
    "To_Activity",
    "Average_Time_Minutes",
    "Patient_Transitions"
]

average_times = average_times.sort_values(
    "Average_Time_Minutes",
    ascending=False
)

# Display top 3 potential bottlenecks
print("\n===== TOP 3 POTENTIAL BOTTLENECKS =====")

print(
    average_times.head(3).round(2).to_string(index=False)
)

# Save analysis
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "transition_analysis.csv"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

average_times.to_csv(OUTPUT_FILE, index=False)

print("\nAnalysis saved to:", OUTPUT_FILE)
print("\nBottleneck analysis completed!")




import matplotlib
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["font.enable_last_resort"] = False

import matplotlib.pyplot as plt


# Select top 10 transitions
top = average_times.head(10)

# Create chart
plt.figure(figsize=(12, 8))

plt.bar(
    range(len(top)),
    top["Average_Time_Minutes"]
)

plt.xticks(
    range(len(top)),
    top["From_Activity"] + " to " + top["To_Activity"],
    rotation=45,
    ha="right"
)

plt.xlabel("Activity Transitions")
plt.ylabel("Average Time (Minutes)")
plt.title("Top 10 Potential Bottlenecks")

# Save chart 
CHART_FILE = PROJECT_ROOT / "data" / "processed" / "top_bottlenecks.png"

plt.tight_layout()
plt.subplots_adjust(bottom=0.40)
plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
plt.show()

print("Chart saved:", CHART_FILE)

