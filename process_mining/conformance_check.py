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
# 7. CONFORMANCE CHECKING CORE AI ENGINE (Day 5 Task)
# ============================================================
print("\nInitializing sequence alignment and conformance analysis engine...")

conformance_records = []

# हर एक मरीज के वास्तविक रास्ते का आदर्श रास्ते से मिलान करना
for _, row in patient_paths.iterrows():
    case_id = row["case:concept:name"]
    actual_path = row["concept:name"]
    
    # मेट्रिक्स इनिशियलाइज़ करना
    is_conforming = True
    missing_activities = []
    incorrect_sequence = False
    
    # चेकमार्क 1: मिसिंग एक्टिविटी ढूंढना
    for activity in ideal_path:
        if activity not in actual_path:
            missing_activities.append(activity)
            is_conforming = False
            
    # चेकमार्क 2: क्रम की सटीकता (Sequence Order Check)
    # केवल उन एक्टिविटीज का क्रम देखना जो मरीज के रास्ते में मौजूद हैं
    indices = [ideal_path.index(act) for act in actual_path if act in ideal_path]
    if indices != sorted(indices):
        incorrect_sequence = True
        is_conforming = False
        
    # मरीज के लिए अंतिम निर्णय (Decision Framework)
    status = "CONFORMING" if is_conforming else "NON_CONFORMING"
    
    # गड़बड़ का कारण (Violation Reason) दर्ज करना
    reasons = []
    if missing_activities:
        reasons.append(f"Missing: {missing_activities}")
    if incorrect_sequence:
        reasons.append("Out-of-Order Sequence Detected")
        
    violation_reason = " | ".join(reasons) if reasons else "None"
    
    conformance_records.append({
        "Case_ID": case_id,
        "Actual_Path": " -> ".join(actual_path),
        "Conformance_Status": status,
        "Violation_Reason": violation_reason,
        "Total_Activities": len(actual_path)
    })

# ============================================================
# 8. METRICS GENERATION & EXPORT WORKFLOW (Day 6 Task)
# ============================================================
print("\nCompiling final clinical compliance metrics...")

results_df = pd.DataFrame(conformance_records)

# टोटल पास/फेल काउंट निकालना
total_cases = len(results_df)
conforming_count = len(results_df[results_df["Conformance_Status"] == "CONFORMING"])
non_conforming_count = total_cases - conforming_count
compliance_rate = (conforming_count / total_cases) * 100 if total_cases > 0 else 0

print(f" -> Total Audited Cases: {total_cases}")
print(f" -> Perfectly Conforming Cases: {conforming_count}")
print(f" -> Non-Conforming Violations: {non_conforming_count}")
print(f" -> Overall Clinical Compliance Rate: {compliance_rate:.2f}%")

# आउटपुट डायरेक्टरी सुनिश्चित करना और फाइल एक्सपोर्ट करना
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
results_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n[SUCCESS] Careflow Audit Complete! Results exported to: '{OUTPUT_FILE}'")
