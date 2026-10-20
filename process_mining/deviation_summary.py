import pandas as pd
from pathlib import Path
from collections import Counter

# Step 1: Load the existing conformance results
input_file = Path("data/processed/conformance_results.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "Conformance results not found. Run conformance_check.py first."
    )

df = pd.read_csv(input_file)

if df.empty:
    raise ValueError(
        "Conformance results are empty. Run conformance_check.py again."
    )

# Step 2: Check required columns
required_columns = {
    "Case_ID",
    "Exact_Match",
    "Missing_Activities",
    "Additional_Activities",
    "First_Difference",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {sorted(missing_columns)}")
# Validate case IDs
if df["Case_ID"].replace(r"^\s*$", pd.NA, regex=True).isna().any():
    raise ValueError(
        "Conformance results contain missing or blank Case_ID values."
    )

# Prepare empty values for summary calculations
df = df.fillna("")

# Step 3: Calculate overall results
total_patients = len(df)

exact_matches = (
    df["Exact_Match"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("true")
    .sum()
)

different_journeys = total_patients - exact_matches

print("\n===== CAREFLOW DEVIATION SUMMARY =====")
print("Total patient journeys:", total_patients)
print("Exact pathway matches:", exact_matches)
print("Journeys differing from expected pathway:", different_journeys)

if total_patients:
    percentage = exact_matches / total_patients * 100
    print(f"Exact-match percentage: {percentage:.2f}%")

# Step 4: Count additional activities
additional_counts = Counter()

for activities in df["Additional_Activities"]:
    if str(activities).strip() and str(activities).strip().lower() != "none":
        for activity in str(activities).split(","):
            activity = activity.strip()
            if activity:
                additional_counts[activity] += 1

print("\n===== ADDITIONAL ACTIVITIES =====")

if additional_counts:
    for activity, count in additional_counts.most_common():
        print(f"{activity}: {count} patient journeys")
else:
    print("No additional activities recorded.")

# Step 5: Count missing activities
missing_counts = Counter()

for activities in df["Missing_Activities"]:
    if str(activities).strip() and str(activities).strip().lower() != "none":
        for activity in str(activities).split(","):
            activity = activity.strip()
            if activity:
                missing_counts[activity] += 1

print("\n===== MISSING ACTIVITIES =====")

if missing_counts:
    for activity, count in missing_counts.most_common():
        print(f"{activity}: {count} patient journeys")
else:
    print("No missing activities recorded.")

# Step 6: Count first-difference patterns
difference_counts = Counter()

for difference in df["First_Difference"]:
    difference = str(difference).strip()

    if difference and difference.lower() != "none":
        difference_counts[difference] += 1

print("\n===== FIRST DIFFERENCE PATTERNS =====")

if difference_counts:
    for difference, count in difference_counts.most_common():
        print(f"{difference}: {count} patient journeys")
else:
    print("No first differences recorded.")

# Step 7: Save a summary report
summary_rows = []

summary_rows.append({
    "Category": "Overall",
    "Finding": "Total patient journeys",
    "Patient_Count": total_patients
})

summary_rows.append({
    "Category": "Overall",
    "Finding": "Exact pathway matches",
    "Patient_Count": int(exact_matches)
})

summary_rows.append({
    "Category": "Overall",
    "Finding": "Journeys differing from expected pathway",
    "Patient_Count": int(different_journeys)
})

for activity, count in additional_counts.most_common():
    summary_rows.append({
        "Category": "Additional Activity",
        "Finding": activity,
        "Patient_Count": count
    })

for activity, count in missing_counts.most_common():
    summary_rows.append({
        "Category": "Missing Activity",
        "Finding": activity,
        "Patient_Count": count
    })

for difference, count in difference_counts.most_common():
    summary_rows.append({
        "Category": "First Difference",
        "Finding": difference,
        "Patient_Count": count
    })

output_file = Path("data/processed/deviation_summary.csv")
output_file.parent.mkdir(parents=True, exist_ok=True)

pd.DataFrame(summary_rows).to_csv(output_file, index=False)

print("\nSummary report saved to:", output_file)
print("\n===== ANALYSIS COMPLETED =====")