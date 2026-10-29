from pathlib import Path
import pandas as pd

# Step 1: Base paths set up by Member 2
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "conformance_results.csv"

print("=== CONFORMANCE CHECKING - DAY 2 ===")
print("Data path initialized:", DATA_FILE)

# Step 2: Load the full dataset (Today's Update)
df = pd.read_csv(DATA_FILE)
print("Raw dataset shape:", df.shape)

# Step 3: Clean data - Remove empty values from essential rows
event_log = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"]).copy()

# Step 4: Standardize column names for PM4Py (Renaming logic)
event_log = event_log.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

print("Data cleaned and standardized successfully!")
print("Valid event records remaining:", len(event_log))
print("Standard columns:", event_log.columns.tolist())
