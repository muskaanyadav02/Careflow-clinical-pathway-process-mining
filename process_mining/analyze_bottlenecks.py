from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Project path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"

# Load data
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Event log file not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

if df.empty:
    raise ValueError("The event log is empty.")

# Validate required columns
required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Required column missing: {column}")

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

# Calculate transition time in minutes
df["Transition_Time_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

# Remove last activity of each patient
transitions = df.dropna(
    subset=["Next_Activity", "Next_Timestamp"]
).copy()

# Calculate transition statistics
average_times = (
    transitions.groupby(
        ["Activity_Name", "Next_Activity"]
    )["Transition_Time_Minutes"]
    .agg(["mean", "count", "median", "max"])
    .reset_index()
)

# Rename columns
average_times.columns = [
    "from_activity",
    "to_activity",
    "average_time_minutes",
    "transition_count",
    "median_time_minutes",
    "maximum_time_minutes"
]

# Sort by average transition time
average_times = average_times.sort_values(
    "average_time_minutes",
    ascending=False
)

# Display top 3 potential bottlenecks
print("\n===== TOP 3 POTENTIAL BOTTLENECKS =====")

print(
    average_times.head(3).round(2).to_string(index=False)
)

# Save bottleneck analysis
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "bottleneck_summary.csv"
)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

average_times.to_csv(OUTPUT_FILE, index=False)

print("\nAnalysis saved to:", OUTPUT_FILE)

# Create bottleneck chart
matplotlib.rcParams["font.family"] = "DejaVu Sans"

top = average_times.head(10)

plt.figure(figsize=(12, 8))

plt.bar(
    range(len(top)),
    top["average_time_minutes"],
    color="#FFD580",
    edgecolor="#0f3c5a",
    linewidth=1.5,
    width=0.6,
    alpha=0.85
)

plt.xticks(
    range(len(top)),
    top["from_activity"] + " to " + top["to_activity"],
    rotation=45,
    ha="right"
)

plt.xlabel("Activity Transitions")
plt.ylabel("Average Time (Minutes)")
plt.title("Top 10 Potential Bottlenecks")

CHART_FILE = (
    PROJECT_ROOT / "data" / "processed" / "top_bottlenecks.png"
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.40)
plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
plt.close()

print("\nChart saved to:", CHART_FILE)
print("\n===== BOTTLENECK ANALYSIS COMPLETED =====")