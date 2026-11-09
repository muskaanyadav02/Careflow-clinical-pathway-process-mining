from pathlib import Path
import pandas as pd

# ============================================================
# 1. PATH CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "hospital_event_log_full.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "conformance_results.csv"

print("=== CAREFLOW CLINICAL PATHWAY CONFORMANCE CHECKING - DAY 4 ===")
print(f"Target execution directory successfully mapped to: {PROJECT_ROOT}")

# ============================================================
# 2. DATA LOADING & PRE-PROCESSING
# ============================================================
if not DATA_FILE.exists():
    print(f"Execution Error: Missing target raw file at {DATA_FILE}")
    exit()

df = pd.read_csv(DATA_FILE)
print(f"Dataset successfully ingested. Total historical log records: {df.shape}")

# Remove truncated or invalid trace rows missing core transactional values
event_log = df.dropna(subset=["Case_ID", "Activity_Name", "Timestamp"]).copy()

# Enforce explicit datetime sequencing types for chronological precision
event_log["Timestamp"] = pd.to_datetime(event_log["Timestamp"])
event_log = event_log.sort_values(["Case_ID", "Timestamp"]).reset_index(drop=True)

# ============================================================
# 3. SCHEMA STANDARDIZATION FOR PM4PY CORE COMPLIANCE
# ============================================================
event_log = event_log.rename(columns={
    "Case_ID": "case:concept:name",
    "Activity_Name": "concept:name",
    "Timestamp": "time:timestamp"
})

print("Schema attributes successfully mapped to PM4Py structural naming conventions.")
print(f"Total sanitized and isolated event logs remaining for processing: {len(event_log)}")

# ============================================================
# 4. ADVANCED DATA DESCRIPTIVE METRICS 
# ============================================================
print("Generating core activity frequency metrics...")
top_activities = event_log["concept:name"].value_counts().head(3)
for activity, count in top_activities.items():
    print(f" -> Volumetric Checkpoint: Activity '{activity}' triggered {count} times.")

# ============================================================
# 5. CORE WORKFLOW: CHROMATIC SEQUENCE GROUPING
# ============================================================
print("Commencing chronological patient trace pathway aggregation...")
patient_paths = event_log.groupby("case:concept:name")["concept:name"].apply(list).reset_index()

total_isolated_cases = len(patient_paths)
print(f"Trace aggregation complete. Found {total_isolated_cases} unique patient cases.")

# ============================================================
# 6. DEFINE IDEAL CLINICAL PATHWAY METRICS (Today's Task - 1 Nov)
# ============================================================
print("Defining target ideal clinical pathway architecture...")

# Establishing the gold-standard sequence of activities for a standard patient journey
ideal_path = [
    "Patient Registration",
    "Triage",
    "Doctor Consultation",   
    "Lab Test",
    "Lab Results Review",
    "Treatment",
    "Discharge"
]

print("Ideal clinical pathway successfully defined:")
print(" -> Base Sequence: " + " -> ".join(ideal_path))



# ============================================================
# 7. ITERATIVE TRACE MATCHING FRAMEWORK (Today's Expansion)
# ============================================================
print("\n[🔄] Deploying trace matching execution framework...")
conformance_records = []

# Iterating over each structured patient path to trace process deviation limits
for index, row in patient_paths.iterrows():
    case_id = row["case:concept:name"]
    actual_path = row["concept:name"]
    
    # ============================================================
    # 8. CONDITIONAL VARIANCE INTERSECTION LOGIC
    # ============================================================
    # Evaluating structural compliance by performing precise array comparison
    if actual_path == ideal_path:
        is_conforming = "YES"
    else:
        is_conforming = "NO"
        
    # ============================================================
    # 9. METRICS BUFFER STORAGE & RECORD AGGREGATION
    # ============================================================
    # Appending classified operational metrics into the tracking buffer array
    conformance_records.append({
        "Case_ID": case_id,
        "Is_Conforming": is_conforming
    })

print(f"[✔] Successfully processed and mapped all {len(conformance_records)} operational traces.")
print("Preview of internal memory metrics buffer:")
print(conformance_records[:3])

# ============================================================
# 10. DATAFRAME EXPORT & TARGET FILE PERSISTENCE (Today's New Task)
# ============================================================
print("\n[💾] Converting structural buffer memory logs to DataFrame...")
conformance_df = pd.DataFrame(conformance_records)

# Enforce dynamic parent directory verification before storage dump
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Exporting target analytics CSV for dashboard ingestion
conformance_df.to_csv(OUTPUT_FILE, index=False)

print(f"[✔] Conformance engine processing fully finalized.")
print(f"[📊] Final Export Success. File persisted at: {OUTPUT_FILE}")
print(conformance_df.head(5).to_string())