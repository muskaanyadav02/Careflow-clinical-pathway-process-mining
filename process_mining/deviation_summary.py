from pathlib import Path
import pandas as pd

# ============================================================
# 1. PATH CONFIGURATION
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "conformance_results.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "deviation_summary.csv"

print("=== CAREFLOW CLINICAL PATHWAY: DEVIATION SUMMARY METRICS ===")
print(f"Target data execution paths successfully mapped by Member 2.")

# ============================================================
# 2. DATA INGESTION & VALIDATION
# ============================================================
if not INPUT_FILE.exists():
    print(f"Execution Error: Missing target conformance results file at {INPUT_FILE}")
    print("Please ensure conformance_check.py is executed successfully first.")
    exit()

# Load the compiled conformance records from the target directory
df = pd.read_csv(INPUT_FILE)
print(f"Ingested conformance results successfully. Total traced cases: {len(df)}")

# ============================================================
# 3. VOLUMETRIC COUNT & AGGREGATION ANALYSIS
# ============================================================
print("\n[📊] Commencing trace variance counting and aggregation...")

# Group and count the categorical compliance status using value_counts
summary = df["Is_Conforming"].value_counts().reset_index()
summary.columns = ["Status", "Count"]

# Calculate percentage metrics for deeper analytical insights
total_cases = summary["Count"].sum()
summary["Percentage"] = (summary["Count"] / total_cases) * 100
summary["Percentage"] = summary["Percentage"].round(2)

# ============================================================
# 4. FILE PERSISTENCE & OUTPUT EXPORT
# ============================================================
print("\n[💾] Exporting calculated deviation summary metrics to target file...")

# Verify dynamic parent directory existence before storage dump
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Exporting summary data directly for dashboard consumption
summary.to_csv(OUTPUT_FILE, index=False)

print(f"[✔] Deviation summary processing fully finalized by Member 2.")
print(f"[📊] Final Summary Exported successfully at: {OUTPUT_FILE}")
print("\nExecution Output Summary Table:")
print(summary.to_string(index=False))
