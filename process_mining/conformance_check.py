from pathlib import Path
import pandas as pd


# 1. PATH CONFIGURATION
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "conformance_results.csv"

print("=== CAREFLOW CLINICAL PATHWAY CONFORMANCE CHECKING - DAY 3 ===")
print(f"Target execution directory successfully mapped to: {PROJECT_ROOT}")


# 2. DATA LOADING & PRE-PROCESSING
if not DATA_FILE.exists():
    print(f"Execution Error: Missing target raw file at {DATA_FILE}")
    exit()

df = pd.read_csv(DATA_FILE)
print(f"Dataset successfully ingested. Total historical log records: {df.shape[0]}")

# Remove truncated or invalid trace rows missing core transactional values
event_log = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"]).copy()

# Enforce explicit datetime sequencing types for chronological precision
event_log["Timestamp"] = pd.to_datetime(event_log["Timestamp"])
event_log = event_log.sort_values(["Case_ID", "Timestamp"]).reset_index(drop=True)



# 3. SCHEMA STANDARDIZATION FOR PM4PY CORE COMPLIANCE
event_log = event_log.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

print("Schema attributes successfully mapped to PM4Py structural naming conventions.")
print(f"Total sanitized and isolated event logs remaining for processing: {len(event_log)}")



# 4. ADVANCED DATA DESCRIPTIVE METRICS (Extended Code Block)
print("Generating core activity frequency metrics...")
top_activities = event_log["concept:name"].value_counts().head(3)
for activity, count in top_activities.items():
    print(f" -> Volumetric Checkpoint: Activity '{activity}' triggered {count} times.")


# 5. CORE WORKFLOW: CHROMATIC SEQUENCE GROUPING (Today's Task)
print("Commencing chronological patient trace pathway aggregation...")
patient_paths = event_log.groupby("case:concept:name")["concept:name"].apply(list).reset_index()

total_isolated_cases = len(patient_paths)
print(f"[✔] Trace aggregation complete. Found {total_isolated_cases} unique patient cases.")
print("\nPreview of structured operational trace paths:")
print(patient_paths.head(5).to_string())
